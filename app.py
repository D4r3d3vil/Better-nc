import requests, io
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS, cross_origin
from config import Config
import mimetypes

app = Flask(__name__)
cors = CORS(app)
app.config.from_object(Config)

global files, file_names
files = []
file_names = []

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    file = request.files['file'].read()
    file_names.append(str(request.files['file']).split("<FileStorage: '", 2)[1].split("'")[0])
    files.append(file)
    return jsonify({'message':'File uploaded successfully'})

@app.route('/getfile', methods=['GET'])
@cross_origin()
def get_files():
    if len(files) < 1: return '' 
    file_like_object = io.BytesIO(files.pop())
    return send_file(file_like_object, mimetype='application/octet-stream' ,as_attachment=True, download_name='file')

@app.route('/getname', methods=['GET'])
@cross_origin()
def get_name():
    return jsonify({'name': file_names.pop()})

@app.route("/mimetype")
@cross_origin()
def detect_mimetype():
  filename = request.args.get("name")
  ext = filename.split(".")[-1]
  mimetype = mimetypes.types_map.get("." + ext, "unknown")
  return jsonify({"mimetype": mimetype})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    app.run(host='0.0.0.0', port=8000)