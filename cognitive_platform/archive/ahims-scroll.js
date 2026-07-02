/**
 * AHIMS™ Scroll Engine
 * IntersectionObserver-driven reveals, chapter tracking, count-up numerals,
 * animated score rings, staggered entrances, dot-rail sync.
 */
(function () {
  'use strict';

  // ---------------------------------------------------------------------------
  // Chapter tracking
  // ---------------------------------------------------------------------------

  const CHAPTERS = document.querySelectorAll('.chapter');
  const NAV = document.querySelector('.nav');
  const NAV_CHAPTER_LABEL = document.querySelector('.nav__chapter');
  const NAV_PROGRESS = document.querySelector('.nav__progress');
  const DOT_RAIL = document.querySelector('.dot-rail');
  const DOT_RAIL_DOTS = DOT_RAIL ? DOT_RAIL.querySelectorAll('.dot-rail__dot') : [];
  const CHAPTER_NAMES = [
    'Cover', 'Who Am I?', 'How Did I Perform?',
    'How Did I Perform?', 'How Did I Perform?',
    'Why Did I Perform This Way?', 'Why Did I Perform This Way?',
    'What Does It Mean?', 'What Does It Mean?',
    'What Does It Mean?', 'What Does It Mean?',
    'What Should I Do Next?', 'What Should I Do Next?',
    'How Should I Interpret This?'
  ];

  let currentChapterIndex = 0;
  let hasScrolled = false;

  function updateNav() {
    if (!hasScrolled) return;
    NAV.classList.toggle('nav--scrolled', window.scrollY > 100);
    if (DOT_RAIL) DOT_RAIL.classList.toggle('dot-rail--visible', window.scrollY > window.innerHeight * 0.5);
  }

  function trackChapters() {
    CHAPTERS.forEach(function (ch, i) {
      const rect = ch.getBoundingClientRect();
      if (rect.top <= window.innerHeight * 0.4 && rect.bottom > window.innerHeight * 0.4) {
        if (i !== currentChapterIndex) {
          currentChapterIndex = i;
          if (NAV_CHAPTER_LABEL) {
            NAV_CHAPTER_LABEL.textContent = CHAPTER_NAMES[i] || '';
          }
          DOT_RAIL_DOTS.forEach(function (d, di) {
            d.classList.toggle('is-active', di === i);
          });
        }
      }
    });
  }

  function updateProgress() {
    if (!NAV_PROGRESS) return;
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    NAV_PROGRESS.style.width = progress + '%';
  }

  // ---------------------------------------------------------------------------
  // Scroll reveal (IntersectionObserver)
  // ---------------------------------------------------------------------------

  function initReveals() {
    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('.reveal').forEach(function (el) {
        el.classList.add('is-visible');
      });
      return;
    }

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

    document.querySelectorAll('.reveal').forEach(function (el) {
      observer.observe(el);
    });
  }

  // ---------------------------------------------------------------------------
  // Count-up numerals
  // ---------------------------------------------------------------------------

  function animateCountUp(el) {
    const target = parseFloat(el.getAttribute('data-count'));
    const suffix = el.getAttribute('data-suffix') || '';
    const decimals = el.getAttribute('data-decimals') || 0;
    const duration = 1500;
    const start = performance.now();

    function step(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = eased * target;
      el.textContent = current.toFixed(decimals) + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
  }

  function initCountUps() {
    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('[data-count]').forEach(function (el) {
        el.textContent = el.getAttribute('data-count') + (el.getAttribute('data-suffix') || '');
      });
      return;
    }

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCountUp(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    document.querySelectorAll('[data-count]').forEach(function (el) {
      observer.observe(el);
    });
  }

  // ---------------------------------------------------------------------------
  // Score ring animation
  // ---------------------------------------------------------------------------

  function initScoreRings() {
    document.querySelectorAll('.score-ring').forEach(function (ring) {
      const fill = ring.querySelector('.score-ring__fill');
      if (!fill) return;
      const circumference = parseFloat(fill.style.getPropertyValue('--circumference'));
      const offset = parseFloat(fill.style.getPropertyValue('--offset'));
      if (!isNaN(circumference) && !isNaN(offset)) {
        fill.style.strokeDasharray = circumference;
        fill.style.strokeDashoffset = circumference;
      }
    });

    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('.score-ring').forEach(function (ring) {
        ring.closest('.reveal, .chapter, section')?.classList.add('is-visible');
      });
      return;
    }

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    document.querySelectorAll('.score-ring').forEach(function (ring) {
      const parent = ring.closest('.reveal') || ring;
      observer.observe(parent);
    });
  }

  // ---------------------------------------------------------------------------
  // Brain connector line draw-in
  // ---------------------------------------------------------------------------

  function initBrainLines() {
    if (!('IntersectionObserver' in window)) return;

    const brainSection = document.querySelector('.brain-section');
    if (!brainSection) return;

    const lines = brainSection.querySelectorAll('.brain-line');
    lines.forEach(function (line) {
      const length = line.getTotalLength ? line.getTotalLength() : 200;
      line.style.strokeDasharray = length;
      line.style.strokeDashoffset = length;
      line.style.transition = 'stroke-dashoffset 1s cubic-bezier(0.16, 1, 0.3, 1)';
    });

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          lines.forEach(function (line, i) {
            setTimeout(function () {
              line.style.strokeDashoffset = '0';
            }, i * 80);
          });
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    observer.observe(brainSection);
  }

  // ---------------------------------------------------------------------------
  // Radar / fingerprint polygon draw-in
  // ---------------------------------------------------------------------------

  function initFingerprint() {
    if (!('IntersectionObserver' in window)) return;

    const fp = document.querySelector('.fingerprint-svg');
    if (!fp) return;

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          fp.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    observer.observe(fp);
  }

  // ---------------------------------------------------------------------------
  // Lollipop chart animation
  // ---------------------------------------------------------------------------

  function initLollipops() {
    if (!('IntersectionObserver' in window)) return;

    const charts = document.querySelectorAll('.lollipop');
    charts.forEach(function (chart) {
      const fills = chart.querySelectorAll('.lollipop__fill');
      const dots = chart.querySelectorAll('.lollipop__dot');

      fills.forEach(function (f) { f.style.width = '0'; });
      dots.forEach(function (d) { d.style.left = '0'; });

      const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            fills.forEach(function (f, i) {
              setTimeout(function () {
                f.style.width = f.getAttribute('data-width');
              }, i * 100);
            });
            dots.forEach(function (d, i) {
              setTimeout(function () {
                d.style.left = d.getAttribute('data-left');
              }, i * 100);
            });
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.2 });

      observer.observe(chart);
    });
  }

  // ---------------------------------------------------------------------------
  // Dot rail navigation
  // ---------------------------------------------------------------------------

  function initDotRail() {
    DOT_RAIL_DOTS.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        const target = CHAPTERS[i];
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }

  // ---------------------------------------------------------------------------
  // Domain card expand/collapse
  // ---------------------------------------------------------------------------

  function initDomainCards() {
    document.querySelectorAll('.domain-card').forEach(function (card) {
      card.addEventListener('click', function () {
        const wasExpanded = card.classList.contains('is-expanded');
        document.querySelectorAll('.domain-card.is-expanded').forEach(function (c) {
          c.classList.remove('is-expanded');
        });
        if (!wasExpanded) card.classList.add('is-expanded');
      });
    });
  }

  // ---------------------------------------------------------------------------
  // Tooltip system
  // ---------------------------------------------------------------------------

  let tooltipEl = null;

  function showTooltip(html, x, y) {
    if (!tooltipEl) {
      tooltipEl = document.createElement('div');
      tooltipEl.className = 'tooltip';
      document.body.appendChild(tooltipEl);
    }
    tooltipEl.innerHTML = html;
    tooltipEl.classList.add('is-visible');
    tooltipEl.style.left = Math.min(x + 14, window.innerWidth - 260) + 'px';
    tooltipEl.style.top = (y - 10) + 'px';
  }

  function hideTooltip() {
    if (tooltipEl) tooltipEl.classList.remove('is-visible');
  }

  document.addEventListener('mousemove', function (e) {
    const target = e.target.closest('[data-tooltip]');
    if (target) {
      showTooltip(target.getAttribute('data-tooltip'), e.clientX, e.clientY);
    } else {
      hideTooltip();
    }
  });

  // ---------------------------------------------------------------------------
  // Persona word-by-word reveal
  // ---------------------------------------------------------------------------

  function initPersonaReveal() {
    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('.persona__word').forEach(function (w) {
        w.classList.add('is-visible');
      });
      return;
    }

    const personaChapter = document.querySelector('.persona-chapter');
    if (!personaChapter) return;

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const words = entry.target.querySelectorAll('.persona__word');
          words.forEach(function (w, i) {
            setTimeout(function () {
              w.classList.add('is-visible');
            }, i * 120);
          });
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    observer.observe(personaChapter);
  }

  // ---------------------------------------------------------------------------
  // Scroll listener (throttled)
  // ---------------------------------------------------------------------------

  let ticking = false;

  function onScroll() {
    hasScrolled = true;
    if (!ticking) {
      requestAnimationFrame(function () {
        updateNav();
        trackChapters();
        updateProgress();
        ticking = false;
      });
      ticking = true;
    }
  }

  // ---------------------------------------------------------------------------
  // Boot
  // ---------------------------------------------------------------------------

  function init() {
    initReveals();
    initCountUps();
    initScoreRings();
    initBrainLines();
    initFingerprint();
    initLollipops();
    initDotRail();
    initDomainCards();
    initPersonaReveal();
    updateNav();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
