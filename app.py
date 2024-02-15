from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import base64
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['image_db']
collection = db['images']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)
    
    image = request.files['image']
    
    if image.filename == '':
        return redirect(request.url)
    
    if image:
        image_data = image.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        filename = image.filename
        image_doc = {'filename': filename, 'base64_image': base64_image}
        collection.insert_one(image_doc)
        
        return 'Image uploaded successfully and stored in MongoDB!'

    return 'Failed to upload image.'

if __name__ == '__main__':
    app.run(debug=True)

