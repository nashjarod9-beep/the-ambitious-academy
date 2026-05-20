document.addEventListener('DOMContentLoaded', () => {
  // --- INITIATE PROGRESS BAR ---
  const initProgressBar = () => {
    const progressBar = document.createElement('div');
    progressBar.id = 'reading-progress';
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', () => {
      const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrollPercent = scrollHeight > 0 ? (window.scrollY / scrollHeight) * 100 : 0;
      progressBar.style.width = scrollPercent + '%';
    });
  };
  initProgressBar();

  // --- INITIATE CUSTOM CURSOR (60FPS GPU-ACCELERATED LERP) ---
  const initCustomCursor = () => {
    // Only enable cursor on desktop/mouse devices
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    if (isTouchDevice || window.innerWidth < 1024) return;

    const circle = document.createElement('div');
    circle.className = 'custom-cursor-circle';
    const dot = document.createElement('div');
    dot.className = 'custom-cursor-dot';

    document.body.appendChild(circle);
    document.body.appendChild(dot);

    circle.style.display = 'block';
    dot.style.display = 'block';

    let mouseX = 0, mouseY = 0;
    let ballX = 0, ballY = 0;
    const speed = 0.09; // Elegant damping lag factor

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    // Animate custom cursor with ultra-performance translate3d (GPU thread)
    const updatePosition = () => {
      ballX += (mouseX - ballX) * speed;
      ballY += (mouseY - ballY) * speed;
      
      circle.style.transform = `translate3d(${ballX}px, ${ballY}px, 0) translate3d(-50%, -50%, 0)`;
      dot.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0) translate3d(-50%, -50%, 0)`;
      
      requestAnimationFrame(updatePosition);
    };
    updatePosition();

    // Premium dynamic hover scale effects on interactive elements via event delegation
    const interactiveSelector = 'a, button, .pain-card, .agitation-card, .testimonial-card, .audience-card, .bonus-card, .formation-card, .accordion-header, input, textarea';
    
    document.body.addEventListener('mouseover', (e) => {
      const target = e.target.closest(interactiveSelector);
      if (target) {
        circle.classList.add('custom-cursor-hover');
      }
    });

    document.body.addEventListener('mouseout', (e) => {
      const target = e.target.closest(interactiveSelector);
      if (target) {
        const related = e.relatedTarget;
        if (!related || !target.contains(related)) {
          circle.classList.remove('custom-cursor-hover');
        }
      }
    });
  };
  initCustomCursor();

  // --- INITIATE NAVBAR SCROLL LOGIC ---
  const initNavbarScroll = () => {
    const header = document.querySelector('.header');
    if (!header) return;

    window.addEventListener('scroll', () => {
      if (window.scrollY > 80) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  };
  initNavbarScroll();

  // --- INITIATE MOBILE HAMBURGER MENU ---
  const initMobileNav = () => {
    const hamburger = document.querySelector('.hamburger');
    const mobileNav = document.querySelector('.mobile-nav-overlay');
    if (!hamburger || !mobileNav) return;

    hamburger.addEventListener('click', () => {
      mobileNav.classList.toggle('active');
      hamburger.querySelectorAll('span').forEach((span, idx) => {
        if (mobileNav.classList.contains('active')) {
          if (idx === 0) span.style.transform = 'translateY(7px) rotate(45deg)';
          if (idx === 1) span.style.opacity = '0';
          if (idx === 2) span.style.transform = 'translateY(-7px) rotate(-45deg)';
        } else {
          span.style.transform = 'none';
          span.style.opacity = '1';
        }
      });
    });

    // Close mobile nav when clicking a link
    mobileNav.querySelectorAll('.mobile-nav-link').forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('active');
        hamburger.querySelectorAll('span').forEach(span => {
          span.style.transform = 'none';
          span.style.opacity = '1';
        });
      });
    });
  };
  initMobileNav();

  // --- INITIATE EVERGREEN TIMER ---
  const initEvergreenTimer = () => {
    const timerStorageKey = 'AA_timer_target';
    let targetTime = localStorage.getItem(timerStorageKey);

    const getNewTargetTime = () => Date.now() + 48 * 60 * 60 * 1000;

    if (!targetTime || parseInt(targetTime) < Date.now()) {
      targetTime = getNewTargetTime();
      localStorage.setItem(timerStorageKey, targetTime);
    } else {
      targetTime = parseInt(targetTime);
    }

    const updateTimerDisplay = () => {
      const now = Date.now();
      let timeLeft = targetTime - now;

      // Evergreen Reset
      if (timeLeft <= 0) {
        targetTime = getNewTargetTime();
        localStorage.setItem(timerStorageKey, targetTime);
        timeLeft = targetTime - now;
      }

      const hours = Math.floor(timeLeft / (1000 * 60 * 60));
      const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

      const pad = (num) => String(num).padStart(2, '0');

      // Update Hours
      document.querySelectorAll('.timer-hours').forEach(elem => {
        elem.textContent = pad(hours);
      });
      // Update Minutes
      document.querySelectorAll('.timer-minutes').forEach(elem => {
        elem.textContent = pad(minutes);
      });
      // Update Seconds
      document.querySelectorAll('.timer-seconds').forEach(elem => {
        elem.textContent = pad(seconds);
      });

      // Update generic text timers if any
      document.querySelectorAll('.timer-text-string').forEach(elem => {
        elem.textContent = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
      });
    };

    updateTimerDisplay();
    setInterval(updateTimerDisplay, 1000);
  };
  initEvergreenTimer();

  // --- INITIATE SCROLL REVEAL (CUBIC BEZIER EASING) ---
  const initScrollReveal = () => {
    const revealElements = document.querySelectorAll('.scroll-reveal');

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target); // Reveal once
        }
      });
    }, {
      threshold: 0.08,
      rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(elem => observer.observe(elem));
  };
  initScrollReveal();

  // --- INITIATE FAQ AND MODULE ACCORDIONS ---
  const initAccordions = () => {
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
      header.addEventListener('click', () => {
        const item = header.parentElement;
        const collapse = item.querySelector('.accordion-collapse');
        const isActive = item.classList.contains('active');

        // Close other items in the same container
        const siblings = item.parentElement.querySelectorAll('.accordion-item');
        siblings.forEach(sibling => {
          sibling.classList.remove('active');
          const siblingCollapse = sibling.querySelector('.accordion-collapse');
          if (siblingCollapse) siblingCollapse.style.maxHeight = null;
        });

        if (!isActive) {
          item.classList.add('active');
          collapse.style.maxHeight = collapse.scrollHeight + 'px';
        }
      });
    });
  };
  initAccordions();

  // --- INITIATE MOBILE CAROUSEL FOR TESTIMONIALS ---
  const initTestimonialCarousel = () => {
    const container = document.querySelector('.testimonials-carousel-container');
    const track = document.querySelector('.testimonials-carousel-track');
    const slides = document.querySelectorAll('.carousel-slide');
    const nav = document.querySelector('.carousel-nav');

    if (!container || !track || slides.length === 0) return;

    let currentIndex = 0;
    let startX = 0;
    let currentTranslate = 0;
    let prevTranslate = 0;
    let animationID = 0;
    let isDragging = false;

    // Create navigation bullets
    slides.forEach((_, idx) => {
      const bullet = document.createElement('button');
      bullet.className = `carousel-bullet ${idx === 0 ? 'active' : ''}`;
      bullet.setAttribute('aria-label', `Slide ${idx + 1}`);
      bullet.addEventListener('click', () => goToSlide(idx));
      nav.appendChild(bullet);
    });

    const bullets = document.querySelectorAll('.carousel-bullet');

    const updateBullets = () => {
      bullets.forEach((bullet, idx) => {
        if (idx === currentIndex) {
          bullet.classList.add('active');
        } else {
          bullet.classList.remove('active');
        }
      });
    };

    const setPositionByIndex = () => {
      currentTranslate = currentIndex * -container.offsetWidth;
      prevTranslate = currentTranslate;
      track.style.transform = `translate3d(${currentTranslate}px, 0, 0)`;
      updateBullets();
    };

    const goToSlide = (index) => {
      currentIndex = index;
      setPositionByIndex();
    };

    // Resize listener to ensure correct offsets
    window.addEventListener('resize', setPositionByIndex);

    // Touch event handlers for swipe
    track.addEventListener('touchstart', touchStart);
    track.addEventListener('touchmove', touchMove);
    track.addEventListener('touchend', touchEnd);

    function touchStart(e) {
      startX = getPositionX(e);
      isDragging = true;
      animationID = requestAnimationFrame(animation);
      track.style.transition = 'none';
    }

    function touchMove(e) {
      if (!isDragging) return;
      const currentX = getPositionX(e);
      currentTranslate = prevTranslate + currentX - startX;
    }

    function touchEnd() {
      cancelAnimationFrame(animationID);
      isDragging = false;
      const movedBy = currentTranslate - prevTranslate;

      // Threshold of 80px to switch slides
      if (movedBy < -80 && currentIndex < slides.length - 1) {
        currentIndex += 1;
      } else if (movedBy > 80 && currentIndex > 0) {
        currentIndex -= 1;
      }

      track.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
      setPositionByIndex();
    }

    function getPositionX(e) {
      return e.touches[0].clientX;
    }

    function animation() {
      track.style.transform = `translate3d(${currentTranslate}px, 0, 0)`;
      if (isDragging) requestAnimationFrame(animation);
    }
  };
  initTestimonialCarousel();

  // --- FLOATING PARTICLES IN HERO (SINE & COSINE DRIFT) ---
  const initHeroParticles = () => {
    const hero = document.querySelector('.hero');
    if (!hero) return;

    const numParticles = 8;
    const particles = [];

    for (let i = 0; i < numParticles; i++) {
      const p = document.createElement('div');
      p.className = 'hero-particle';
      
      // Random positioning
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      p.style.left = `${x}%`;
      p.style.top = `${y}%`;
      
      // Random scaling
      const scale = Math.random() * 1.5 + 0.5;
      p.style.transform = `scale(${scale})`;
      
      hero.appendChild(p);

      particles.push({
        el: p,
        x: x,
        y: y,
        offsetX: Math.random() * 100,
        offsetY: Math.random() * 100,
        speedX: (Math.random() - 0.5) * 0.03,
        speedY: (Math.random() - 0.5) * 0.03
      });
    }

    const animateParticles = () => {
      const time = Date.now() * 0.0008;
      particles.forEach(p => {
        // Luxury fluid drift using trigonometric formulas
        p.x += Math.sin(time + p.offsetX) * 0.02 + p.speedX;
        p.y += Math.cos(time + p.offsetY) * 0.02 + p.speedY;

        // Wrap around boundaries elegantly instead of rigid bouncing
        if (p.x < -5) p.x = 105;
        if (p.x > 105) p.x = -5;
        if (p.y < -5) p.y = 105;
        if (p.y > 105) p.y = -5;

        p.el.style.left = `${p.x}%`;
        p.el.style.top = `${p.y}%`;
      });
      requestAnimationFrame(animateParticles);
    };
    animateParticles();
  };
  initHeroParticles();
});
