# Prototype Object Detection API

This project is an API developed with FastAPI for object detection in images using the YOLOv8 model. The API allows image uploads, processing with YOLOv8, and exporting results in a JSON format compatible with Label Studio.

## Features

- Upload images for object detection.
- Process images using the YOLOv8 model.
- Generate annotations in JSON format.
- Export annotations separately or consolidated in a single JSON file.
- Display labeled images.
- Clear cache of images and annotations.

## Prerequisites

Before running the project, install the following software:

- Python 3.8+
- Git
- Pip (Python package manager)
- Virtualenv (optional but recommended)

## Installation and Execution

Follow the steps below to set up and run the API:

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r pytorch.txt -r requirements.txt
```

### 4. Run the FastAPI server
```bash
python main.py
```

The API will start and be available at: `http://127.0.0.1:8000`

## Using the API

### 1. Access the web interface
Open in your browser: `http://127.0.0.1:8000` to access the image upload page.

### 2. Uploading Images
- Select images to upload.
- Specify the desired classes for detection.
- Click the button to process the images.

### 3. Exporting Results
The API allows exporting annotations:
- **Separate JSONs:** `GET /export_separate_jsons` (generates a ZIP file with all JSON files)
- **Consolidated JSON:** `GET /export_consolidated_json` (generates a single JSON file with all annotations)

### 4. Clearing the Cache
To clear processed images and annotations, access: `GET /clear_cache`

## Project Structure
```
├── main.py               # Main API code
├── requirements.txt      # Project dependencies
├── templates/            # HTML files for the web interface
├── static/               # Static files (CSS, JS, etc.)
├── temp_images/          # Folder where images are temporarily stored
├── temp_annotations/     # Folder where JSON annotations are stored
└── README.md             # Project documentation
```

## Technologies Used

- **FastAPI**: Framework for building fast and efficient APIs.
- **YOLOv8 (Ultralytics)**: Object detection model.
- **OpenCV**: Image processing.
- **Matplotlib**: Detection visualization.
- **Jinja2**: HTML template rendering.
- **Uvicorn**: ASGI server for FastAPI.
