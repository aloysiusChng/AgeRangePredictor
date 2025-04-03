# AAI3001 Computer Vision and Deep Learning Final Project Group 9

| Team Members | Student ID |
|:--------------:|:------------:|
CHNG SONG HENG ALOYSIUS | 2302857
WONG KHIN FOONG | 2302728
LIM JUN KHAI JAVIN | 2302694

Project Github Repo: https://github.com/aloysiusChng/AgeRangePredictor
 
# Set Up & Run Project
1. Have Python 3.11 installed
2. Install requirements
```
pip install -r requirements.txt
```
3. Launch App
```
python app.py
```

# Using the App
1. Prepare an Image of a person's face
2. Choose File and Press "Predict Age"
3. Find out the estimated age of person in the image

# Background Information
This project was inspired by the IMDB-WIKI dataset (https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/) used for age estimation done by Rasmus Rothe, Radu Timofte and Luc Van Gool. The data used in this project is taken from the public dataset available on there.

# Our Project
Our model was pre-trained using VGG-16 architecture on 12800 images annotated with the age of the person at the moment the picture was taken. The original dataset metadata contained the person's date of birth and the date the picture was taken. This was used to label the person's age for the image to be trained on.

The model prediction outputs a value from 0 to 3, a total of 4 labels that represent the estimated age range of the person in the image.

| Index | Age Range (Years Old (YO)) |
|:--------------:|:------------:|
0 | 0 - 20 YO
1 | 21 - 40 YO
2 | 41 - 60 YO
3 | 61 - 80 YO

# Plans for Improvements
1. Increase the number of prediction labels to cover a smaller range of ages so that the predictions can be more precise. (E.g., "0 - 5 YO")
2. Switch architecture to a more modern pre-trained model that has better overall accuracy. VGG-16 came out in 2014, though we attempted to use ResNet50, the accuracy was worse and hence, stuck with VGG-16.
3. Include the confidence score of the model's prediction in the output to give a better understanding of what the model thinks of the input image.
