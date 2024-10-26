---

# Scam Call Detection System

This project is a Python-based system designed to detect potential scam calls by recording audio, transcribing it to text, and analyzing the conversation for scam indicators. Using Google Cloud's Speech-to-Text API and Generative AI (Gemini), the application processes the caller's dialogue to determine the likelihood of a scam, returning a score from 0 (not a scam) to 100 (definitely a scam).

## Prerequisites

1. **FFmpeg**: Required by `pydub` to process audio.
   - Install and ensure `ffmpeg.exe` is in `C:/Program Files/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe`.
2. **Google Cloud APIs**:
   - Enable Cloud Speech-to-Text API for transcription and Generative Language API for text processing.
3. **Python Packages**:
   - Install the following packages: `google-cloud-speech`, `pyaudio`, `pydub`, `keyboard`, `google-generativeai`, `google_auth_oauthlib`, `google.oauth2`

   ```bash
   pip install google-cloud-speech pyaudio pydub keyboard google-generativeai google.oauth2 google_auth_oauthlib
   ```

4. **Credentials**:
   - Ensure you have a client secret called `client_secret.json` in the directory

## Usage

1. **Recording and Transcription**:
   - The system uses `pyaudio` to record audio samples of up to 10 seconds each.
   - The recorded audio is saved in MP3 format and transcribed to text using Google Cloud Speech-to-Text.

2. **Scam Analysis**:
   - The transcription is sent to a tuned Generative AI model to determine if the call has characteristics of a scam.
   - The AI model returns a "scam score," which is logged and can halt recordings if it exceeds a threshold.

### Key Functions

- **`generateAudioSample(filename)`**: Records audio and saves it as an MP3.
- **`transcribeAudioToText(file_name)`**: Transcribes an audio file into text using Google Cloud's Speech-to-Text.
- **`generateSTT(filename, chat_session)`**: Manages the process of recording, transcribing, and analyzing audio samples.
- **`process_audio(audio_filename, chat_session)`**: Transcribes and analyzes a single audio sample.
- **`main()`**: Initializes the AI model and begins the call detection process.

## Running the Application

To run the call simulation run:

```bash
python index.py
```

To run the application without call simulation, run:

```bash
python <your_script_name>.py
```

During execution, press **SPACE** (or hang up if you are using the simulation) to stop recording. The application will also stop if a high scam score is detected over multiple recordings.

## Configuration

Customize the model parameters and generation settings in `generation_config`. Adjust the **scam score threshold** and other parameters based on your use case.

## Note

This application assumes a pre-trained model located at `tunedModels/scamstuned-ski2920q7evd`. Replace this path if needed to match your model’s location.
