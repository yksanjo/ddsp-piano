# DDSP Piano Audio Visualizer

An interactive web-based audio visualizer for the DDSP Piano project. This application allows you to generate and visualize piano audio in real-time using the DDSP neural synthesis models.

## Features

- Generate piano audio using DDSP models
- Real-time audio visualization (waveform and frequency spectrum)
- Interactive controls for adjusting parameters
- Web-based interface accessible from any browser

## Requirements

- Python 3.8+
- TensorFlow 2.8+
- DDSP 3.2.0+
- Flask 2.0+

## Installation

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you have the main DDSP Piano dependencies installed:
   ```bash
   pip install -r ../requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python run.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Use the controls to generate and visualize piano audio

## Architecture

- **Backend**: Flask server that interfaces with DDSP Piano models
- **Frontend**: HTML/CSS/JavaScript with Canvas API for visualizations
- **Audio Processing**: Web Audio API for playback and analysis

## Note

This is a demonstration application. For full functionality with actual DDSP model weights, you would need to download the pre-trained models from the DDSP Piano project.