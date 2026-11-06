import os
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import init_db, add_clothing, get_all_clothes, delete_clothing, get_usage, increment_usage
from utils import detect_category, detect_color, generate_outfit

# ── App setup ────────────────────────────────────────────────────────────────

app = FastAPI(title="AI Styler")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

templates = Jinja2Templates(directory="templates")

CLOTHES_LIMIT = 35
OUTFIT_LIMIT  = 3

@app.on_event("startup")
def startup():
    init_db()

# ── Home / Wardrobe ──────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, message: str = "", error: str = ""):
    clothes = get_all_clothes()
    usage   = get_usage()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "clothes": clothes,
        "usage": usage,
        "clothes_limit": CLOTHES_LIMIT,
        "outfit_limit": OUTFIT_LIMIT,
        "message": message,
        "error": error,
    })

# ── Upload clothing ───────────────────────────────────────────────────────────

@app.post("/upload")
async def upload_clothing(request: Request, file: UploadFile = File(...)):
    usage = get_usage()
    if usage["clothes_uploaded"] >= CLOTHES_LIMIT:
        return RedirectResponse(
            url="/?error=Daily+upload+limit+reached+(35+items).+Try+again+tomorrow.",
            status_code=303
        )

    ext      = Path(file.filename).suffix or ".jpg"
    uid      = uuid.uuid4().hex[:8]
    filename = f"{uid}_{file.filename}"
    filepath = UPLOAD_DIR / filename

    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    category = detect_category(file.filename)
    color    = detect_color(str(filepath))

    add_clothing(filename, category, color)
    increment_usage("clothes_uploaded")

    return RedirectResponse(url=f"/?message={filename}+added+as+{category}+({color})", status_code=303)

# ── Delete clothing ───────────────────────────────────────────────────────────

@app.post("/delete/{item_id}")
async def delete_item(item_id: int):
    delete_clothing(item_id)
    return RedirectResponse(url="/?message=Item+deleted.", status_code=303)

# ── Outfit generator page ─────────────────────────────────────────────────────

@app.get("/outfit", response_class=HTMLResponse)
async def outfit_page(request: Request):
    usage = get_usage()
    return templates.TemplateResponse("outfit.html", {
        "request": request,
        "usage": usage,
        "outfit_limit": OUTFIT_LIMIT,
        "outfit": None,
        "style": "",
        "error": "",
    })

@app.post("/outfit", response_class=HTMLResponse)
async def generate_outfit_route(request: Request, style: str = Form(...)):
    usage = get_usage()

    if usage["outfits_generated"] >= OUTFIT_LIMIT:
        return templates.TemplateResponse("outfit.html", {
            "request": request,
            "usage": usage,
            "outfit_limit": OUTFIT_LIMIT,
            "outfit": None,
            "style": style,
            "error": f"Daily outfit limit reached ({OUTFIT_LIMIT} outfits). Come back tomorrow!",
        })

    wardrobe = get_all_clothes()
    if not wardrobe:
        return templates.TemplateResponse("outfit.html", {
            "request": request,
            "usage": usage,
            "outfit_limit": OUTFIT_LIMIT,
            "outfit": None,
            "style": style,
            "error": "Your wardrobe is empty! Upload some clothes first.",
        })

    result = generate_outfit(style, wardrobe)
    increment_usage("outfits_generated")
    usage = get_usage()  # refresh

    return templates.TemplateResponse("outfit.html", {
        "request": request,
        "usage": usage,
        "outfit_limit": OUTFIT_LIMIT,
        "outfit": result,
        "style": style,
        "error": "",
    })

# ── API: wardrobe JSON ────────────────────────────────────────────────────────

@app.get("/api/wardrobe")
async def api_wardrobe():
    return JSONResponse(get_all_clothes())
