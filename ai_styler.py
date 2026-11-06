#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║           AI STYLER — All-in-One Standalone App          ║
║  Run:  python ai_styler.py                               ║
║  Then open:  http://localhost:8000                       ║
╚══════════════════════════════════════════════════════════╝

Install kar phele 😊🙏:
    pip install fastapi uvicorn[standard] jinja2 python-multipart opencv-python-headless numpy aiofiles
"""

import os, sys, shutil, uuid, random, sqlite3
from pathlib import Path
from datetime import date
from types import SimpleNamespace

# ══════════════════════════════════════════════════════════════
#  EMBEDDED TEMPLATES
# ══════════════════════════════════════════════════════════════

BASE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{% block title %}AI Styler{% endblock %}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --cream:#F5F0E8; --warm:#EDE6D6; --ink:#1A1510; --ink2:#3D3530;
      --gold:#C9A84C; --gold2:#E8C97A; --rust:#B85C38; --sage:#7A9E7E;
      --muted:#8C7B6B; --border:#D4C9B8; --card:#FDFAF5;
      --shadow:0 4px 24px rgba(26,21,16,.10); --shadow-lg:0 16px 56px rgba(26,21,16,.18);
      --r:14px;
    }
    @keyframes fadeUp   { from{opacity:0;transform:translateY(22px)} to{opacity:1;transform:translateY(0)} }
    @keyframes fadeIn   { from{opacity:0} to{opacity:1} }
    @keyframes slideIn  { from{opacity:0;transform:translateX(-18px)} to{opacity:1;transform:translateX(0)} }
    @keyframes popIn    { from{opacity:0;transform:scale(.88)} to{opacity:1;transform:scale(1)} }
    @keyframes spin     { to{transform:rotate(360deg)} }
    @keyframes pulse    { 0%,100%{opacity:1} 50%{opacity:.5} }
    .anim-fade-up  { animation: fadeUp  .55s cubic-bezier(.22,1,.36,1) both; }
    .anim-fade-in  { animation: fadeIn  .4s ease both; }
    .anim-pop-in   { animation: popIn   .45s cubic-bezier(.34,1.56,.64,1) both; }
    .anim-slide-in { animation: slideIn .45s cubic-bezier(.22,1,.36,1) both; }
    .delay-1{animation-delay:.08s;} .delay-2{animation-delay:.16s;} .delay-3{animation-delay:.24s;}
    body { font-family:'DM Sans',sans-serif; background:var(--cream); color:var(--ink); min-height:100vh; line-height:1.6; }
    nav { background:var(--ink); padding:0 2rem; display:flex; align-items:center; gap:2rem; height:64px; position:sticky; top:0; z-index:200; box-shadow:0 2px 20px rgba(0,0,0,.35); }
    .nav-brand { font-family:'Playfair Display',serif; font-size:1.45rem; color:var(--gold); letter-spacing:.02em; flex:1; text-decoration:none; transition:opacity .2s; }
    .nav-brand:hover{opacity:.85;} .nav-brand span{color:var(--cream);font-style:italic;}
    nav a { color:#bbb; text-decoration:none; font-size:.85rem; font-weight:500; letter-spacing:.06em; text-transform:uppercase; padding:.35rem 0; border-bottom:2px solid transparent; transition:color .2s,border-color .2s; }
    nav a:hover, nav a.active { color:var(--gold); border-color:var(--gold); }
    .page-header { background:linear-gradient(135deg,var(--ink) 0%,#2E2218 60%,#1a1510 100%); color:var(--cream); padding:3.5rem 2rem 3rem; margin-bottom:2.5rem; position:relative; overflow:hidden; }
    .page-header::before { content:''; position:absolute; inset:0; background:repeating-linear-gradient(45deg,transparent,transparent 40px,rgba(201,168,76,.05) 40px,rgba(201,168,76,.05) 80px); }
    .page-header::after  { content:''; position:absolute; bottom:-2px; left:0; right:0; height:3px; background:linear-gradient(90deg,transparent,var(--gold),transparent); }
    .page-header-inner { max-width:1200px; margin:0 auto; padding:0 2rem; position:relative; }
    .page-header h1 { font-family:'Playfair Display',serif; font-size:clamp(2rem,4vw,3.4rem); font-weight:900; line-height:1.1; animation:fadeUp .6s cubic-bezier(.22,1,.36,1) both; }
    .page-header h1 em { color:var(--gold); font-style:italic; }
    .page-header p { color:#aaa; margin-top:.7rem; font-size:1rem; animation:fadeUp .6s .1s cubic-bezier(.22,1,.36,1) both; }
    .container { max-width:1200px; margin:0 auto; padding:2.5rem 2rem; }
    .two-col { display:grid; grid-template-columns:340px 1fr; gap:2rem; align-items:start; }
    @media(max-width:768px){.two-col{grid-template-columns:1fr;}}
    .card { background:var(--card); border:1px solid var(--border); border-radius:var(--r); box-shadow:var(--shadow); overflow:hidden; transition:box-shadow .25s; }
    .card:hover{box-shadow:var(--shadow-lg);}
    .card-header { padding:1.25rem 1.5rem; border-bottom:1px solid var(--border); display:flex; align-items:center; gap:.75rem; background:linear-gradient(to right,var(--warm),var(--card)); }
    .card-header h2 { font-family:'Playfair Display',serif; font-size:1.15rem; font-weight:700; }
    .card-body { padding:1.5rem; }
    .btn { display:inline-flex; align-items:center; gap:.5rem; padding:.72rem 1.5rem; border-radius:9px; font-family:'DM Sans',sans-serif; font-weight:500; font-size:.9rem; cursor:pointer; border:none; text-decoration:none; transition:all .22s; letter-spacing:.02em; }
    .btn-gold  { background:var(--gold); color:var(--ink); }
    .btn-gold:hover  { background:var(--gold2); transform:translateY(-2px); box-shadow:0 6px 20px rgba(201,168,76,.45); }
    .btn-ink   { background:var(--ink); color:var(--cream); }
    .btn-ink:hover   { background:var(--ink2); transform:translateY(-2px); }
    .btn-ghost { background:transparent; color:var(--rust); border:1px solid var(--rust); }
    .btn-ghost:hover { background:var(--rust); color:white; }
    .btn-sage  { background:var(--sage); color:white; }
    .btn-sage:hover  { background:#6a9270; }
    .btn-sm{padding:.4rem .9rem;font-size:.8rem;}
    .btn:active{transform:translateY(0) scale(.97);}
    .usage-bar-wrap{margin-bottom:.4rem;}
    .usage-label{display:flex;justify-content:space-between;font-size:.8rem;color:var(--muted);margin-bottom:.35rem;}
    .usage-track{height:7px;background:var(--warm);border-radius:99px;overflow:hidden;}
    .usage-fill{height:100%;border-radius:99px;}
    .usage-fill.ok   { background:linear-gradient(90deg,var(--sage),#9dc9a1); }
    .usage-fill.warn { background:linear-gradient(90deg,var(--gold),var(--gold2)); }
    .usage-fill.full { background:linear-gradient(90deg,var(--rust),#d97a5a); }
    .alert { padding:.9rem 1.2rem; border-radius:var(--r); font-size:.9rem; margin-bottom:1.5rem; display:flex; align-items:flex-start; gap:.7rem; animation:slideIn .4s cubic-bezier(.22,1,.36,1) both; }
    .alert-success{background:#EDF7EE;border:1px solid #7A9E7E;color:#2D5C32;}
    .alert-error  {background:#FDF0EC;border:1px solid #B85C38;color:#7A2C10;}
    .alert-warn   {background:#FDF8EC;border:1px solid #C9A84C;color:#6B5010;}
    .tag{display:inline-block;padding:.22rem .7rem;border-radius:99px;font-size:.74rem;font-weight:500;letter-spacing:.03em;text-transform:capitalize;}
    .tag-cat  {background:var(--warm);color:var(--ink2);border:1px solid var(--border);}
    .tag-color{background:var(--ink); color:var(--gold);}
    .clothes-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(185px,1fr));gap:1.25rem;}
    .clothing-card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;transition:transform .25s,box-shadow .25s;animation:fadeUp .5s cubic-bezier(.22,1,.36,1) both;}
    .clothing-card:hover{transform:translateY(-5px);box-shadow:var(--shadow-lg);}
    .clothing-img{width:100%;aspect-ratio:1;object-fit:cover;background:var(--warm);display:block;transition:transform .35s;}
    .clothing-card:hover .clothing-img{transform:scale(1.05);}
    .clothing-placeholder{width:100%;aspect-ratio:1;background:linear-gradient(135deg,var(--warm),var(--border));display:flex;align-items:center;justify-content:center;font-size:3.2rem;transition:transform .35s;}
    .clothing-card:hover .clothing-placeholder{transform:scale(1.06);}
    .clothing-info{padding:.85rem;}
    .clothing-name    {font-size:.82rem;font-weight:500;color:var(--ink);margin-bottom:.15rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
    .clothing-filename{font-size:.73rem;color:var(--muted);margin-bottom:.45rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
    .clothing-tags{display:flex;gap:.3rem;flex-wrap:wrap;margin-bottom:.65rem;}
    .card-actions{display:flex;gap:.4rem;}
    .card-actions .btn{flex:1;justify-content:center;}
    .upload-zone{border:2px dashed var(--border);border-radius:var(--r);padding:2.5rem 1.5rem;text-align:center;cursor:pointer;transition:all .25s;background:var(--warm);display:block;}
    .upload-zone:hover{border-color:var(--gold);background:#F0E8D4;transform:scale(1.01);}
    .upload-zone input[type=file]{display:none;}
    .upload-icon{font-size:3rem;margin-bottom:.75rem;transition:transform .3s;display:inline-block;}
    .upload-zone:hover .upload-icon{transform:scale(1.15) rotate(-5deg);}
    .upload-zone h3{font-family:'Playfair Display',serif;font-size:1.1rem;margin-bottom:.3rem;}
    .upload-zone p{font-size:.85rem;color:var(--muted);}
    .file-chosen{margin-top:.8rem;font-size:.85rem;color:var(--sage);font-weight:500;}
    .style-chips{display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:1rem;}
    .chip{padding:.4rem 1.05rem;border-radius:99px;border:1px solid var(--border);background:white;font-size:.84rem;cursor:pointer;transition:all .2s;font-family:'DM Sans',sans-serif;}
    .chip:hover,.chip.active{background:var(--ink);color:var(--gold);border-color:var(--ink);transform:translateY(-1px);}
    .style-input{width:100%;padding:.85rem 1rem;border:1.5px solid var(--border);border-radius:10px;font-family:'DM Sans',sans-serif;font-size:1rem;background:white;color:var(--ink);outline:none;transition:border-color .2s,box-shadow .2s;margin-bottom:1rem;}
    .style-input:focus{border-color:var(--gold);box-shadow:0 0 0 3px rgba(201,168,76,.18);}
    .outfit-result{background:linear-gradient(145deg,var(--ink),#2E2218 60%,#1a1510);border-radius:var(--r);padding:2rem;color:var(--cream);animation:popIn .5s cubic-bezier(.34,1.56,.64,1) both;border:1px solid rgba(201,168,76,.2);box-shadow:0 12px 48px rgba(0,0,0,.3);}
    .outfit-result h3{font-family:'Playfair Display',serif;font-size:1.5rem;color:var(--gold);margin-bottom:1.25rem;}
    .outfit-items{display:flex;flex-direction:column;gap:.8rem;}
    .outfit-item{display:flex;align-items:center;gap:1rem;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:11px;padding:.85rem 1rem;transition:background .2s,transform .2s;animation:slideIn .4s cubic-bezier(.22,1,.36,1) both;}
    .outfit-item:hover{background:rgba(255,255,255,.12);transform:translateX(4px);}
    .outfit-item-img{width:58px;height:58px;border-radius:9px;object-fit:cover;flex-shrink:0;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);}
    .outfit-item-ph {width:58px;height:58px;border-radius:9px;background:rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center;font-size:1.7rem;flex-shrink:0;border:1px solid rgba(255,255,255,.12);}
    .outfit-item-info .cat  {font-size:.7rem;color:var(--gold);text-transform:uppercase;letter-spacing:.09em;}
    .outfit-item-info .fname{font-size:.88rem;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
    .outfit-item-info .clr  {font-size:.78rem;color:#aaa;}
    .outfit-missing{margin-top:1rem;padding:.8rem 1rem;background:rgba(184,92,56,.2);border:1px solid rgba(184,92,56,.4);border-radius:10px;font-size:.85rem;}
    .empty{text-align:center;padding:4rem 2rem;color:var(--muted);}
    .empty .icon{font-size:4.5rem;margin-bottom:1rem;animation:pulse 3s ease infinite;}
    .empty h3{font-family:'Playfair Display',serif;font-size:1.5rem;color:var(--ink2);margin-bottom:.5rem;}
    /* Modal */
    .modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:500;display:flex;align-items:center;justify-content:center;animation:fadeIn .2s ease both;backdrop-filter:blur(4px);}
    .modal-box{background:var(--card);border-radius:var(--r);box-shadow:var(--shadow-lg);width:min(480px,92vw);animation:popIn .35s cubic-bezier(.34,1.56,.64,1) both;overflow:hidden;border:1px solid var(--border);}
    .modal-header{padding:1.25rem 1.5rem;border-bottom:1px solid var(--border);background:linear-gradient(to right,var(--warm),var(--card));display:flex;align-items:center;justify-content:space-between;}
    .modal-header h3{font-family:'Playfair Display',serif;font-size:1.15rem;}
    .modal-close{background:none;border:none;font-size:1.4rem;cursor:pointer;color:var(--muted);line-height:1;transition:color .2s;}
    .modal-close:hover{color:var(--rust);}
    .modal-body{padding:1.5rem;}
    .modal-preview{width:100%;max-height:200px;object-fit:cover;border-radius:10px;margin-bottom:1.25rem;display:block;}
    .modal-preview-ph{width:100%;height:140px;background:linear-gradient(135deg,var(--warm),var(--border));border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:4rem;margin-bottom:1.25rem;}
    .form-group{margin-bottom:1rem;}
    .form-label{display:block;font-size:.85rem;font-weight:500;color:var(--ink2);margin-bottom:.4rem;}
    .form-input,.form-select{width:100%;padding:.75rem 1rem;border:1.5px solid var(--border);border-radius:9px;font-family:'DM Sans',sans-serif;font-size:.95rem;background:white;color:var(--ink);outline:none;transition:border-color .2s,box-shadow .2s;}
    .form-input:focus,.form-select:focus{border-color:var(--gold);box-shadow:0 0 0 3px rgba(201,168,76,.15);}
    .modal-actions{display:flex;gap:.75rem;margin-top:1.25rem;}
    .modal-actions .btn{flex:1;justify-content:center;}
    .spinner{width:18px;height:18px;border:2px solid rgba(26,21,16,.2);border-top-color:var(--ink);border-radius:50%;animation:spin .7s linear infinite;}
    footer{text-align:center;padding:2rem;color:var(--muted);font-size:.82rem;margin-top:2rem;border-top:1px solid var(--border);}
  </style>
</head>
<body>
  <nav>
    <a class="nav-brand" href="/"><span>AI</span> Styler</a>
    <a href="/" {% if request.url.path == "/" %}class="active"{% endif %}>Wardrobe</a>
    <a href="/outfit" {% if request.url.path == "/outfit" %}class="active"{% endif %}>Outfit Generator</a>
  </nav>
  {% block content %}{% endblock %}
  <footer>AI Styler &nbsp;·&nbsp; Hackathon MVP &nbsp;·&nbsp; Built with FastAPI &amp; OpenCV</footer>
  <script>
    const CAT_EMOJI={shirt:"👕",hoodie:"🧥",jacket:"🥼",pants:"👖",shoes:"👟",dress:"👗",accessory:"👒",default:"👔"};
    function catEmoji(c){return CAT_EMOJI[c]||CAT_EMOJI.default;}
    document.addEventListener('DOMContentLoaded',()=>{
      document.querySelectorAll('.clothing-card').forEach((c,i)=>{c.style.animationDelay=(i*0.06)+'s';});
    });
  </script>
  {% block scripts %}{% endblock %}
</body>
</html>
"""

INDEX_HTML = r"""{% extends "base.html" %}
{% block title %}Wardrobe — AI Styler{% endblock %}
{% block content %}
<div class="page-header">
  <div class="page-header-inner">
    <h1>Your Digital <em>Wardrobe</em></h1>
    <p>Upload clothes, rename & fix labels, then generate perfect outfits.</p>
  </div>
</div>
<div class="container">
  {% if message %}<div class="alert alert-success anim-slide-in">✅ {{ message }}</div>{% endif %}
  {% if error   %}<div class="alert alert-error  anim-slide-in">⚠️ {{ error }}</div>{% endif %}
  <div class="two-col">
    <!-- LEFT -->
    <div style="display:flex;flex-direction:column;gap:1.5rem;">
      <div class="card anim-fade-up">
        <div class="card-header"><span>📊</span><h2>Today's Usage</h2></div>
        <div class="card-body">
          {% set cu=usage.clothes_uploaded  %}{% set cp=[(cu*100//clothes_limit),100]|min %}
          {% set ou=usage.outfits_generated %}{% set op=[(ou*100//outfit_limit), 100]|min %}
          <div class="usage-bar-wrap">
            <div class="usage-label"><span>Uploads</span><span>{{ cu }}&thinsp;/&thinsp;{{ clothes_limit }}</span></div>
            <div class="usage-track"><div class="usage-fill {% if cp>=100 %}full{% elif cp>=70 %}warn{% else %}ok{% endif %}" style="width:{{ cp }}%;transition:width 1s cubic-bezier(.22,1,.36,1)"></div></div>
          </div>
          <div class="usage-bar-wrap" style="margin-top:.8rem;">
            <div class="usage-label"><span>Outfits Generated</span><span>{{ ou }}&thinsp;/&thinsp;{{ outfit_limit }}</span></div>
            <div class="usage-track"><div class="usage-fill {% if op>=100 %}full{% elif op>=67 %}warn{% else %}ok{% endif %}" style="width:{{ op }}%;transition:width 1s .2s cubic-bezier(.22,1,.36,1)"></div></div>
          </div>
          {% if cu>=clothes_limit %}<div class="alert alert-warn" style="margin-top:1rem;margin-bottom:0;">🚫 Upload limit reached. Resets at midnight.</div>{% endif %}
        </div>
      </div>
      <div class="card anim-fade-up delay-1">
        <div class="card-header"><span>📸</span><h2>Upload Clothing</h2></div>
        <div class="card-body">
          {% if usage.clothes_uploaded >= clothes_limit %}
          <div class="alert alert-error" style="margin-bottom:0;">Daily limit reached ({{ clothes_limit }} items). Come back tomorrow!</div>
          {% else %}
          <label class="upload-zone" for="fileInput">
            <input type="file" name="file" id="fileInput" accept="image/*" onchange="onFileChosen(this)">
            <div class="upload-icon">📷</div>
            <h3>Drop or click to upload</h3>
            <p>JPG, PNG, WEBP supported</p>
            <div class="file-chosen" id="fileChosen"></div>
          </label>
          {% endif %}
        </div>
      </div>
      <a href="/outfit" class="btn btn-ink anim-fade-up delay-2" style="justify-content:center;">👗 Generate an Outfit →</a>
    </div>
    <!-- RIGHT -->
    <div>
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.25rem;" class="anim-fade-in">
        <h2 style="font-family:'Playfair Display',serif;font-size:1.5rem;">
          My Clothes
          <span style="font-family:'DM Sans',sans-serif;font-size:.95rem;font-weight:400;color:var(--muted);margin-left:.5rem;">({{ clothes|length }} item{{ 's' if clothes|length!=1 }})</span>
        </h2>
        {% if clothes %}<span style="font-size:.82rem;color:var(--muted);">Newest first</span>{% endif %}
      </div>
      {% if clothes %}
      <div class="clothes-grid">
        {% for item in clothes %}
        <div class="clothing-card">
          <div style="overflow:hidden;">
            {% set ext=item.filename.split('.')[-1].lower() %}
            {% if ext in ['jpg','jpeg','png','webp','gif'] %}
            <img src="/uploads/{{ item.filename }}" alt="{{ item.label or item.category }}" class="clothing-img"
                 onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
            <div class="clothing-placeholder" style="display:none;" data-cat="{{ item.category }}"></div>
            {% else %}
            <div class="clothing-placeholder" data-cat="{{ item.category }}"></div>
            {% endif %}
          </div>
          <div class="clothing-info">
            <div class="clothing-name">{{ item.label if item.label else item.filename }}</div>
            <div class="clothing-filename" title="{{ item.filename }}">{{ item.filename }}</div>
            <div class="clothing-tags">
              <span class="tag tag-cat">{{ item.category }}</span>
              <span class="tag tag-color">{{ item.color }}</span>
            </div>
            <div class="card-actions">
              <button class="btn btn-sage btn-sm"
                onclick="openEdit({{ item.id }},'{{ (item.label or '') | replace("'","") }}','{{ item.category }}')">✏️ Edit</button>
              <form action="/delete/{{ item.id }}" method="post" onsubmit="return confirm('Remove this item?')" style="flex:1;">
                <button type="submit" class="btn btn-ghost btn-sm" style="width:100%;">🗑</button>
              </form>
            </div>
          </div>
        </div>
        {% endfor %}
      </div>
      {% else %}
      <div class="empty anim-fade-up"><div class="icon">👗</div><h3>Your wardrobe is empty</h3><p>Upload some clothes to get started!</p></div>
      {% endif %}
    </div>
  </div>
</div>

<!-- UPLOAD PREVIEW MODAL -->
<div class="modal-overlay" id="uploadModal" style="display:none;">
  <div class="modal-box">
    <div class="modal-header">
      <h3>✨ Review before adding</h3>
      <button class="modal-close" onclick="closeUploadModal()">×</button>
    </div>
    <div class="modal-body">
      <img id="previewImg" class="modal-preview" src="" alt="preview" style="display:none;">
      <div class="modal-preview-ph" id="previewPh">📷</div>
      <form action="/upload" method="post" enctype="multipart/form-data" id="uploadForm">
        <input type="file" name="file" id="hiddenFile" style="display:none;">
        <div class="form-group">
          <label class="form-label">Item Name</label>
          <input type="text" name="label" id="modalLabel" class="form-input" placeholder="e.g. My Blue Denim Jacket" maxlength="80">
        </div>
        <div class="form-group">
          <label class="form-label">Category <span style="font-size:.75rem;color:var(--muted);font-weight:400;">— auto-detected, change if wrong</span></label>
          <select name="category" id="modalCategory" class="form-select">
            <option value="">Auto detect</option>
            <option value="shirt">👕 Shirt / T-Shirt / Top</option>
            <option value="hoodie">🧥 Hoodie / Sweatshirt</option>
            <option value="jacket">🥼 Jacket / Coat / Blazer</option>
            <option value="pants">👖 Pants / Jeans / Trousers</option>
            <option value="shoes">👟 Shoes / Sneakers / Boots</option>
            <option value="dress">👗 Dress / Skirt</option>
            <option value="accessory">👒 Accessory / Hat / Bag</option>
          </select>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-ghost" onclick="closeUploadModal()">Cancel</button>
          <button type="submit" class="btn btn-gold" id="confirmBtn">✨ Add to Wardrobe</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- EDIT MODAL -->
<div class="modal-overlay" id="editModal" style="display:none;">
  <div class="modal-box">
    <div class="modal-header">
      <h3>✏️ Edit Item</h3>
      <button class="modal-close" onclick="closeEditModal()">×</button>
    </div>
    <div class="modal-body">
      <form id="editForm" method="post">
        <input type="hidden" name="item_id" id="editItemId">
        <div class="form-group">
          <label class="form-label">Item Name</label>
          <input type="text" name="label" id="editLabel" class="form-input" placeholder="e.g. Favourite White Tee" maxlength="80">
        </div>
        <div class="form-group">
          <label class="form-label">Category</label>
          <select name="category" id="editCategory" class="form-select">
            <option value="shirt">👕 Shirt / T-Shirt / Top</option>
            <option value="hoodie">🧥 Hoodie / Sweatshirt</option>
            <option value="jacket">🥼 Jacket / Coat / Blazer</option>
            <option value="pants">👖 Pants / Jeans / Trousers</option>
            <option value="shoes">👟 Shoes / Sneakers / Boots</option>
            <option value="dress">👗 Dress / Skirt</option>
            <option value="accessory">👒 Accessory / Hat / Bag</option>
          </select>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-ghost" onclick="closeEditModal()">Cancel</button>
          <button type="submit" class="btn btn-gold">💾 Save Changes</button>
        </div>
      </form>
    </div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.querySelectorAll('.clothing-placeholder[data-cat]').forEach(el=>{el.textContent=catEmoji(el.dataset.cat);});

let chosenFile=null;
const CAT_KEYWORDS={shirt:['shirt','tee','top','blouse','polo'],hoodie:['hoodie','sweatshirt','sweater'],jacket:['jacket','coat','blazer'],pants:['pants','jeans','trousers','chinos','denim','cargo'],shoes:['shoes','sneakers','boots','loafers','sandals'],dress:['dress','skirt'],accessory:['hat','cap','bag','belt','scarf']};

function onFileChosen(input){
  if(!input.files||!input.files[0])return;
  chosenFile=input.files[0];
  const name=chosenFile.name.toLowerCase();
  let detected='';
  for(const[cat,kws]of Object.entries(CAT_KEYWORDS)){if(kws.some(k=>name.includes(k))){detected=cat;break;}}
  document.getElementById('modalCategory').value=detected;
  let label=chosenFile.name.replace(/\.[^.]+$/,'').replace(/^[a-f0-9]{8}_/,'').replace(/[-_]/g,' ');
  document.getElementById('modalLabel').value=label;
  const reader=new FileReader();
  reader.onload=e=>{
    const img=document.getElementById('previewImg'),ph=document.getElementById('previewPh');
    img.src=e.target.result;img.style.display='block';ph.style.display='none';
  };
  reader.readAsDataURL(chosenFile);
  document.getElementById('uploadModal').style.display='flex';
}

document.getElementById('uploadForm').addEventListener('submit',function(){
  if(chosenFile){const dt=new DataTransfer();dt.items.add(chosenFile);document.getElementById('hiddenFile').files=dt.files;}
  document.getElementById('confirmBtn').innerHTML='<div class="spinner"></div> Adding…';
});

function closeUploadModal(){
  document.getElementById('uploadModal').style.display='none';
  document.getElementById('fileInput').value='';chosenFile=null;
  document.getElementById('previewImg').style.display='none';
  document.getElementById('previewPh').style.display='flex';
}

function openEdit(id,label,category){
  document.getElementById('editItemId').value=id;
  document.getElementById('editLabel').value=label;
  document.getElementById('editCategory').value=category;
  document.getElementById('editForm').action='/edit/'+id;
  document.getElementById('editModal').style.display='flex';
}
function closeEditModal(){document.getElementById('editModal').style.display='none';}

document.getElementById('uploadModal').addEventListener('click',function(e){if(e.target===this)closeUploadModal();});
document.getElementById('editModal').addEventListener('click',function(e){if(e.target===this)closeEditModal();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeUploadModal();closeEditModal();}});
</script>
{% endblock %}
"""

OUTFIT_HTML = r"""{% extends "base.html" %}
{% block title %}Outfit Generator — AI Styler{% endblock %}
{% block content %}
<div class="page-header">
  <div class="page-header-inner">
    <h1>Outfit <em>Generator</em></h1>
    <p>Tell us your vibe and we'll curate the perfect look from your wardrobe.</p>
  </div>
</div>
<div class="container">
  <div class="two-col">
    <!-- LEFT -->
    <div style="display:flex;flex-direction:column;gap:1.5rem;">
      <div class="card anim-fade-up">
        <div class="card-header"><span>📊</span><h2>Today's Usage</h2></div>
        <div class="card-body">
          {% set op=[(usage.outfits_generated*100//outfit_limit),100]|min %}
          <div class="usage-bar-wrap">
            <div class="usage-label"><span>Outfits Generated</span><span>{{ usage.outfits_generated }}&thinsp;/&thinsp;{{ outfit_limit }}</span></div>
            <div class="usage-track"><div class="usage-fill {% if op>=100 %}full{% elif op>=67 %}warn{% else %}ok{% endif %}" style="width:{{ op }}%;transition:width 1s cubic-bezier(.22,1,.36,1)"></div></div>
          </div>
          {% if usage.outfits_generated>=outfit_limit %}<div class="alert alert-warn" style="margin-top:1rem;margin-bottom:0;">🚫 Outfit limit reached. Come back tomorrow!</div>{% endif %}
        </div>
      </div>
      <div class="card anim-fade-up delay-1">
        <div class="card-header"><span>✨</span><h2>Pick Your Style</h2></div>
        <div class="card-body">
          {% if error %}<div class="alert alert-error">{{ error }}</div>{% endif %}
          {% if usage.outfits_generated < outfit_limit %}
          <p style="font-size:.88rem;color:var(--muted);margin-bottom:1rem;">Choose a preset or type your own:</p>
          <div class="style-chips">
            {% for s in ["casual","formal","streetwear","classic","sporty","chic","smart"] %}
            <button class="chip {% if style==s %}active{% endif %}" onclick="setStyle('{{ s }}')">{{ s }}</button>
            {% endfor %}
          </div>
          <form action="/outfit" method="post" id="outfitForm">
            <input type="text" name="style" id="styleInput" class="style-input"
                   placeholder="e.g. casual, formal, streetwear…" value="{{ style }}" required maxlength="60">
            <button type="submit" class="btn btn-gold" id="genBtn" style="width:100%;justify-content:center;font-size:1rem;padding:.9rem;">
              🪄 Generate Outfit
            </button>
          </form>
          {% else %}
          <div class="alert alert-error" style="margin-bottom:0;">Daily limit reached ({{ outfit_limit }} outfits). Reset at midnight.</div>
          {% endif %}
        </div>
      </div>
      <a href="/" class="btn btn-ink anim-fade-up delay-2" style="justify-content:center;">← Back to Wardrobe</a>
    </div>
    <!-- RIGHT -->
    <div>
      {% if outfit %}
        {% if outfit.items %}
        <div class="outfit-result">
          <h3>🎨 Your {{ outfit.style|capitalize }} Look
            {% if outfit.complete %}<span style="font-size:.75rem;background:var(--sage);color:white;padding:.18rem .65rem;border-radius:99px;margin-left:.6rem;vertical-align:middle;">Complete ✓</span>{% endif %}
          </h3>
          <div class="outfit-items">
            {% for item in outfit.items %}
            <div class="outfit-item" style="animation-delay:{{ loop.index0 * 0.1 }}s;">
              {% set ext=item.filename.split('.')[-1].lower() %}
              {% if ext in ['jpg','jpeg','png','webp','gif'] %}
              <img src="/uploads/{{ item.filename }}" alt="{{ item.category }}" class="outfit-item-img"
                   onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
              <div class="outfit-item-ph" style="display:none;" data-cat="{{ item.category }}"></div>
              {% else %}
              <div class="outfit-item-ph" data-cat="{{ item.category }}"></div>
              {% endif %}
              <div class="outfit-item-info">
                <div class="cat">{{ item.category }}</div>
                <div class="fname">{{ item.label if item.label else item.filename }}</div>
                <div class="clr">🎨 {{ item.color }}</div>
              </div>
            </div>
            {% endfor %}
          </div>
          {% if outfit.missing_categories %}
          <div class="outfit-missing">ℹ️ Missing: <strong>{{ outfit.missing_categories|join(', ') }}</strong> — upload these for a complete look!</div>
          {% endif %}
        </div>
        {% else %}
        <div class="card anim-pop-in"><div class="card-body"><div class="empty"><div class="icon">🤔</div><h3>No matching items</h3><p>Your wardrobe doesn't have clothes for <strong>{{ outfit.style }}</strong> yet.<br>Upload some and try again!</p></div></div></div>
        {% endif %}
      {% else %}
      <div class="card anim-fade-up"><div class="card-body"><div class="empty">
        <div class="icon">👔</div><h3>Ready to style you</h3>
        <p>Pick a style on the left and hit <strong>Generate Outfit</strong>.</p>
        <div style="margin-top:1.5rem;display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;">
          {% for s in ["casual","formal","streetwear","classic","sporty","chic"] %}
          <span class="chip" onclick="setStyle('{{ s }}')">{{ s }}</span>
          {% endfor %}
        </div>
      </div></div></div>
      {% endif %}
    </div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
document.querySelectorAll('.outfit-item-ph[data-cat]').forEach(el=>{el.textContent=catEmoji(el.dataset.cat);});
function setStyle(s){
  const inp=document.getElementById('styleInput');
  if(inp)inp.value=s;
  document.querySelectorAll('.chip').forEach(c=>c.classList.toggle('active',c.textContent.trim()===s));
}
document.getElementById('outfitForm')?.addEventListener('submit',function(){
  const btn=document.getElementById('genBtn');
  btn.innerHTML='<div class="spinner"></div> Styling…';btn.disabled=true;
});
</script>
{% endblock %}
"""

# ══════════════════════════════════════════════════════════════
#  WRITE TEMPLATES TO DISK
# ══════════════════════════════════════════════════════════════

def setup_files():
    Path("uploads").mkdir(exist_ok=True)
    Path("templates").mkdir(exist_ok=True)
    Path("templates/base.html").write_text(BASE_HTML,    encoding="utf-8")
    Path("templates/index.html").write_text(INDEX_HTML,  encoding="utf-8")
    Path("templates/outfit.html").write_text(OUTFIT_HTML, encoding="utf-8")
    print("✅ Templates & folders ready.")

setup_files()

# ══════════════════════════════════════════════════════════════
#  DATABASE
# ══════════════════════════════════════════════════════════════

DB_PATH = "wardrobe.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS clothes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        filename    TEXT NOT NULL,
        label       TEXT DEFAULT '',
        category    TEXT NOT NULL,
        color       TEXT NOT NULL,
        uploaded_at TEXT DEFAULT (date('now'))
    )""")
    # Migrate: add label column if it doesn't exist yet
    try:
        c.execute("ALTER TABLE clothes ADD COLUMN label TEXT DEFAULT ''")
    except Exception:
        pass
    c.execute("""CREATE TABLE IF NOT EXISTS usage_limits (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id           TEXT NOT NULL DEFAULT 'default_user',
        date              TEXT NOT NULL,
        outfits_generated INTEGER DEFAULT 0,
        clothes_uploaded  INTEGER DEFAULT 0,
        UNIQUE(user_id, date)
    )""")
    conn.commit()
    conn.close()

def get_usage(user_id="default_user"):
    conn = get_connection()
    c = conn.cursor()
    today = str(date.today())
    c.execute("SELECT * FROM usage_limits WHERE user_id=? AND date=?", (user_id, today))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else {"user_id":user_id,"date":today,"outfits_generated":0,"clothes_uploaded":0}

def increment_usage(field: str, user_id="default_user"):
    conn = get_connection()
    c = conn.cursor()
    today = str(date.today())
    c.execute("""INSERT INTO usage_limits (user_id,date,outfits_generated,clothes_uploaded)
                 VALUES(?,?,0,0) ON CONFLICT(user_id,date) DO NOTHING""", (user_id, today))
    c.execute(f"UPDATE usage_limits SET {field}={field}+1 WHERE user_id=? AND date=?", (user_id, today))
    conn.commit()
    conn.close()

def add_clothing(filename, category, color, label=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO clothes (filename,label,category,color) VALUES(?,?,?,?)",
              (filename, label, category, color))
    conn.commit()
    row_id = c.lastrowid
    conn.close()
    return row_id

def update_clothing(item_id: int, label: str, category: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE clothes SET label=?, category=? WHERE id=?", (label, category, item_id))
    conn.commit()
    conn.close()

def get_all_clothes():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM clothes ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_clothing(item_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM clothes WHERE id=?", (item_id,))
    conn.commit()
    conn.close()

# ══════════════════════════════════════════════════════════════
#  CLASSIFICATION + OUTFIT LOGIC
# ══════════════════════════════════════════════════════════════

try:
    import cv2, numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️  OpenCV not found — fallback color detection active. pip install opencv-python-headless numpy")

CATEGORY_KEYWORDS = {
    "shirt":     ["shirt","tee","top","blouse","polo","tshirt","t-shirt"],
    "hoodie":    ["hoodie","sweatshirt","pullover","sweater","jumper"],
    "jacket":    ["jacket","coat","blazer","windbreaker","parka"],
    "pants":     ["pants","jeans","trousers","chinos","shorts","denim","cargo"],
    "shoes":     ["shoes","sneakers","boots","loafers","heels","sandals","trainers"],
    "dress":     ["dress","skirt","gown","frock"],
    "accessory": ["hat","cap","scarf","belt","bag","watch","glasses"],
}
CATEGORY_LIST = list(CATEGORY_KEYWORDS.keys())

def detect_category(filename: str) -> str:
    name = filename.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(k in name for k in kws):
            return cat
    return random.choice(CATEGORY_LIST)

COLOR_RANGES_HSV = {
    "red":    [((0,70,50),(10,255,255)),((170,70,50),(180,255,255))],
    "orange": [((11,70,50),(25,255,255))],
    "yellow": [((26,70,50),(34,255,255))],
    "green":  [((35,40,40),(85,255,255))],
    "blue":   [((86,40,40),(130,255,255))],
    "purple": [((131,40,40),(160,255,255))],
    "pink":   [((161,40,100),(169,255,255))],
}

def detect_color(filepath: str) -> str:
    if not CV2_AVAILABLE:
        return random.choice(["black","white","blue","grey","red","navy","beige","brown"])
    try:
        img = cv2.imread(filepath)
        if img is None:
            return random.choice(["black","white","blue","grey"])
        img  = cv2.resize(img,(100,100))
        hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mb   = float(gray.mean())
        if mb > 200: return "white"
        if mb < 40:  return "black"
        best_color, best_count = "grey", 0
        total = img.shape[0]*img.shape[1]
        for color_name, ranges in COLOR_RANGES_HSV.items():
            mask = None
            for lo,hi in ranges:
                m = cv2.inRange(hsv, np.array(lo), np.array(hi))
                mask = m if mask is None else mask | m
            cnt = int(np.sum(mask>0))
            if cnt > best_count:
                best_count, best_color = cnt, color_name
        if best_count/total < 0.08:
            return "dark grey" if mb < 90 else "grey"
        return best_color
    except Exception:
        return random.choice(["black","white","blue","grey"])

STYLE_TEMPLATES = {
    "casual":     ["shirt","pants","shoes"],
    "formal":     ["shirt","pants","shoes","jacket"],
    "streetwear": ["hoodie","pants","shoes"],
    "classic":    ["shirt","pants","shoes"],
    "sporty":     ["shirt","pants","shoes"],
    "chic":       ["dress","shoes","accessory"],
    "smart":      ["shirt","pants","shoes","jacket"],
}
CATEGORY_FALLBACKS = {
    "hoodie": ["jacket","shirt"],
    "dress":  ["shirt","pants"],
    "jacket": ["hoodie"],
}
STYLE_COLOR_PREFS = {
    "casual":     ["blue","white","grey"],
    "formal":     ["black","white","navy","dark grey"],
    "streetwear": ["black","grey","white"],
    "classic":    ["navy","white","beige","grey"],
    "sporty":     ["black","white","red","blue"],
    "chic":       ["black","white","pink"],
    "smart":      ["navy","white","grey"],
}

def generate_outfit(style: str, wardrobe_items: list) -> dict:
    style = style.lower().strip()
    template = STYLE_TEMPLATES.get(style)
    if not template:
        for key in STYLE_TEMPLATES:
            if key in style or style in key:
                template = STYLE_TEMPLATES[key]; style = key; break
    if not template:
        template = STYLE_TEMPLATES["casual"]; style = "casual"

    pref_colors = STYLE_COLOR_PREFS.get(style, [])
    by_cat: dict = {}
    for item in wardrobe_items:
        by_cat.setdefault(item["category"], []).append(item)

    outfit, missing = [], []
    for needed in template:
        candidates = by_cat.get(needed, [])
        if not candidates:
            for fb in CATEGORY_FALLBACKS.get(needed, []):
                candidates = by_cat.get(fb, [])
                if candidates: break
        if candidates:
            pref   = [c for c in candidates if c["color"] in pref_colors]
            others = [c for c in candidates if c["color"] not in pref_colors]
            random.shuffle(pref); random.shuffle(others)
            used = {i["id"] for i in outfit}
            pick = next((c for c in pref+others if c["id"] not in used), None)
            if pick: outfit.append(pick)
            else: missing.append(needed)
        else:
            missing.append(needed)

    return {"style": style, "items": outfit, "missing_categories": missing, "complete": len(missing)==0}


def dict_to_ns(obj):
    """Recursively convert dicts → SimpleNamespace so Jinja2 dot-notation works."""
    if isinstance(obj, dict):
        return SimpleNamespace(**{k: dict_to_ns(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [dict_to_ns(i) for i in obj]
    return obj


# ══════════════════════════════════════════════════════════════
#  FASTAPI APP
# ══════════════════════════════════════════════════════════════

from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from urllib.parse import quote

app = FastAPI(title="AI Styler")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
tmpl = Jinja2Templates(directory="templates")

CLOTHES_LIMIT = 35
OUTFIT_LIMIT  = 3

@app.on_event("startup")
def startup():
    init_db()
    print("\n" + "═"*52)
    print("  🎨  AI Styler is running!")
    print("  👉  Open:  http://localhost:8000")
    print("═"*52 + "\n")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, message: str = "", error: str = ""):
    return tmpl.TemplateResponse("index.html", {
        "request": request, "clothes": get_all_clothes(), "usage": get_usage(),
        "clothes_limit": CLOTHES_LIMIT, "outfit_limit": OUTFIT_LIMIT,
        "message": message, "error": error,
    })

@app.post("/upload")
async def upload_clothing(
    request:  Request,
    file:     UploadFile = File(...),
    label:    str        = Form(""),
    category: str        = Form(""),
):
    usage = get_usage()
    if usage["clothes_uploaded"] >= CLOTHES_LIMIT:
        return RedirectResponse(url="/?error=Daily+upload+limit+reached+(35+items).", status_code=303)
    ext      = Path(file.filename).suffix or ".jpg"
    uid      = uuid.uuid4().hex[:8]
    filename = f"{uid}_{file.filename}"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    cat   = category.strip() if category.strip() else detect_category(file.filename)
    color = detect_color(str(filepath))
    lbl   = label.strip()
    add_clothing(filename, cat, color, lbl)
    increment_usage("clothes_uploaded")
    display = lbl or filename
    return RedirectResponse(url=f"/?message={quote(display+' added as '+cat+' ('+color+')')}", status_code=303)

@app.post("/edit/{item_id}")
async def edit_item(item_id: int, label: str = Form(""), category: str = Form("")):
    update_clothing(item_id, label.strip(), category.strip())
    return RedirectResponse(url="/?message=Item+updated+successfully!", status_code=303)

@app.post("/delete/{item_id}")
async def delete_item(item_id: int):
    delete_clothing(item_id)
    return RedirectResponse(url="/?message=Item+deleted.", status_code=303)

@app.get("/outfit", response_class=HTMLResponse)
async def outfit_page(request: Request):
    return tmpl.TemplateResponse("outfit.html", {
        "request": request, "usage": get_usage(),
        "outfit_limit": OUTFIT_LIMIT, "outfit": None, "style": "", "error": "",
    })

@app.post("/outfit", response_class=HTMLResponse)
async def generate_outfit_route(request: Request, style: str = Form(...)):
    usage = get_usage()
    if usage["outfits_generated"] >= OUTFIT_LIMIT:
        return tmpl.TemplateResponse("outfit.html", {
            "request": request, "usage": usage, "outfit_limit": OUTFIT_LIMIT,
            "outfit": None, "style": style,
            "error": f"Daily outfit limit reached ({OUTFIT_LIMIT} outfits). Come back tomorrow!",
        })
    wardrobe = get_all_clothes()
    if not wardrobe:
        return tmpl.TemplateResponse("outfit.html", {
            "request": request, "usage": usage, "outfit_limit": OUTFIT_LIMIT,
            "outfit": None, "style": style,
            "error": "Your wardrobe is empty! Upload some clothes first.",
        })

    # ── KEY FIX: wrap result in SimpleNamespace so outfit.items / outfit.style works in Jinja ──
    result_dict = generate_outfit(style, wardrobe)
    result_ns   = dict_to_ns(result_dict)
    increment_usage("outfits_generated")

    return tmpl.TemplateResponse("outfit.html", {
        "request": request, "usage": get_usage(),
        "outfit_limit": OUTFIT_LIMIT,
        "outfit": result_ns,                   # ← namespace, not raw dict
        "style":  result_dict["style"],
        "error":  "",
    })

@app.get("/api/wardrobe")
async def api_wardrobe():
    return JSONResponse(get_all_clothes())

@app.get("/api/usage")
async def api_usage():
    return JSONResponse(get_usage())

# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        import uvicorn
    except ImportError:
        print("❌ uvicorn not installed. Run:  pip install uvicorn[standard]")
        sys.exit(1)
    print("""
╔══════════════════════════════════════════════════════════╗
║           AI Styler — Starting up                        ║
║                                                          ║
║  Install deps (first time only):                         ║
║  pip install fastapi uvicorn[standard] jinja2 \\          ║
║              python-multipart opencv-python-headless \\   ║
║              numpy aiofiles                              ║
╚══════════════════════════════════════════════════════════╝
""")
    uvicorn.run("ai_styler:app", host="0.0.0.0", port=8000, reload=False)
