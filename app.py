"""
AI Voice Detection API - Railway Deployment
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import base64
import tempfile
import os
import numpy as np
import librosa
import joblib
from pathlib import Path
import logging
import secrets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Voice Detection API",
    description="Detect AI-generated vs Human voices",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

VALID_API_KEYS = {
    os.getenv("API_KEY", "demo_key_12345"): {"name": "Default", "requests": 0},
}

model = None
scaler = None
MODEL_PATH = Path("models/voice_detector.pkl")


class VoiceRequest(BaseModel):
    audio_base64: str
    language: Optional[str] = "english"


class VoiceResponse(BaseModel):
    classification: str
    confidence: float
    confidence_percentage: str
    explanation: str
    language: Optional[str]


class APIKeyResponse(BaseModel):
    api_key: str
    message: str


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header in VALID_API_KEYS:
        VALID_API_KEYS[api_key_header]["requests"] += 1
        return api_key_header
    raise HTTPException(403, "Invalid API Key")


def extract_features(audio_path: str) -> np.ndarray:
    try:
        y, sr = librosa.load(audio_path, sr=22050, duration=30)
        if len(y) == 0:
            raise ValueError("Empty audio")
        y = librosa.util.normalize(y)
        
        features = []
        
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        features.extend([
            np.mean(mfcc, axis=1),
            np.std(mfcc, axis=1),
            np.max(mfcc, axis=1),
            np.min(mfcc, axis=1)
        ])
        
        features.extend([
            [np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0]),
             np.std(librosa.feature.spectral_centroid(y=y, sr=sr)[0])],
            [np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)[0]),
             np.std(librosa.feature.spectral_rolloff(y=y, sr=sr)[0])],
            [np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]),
             np.std(librosa.feature.spectral_bandwidth(y=y, sr=sr)[0])]
        ])
        
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        features.append([np.mean(zcr), np.std(zcr)])
        
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features.append(np.mean(chroma, axis=1))
        
        flat = []
        for f in features:
            if isinstance(f, (list, np.ndarray)):
                flat.extend(np.array(f).flatten())
            else:
                flat.append(f)
        
        return np.array(flat)
    except Exception as e:
        logger.error(f"Feature extraction error: {e}")
        raise ValueError(f"Failed to extract features: {str(e)}")


def load_model():
    global model, scaler
    try:
        if MODEL_PATH.exists():
            data = joblib.load(MODEL_PATH)
            model = data['model']
            scaler = data['scaler']
            logger.info("✓ Model loaded successfully")
            return True
        logger.warning(f"⚠ Model not found at {MODEL_PATH}")
        return False
    except Exception as e:
        logger.error(f"Model load error: {e}")
        return False


@app.on_event("startup")
async def startup_event():
    load_model()


@app.get("/")
async def root():
    return {
        "message": "AI Voice Detection API",
        "version": "1.0.0",
        "status": "running",
        "model_loaded": model is not None,
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/generate-api-key", response_model=APIKeyResponse)
async def generate_api_key():
    new_key = f"aivoice_{secrets.token_urlsafe(32)}"
    VALID_API_KEYS[new_key] = {"name": "User", "requests": 0}
    return APIKeyResponse(
        api_key=new_key,
        message="API key generated successfully"
    )


@app.post("/detect", response_model=VoiceResponse)
async def detect_voice(
    request: VoiceRequest,
    api_key: str = Depends(get_api_key)
):
    if model is None:
        raise HTTPException(503, "Model not loaded")
    
    temp_path = None
    try:
        audio_base64 = request.audio_base64
        if ',' in audio_base64:
            audio_base64 = audio_base64.split(',')[1]
        audio_bytes = base64.b64decode(audio_base64)
        
        if len(audio_bytes) == 0:
            raise ValueError("Empty audio")
        
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(audio_bytes)
            temp_path = f.name
        
        features = extract_features(temp_path)
        features_scaled = scaler.transform(features.reshape(1, -1))
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        label = "AI-Generated" if prediction == 1 else "Human"
        confidence = float(probabilities[prediction])
        
        conf_level = "Very high" if confidence > 0.9 else "High" if confidence > 0.75 else "Medium" if confidence > 0.6 else "Low"
        
        if prediction == 1:
            explanation = f"{conf_level} confidence ({confidence*100:.1f}%) that this is AI-generated."
        else:
            explanation = f"{conf_level} confidence ({confidence*100:.1f}%) that this is human speech."
        
        return VoiceResponse(
            classification=label,
            confidence=confidence,
            confidence_percentage=f"{confidence*100:.1f}%",
            explanation=explanation,
            language=request.language
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass


@app.post("/detect/upload", response_model=VoiceResponse)
async def detect_upload(
    file: UploadFile = File(...),
    language: Optional[str] = "english",
    api_key: str = Depends(get_api_key)
):
    if model is None:
        raise HTTPException(503, "Model not loaded")
    
    if not file.filename.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
        raise HTTPException(400, "Invalid format")
    
    temp_path = None
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(400, "Empty file")
        
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(contents)
            temp_path = f.name
        
        features = extract_features(temp_path)
        features_scaled = scaler.transform(features.reshape(1, -1))
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        label = "AI-Generated" if prediction == 1 else "Human"
        confidence = float(probabilities[prediction])
        
        conf_level = "Very high" if confidence > 0.9 else "High" if confidence > 0.75 else "Medium" if confidence > 0.6 else "Low"
        
        if prediction == 1:
            explanation = f"{conf_level} confidence ({confidence*100:.1f}%) that this is AI-generated."
        else:
            explanation = f"{conf_level} confidence ({confidence*100:.1f}%) that this is human speech."
        
        return VoiceResponse(
            classification=label,
            confidence=confidence,
            confidence_percentage=f"{confidence*100:.1f}%",
            explanation=explanation,
            language=language
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
