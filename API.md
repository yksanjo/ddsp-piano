# API Documentation

## Overview

DDSP-Piano provides multiple integration options for developers and enterprises:

- **Python SDK**: Native Python library for direct integration
- **REST API**: HTTP-based API for web and mobile applications
- **Command-Line Interface**: Batch processing and automation
- **Docker API**: Containerized API service

## Python SDK

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from ddsp_piano import PianoSynthesizer

# Initialize synthesizer
synthesizer = PianoSynthesizer(
    config='ddsp_piano/configs/maestro-v2.gin',
    checkpoint='ddsp_piano/model_weights/v2/',
    piano_type=9
)

# Synthesize MIDI file
audio = synthesizer.synthesize('input.mid')

# Save to file
synthesizer.save('output.wav', audio)
```

### Advanced Usage

```python
from ddsp_piano import PianoSynthesizer
import numpy as np

# Initialize with custom settings
synthesizer = PianoSynthesizer(
    config='ddsp_piano/configs/maestro-v2.gin',
    checkpoint='ddsp_piano/model_weights/v2/',
    piano_type=9,
    sample_rate=24000,
    warm_up_duration=0.5
)

# Synthesize with options
audio = synthesizer.synthesize(
    'input.mid',
    duration=60.0,  # Maximum duration in seconds
    normalize=-3.0,  # Normalize to -3 dBFS
    include_dry=True  # Include dry signal (no reverb)
)

# Get audio as numpy array
audio_array = synthesizer.synthesize_to_array('input.mid')

# Batch processing
midi_files = ['track1.mid', 'track2.mid', 'track3.mid']
for midi_file in midi_files:
    audio = synthesizer.synthesize(midi_file)
    synthesizer.save(f'{midi_file}.wav', audio)
```

### API Reference

#### `PianoSynthesizer`

Main class for piano synthesis.

**Parameters:**
- `config` (str): Path to model configuration file (.gin)
- `checkpoint` (str): Path to model checkpoint directory
- `piano_type` (int): Piano model type (0-9), default: 9
- `sample_rate` (int): Output sample rate, default: 24000
- `warm_up_duration` (float): Warm-up duration in seconds, default: 0.5

**Methods:**

##### `synthesize(midi_file, duration=None, normalize=None, include_dry=False)`
Synthesize audio from MIDI file.

**Parameters:**
- `midi_file` (str): Path to input MIDI file
- `duration` (float, optional): Maximum duration in seconds
- `normalize` (float, optional): Normalize to dBFS level
- `include_dry` (bool): Include dry signal without reverb

**Returns:** Audio array (numpy.ndarray)

##### `synthesize_to_array(midi_file, **kwargs)`
Synthesize and return as numpy array.

**Returns:** numpy.ndarray

##### `save(output_file, audio)`
Save audio to file.

**Parameters:**
- `output_file` (str): Output file path
- `audio` (numpy.ndarray): Audio data

## REST API

### Base URL

```
https://api.ddsp-piano.com/v1  # Production (placeholder)
http://localhost:8080/v1       # Local development
```

### Authentication

```bash
# API Key authentication
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.ddsp-piano.com/v1/synthesize
```

### Endpoints

#### POST `/synthesize`

Synthesize audio from MIDI file.

**Request:**
```json
{
  "midi_file": "base64_encoded_midi_data",
  "piano_type": 9,
  "duration": 60.0,
  "normalize": -3.0,
  "include_dry": false,
  "config": "maestro-v2",
  "sample_rate": 24000
}
```

**Response:**
```json
{
  "status": "success",
  "audio_file": "base64_encoded_wav_data",
  "duration": 45.2,
  "sample_rate": 24000,
  "piano_type": 9,
  "processing_time": 1.23
}
```

**Error Response:**
```json
{
  "status": "error",
  "error_code": "INVALID_MIDI",
  "message": "Invalid MIDI file format"
}
```

#### POST `/synthesize/batch`

Batch synthesis of multiple MIDI files.

**Request:**
```json
{
  "files": [
    {
      "id": "track1",
      "midi_file": "base64_encoded_midi_data",
      "piano_type": 9
    },
    {
      "id": "track2",
      "midi_file": "base64_encoded_midi_data",
      "piano_type": 5
    }
  ],
  "options": {
    "normalize": -3.0,
    "include_dry": false
  }
}
```

**Response:**
```json
{
  "status": "success",
  "results": [
    {
      "id": "track1",
      "audio_file": "base64_encoded_wav_data",
      "duration": 45.2,
      "processing_time": 1.23
    },
    {
      "id": "track2",
      "audio_file": "base64_encoded_wav_data",
      "duration": 32.1,
      "processing_time": 0.98
    }
  ],
  "total_processing_time": 2.21
}
```

#### GET `/models`

List available piano models.

**Response:**
```json
{
  "models": [
    {
      "id": 0,
      "name": "Piano Model 0",
      "description": "Bright, modern piano sound"
    },
    {
      "id": 9,
      "name": "Piano Model 9",
      "description": "Warm, classical piano sound"
    }
  ]
}
```

#### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "uptime": 12345,
  "gpu_available": true
}
```

### Rate Limits

- **Free Tier**: 100 requests/day
- **Commercial**: 10,000 requests/day
- **Enterprise**: Custom limits based on agreement

### Error Codes

| Code | Description |
|------|-------------|
| `INVALID_MIDI` | Invalid MIDI file format |
| `INVALID_PIANO_TYPE` | Piano type out of range (0-9) |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `SERVER_ERROR` | Internal server error |
| `AUTHENTICATION_FAILED` | Invalid API key |

## Command-Line Interface

### Basic Synthesis

```bash
python synthesize_midi_file.py input.mid output.wav
```

### With Options

```bash
python synthesize_midi_file.py \
    --config ddsp_piano/configs/maestro-v2.gin \
    --ckpt ddsp_piano/model_weights/v2/ \
    --piano_type 9 \
    --duration 60.0 \
    --warm_up 0.5 \
    --normalize -3.0 \
    --unreverbed \
    input.mid output.wav
```

### Batch Processing

```bash
python synthesize_from_csv.py \
    /path/to/maestro-v3.0.0/ \
    tracks.csv \
    output_directory/ \
    --config ddsp_piano/configs/maestro-v2.gin \
    --ckpt ddsp_piano/model_weights/v2/
```

## Docker API

### Running API Server

```bash
# Build image
docker build -t ddsp-piano-api .

# Run API server
docker run -p 8080:8080 \
    -v $(pwd)/models:/models \
    ddsp-piano-api \
    python -m ddsp_piano.api.server --port 8080
```

### Docker Compose

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./models:/models
    environment:
      - API_KEY=your_api_key
      - LOG_LEVEL=INFO
```

## Integration Examples

### Python Web Application

```python
from flask import Flask, request, jsonify
from ddsp_piano import PianoSynthesizer
import base64
import io

app = Flask(__name__)
synthesizer = PianoSynthesizer()

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.json
    midi_data = base64.b64decode(data['midi_file'])
    
    # Save MIDI to temporary file
    with open('temp.mid', 'wb') as f:
        f.write(midi_data)
    
    # Synthesize
    audio = synthesizer.synthesize('temp.mid')
    
    # Convert to base64
    audio_b64 = base64.b64encode(audio.tobytes()).decode()
    
    return jsonify({
        'audio_file': audio_b64,
        'duration': len(audio) / 24000
    })

if __name__ == '__main__':
    app.run(port=8080)
```

### Node.js Integration

```javascript
const axios = require('axios');
const fs = require('fs');

async function synthesizeMIDI(midiPath, outputPath) {
    const midiData = fs.readFileSync(midiPath);
    const midiBase64 = midiData.toString('base64');
    
    const response = await axios.post('https://api.ddsp-piano.com/v1/synthesize', {
        midi_file: midiBase64,
        piano_type: 9,
        normalize: -3.0
    }, {
        headers: {
            'Authorization': `Bearer ${process.env.API_KEY}`,
            'Content-Type': 'application/json'
        }
    });
    
    const audioData = Buffer.from(response.data.audio_file, 'base64');
    fs.writeFileSync(outputPath, audioData);
}

synthesizeMIDI('input.mid', 'output.wav');
```

## Best Practices

### Performance Optimization
- Use batch processing for multiple files
- Cache model loading for repeated requests
- Use appropriate piano_type for your use case
- Consider GPU acceleration for production

### Error Handling
- Always validate MIDI files before synthesis
- Handle rate limits gracefully
- Implement retry logic for transient errors
- Log errors for debugging

### Security
- Store API keys securely (environment variables)
- Validate input data
- Implement rate limiting on client side
- Use HTTPS for production APIs

## Support

For API support:
- **Documentation**: This file
- **Issues**: GitHub Issues
- **Email**: support@ddsp-piano.com (placeholder)
- **Enterprise Support**: See [SUPPORT.md](SUPPORT.md)











