# 🚀 DEPLOY TO RAILWAY - STEP BY STEP

## ⚡ QUICK STEPS

### 1️⃣ Add Your Model File

**IMPORTANT:** Copy your trained model to this folder!

```
FROM: C:\AI VOICE DETECTION\AI_Voice_API\models\voice_detector.pkl
TO:   models/voice_detector.pkl
```

Verify:
```bash
dir models\voice_detector.pkl
```

### 2️⃣ Initialize Git

```bash
cd railway_deploy
git init
git add .
git commit -m "Initial commit"
```

### 3️⃣ Create GitHub Repository

1. Go to: https://github.com/new
2. Name: `ai-voice-detection`
3. Keep **PUBLIC**
4. **DO NOT** check "Initialize with README"
5. Click "Create repository"

### 4️⃣ Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-voice-detection.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username!

### 5️⃣ Deploy on Railway

1. Go to: https://railway.app/
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose: `ai-voice-detection`
6. Railway auto-deploys! ⚡

**Wait 2-3 minutes...**

### 6️⃣ Get Your Live URL

Railway will show:
```
https://ai-voice-detection-production.up.railway.app
```

### 7️⃣ Test Your API

Open browser:
```
https://your-url.up.railway.app/docs
```

You'll see Swagger UI! 🎉

---

## 🧪 TEST YOUR API

### Generate API Key

```bash
curl -X POST https://your-url.up.railway.app/generate-api-key
```

Copy the `api_key` from response.

### Test File Upload

In browser at `/docs`:
1. Click **"Authorize"** button
2. Enter your API key
3. Go to **POST /detect/upload**
4. Click "Try it out"
5. Upload an MP3 file
6. Click "Execute"

---

## 📁 WHAT'S IN THIS FOLDER

```
railway_deploy/
├── app.py              ✅ Main API (production-ready)
├── requirements.txt    ✅ Dependencies
├── Procfile           ✅ Railway config
├── .gitignore         ✅ Git rules
├── README.md          ✅ API docs
├── DEPLOY.md          ✅ This file
└── models/
    └── voice_detector.pkl  ⚠️ ADD YOUR MODEL HERE!
```

---

## ⚠️ TROUBLESHOOTING

### Model Not Found

Check:
```bash
# Should show the file
dir models\voice_detector.pkl
```

If missing, copy from:
```
C:\AI VOICE DETECTION\AI_Voice_API\models\voice_detector.pkl
```

### Build Failed on Railway

Check Railway logs:
- Click on your project
- Go to "Deployments"
- Click latest deployment
- View logs

Common issues:
- Missing `voice_detector.pkl`
- Wrong Python version
- Dependency conflicts

### Model Too Large (>100MB)

Use Git LFS:
```bash
git lfs install
git lfs track "models/*.pkl"
git add .gitattributes
git add models/voice_detector.pkl
git commit -m "Add model with LFS"
git push
```

---

## ✅ CHECKLIST

Before deploying:

- [ ] Copied `voice_detector.pkl` to `models/` folder
- [ ] Verified file exists: `dir models\voice_detector.pkl`
- [ ] Initialized Git: `git init`
- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] Deployed on Railway
- [ ] Got live URL
- [ ] Tested `/health` endpoint
- [ ] Generated API key
- [ ] Tested file upload

---

## 🎉 SUCCESS!

Once deployed, you'll have:
- ✅ Live API endpoint
- ✅ Interactive documentation at `/docs`
- ✅ API key authentication
- ✅ Support for 5 languages
- ✅ Auto-scaling on Railway

Share your API:
```
https://your-app.up.railway.app
```

---

## 🔄 UPDATE YOUR API

Make changes and redeploy:

```bash
git add .
git commit -m "Updated API"
git push
```

Railway auto-deploys! ⚡

---

**Need help? Check Railway logs or Railway Discord!**
