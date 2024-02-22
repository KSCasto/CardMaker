from services.blueprints.cardMaker.utils import cm
from flask import Flask,Blueprint,request, jsonify, current_app
import os, zipfile

CardMaker = Blueprint('card-maker',__name__)

@CardMaker.route("/makeCards",methods = ['POST'])
def makeCards():
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                print(request.files)
                return jsonify({'error': 'No file sent'}), 400
            
            zip_file = request.files['file']

            # Check if the file is a zip file
            if not zip_file.filename.endswith('.zip'):
                return jsonify({'error': 'Invalid file format, must be a zip file'}), 400

            # Save the zip file to a temporary location
            zip_file_path = os.path.join(current_app.config.get('CM_INPUT_FOLDER'), zip_file.filename)
            zip_file.save(zip_file_path)

            cm.unzip_archive(zip_file_path,current_app.config.get('CM_INPUT_FOLDER'))

            return zip_file_path

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
