/**
 * NeuroSpectrum — Page Navigation System
 * Smooth page transitions with sidebar active state management.
 */
(function () {
  'use strict';

  const PAGES = [
    'cover', 'overview', 'executive', 'performance', 'brain',
    'matrix', 'patterns', 'persona', 'interpersonal',
    'development', 'labs', 'methodology', 'backcover'
  ];

  let currentPage = 0;

  function init() {
    const links = document.querySelectorAll('.nav-sidebar__link');
    const pages = document.querySelectorAll('.page');

    links.forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const targetPage = link.getAttribute('data-page');
        navigateTo(targetPage);
      });
    });

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        if (currentPage < PAGES.length - 1) {
          navigateTo(PAGES[currentPage + 1]);
        }
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (currentPage > 0) {
          navigateTo(PAGES[currentPage - 1]);
        }
      }
    });

    // Initialize score rings
    initScoreRings();
  }

  function navigateTo(pageName) {
    const targetIndex = PAGES.indexOf(pageName);
    if (targetIndex === -1) return;

    // Hide current page
    const currentPageEl = document.querySelector('.page.is-active');
    if (currentPageEl) {
      currentPageEl.classList.remove('is-active');
      currentPageEl.style.opacity = '0';
      currentPageEl.style.transform = 'translateY(10px)';
    }

    // Update nav
    document.querySelectorAll('.nav-sidebar__link').forEach(function (link) {
      link.classList.remove('is-active');
    });
    const activeLink = document.querySelector('[data-page="' + pageName + '"]');
    if (activeLink) activeLink.classList.add('is-active');

    // Show new page with transition
    setTimeout(function () {
      const newPage = document.getElementById('page-' + pageName);
      if (newPage) {
        newPage.classList.add('is-active');
        newPage.style.opacity = '0';
        newPage.style.transform = 'translateY(10px)';
        newPage.style.transition = 'opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1), transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)';

        requestAnimationFrame(function () {
          newPage.style.opacity = '1';
          newPage.style.transform = 'translateY(0)';
        });

        // Scroll to top
        newPage.scrollTop = 0;
      }
    }, currentPageEl ? 150 : 0);

    currentPage = targetIndex;
  }

  // ---------------------------------------------------------------------------
  // Score Ring SVG Generation
  // ---------------------------------------------------------------------------

  function createScoreRing(container, score, tier, size) {
    size = size || 160;
    var radius = (size / 2) - 10;
    var circumference = 2 * Math.PI * radius;
    var offset = circumference - (score / 100) * circumference;

    var tierColors = {
      distinguished: '#2D3436',
      high: '#00B894',
      moderate: '#FDCB6E',
      developing: '#B2BEC3'
    };
    var color = tierColors[tier] || '#1A365D';

    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', size);
    svg.setAttribute('height', size);
    svg.setAttribute('viewBox', '0 0 ' + size + ' ' + size);
    svg.classList.add('score-ring__svg');

    // Track
    var track = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    track.setAttribute('cx', size / 2);
    track.setAttribute('cy', size / 2);
    track.setAttribute('r', radius);
    track.classList.add('score-ring__track');
    svg.appendChild(track);

    // Fill
    var fill = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    fill.setAttribute('cx', size / 2);
    fill.setAttribute('cy', size / 2);
    fill.setAttribute('r', radius);
    fill.classList.add('score-ring__fill');
    fill.setAttribute('stroke', color);
    fill.setAttribute('stroke-dasharray', circumference);
    fill.setAttribute('stroke-dashoffset', circumference);
    svg.appendChild(fill);

    // Score text
    var text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', size / 2);
    text.setAttribute('y', size / 2 - 4);
    text.classList.add('score-ring__text');
    text.setAttribute('font-size', size > 120 ? '36' : '24');
    text.textContent = Math.round(score) + '%';
    svg.appendChild(text);

    // Tier label
    var label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', size / 2);
    label.setAttribute('y', size / 2 + (size > 120 ? 24 : 16));
    label.classList.add('score-ring__label');
    label.setAttribute('font-size', size > 120 ? '11' : '9');
    label.textContent = tier.toUpperCase();
    svg.appendChild(label);

    container.appendChild(svg);

    // Animate
    requestAnimationFrame(function () {
      setTimeout(function () {
        fill.style.transition = 'stroke-dashoffset 1.5s cubic-bezier(0.16, 1, 0.3, 1)';
        fill.setAttribute('stroke-dashoffset', offset);
      }, 200);
    });
  }

  function initScoreRings() {
    var data = window.__REPORT_DATA__;
    if (!data) return;

    var coverRing = document.getElementById('cover-score-ring');
    if (coverRing) createScoreRing(coverRing, data.overallScore, data.overallTier, 180);

    var overviewRing = document.getElementById('overview-score-ring');
    if (overviewRing) createScoreRing(overviewRing, data.overallScore, data.overallTier, 140);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
