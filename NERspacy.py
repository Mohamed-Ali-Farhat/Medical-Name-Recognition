import cv2
import easyocr
import spacy
import string
from datetime import datetime, timedelta

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
                    print(detected_text)

# Capture video from the default camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

start_time = datetime.now()
end_time = start_time + timedelta(seconds=15)  # Run OCR for 15 seconds

# Loop to capture frames from the camera
while datetime.now() < end_time:
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

# Release the camera
cap.release()

# Close OpenCV windows
cv2.destroyAllWindows()

# Read detected text from file
file_path = "./detected_text.txt"
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

# Preprocess text
cleaned_text = preprocess_text(text)
doc = nlp(cleaned_text)


#
print('The Medication Label Name is')

# Iterate over entities in the document
for ent in doc.ents:
    print(ent.text)
    drug_name_to_find=ent.text
    break
    






def keep_only_first_line(filename):
    # Open the file in read mode
    with open(filename, 'r') as file:
        # Read the first line
        first_line = file.readline()

    # Open the file in write mode (truncating it)
    with open(filename, 'w') as file:
        # Write the first line back into the file
        file.write(first_line)

# Example usage:
filename = 'detected_text.txt'
keep_only_first_line(filename)



print(' ')

def find_blister_count(drug_name, filename):
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split('\t')  # Assuming tab is the delimiter between drug name and blister count
            if len(parts) == 2:
                name_of_drug = parts[0]
                num_of_blister = parts[1].strip()  # Remove any leading/trailing whitespace
                if name_of_drug == drug_name:
                    return num_of_blister
    return None  # Return None if drug name is not found

# Example usage:
filename = 'Blister_Num.txt'  # Replace with your file name

blister_count = find_blister_count(drug_name_to_find, filename)
if blister_count is not None:
    print(f"{drug_name_to_find} have  {blister_count} in a blister.")
else:
    print(f"No blister count found for {drug_name_to_find}.")







