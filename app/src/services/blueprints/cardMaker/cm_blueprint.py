from services.blueprints.cardMaker.utils import cm
from flask import Flask, Blueprint, request, jsonify, current_app, send_file, after_this_request
import os, zipfile, logging

CardMaker = Blueprint('card-maker',__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

@CardMaker.route("/makeCards",methods = ['POST'])
def makeCards():
    try:
        if request.method == 'POST':
            # if 'name' in request.args:
            #     deckName = request.args.get('name')
            # else:
            #     deckName = "output"
            deckName = request.form.get('deck_name','output')
            
            if 'file' not in request.files:
                print(jsonify(request.files))
                return jsonify(f'No file found for deck: {deckName} : {request.files.get("file")}'), 400
            
            zip_file = request.files['file']

            # Check if the file is a zip file
            if not zip_file.filename.endswith('.zip'):
                return jsonify({'error': 'Invalid file format, must be a zip file'}), 400

            # Save the zip file to a temporary location
            input_file_path = os.path.join(current_app.config.get('CM_INPUT_FOLDER'), zip_file.filename)
            zip_file.save(input_file_path)

            cm.unzip_archive(input_file_path,current_app.config.get('CM_INPUT_FOLDER'))
            cm.remove_zip(input_file_path)

            pdf_path = cm.makePDF(deckName,current_app.config.get('CM_INPUT_FOLDER'),current_app.config.get('CM_OUTPUT_FOLDER'))

            cm.cleanup_files(current_app.config.get('CM_INPUT_FOLDER'))

            @after_this_request
            def outputCleanup(response):
                try:
                    cm.cleanup_files(current_app.config.get('CM_OUTPUT_FOLDER'))
                    print(f"Deleted: {pdf_path}")
                except Exception as e:
                    print(f"An error occurred while deleting the file: {e}")
                return response
            return send_file(pdf_path,as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
