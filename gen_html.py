import os
import urllib.parse
from collections import defaultdict

# Read all videos from videos.txt — format: CATEGORY/filename.mp4
videos_data = []
if os.path.exists('videos.txt'):
    with open('videos.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '/' in line and line:
                parts = line.split('/', 1)
                cat = parts[0].strip()
                filename = parts[1].strip()
                title = filename.rsplit('.', 1)[0]
                # URL encode the entire path for safe serving
                encoded_file = urllib.parse.quote(line)
                videos_data.append({'cat': cat, 'file': line, 'encoded_file': encoded_file, 'title': title})

# Group by category
categories = defaultdict(list)
category_names = []
for v in videos_data:
    categories[v['cat']].append(v)
    if v['cat'] not in category_names:
        category_names.append(v['cat'])

html_template = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOGCLIPS — Le Reel Maker qu'il te faut</title>
    <meta name="description" content="Sogclips — Des images qui captivent. Des Reels qui marquent.">
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,300;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"/>
</head>
<body>

    <!-- Minimal Navigation (Alex Jackson style) -->
    <nav class="site-nav" id="site-nav">
        <a href="#home" class="nav-brand">SOGCLIPS</a>
        <div class="nav-links">
            <a href="#work">PORTFOLIO</a>
            <a href="#about">À PROPOS</a>
            <a href="#contact">CONTACT</a>
        </div>
    </nav>

    <!-- Hero: Swipeable Full-screen video background -->
    <header class="hero" id="home">
        <div class="hero-video-bg">
            <div class="swiper hero-swiper">
                <div class="swiper-wrapper">
                    <div class="swiper-slide">
                        <video autoplay muted loop playsinline>
                            <source src="BOUTIQUES/v24044gl0000cugjla7og65sqjhh2ft0.MP4" type="video/mp4">
                        </video>
                    </div>
                    <div class="swiper-slide">
                        <video autoplay muted loop playsinline>
                            <source src="CORPORATE/RECRUTEMENT%20ANTILIA.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="swiper-slide">
                        <video autoplay muted loop playsinline>
                            <source src="IMMOBILIER/REEL%20TRIPLEX%20BASSAM.mp4" type="video/mp4">
                        </video>
                    </div>
                </div>
            </div>
            <div class="hero-overlay"></div>
        </div>
        <div class="hero-content">
            <h1 class="hero-title">
                <span class="line-1">LE REEL MAKER</span>
                <span class="line-2">QU'IL TE FAUT</span>
            </h1>
            <a href="#work" class="hero-cta">DÉCOUVRIR LE PORTFOLIO</a>
        </div>
        <div class="hero-swipe-hint">
            <span>SWIPE</span>
            <i class="fa-solid fa-arrow-right-long"></i>
        </div>
        <div class="hero-scroll">
            <div class="scroll-line"></div>
        </div>
    </header>

    <!-- Gear Showcase -->
    <section class="gear-showcase" id="work">
        <div class="gear-content">
            <div class="gear-text">
                <span class="featured-label" style="padding:0; margin-bottom:1rem; display:block;">NOTRE EXIGENCE</span>
                <h2 class="gear-title">DES ÉQUIPEMENTS DE POINTE POUR UNE QUALITÉ CINÉMATOGRAPHIQUE.</h2>
                <p class="gear-desc">Pour des visuels qui marquent les esprits, j'utilise un arsenal de production vidéo haut de gamme. Caméras cinéma, optiques lumineuses de précision, drones DJI et stabilisation de pointe : chaque projet bénéficie des meilleurs standards de l'industrie pour un rendu exceptionnel.</p>
            </div>
            <div class="gear-image-stack">
                <div class="gear-image">
                    <img src="mes photos/IMG_5644.PNG" alt="Appareils SOGCLIPS">
                </div>
                <div class="gear-image">
                    <img src="gear.png" alt="Matériel Vidéo Professionnel SOGCLIPS">
                </div>
            </div>
        </div>
    </section>

    <!-- Portfolio Section -->
    <div class="portfolio-section-header">
        <h2 class="portfolio-title"><span class="accent">DÉCOUVREZ</span><br>NOTRE UNIVERS</h2>
    </div>

    <!-- Portfolio Filters -->
    <div class="portfolio-filter">
"""
for idx, cat in enumerate(category_names):
    # Set IMMOBILIER as active by default, or the first category if not found
    is_active = "active" if cat == "IMMOBILIER" else ""
    html_template += f'        <button class="filter-btn {is_active}" data-filter="{cat}">{cat.upper()}</button>\n'

html_template += """    </div>

    <!-- Portfolio Vertical Grid -->
    <section class="portfolio-grid">
"""

for cat, vids in categories.items():
    for v in vids:
        filepath_encoded = v['encoded_file']
        title = v['title']
        html_template += f"""        <article class="project-card" data-category="{cat}">
            <div class="card-video-wrapper">
                <video
                    preload="metadata"
                    muted
                    loop
                    playsinline
                    src="{filepath_encoded}#t=0.1">
                </video>
                <div class="card-overlay">
                    <span class="card-tag">{cat.upper()}</span>
                    <button class="card-play-btn" aria-label="Lire la vidéo">
                        <i class="fa-solid fa-play"></i>
                    </button>
                    <div class="card-info-inner">
                        <h3 class="card-inner-title">{cat}</h3> <!-- Using category name for now as a clean handle -->
                    </div>
                </div>
            </div>
        </article>
"""

html_template += """    </section>

    <!-- About (Qui sommes nous style) -->
    <section class="about" id="about">
        <div class="about-portrait">
            <img src="mes photos/IMG_5647.PNG" alt="Sogclips — Reel Maker">
        </div>
        <div class="about-content">
            <div class="about-label">QUI SUIS-JE ?</div>
            <h2 class="about-title">SOGCLIPS</h2>
            <p class="about-text">
                Je suis un créateur de contenu passionné par l'image et le storytelling visuel. Avec une expertise dans la création de Reels, TikToks et Shorts, je transforme vos idées en vidéos percutantes qui captivent et engagent.
            </p>
            <p class="about-text">
                Mon approche combine un œil artistique aiguisé et une maîtrise technique pour produire du contenu qui non seulement séduit, mais performe sur tous les algorithmes.
            </p>
            <a href="#contact" class="about-cta">TRAVAILLER ENSEMBLE</a>
        </div>
    </section>

    <!-- Footer Contact (Alex Jackson style) -->
    <footer class="footer" id="contact">
        <div class="footer-inner">
            <h2 class="footer-cta-text">UNE IDÉE ?<br><em>IMAGINONS ENSEMBLE.</em></h2>
            <div class="footer-contact-links">
                <a href="https://wa.me/2250749013665" class="footer-link">
                    <i class="fa-brands fa-whatsapp"></i>
                    WhatsApp
                </a>
                <a href="mailto:contact@sogclips.com" class="footer-link">
                    <i class="fa-solid fa-envelope"></i>
                    contact@sogclips.com
                </a>
            </div>
        </div>
        <div class="footer-bottom">
            <span>© 2026 SOGCLIPS</span>
            <span>LE REEL MAKER QU'IL TE FAUT</span>
        </div>
    </footer>

    <!-- Video Lightbox -->
    <div class="lightbox" id="lightbox">
        <div class="lightbox-overlay"></div>
        <div class="lightbox-content">
            <button class="lightbox-close" id="lightbox-close"><i class="fa-solid fa-xmark"></i></button>
            <video id="lightbox-video" controls playsinline></video>
        </div>
    </div>

    <!-- WhatsApp Floating Popup -->
    <a href="https://wa.me/2250749013665" class="whatsapp-float" target="_blank" aria-label="WhatsApp">
        <i class="fa-brands fa-whatsapp"></i>
        <span class="whatsapp-tooltip">Discuter sur WhatsApp</span>
    </a>

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script src="script.js"></script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Portfolio Alex Jackson style généré avec succès !")
