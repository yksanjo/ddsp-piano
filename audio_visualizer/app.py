import os
import io
import json
from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import soundfile as sf
import base64
import random

app = Flask(__name__, static_folder='static', template_folder='templates')

# For demo purposes, we'll simulate the model functionality
sample_rate = 24000  # Default sample rate

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    """Synthesize audio from parameters"""
    try:
        data = request.json
        piano_type = data.get('piano_type', 9)
        duration = data.get('duration', 3.0)

        # Generate a more complex piano-like sound for visualization
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Create a more realistic piano sound with harmonics and decay
        fundamental_freq = 220.0 * (2 ** (piano_type / 12))  # Adjust based on piano type
        signal = np.zeros_like(t)

        # Add fundamental and harmonics with different decay rates
        for i, harmonic in enumerate([1, 2, 3, 4, 5]):  # Harmonics
            freq = fundamental_freq * harmonic
            # Different decay rates for different harmonics (more realistic)
            decay_rate = 0.5 + (i * 0.3)
            amplitude = 1.0 / (i + 1)  # Harmonics get weaker

            # Create the harmonic with envelope
            harmonic_signal = amplitude * np.sin(2 * np.pi * freq * t)
            envelope = np.exp(-t * decay_rate)  # Exponential decay
            signal += harmonic_signal * envelope

        # Add some noise for realism
        noise = np.random.normal(0, 0.02, signal.shape)
        signal += noise

        # Normalize the signal
        signal = signal / np.max(np.abs(signal)) * 0.7

        # Convert to WAV format
        buffer = io.BytesIO()
        sf.write(buffer, signal, sample_rate, format='WAV')
        buffer.seek(0)

        # Encode to base64 for transmission
        audio_data = base64.b64encode(buffer.read()).decode('utf-8')

        return jsonify({
            'success': True,
            'audio_data': audio_data,
            'sample_rate': sample_rate,
            'duration': duration
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/visualize_audio', methods=['POST'])
def visualize_audio():
    """Generate visualization data from audio"""
    try:
        data = request.json
        audio_data = data.get('audio_data')
        sample_rate = data.get('sample_rate', 24000)

        # Decode base64 audio data
        audio_bytes = base64.b64decode(audio_data)
        audio_buffer = io.BytesIO(audio_bytes)

        # Load audio
        audio, sr = sf.read(audio_buffer)
        if len(audio.shape) > 1:
            audio = audio[:, 0]  # Take first channel if stereo

        # Generate visualization data
        visualization_data = generate_visualization_data(audio, sr)

        return jsonify({
            'success': True,
            'visualization_data': visualization_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def generate_visualization_data(audio, sample_rate):
    """Generate visualization data from audio"""
    # Generate waveform data (downsampled for performance)
    waveform_points = 1000  # Number of points for waveform
    step = max(1, len(audio) // waveform_points)
    waveform = audio[::step].tolist()

    # Generate frequency spectrum (FFT)
    fft_size = 1024
    if len(audio) >= fft_size:
        # Take a segment for FFT
        segment = audio[:fft_size]
        fft = np.fft.fft(segment)
        magnitude = np.abs(fft[:fft_size//2])
        frequencies = np.linspace(0, sample_rate/2, len(magnitude)).tolist()
        magnitudes = magnitude.tolist()
    else:
        # Pad with zeros if audio is too short
        padded = np.pad(audio, (0, fft_size - len(audio)), 'constant')
        fft = np.fft.fft(padded)
        magnitude = np.abs(fft[:fft_size//2])
        frequencies = np.linspace(0, sample_rate/2, len(magnitude)).tolist()
        magnitudes = magnitude.tolist()

    return {
        'waveform': waveform,
        'frequencies': frequencies,
        'magnitudes': magnitudes
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)