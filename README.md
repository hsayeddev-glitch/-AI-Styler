# 👗 AI Styler — Hackathon MVP

A full-stack AI-powered wardrobe & outfit generator built with FastAPI + OpenCV + SQLite.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the server
```bash
uvicorn main:app --reload
```

### 3. Open in browser
```
http://localhost:8000
```

---

## 📁 Project Structure

```
project/
├── main.py          # FastAPI routes & app entry point
├── database.py      # SQLite helpers (init, CRUD, usage tracking)
├── models.py        # Pydantic data models
├── utils.py         # Image classification & outfit generation logic
├── requirements.txt # Python dependencies
├── wardrobe.db      # Auto-created SQLite database
├── uploads/         # Auto-created folder for uploaded images
└── templates/
    ├── base.html    # Shared layout + CSS design system
    ├── index.html   # Wardrobe / Home page
    └── outfit.html  # Outfit Generator page
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 📸 Clothes Upload | Upload images → auto-detect category & color via OpenCV |
| 👗 Digital Wardrobe | Browse, view, and delete clothing items |
| 🪄 Outfit Generator | Type a style (casual, formal, streetwear…) → get a curated outfit |
| 📊 Usage Limits | 35 uploads/day · 3 outfit generations/day (resets at midnight) |
| 🎨 Color Matching | Outfit picks prefer colors that match the chosen style |

---

## 🎨 Supported Styles
`casual` · `formal` · `streetwear` · `classic` · `sporty` · `chic` · `smart`

---

## ⚙️ Tech Stack
- **Backend**: Python 3.10+ / FastAPI
- **Frontend**: Jinja2 HTML templates + vanilla CSS/JS
- **Database**: SQLite (auto-created)
- **Image Processing**: OpenCV (color detection) + rule-based category detection
- **No paid APIs required**

---

## 📝 Notes
- The database (`wardrobe.db`) and uploads folder are created automatically on first run.
- Usage limits reset daily based on server date.
- Category detection uses filename keywords; falls back to random assignment.
- Color detection uses HSV color space analysis via OpenCV.
