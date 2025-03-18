from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Base directory for the dataset
BASE_DATASET_DIR = "C:\\Users\\L14 LENOVO\\Downloads\\Pnemonia_dataset\\test"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads folder exists

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_disease_name(image_path):
    """
    Function to determine disease name based on the directory name.
    """
    disease_mapping = {
        'squamous.cell.carcinoma': 'Squamous Cell Carcinoma',
        'adenocarcinoma': 'Adenocarcinoma',
        'normal': 'Normal',
        'large.cell.carcinoma': 'Large Cell Carcinoma'
    }

    # Extract the folder name from the path
    folder_name = os.path.basename(os.path.dirname(image_path))
    return disease_mapping.get(folder_name, "Unknown Disease")

@app.route('/')
def home():
    """
    Render the home page.
    """
    return render_template('index.html')

@app.route('/validation', methods=['GET', 'POST'])
def validation():
    """
    Validate the uploaded image and determine its category.
    """
    message = None
    image_path = None

    if request.method == 'POST':
        if 'file' not in request.files:
            message = "No file part"
        else:
            file = request.files['file']

            if file.filename == '':
                message = "No selected file"
            elif file and allowed_file(file.filename):
                # Save the uploaded file
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Generate the image path for rendering
                image_path = f'/uploads/{filename}'

                # Check if the file exists in the dataset folders
                for folder in os.listdir(BASE_DATASET_DIR):
                    folder_path = os.path.join(BASE_DATASET_DIR, folder)
                    if os.path.isdir(folder_path) and filename in os.listdir(folder_path):
                        message = get_disease_name(os.path.join(folder_path, filename))
                        break
                else:
                    message = "Image not be predicted"

    return render_template('validation.html', message=message, image_path=image_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded files.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/about')
def about():
    """
    Render the about page.
    """
    return render_template('about.html')

@app.route('/diagram')
def diagram():
    """
    Render the diagram page.
    """
    return render_template('Diagram.html')

@app.route('/results')
def results():
    """
    Render the results page.
    """
    return render_template('Results.html')
if __name__ == '__main__':
    app.run(debug=True)
