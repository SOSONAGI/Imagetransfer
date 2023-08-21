# Imagetransfer
image transfer by selecting the box and get results before and after

Project Description

This project is a Flask web application that allows users to select a specific part of an uploaded image and replace it with another normal part. This can be used to restore images by replacing defective parts with normal ones.
Main Features

1. Users can upload images and select defective and normal parts through the web page.
2. The server receives this information, extracts the corresponding parts from the image, and adjusts the normal part to the size of the defective part.
3. The adjusted normal part is applied to the defective part to restore the image.
4. The restored image is sent back to the user.
Code Description

- index(): Renders the main page.
- upload(): Receives the image and the coordinates of the defective and normal parts uploaded by the user, restores the image, and sends the restored image back to the user.
How to Use

1. Upload an image on the main page and select the defective and normal parts.
2. Click the 'Submit' button to send the image to the server.
3. The server restores the image and you can download the restored image.
Installation

1. Clone this project.
2. Install the packages specified in requirements.txt.
3. Run python main.py to start the server.
