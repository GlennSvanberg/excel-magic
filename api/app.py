from flask import Flask, request, send_from_directory
from flask_restx import Api, Resource, fields
import pandas as pd
import os
from werkzeug.utils import secure_filename
from agent import do_magic, get_head_of_file
from flask_restx import fields
from flask import url_for
app = Flask(__name__)
api = Api(app, version='1.0', title='Excel Magic API', description='A simple API doing Magic with Excel')
ns = api.namespace('api', description='API operations')

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@ns.route('/upload')
class UploadFile(Resource):
    @api.response(200, 'Success')
    #@api.response(400, 'Validation Error')
    def post(self):
        '''Upload a file'''
        print("Uploading file...")
        args= request.files
        print(args)
        file = args['file']
        if file.filename == '':
            api.abort(400, 'No selected file')
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return {'message': f'File {filename} uploaded successfully'}, 200

@ns.route('/uploads/<filename>')
class GetHead(Resource):
    def get(self, filename):
        '''Get the head of a file'''
        head = get_head_of_file(filename)
        print(head)
        return head.to_csv(index=False)


message_model = api.model('Message', {
    'sender': fields.String(required=True,  enum=["User", "AI"],description='The sender of the message'),
    'message': fields.String(required=True, description='The content of the message')
})

# Update the do_magic_model to include the messages using fields.List with fields.Nested
do_magic_model = api.model('DoMagic', {
    'files': fields.List(fields.String, required=True, description='List of files'),
    'messages': fields.List(fields.Nested(message_model), required=True, description='List of messages')
})
@ns.route('/do_magic')
class DoMagicRoute(Resource):
    @api.expect(do_magic_model)
    def post(self):
        '''Perform magic on files and messages'''
        data = api.payload
        messages = [{"sender": msg["sender"], "message": msg["message"]} for msg in data['messages']]
        
        # Assuming do_magic returns a list of filenames located in static/output
        filenames, ai_response = do_magic(data['files'], messages)
        
        # Construct URLs for each file
        file_urls = [url_for('static', filename=f'output/{filename}', _external=True) for filename in filenames]
        
        # Include a message in the response
        return {
            'files': file_urls,
            'message': ai_response
        }
    
if __name__ == '__main__':
    app.run("0.0.0.0", 7000, debug=True)