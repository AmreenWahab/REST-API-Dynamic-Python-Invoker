from flask import Flask, request, jsonify, json
from flask_restful import reqparse, Api, Resource
import rocksdb
import uuid
import os
import subprocess
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD = 'api/v1/scripts/'
UPLOAD_FOLDER = os.path.join(ROOT, UPLOAD)
app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/api/v1/scripts/<scriptid>', methods=['GET'])
def get(scriptid):
    db = rocksdb.DB("assign1.db", rocksdb.Options(create_if_missing=True))
    filename = db.get(scriptid.encode()).decode()
    r1 = str(os.path.join(UPLOAD_FOLDER, filename))
    resp = subprocess.check_output(['python3.6',r1])  
    return resp, 200

@app.route('/api/v1/scripts/', methods=['POST'])
def post():
    db = rocksdb.DB("assign1.db", rocksdb.Options(create_if_missing=True))
    file = request.files.get("data")
    key = uuid.uuid4().hex
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    db.put(key.encode(), file.filename.encode());
    response ={'script-id':key}
    return jsonify(response), 201

if __name__ == '__main__':
    app.run(debug=True)       
