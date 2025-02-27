
import io
import torch
import torchaudio
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import uvicorn

app = FastAPI()

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

@app.get("/ping")
def ping():
    """
    Simple health check endpoint
    Returns 'pong' if the service is running.
    """
    return "pong"

@app.post("/asr")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Endpoint: /asr
    Accepts an MP3 audio file via multipart/form-data.
    Returns a JSON response with 'transcription' and 'duration'.
    """

    # 1. Check if a file was uploaded
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded."
        )

    try:
        # 2. Read the file bytes
        audio_bytes = await file.read()

        # 3. Attempt to decode the audio
        #    We rely on torchaudio to detect that it's MP3 (or fail otherwise).
        try:
            audio, sr = torchaudio.load(io.BytesIO(audio_bytes), format="mp3")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not decode audio: {str(e)}"
            )

        # 4. Resample to 16 kHz if necessary (Wav2Vec2 expects 16 kHz mono)
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(sr, 16000)
            audio = resampler(audio)
            sr = 16000

        # 5. Convert multi-channel to mono if needed
        if audio.ndim > 1 and audio.shape[0] > 1:
            audio = torch.mean(audio, dim=0)
        # Remove any leftover first dimension
        if audio.ndim > 1:
            audio = audio.squeeze(0)

        # 6. Preprocess and run model inference
        input_values = processor(
            audio,
            sampling_rate=sr,
            return_tensors="pt"
        ).input_values

        with torch.no_grad():
            logits = model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(predicted_ids[0])

        # 7. Calculate duration in seconds
        duration_sec = audio.shape[-1] / sr

        return {
            "transcription": transcription,
            "duration": str(duration_sec)
        }

    except HTTPException:
        # Re-raise HTTPExceptions so FastAPI can handle them
        raise
    except Exception as e:
        # Catch-all for other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
