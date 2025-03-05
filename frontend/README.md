# Audio Deepfake Detection

## Overview

This project provides a tool for detecting audio deepfakes—a growing concern in digital media. 

### What the Model Does

The backend of this application uses a deep learning model hosted on Hugging Face's API to analyze audio files and detect whether they are genuine or manipulated. Specifically, the model is trained to distinguish between real and synthetic audio, identifying potential deepfakes with high accuracy.

### Relevance

Audio deepfakes involve using advanced AI techniques to create convincing but fake audio recordings. These can be used for malicious purposes such as misinformation, fraud, or impersonation. With the rise of such technologies, it is crucial to have reliable detection tools. This project aims to address this need by providing an easy-to-use interface for analyzing audio files and determining their authenticity. By leveraging cutting-edge machine learning techniques, it helps in mitigating the risks associated with deepfake technologies.

## Project Structure

- `frontend/` - Contains the React application.
- `backend/` - Contains the Flask application.

## Getting Started

### Prerequisites

- Python 3.6+
- Node.js 14+
- pip (Python package installer)
- npm (Node package manager)

### Backend Setup

1. **Navigate to the `backend/` directory**:

    ```bash
    cd backend
    ```

2. **Install Python dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `requirements.txt` file** in the `backend/` directory with the following content:

    ```
    Flask==2.1.2
    Flask-Cors==3.1.1
    requests==2.28.1
    ```

4. **Start the Flask server**:

    ```bash
    python app.py
    ```

   The server will start on `http://localhost:5000`.

### Frontend Setup

1. **Navigate to the `frontend/` directory**:

    ```bash
    cd frontend
    ```

2. **Install Node.js dependencies**:

    ```bash
    npm install
    ```

3. **Start the React development server**:

    ```bash
    npm start
    ```

   The React app will start on `http://localhost:3000`.

## Usage

1. **Upload an Audio File**:
   - Open your browser and go to `http://localhost:3000`.
   - Use the form to upload an audio file.
   - The result of the deepfake detection will be displayed below the form.

## Troubleshooting

- **CORS Issues**:
  Ensure that CORS is properly configured in the Flask backend. This project uses `flask-cors` to handle cross-origin requests.

- **API Key**:
  Replace the placeholder `#` in the `headers` dictionary in `app.py` with your actual Hugging Face API token.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your fork.
4. Create a pull request with a description of your changes.


