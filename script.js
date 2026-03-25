document.addEventListener('DOMContentLoaded', () => {
    // ---- 0. Hero Background Swiper ----
    if (typeof Swiper !== 'undefined') {
        new Swiper('.hero-swiper', {
            direction: 'horizontal',
            loop: true,
            grabCursor: true,
            effect: 'slide',
            speed: 800,
            on: {
                slideChangeTransitionStart: function () {
                    // Ensures only the active slide's video plays
                    document.querySelectorAll('.hero-swiper video').forEach(v => {
                        v.pause();
                        v.currentTime = 0;
                    });
                    const activeVideo = this.slides[this.activeIndex].querySelector('video');
                    if (activeVideo) {
                        activeVideo.play().catch(() => {});
                    }
                }
            }
        });
    }

    // ---- 1. Portfolio card click → Lightbox ----
    const lightbox = document.getElementById('lightbox');
    const lightboxVideo = document.getElementById('lightbox-video');
    const lightboxClose = document.getElementById('lightbox-close');
    const lightboxOverlay = lightbox?.querySelector('.lightbox-overlay');

    document.querySelectorAll('.project-card').forEach(card => {
        const video = card.querySelector('video');
        const playBtn = card.querySelector('.card-play-btn');

        // Hover: play preview muted
        card.addEventListener('mouseenter', () => {
            if (video) { video.play().catch(() => {}); }
        });

        card.addEventListener('mouseleave', () => {
            if (video) { video.pause(); video.currentTime = 0; }
        });

        // Click: open lightbox
        const openLightbox = () => {
            if (!video || !lightbox) return;
            const src = video.getAttribute('src') || video.querySelector('source')?.src;
            if (!src) return;

            // Strip the #t=0.1 trick
            lightboxVideo.src = src.replace('#t=0.1', '');
            lightbox.classList.add('open');
            document.body.style.overflow = 'hidden';
            lightboxVideo.play().catch(() => {});
        };

        card.addEventListener('click', openLightbox);
    });

    // Close lightbox
    const closeLightbox = () => {
        if (!lightbox) return;
        lightbox.classList.remove('open');
        lightboxVideo.pause();
        lightboxVideo.src = '';
        document.body.style.overflow = '';
    };

    lightboxClose?.addEventListener('click', closeLightbox);
    lightboxOverlay?.addEventListener('click', closeLightbox);
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeLightbox();
    });

    // ---- 1.5. Portfolio Filters ----
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    // Initial filter on load based on default active button
    const activeBtn = document.querySelector('.filter-btn.active');
    if (activeBtn) {
        activeBtn.click();
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter');

            projectCards.forEach(card => {
                const category = card.getAttribute('data-category');
                
                if (filter === 'all' || category === filter) {
                    card.style.display = 'flex';
                    // Trigger a small animation
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0) scale(1)';
                    }, 50);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px) scale(0.95)';
                    setTimeout(() => {
                        card.style.display = 'none'; // Hide physically after fade out
                    }, 300);
                }
            });
        });
    });

    // ---- 2. Nav transparency on scroll ----
    const nav = document.getElementById('site-nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 80) {
            nav.style.mixBlendMode = 'normal';
            nav.style.background = 'rgba(10,10,10,0.85)';
            nav.style.backdropFilter = 'blur(16px)';
        } else {
            nav.style.mixBlendMode = 'difference';
            nav.style.background = 'transparent';
            nav.style.backdropFilter = 'none';
        }
    });

    // ---- 3. Smooth Scroll ----
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                window.scrollTo({ top: target.offsetTop, behavior: 'smooth' });
            }
        });
    });

    // ---- 4. Fade-in on scroll & Lazy Video Load ----
    const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Lazy load video metadata when in view
                const video = entry.target.querySelector('video');
                if (video && video.getAttribute('preload') === 'none') {
                    video.setAttribute('preload', 'metadata');
                }
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px 200px 0px' });

    document.querySelectorAll('.service-item, .project-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(24px)';
        el.style.transition = 'opacity 0.7s ease, transform 0.7s ease';
        io.observe(el);
    });

    // Add visible class effect via CSS
    document.head.insertAdjacentHTML('beforeend', `
        <style>
            .visible { opacity: 1 !important; transform: translateY(0) !important; }
        </style>
    `);

    // Stagger service items
    document.querySelectorAll('.service-item').forEach((el, i) => {
        el.style.transitionDelay = `${i * 0.08}s`;
    });
});
