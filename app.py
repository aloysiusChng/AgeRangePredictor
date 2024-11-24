from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
import numpy as np
import cv2

img_height=224
img_width=224
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to save uploaded images
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load your model
model = load_model('best_val_acc_model.keras')

def preprocess_image(image_path, target_size):
    """Preprocess the image to match the model's expected input."""
    img = load_img(image_path, target_size=target_size)  # Resize image
    img_array = img_to_array(img) / 255.0  # Normalize to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the file upload
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)  # Save the uploaded file
            
            # Preprocess and predict
            processed_image = image_preprocessing(file_path)
            predictions = model.predict(processed_image)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            result = map_class_to_age(predicted_class_index)

            return f'Predicted class: {result}'

    return '''
    <!doctype html>
    <title>Upload an Image</title>
    <h1>Upload an Image for Prediction</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

# Image preprocessing function
def image_preprocessing(img_path):
    '''
    Reads, resizes, and normalizes the image.
    '''
    # Read the image
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Image not found or invalid at path: {img_path}")

    # Resize and normalize
    resized_img = cv2.resize(img, (img_height, img_width))
    normalized_img = resized_img / 255.0

    return normalized_img
def map_class_to_age(class_index):
    # Age ranges for the class indices
    age_ranges = {
        0: "0-24",
        1: "25-49",
        2: "50-74",
        3: "75-99",
        4: "100-124"
    }

    return age_ranges.get(class_index, "Unknown")

if __name__ == '__main__':
    app.run(debug=True)
