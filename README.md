# 🎙️ AI Voice Detection API

Detect AI-generated vs Human voices across multiple languages.

## 🚀 Live API

**Documentation:** [Your Railway URL]/docs

## 📡 API Endpoints

### 1. Generate API Key
```bash
POST /generate-api-key
```

### 2. Detect Voice (Upload)
```bash
POST /detect/upload
Headers: X-API-Key: your_key
Body: file (MP3/WAV/OGG/FLAC)
```

### 3. Detect Voice (Base64)
```bash
POST /detect
Headers: X-API-Key: your_key
Body: {"audio_base64": "...", "language": "english"}
```

## 📊 Response Format

```json
{
  "classification": "Human" | "AI-Generated",
  "confidence": 0.95,
  "confidence_percentage": "95.0%",
  "explanation": "High confidence that...",
  "language": "english"
}
```

## 🌐 Supported Languages

- English
- Tamil
- Hindi
- Malayalam
- Telugu

## 🔧 Tech Stack

- FastAPI
- Librosa (audio processing)
- Scikit-learn (ML model)
- Railway (hosting)

## 📝 License

MIT
