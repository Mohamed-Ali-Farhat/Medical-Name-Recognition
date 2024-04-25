import cv2
import easyocr
import spacy
import string
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Pillow library for handling images

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Initialize SpaCy model
model_path = "./model-best"
nlp = spacy.load(model_path)

# Function to preprocess text
def preprocess_text(text):
    # Remove punctuation
    text = text.upper()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Define stopwords
    stopwords = {'EST', 'ÉTAIT', 'SUIS', 'SOMMES', 'ÉTIONS', 'ÊTES', 'SOYEZ', 'ÉTANT','IS', 'WAS', 'ARE', 'WERE', 'BE', 'BEEN', 'AM', 'BEING'}

    # Remove stopwords
    text_tokens = text.split()
    text = ' '.join([word for word in text_tokens if word.lower() not in stopwords])
    return text

def detect_text(frame):
    # Detect text on the frame
    text_results = reader.readtext(frame)
    
    # Write detected text to the file
    with open("detected_text.txt", "w") as output_file:
        for text in text_results:
            detected_text = text[1]
            cleaned_text = preprocess_text(detected_text)
            doc = nlp(cleaned_text)
            for ent in doc.ents:
                if ent.label_ == 'DRUG':
                    output_file.write(detected_text + "\n")  

# Create Tkinter window
root = tk.Tk()
root.title("Drug Information")
root.attributes('-fullscreen', True)  # Make window full screen

# Load and resize the logo image
logo_image = Image.open("logo.jpg")
logo_tk = ImageTk.PhotoImage(logo_image)

# Create label for logo
logo_label = tk.Label(root, image=logo_tk)
logo_label.pack(side="top", anchor="nw", padx=20, pady=20) 

# Function to update labels with drug information
def update_labels(drug_name, blister_count):
    drug_name_label.config(text=f"Drug Name: {drug_name}", font=("Helvetica", 24), pady=20)
    blister_count_label.config(text=f"Blister Count: {blister_count}", font=("Helvetica", 24), pady=20)

# Function to handle frame capture
def capture_frame():
    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Could not capture frame.")
        return
    detect_text(frame)

    # Read detected text from file
    file_path = "./detected_text.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Preprocess text
    cleaned_text = preprocess_text(text)
    doc = nlp(cleaned_text)

    drug_name_to_find = None
    blister_count = None

    # Iterate over entities in the document
    for ent in doc.ents:
        if ent.label_ == 'DRUG':
            drug_name_to_find = ent.text
            break

    if drug_name_to_find:
        # Find blister count
        filename = 'Blister_Num.txt'  # Replace with your file name
        with open(filename, 'r') as file:
            for line in file:
                parts = line.split('\t')  # Assuming tab is the delimiter between drug name and blister count
                if len(parts) == 2:
                    name_of_drug = parts[0]
                    num_of_blister = parts[1].strip()  # Remove any leading/trailing whitespace
                    if name_of_drug == drug_name_to_find:
                        blister_count = num_of_blister
                        break

    if blister_count is not None:
        # Update labels with drug information
        update_labels(drug_name_to_find, blister_count)
        
        with open("C:/Users/MSI/Desktop/chdoula-ya-m3alem-main/blister_count.txt", "w") as file:
            file.write(str(blister_count))


        # Provide feedback on successful detection
        messagebox.showinfo("Success", "Drug information detected successfully!")






# Function to close the interface
def close_interface():
    cap.release()  # Release the camera
    root.destroy()

# Capture video from the default camera
cap = cv2.VideoCapture(0)  # Change to 1 if your camera index is 1

# Check if the camera is opened successfully
if not cap.isOpened():
    messagebox.showerror("Error", "Could not open camera.")
    root.destroy()
    exit()

# Create labels to display drug name and blister count
drug_name_label = tk.Label(root, text="Detecting...", font=("Helvetica", 24))
drug_name_label.pack(expand=True)

blister_count_label = tk.Label(root, text="", font=("Helvetica", 24))
blister_count_label.pack(expand=True)

# Function to convert OpenCV images to Tkinter-compatible images
def convert_to_tk_image(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    frame = Image.fromarray(frame)  # Convert to PIL Image
    frame = ImageTk.PhotoImage(image=frame)  # Convert to Tkinter Image
    return frame

# Create button to capture frame
capture_button = tk.Button(root, text="Start The Process ", command=capture_frame, font=("Helvetica", 16))
capture_button.pack(expand=True, pady=20)



# Create close button with icon
close_icon = Image.open("close_icon.png")  # Replace "close_icon.png" with the path to your icon file

close_icon_tk = ImageTk.PhotoImage(close_icon)
close_button = tk.Button(root, image=close_icon_tk, command=close_interface, borderwidth=0)
close_button.pack(side="top", anchor="ne", padx=20, pady=20)

# Start Tkinter event loop
root.mainloop()