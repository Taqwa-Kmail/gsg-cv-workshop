# AI-Enhanced Image Stitching and Edge Detection

# Overview
This project demonstrates the integration of AI-based image processing techniques with web development using Flask, enabling users to interactively stitch images and perform edge detection tasks through a web interface.


# Usage
To access the project, open the web browser and navigate to [http://127.0.0.1:5000/].


# General Architecture
The project involves the integration of frontend and backend components. The flask serves as the backbone of the application, coordinating the communication between the frontend and processing functionalities.
1-	Frontend Interface: HTML/CSS/JavaScript for user interaction.
2-	Backend Server: Flask handles HTTP requests and responses.
3-	Image Processing: OpenCV
4-	object detection: ultralytics.
5-	numerical computing: numpy Library.
6-	path operations: posixpath Library, for manipulating paths in a POSIX-compliant way.

# About the pages
1-	app.py: This file contains the Flask application with several routes, to handle both GET and POST requests.
2-	index.html: This HTML file provides a form for uploading images, using a POST request to submit the images to the server.
3-	results.html: This file displays the stitched panoramic image and individual images uploaded by the user.
4-	edge_result.html: This file displays the result of edge detection on the stitched image.
5-	styles.css: The CSS file contains styles for the application's layout and components, ensuring a visually appealing and user-friendly interface.


# Functions

def allowed_file(filename):
This function checks if the file extension is allowed based on a predefined set of allowed extensions. It returns True if allowed, otherwise False.

def stitch_images(image_paths):
It reads each image using OpenCV's imread function and stores them in a list. Then, it creates a stitcher object using OpenCV's Stitcher_create. If is successful, it returns the stitched image; otherwise, it returns None.

def index():
This function handles both GET and POST requests for the home page ('/' route). In POST, it checks for uploaded files, saves them, and redirects to the results page. If it is GET, it renders the index.html template.

def results():
This function renders the results page ('/results' route). It receives a list of filenames as arguments, stitches the uploaded images, performs edge detection, and saves the result.

def adjust_kernel():
This function receives a POST request with a new kernel size for morphological operation.


![Screenshot 2024-03-30 041636](https://github.com/Taqwa-Kmail/gsg-cvc-workshop/assets/114935730/ab5395b1-7d9d-4916-bbbd-fd6241f96f1c)



