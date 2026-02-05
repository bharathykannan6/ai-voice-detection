# ✅ DEPLOYMENT CHECKLIST

Print this and check off as you go!

## BEFORE YOU START

- [ ] I have my trained model file: `voice_detector.pkl`
- [ ] I have a GitHub account (free)
- [ ] I have Git installed on my computer

---

## STEP 1: PREPARE FILES (2 minutes)

- [ ] Extract `railway_deploy` folder
- [ ] Copy model file:
  ```
  FROM: C:\AI VOICE DETECTION\AI_Voice_API\models\voice_detector.pkl
  TO:   railway_deploy\models\voice_detector.pkl
  ```
- [ ] Verify: Open `railway_deploy\models\` and see `voice_detector.pkl`

---

## STEP 2: SETUP GIT (2 minutes)

- [ ] Open Command Prompt
- [ ] Navigate: `cd railway_deploy`
- [ ] Run: `SETUP.bat` (or `git init`, `git add .`, `git commit -m "Initial"`)

---

## STEP 3: GITHUB (3 minutes)

- [ ] Go to: https://github.com/new
- [ ] Repository name: `ai-voice-detection`
- [ ] Visibility: **Public**
- [ ] **DO NOT** check "Add README"
- [ ] Click "Create repository"
- [ ] Copy the commands GitHub shows
- [ ] Run in Command Prompt:
  ```
  git remote add origin https://github.com/YOUR_USERNAME/ai-voice-detection.git
  git branch -M main
  git push -u origin main
  ```

---

## STEP 4: RAILWAY (3 minutes)

- [ ] Go to: https://railway.app/
- [ ] Click "Login" → Sign in with GitHub
- [ ] Click "New Project"
- [ ] Click "Deploy from GitHub repo"
- [ ] Select: `ai-voice-detection`
- [ ] Wait 2-3 minutes for deployment
- [ ] Click "Settings" tab
- [ ] Find "Domains" section
- [ ] Click "Generate Domain"
- [ ] Copy your URL: `https://....up.railway.app`

---

## STEP 5: TEST (2 minutes)

- [ ] Open: `https://your-url.up.railway.app/health`
  - Should show: `{"status":"healthy","model_loaded":true}`
- [ ] Open: `https://your-url.up.railway.app/docs`
  - Should show: Swagger API documentation
- [ ] Generate API key:
  - Click POST /generate-api-key
  - Click "Try it out"
  - Click "Execute"
  - Copy the `api_key`
- [ ] Test file upload:
  - Click "Authorize" button (top right)
  - Paste your API key
  - Click "Authorize" then "Close"
  - Find POST /detect/upload
  - Click "Try it out"
  - Upload an MP3 file
  - Click "Execute"
  - Should see classification result!

---

## 🎉 DONE!

Your API is LIVE!

**Save these:**
- API URL: `https://your-url.up.railway.app`
- API Key: `aivoice_...`
- Docs: `https://your-url.up.railway.app/docs`

**Share with others:**
```
API Documentation: https://your-url.up.railway.app/docs
```

---

## 📝 COMMON ISSUES

### ❌ "Model not loaded"
- Go back to STEP 1
- Make sure `voice_detector.pkl` is in `models/` folder
- Check Railway logs for errors

### ❌ "Build failed"
- Check Railway deployment logs
- Look for red error messages
- Usually: missing model file or wrong Python version

### ❌ "File too large" when pushing to GitHub
- Your model is >100MB
- Use Git LFS (see DEPLOY.md)

### ❌ Can't access Railway URL
- Wait 2-3 minutes after deployment
- Free tier servers may "sleep" - first request takes 30 sec
- Check Railway logs for errors

---

**Total Time: ~12 minutes** ⚡

Print this checklist and check off each box as you complete it!
