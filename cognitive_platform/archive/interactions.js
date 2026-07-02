/**
 * COGNITIVE PLATFORM — INTERACTIVE BEHAVIORS
 * Scroll-driven progressive disclosure, expandable domain systems,
 * hover micro-interpretations. Minimal JS footprint.
 */

(function () {
  'use strict';

  // ---------------------------------------------------------------------------
  // Domain Bar Expand/Collapse
  // Click a domain bar to reveal its interpretation
  // ---------------------------------------------------------------------------

  function initDomainBars() {
    const bars = document.querySelectorAll('.domain-item[role="button"]');

    bars.forEach(function (bar) {
      bar.addEventListener('click', function () {
        const isExpanded = bar.getAttribute('aria-expanded') === 'true';
        const content = bar.querySelector('.domain-item__expand-content');

        if (isExpanded) {
          bar.setAttribute('aria-expanded', 'false');
          content.classList.remove('is-open');
          content.setAttribute('aria-hidden', 'true');
        } else {
          // Close all others first
          bars.forEach(function (otherBar) {
            otherBar.setAttribute('aria-expanded', 'false');
            const otherContent = otherBar.querySelector('.domain-item__expand-content');
            if (otherContent) {
              otherContent.classList.remove('is-open');
              otherContent.setAttribute('aria-hidden', 'true');
            }
          });

          bar.setAttribute('aria-expanded', 'true');
          content.classList.add('is-open');
          content.setAttribute('aria-hidden', 'false');
        }
      });

      bar.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          bar.click();
        }
      });
    });
  }

  // ---------------------------------------------------------------------------
  // Domain Insight Explorer (Section 3)
  // Click-to-expand per domain
  // ---------------------------------------------------------------------------

  function initExplorer() {
    const triggers = document.querySelectorAll('.domain-explorer__trigger');

    triggers.forEach(function (trigger) {
      trigger.addEventListener('click', function () {
        const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
        const domain = trigger.getAttribute('data-explorer');
        const content = document.getElementById('explorer-' + domain);
        const chevron = trigger.querySelector('.domain-explorer__trigger-chevron');

        if (isExpanded) {
          trigger.setAttribute('aria-expanded', 'false');
          content.classList.remove('is-open');
          if (chevron) chevron.style.transform = 'rotate(0deg)';
        } else {
          // Close all others
          triggers.forEach(function (otherTrigger) {
            const otherDomain = otherTrigger.getAttribute('data-explorer');
            const otherContent = document.getElementById('explorer-' + otherDomain);
            const otherChevron = otherTrigger.querySelector('.domain-explorer__trigger-chevron');
            otherTrigger.setAttribute('aria-expanded', 'false');
            if (otherContent) otherContent.classList.remove('is-open');
            if (otherChevron) otherChevron.style.transform = 'rotate(0deg)';
          });

          trigger.setAttribute('aria-expanded', 'true');
          content.classList.add('is-open');
          if (chevron) chevron.style.transform = 'rotate(180deg)';
        }
      });
    });
  }

  // ---------------------------------------------------------------------------
  // Scroll-driven section reveal
  // Sections fade in as they enter the viewport
  // ---------------------------------------------------------------------------

  function initScrollReveal() {
    if (!('IntersectionObserver' in window)) return;

    const sections = document.querySelectorAll('.layout__section, .hero, .overview-card, .executive-insight, .brain-section, .fingerprint-section, .persona-card, .recommendations, .methodology');

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }
        });
      },
      { threshold: 0.05, rootMargin: '0px 0px -40px 0px' }
    );

    sections.forEach(function (section) {
      section.style.opacity = '0';
      section.style.transform = 'translateY(20px)';
      section.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
      observer.observe(section);
    });

    // Hero is always visible
    const hero = document.querySelector('.hero');
    if (hero) {
      hero.style.opacity = '1';
      hero.style.transform = 'none';
    }
  }

  // ---------------------------------------------------------------------------
  // Brain region hover highlighting
  // When hovering a domain, highlight corresponding brain region
  // ---------------------------------------------------------------------------

  function initBrainHighlighting() {
    const brainRegions = document.querySelectorAll('.brain-region');
    const domainItems = document.querySelectorAll('.domain-item');

    domainItems.forEach(function (item) {
      const domain = item.getAttribute('data-domain');

      item.addEventListener('mouseenter', function () {
        brainRegions.forEach(function (region) {
          if (region.getAttribute('data-domain') === domain) {
            region.setAttribute('opacity', '0.4');
            region.style.transition = 'opacity 0.3s ease';
          } else {
            region.setAttribute('opacity', '0.1');
            region.style.transition = 'opacity 0.3s ease';
          }
        });
      });

      item.addEventListener('mouseleave', function () {
        brainRegions.forEach(function (region) {
          region.setAttribute('opacity', '0.15');
          region.style.transition = 'opacity 0.3s ease';
        });
      });
    });
  }

  // ---------------------------------------------------------------------------
  // Smooth scroll for anchor links
  // ---------------------------------------------------------------------------

  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  // ---------------------------------------------------------------------------
  // Boot all interactive behaviors
  // ---------------------------------------------------------------------------

  function init() {
    initDomainBars();
    initExplorer();
    initScrollReveal();
    initBrainHighlighting();
    initSmoothScroll();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
