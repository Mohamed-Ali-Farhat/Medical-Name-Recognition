'''from paddleocr import PaddleOCR
import cv2

try:
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # need to run only once to download and load model into memory
except Exception as e:
    print("Error initializing PaddleOCR:", e)
    exit()

img_path = '1.jpg'
img = cv2.imread(img_path)
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

try:
    result = ocr.ocr(img, cls=True)

    n = len(result[0])

    # Loop through each item in the result list
    for i in range(n):
        # Print the left part of the tuple (recognized text)
        print(result[0][i][1])
except Exception as e:
    print("Error performing OCR:", e)
'''










'''
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np

# read image
image_path = '2.jpg'

img = cv2.imread(image_path)

# instance text detector
reader = easyocr.Reader(['en'], gpu=False)

# detect text on image
text_ = reader.readtext(img)

threshold = 0.25
# draw bbox and text
for t_, t in enumerate(text_):
    print(t)

'''


import cv2
import easyocr

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to perform text detection on a frame
def detect_text(frame):
    # Detect text on the frame
    text_results = reader.readtext(frame)
    
    # Write detected text to the file
    with open("detected_text.txt", "w") as output_file:
        for text in text_results:
            detected_text = text[1]  # Text is at index 1 in the tuple
            output_file.write(detected_text + "\n")  # Write text to the file
            print(detected_text)

# Capture video from the default camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Loop to capture frames from the camera
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not capture frame.")
        break

    # Display the frame
    cv2.imshow('Frame', frame)

    # Detect text on the frame
    detect_text(frame)

    # Exit loop when 'q' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):  # Press 's' to save detected text to the file
        detect_text(frame)  # Call text detection function again to ensure the latest text is saved

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()






















