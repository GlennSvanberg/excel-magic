from flask import Flask, request, send_from_directory, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': f'File {filename} uploaded successfully'}), 200
    

@app.route('/modify', methods=['POST'])
def modify_file():
    data = request.json
    filename = data.get('filename')
    modifications = data.get('modifications')
    
    if not filename or not modifications:
        return jsonify({'error': 'Filename and modifications are required'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File does not exist'}), 404
    
    try:
        df = pd.read_excel(filepath)
        # Example modification: filter columns based on modifications received
        # This part should be adapted based on the specific modifications required
        if 'columns' in modifications:
            df = df[modifications['columns']]
        # Save the modified file
        modified_filepath = os.path.join(app.config['STATIC_FOLDER'], f'modified_{filename}')
        df.to_excel(modified_filepath, index=False)
        return jsonify({'message': f'File {filename} modified successfully', 'modified_file': f'modified_{filename}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
