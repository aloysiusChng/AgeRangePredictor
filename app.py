from flask import Flask, request, render_template, redirect, url_for, jsonify
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
import os
import numpy as np
import cv2
import hashlib
import PIL
import io

img_height=224
img_width=224
app = Flask(
    __name__,
    template_folder = 'templates',
    static_folder = 'static'
)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(
    app.config['UPLOAD_FOLDER'],
    exist_ok = True
)

for root, dirs, files in os.walk(".", topdown=False):
   for name in files:
      print(os.path.join(root, name))
   for name in dirs:
      print(os.path.join(root, name))
model = load_model('./best_val_acc_model.keras')

def image_preprocessing(img_path):
    '''
    Reads, resizes, and normalizes the image.
    '''
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Image not found or invalid at path: {img_path}")
    resized_img = cv2.resize(img, (img_height, img_width))
    normalized_img = resized_img / 255.0
    img_array = img_to_array(normalized_img)
    img_array = np.expand_dims(img_array, axis=0)

    return img_array

@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part', 'success': False}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file', 'success': False}), 400
    if file is None:
        return jsonify({'error': 'Invalid file', 'success': False}), 400
    try:
        file_image = PIL.Image.open( file )
    except:
        return jsonify({'error': 'Invalid image', 'success': False}), 400
    file_image = file_image.convert('RGB').resize( (img_height, img_width) )
    virtual_file = io.BytesIO()
    file_image.save( virtual_file, format='PNG' )
    
    processed_file_hash = hashlib.sha256( virtual_file.getvalue() ).hexdigest()
    processed_file_path = os.path.join( app.config['UPLOAD_FOLDER'], processed_file_hash + '.png' )
    if not os.path.exists( processed_file_path ):
        file_image.save( processed_file_path, format='PNG' )
    return jsonify({'success': True, 'file_hash': processed_file_hash}), 200

@app.route('/api/predict_age/<file_hash>', methods=['GET'])
def get_file_prediction( file_hash : str ):
    file_path = os.path.join( app.config['UPLOAD_FOLDER'], file_hash + '.png' )
    if not os.path.exists( file_path ):
        return jsonify({'error': 'File not found', 'success': False}), 404
    
    processed_image = image_preprocessing( file_path )
    predictions = model.predict( processed_image )
    predicted_class_index = np.argmax( predictions, axis = 1 )[0]
    
    return jsonify({ 'success': True, 'predicted_class': predicted_class_index.item() }), 200

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
