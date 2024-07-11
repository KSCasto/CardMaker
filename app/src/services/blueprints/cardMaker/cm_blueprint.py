from services.blueprints.cardMaker.utils import cm
from flask import Flask, Blueprint, request, jsonify, current_app, send_file, after_this_request
import os, zipfile, logging

CardMaker = Blueprint('card-maker',__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

@CardMaker.route("/makeCards",methods = ['POST'])
def makeCards():
    try:
        if request.method == 'POST':
            deckName = request.form.get('deck_name','output')
            
            if 'file' not in request.files:
                return jsonify(f'No file found for deck: {deckName} : {request.files.get("file")}'), 400
            
            zip_file = request.files['file']

            # Check if the file is a zip file
            if not zip_file.filename.endswith('.zip'):
                return jsonify({'error': 'Invalid file format, must be a zip file of images'}), 400

            input_folder = current_app.config.get('CM_INPUT_FOLDER')
            # Save the zip file to a temporary location
            input_file_path = os.path.join(input_folder, zip_file.filename)
            
            logging.info(f'Saving file to: {input_file_path}')
            zip_file.save(input_file_path)
            logging.info(f'File saved successfully')

            cm.unzip_archive(input_file_path,input_folder)
            cm.remove_zip(input_file_path)

            logging.info("Making PDF...")
            pdf_path = cm.makePDF(deckName,input_folder,current_app.config.get('CM_OUTPUT_FOLDER'))
            logging.info("PDF Created!")

            cm.cleanup_files(input_folder)

            @after_this_request
            def outputCleanup(response):
                try:
                    cm.cleanup_files(current_app.config.get('CM_OUTPUT_FOLDER'))
                    logging.info(f"Deleted: {pdf_path}")
                except Exception as e:
                    logging.info(f"An error occurred while deleting the file: {e}")
                return response
            return send_file(pdf_path,as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
