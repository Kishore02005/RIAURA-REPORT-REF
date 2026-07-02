/* ============================================================
   AHIMS VIZ — SVG Chart Builders v5.0
   Pure SVG, no dependencies.
   ============================================================ */
(function() {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';

  function el(tag, attrs) {
    var e = document.createElementNS(NS, tag);
    if (attrs) Object.keys(attrs).forEach(function(k) { e.setAttribute(k, attrs[k]); });
    return e;
  }

  /* ---- SCORE RING ---- */
  function buildRing(container, score, color, size) {
    size = size || 160;
    var stroke = size * 0.08;
    var r = (size - stroke) / 2;
    var circ = 2 * Math.PI * r;
    var offset = circ * (1 - score / 100);

    var svg = el('svg', { viewBox: '0 0 ' + size + ' ' + size, width: size, height: size });

    var track = el('circle', {
      cx: size/2, cy: size/2, r: r,
      fill: 'none', stroke: 'var(--border)', 'stroke-width': stroke
    });
    svg.appendChild(track);

    var fill = el('circle', {
      cx: size/2, cy: size/2, r: r,
      fill: 'none', stroke: color, 'stroke-width': stroke,
      'stroke-linecap': 'round',
      'stroke-dasharray': circ,
      'stroke-dashoffset': circ,
      transform: 'rotate(-90 ' + size/2 + ' ' + size/2 + ')',
      class: 'ring__fill'
    });
    fill.style.strokeDashoffset = circ;
    fill.style.setProperty('--ring-offset', offset);
    svg.appendChild(fill);

    container.appendChild(svg);
  }

  /* ---- CONSTELLATION STRIP ---- */
  function buildStrip(container, domains) {
    var strip = document.createElement('div');
    strip.className = 'strip';
    domains.forEach(function(d, i) {
      var node = document.createElement('a');
      node.href = '#dc-' + d.key;
      node.className = 'strip__node';
      node.setAttribute('aria-label', d.name + ': ' + d.score + '%');
      node.innerHTML =
        '<span class="strip__score">' + Math.round(d.score) + '</span>' +
        '<span class="strip__dot" style="background:' + d.color + '"></span>' +
        '<span class="strip__name">' + d.name + '</span>';
      strip.appendChild(node);
      if (i < domains.length - 1) {
        var line = document.createElement('span');
        line.className = 'strip__line';
        strip.appendChild(line);
      }
    });
    container.appendChild(strip);
  }

  /* ---- RADAR ---- */
  function buildRadar(container, domains, size) {
    size = size || 400;
    var cx = size / 2, cy = size / 2;
    var maxR = size * 0.30;
    var n = domains.length;
    var gradId = 'radar-grad-' + Date.now();

    var svg = el('svg', { viewBox: '0 0 ' + size + ' ' + size, width: size, height: size });

    /* defs — gradient fill for polygon */
    var defs = el('defs', {});
    var rg = el('radialGradient', { id: gradId, cx: '50%', cy: '50%', r: '50%' });
    rg.appendChild(el('stop', { offset: '0%', 'stop-color': 'var(--gold)', 'stop-opacity': '0.3' }));
    rg.appendChild(el('stop', { offset: '100%', 'stop-color': 'var(--gold)', 'stop-opacity': '0.05' }));
    defs.appendChild(rg); svg.appendChild(defs);

    /* faint concentric guides */
    [0.25, 0.5, 0.75, 1].forEach(function(pct) {
      domains.forEach(function(d, i) {
        var angle = (Math.PI * 2 * i / n) - Math.PI / 2;
        svg.appendChild(el('circle', {
          cx: cx + maxR * pct * Math.cos(angle),
          cy: cy + maxR * pct * Math.sin(angle),
          r: 1
        })).classList.add('radar-guide');
      });
    });

    /* data polygon */
    var points = domains.map(function(d, i) {
      var angle = (Math.PI * 2 * i / n) - Math.PI / 2;
      var r = maxR * d.score / 100;
      return (cx + r * Math.cos(angle)) + ',' + (cy + r * Math.sin(angle));
    }).join(' ');

    var poly = el('polygon', { points: points });
    poly.style.fill = 'url(#' + gradId + ')';
    poly.classList.add('radar-poly');
    svg.appendChild(poly);

    /* data dots + labels */
    domains.forEach(function(d, i) {
      var angle = (Math.PI * 2 * i / n) - Math.PI / 2;
      var r = maxR * d.score / 100;
      var dx = cx + r * Math.cos(angle);
      var dy = cy + r * Math.sin(angle);

      /* subtle line from center to dot */
      svg.appendChild(el('line', {
        x1: cx, y1: cy, x2: dx, y2: dy,
        stroke: d.color, 'stroke-width': 0.5
      })).classList.add('radar-line');

      /* dot */
      svg.appendChild(el('circle', {
        cx: dx, cy: dy, r: 4, fill: d.color
      })).classList.add('radar-dot');

      /* label */
      var lx = cx + (maxR + 36) * Math.cos(angle);
      var ly = cy + (maxR + 36) * Math.sin(angle);
      var txt = el('text', {
        x: lx, y: ly, 'text-anchor': 'middle', 'dominant-baseline': 'middle'
      });
      txt.classList.add('radar-label');
      txt.textContent = d.name;
      svg.appendChild(txt);
    });

    container.appendChild(svg);
  }

  /* ---- LOLLIPOP ---- */
  function buildLollipop(container, ranking, avg) {
    var wrap = document.createElement('div');
    wrap.className = 'gauges';
    var size = 120, stroke = 7, r = (size - stroke) / 2, circ = 2 * Math.PI * r;

    ranking.forEach(function(d) {
      var offset = circ * (1 - d.score / 100);
      var cell = document.createElement('div');
      cell.className = 'gauges__cell';

      var svg = el('svg', { viewBox: '0 0 ' + size + ' ' + size, width: size, height: size });
      svg.appendChild(el('circle', { cx: size/2, cy: size/2, r: r })).classList.add('gauges__track');
      var fill = el('circle', { cx: size/2, cy: size/2, r: r, fill: 'none', stroke: d.color, 'stroke-width': stroke, 'stroke-linecap': 'round', 'stroke-dasharray': circ, 'stroke-dashoffset': circ, transform: 'rotate(-90 ' + size/2 + ' ' + size/2 + ')' });
      fill.classList.add('gauges__fill');
      fill.style.setProperty('--target', offset);
      svg.appendChild(fill);

      var vt = el('text', { x: size/2, y: size/2 - 4, 'text-anchor': 'middle', 'dominant-baseline': 'middle' });
      vt.classList.add('gauges__val');
      vt.textContent = Math.round(d.score);
      svg.appendChild(vt);

      var lt = el('text', { x: size/2, y: size/2 + 16, 'text-anchor': 'middle', 'dominant-baseline': 'middle' });
      lt.classList.add('gauges__lbl');
      lt.textContent = d.name;
      svg.appendChild(lt);

      cell.appendChild(svg);
      wrap.appendChild(cell);
    });

    container.appendChild(wrap);

    /* animate on scroll */
    setTimeout(function() {
      var fills = wrap.querySelectorAll('.gauges__fill');
      var obs = new IntersectionObserver(function(entries) {
        entries.forEach(function(e) {
          if (e.isIntersecting) {
            e.target.style.strokeDashoffset = e.target.style.getPropertyValue('--target');
            obs.unobserve(e.target);
          }
        });
      }, { threshold: 0.3 });
      fills.forEach(function(f) { obs.observe(f); });
    }, 100);
  }

  /* ---- BRAIN DIAGRAM ---- */
  function buildBrain(container, domains) {
    var w = 400, h = 360;
    var svg = el('svg', { viewBox: '0 0 ' + w + ' ' + h, width: w, height: h });

    /* simplified brain outline */
    var brainPath = 'M200,40 C280,40 340,100 340,180 C340,260 280,320 200,320 C120,320 60,260 60,180 C60,100 120,40 200,40 Z';
    svg.appendChild(el('path', {
      d: brainPath, fill: 'none', stroke: 'var(--border-dim)', 'stroke-width': 1.5, opacity: 0.6
    }));

    /* midline */
    svg.appendChild(el('line', {
      x1: 200, y1: 50, x2: 200, y2: 310,
      stroke: 'var(--border)', 'stroke-width': 0.5, 'stroke-dasharray': '4,4'
    }));

    /* domain positions around the brain */
    var positions = [
      { x: 200, y: 60 },   /* top center */
      { x: 310, y: 120 },  /* right upper */
      { x: 330, y: 200 },  /* right mid */
      { x: 280, y: 290 },  /* right lower */
      { x: 120, y: 290 },  /* left lower */
      { x: 70, y: 200 },   /* left mid */
      { x: 90, y: 120 },   /* left upper */
      { x: 200, y: 180 },  /* center */
    ];

    domains.forEach(function(d, i) {
      if (i >= positions.length) return;
      var pos = positions[i];

      /* connecting line */
      svg.appendChild(el('line', {
        x1: 200, y1: 180, x2: pos.x, y2: pos.y,
        stroke: d.color, 'stroke-width': 1, opacity: 0.3, 'stroke-dasharray': '3,3'
      }));

      /* dot */
      var dotR = 6 + (d.score / 100) * 8;
      svg.appendChild(el('circle', {
        cx: pos.x, cy: pos.y, r: dotR,
        fill: d.color, opacity: 0.8
      }));

      /* label */
      var txt = el('text', {
        x: pos.x, y: pos.y + dotR + 14, 'text-anchor': 'middle',
        fill: 'var(--text-dim)', 'font-family': 'var(--font-mono)', 'font-size': '9'
      });
      txt.textContent = d.name.substring(0, 8);
      svg.appendChild(txt);

      /* score */
      var scoreTxt = el('text', {
        x: pos.x, y: pos.y + 3, 'text-anchor': 'middle', 'dominant-baseline': 'middle',
        fill: '#fff', 'font-family': 'var(--font-display)', 'font-size': '9', 'font-weight': '600'
      });
      scoreTxt.textContent = Math.round(d.score);
      svg.appendChild(scoreTxt);
    });

    container.appendChild(svg);
  }

  /* ---- ARCHITECTURE FLOW (Sankey-style) ---- */
  function buildFlow(container, flows) {
    if (!flows || !flows.length) return;

    var w = 700, h = 340;
    var svg = el('svg', { viewBox: '0 0 ' + w + ' ' + h, width: '100%', height: h });

    /* collect unique nodes */
    var nodeMap = {};
    flows.forEach(function(f) {
      nodeMap[f.from] = true;
      nodeMap[f.to] = true;
    });
    var nodes = Object.keys(nodeMap);

    /* assign columns: sources in col 0, intermediates in col 1, targets in col 2 */
    var sources = [], mids = [], targets = [];
    flows.forEach(function(f) {
      if (sources.indexOf(f.from) === -1 && !flows.some(function(g) { return g.to === f.from; })) sources.push(f.from);
      if (targets.indexOf(f.to) === -1 && !flows.some(function(g) { return g.from === f.to; })) targets.push(f.to);
    });
    nodes.forEach(function(n) {
      if (sources.indexOf(n) === -1 && targets.indexOf(n) === -1) mids.push(n);
    });
    if (mids.length === 0) mids = sources.length > targets.length ? [] : sources;

    /* position nodes */
    var cols = [sources, mids.length ? mids : targets, targets];
    if (mids.length === 0) cols = [sources, targets];
    var nodePos = {};
    cols.forEach(function(col, ci) {
      var x = (ci + 1) * w / (cols.length + 1);
      col.forEach(function(name, ni) {
        var y = (ni + 1) * h / (col.length + 1);
        nodePos[name] = { x: x, y: y, col: ci };
      });
    });

    /* draw links */
    var maxStrength = Math.max.apply(null, flows.map(function(f) { return f.strength; }));
    flows.forEach(function(f) {
      var from = nodePos[f.from];
      var to = nodePos[f.to];
      if (!from || !to) return;
      var sw = 1 + (f.strength / maxStrength) * 6;
      var opacity = 0.2 + (f.strength / maxStrength) * 0.5;
      var mx = (from.x + to.x) / 2;
      var path = 'M' + from.x + ',' + from.y + ' C' + mx + ',' + from.y + ' ' + mx + ',' + to.y + ' ' + to.x + ',' + to.y;
      svg.appendChild(el('path', {
        d: path, fill: 'none', stroke: 'var(--gold)', 'stroke-width': sw, opacity: opacity, 'stroke-linecap': 'round'
      }));
    });

    /* draw nodes */
    nodes.forEach(function(name) {
      var pos = nodePos[name];
      if (!pos) return;
      var rw = 70, rh = 24;
      svg.appendChild(el('rect', {
        x: pos.x - rw/2, y: pos.y - rh/2, width: rw, height: rh,
        fill: 'var(--surface-raised)', stroke: 'var(--border)', 'stroke-width': 1, rx: 4, ry: 4
      }));
      var txt = el('text', {
        x: pos.x, y: pos.y + 1, 'text-anchor': 'middle', 'dominant-baseline': 'middle',
        fill: 'var(--text)', 'font-family': 'var(--font-mono)', 'font-size': '9'
      });
      txt.textContent = name.length > 10 ? name.substring(0, 9) + '.' : name;
      svg.appendChild(txt);
    });

    container.appendChild(svg);
  }

  /* ---- COGNITIVE FINGERPRINT ---- */
  function buildBrainAbstract(container, domains, size) {
    size = size || 360;
    var pad = 40;
    var totalSize = size + pad * 2;
    var cx = totalSize / 2, cy = totalSize / 2;
    var outerR = size * 0.40;
    var innerR = size * 0.28;
    var midR = (outerR + innerR) / 2;
    var n = domains.length;
    var total = domains.reduce(function(s, d) { return s + d.score; }, 0);

    var svg = el('svg', { viewBox: '0 0 ' + totalSize + ' ' + totalSize, width: totalSize, height: totalSize });

    /* defs */
    var defs = el('defs', {});
    var glow = el('filter', { id: 'fp-g', x: '-30%', y: '-30%', width: '160%', height: '160%' });
    glow.appendChild(el('feGaussianBlur', { stdDeviation: '3', result: 'b' }));
    var gm = el('feMerge', {});
    gm.appendChild(el('feMergeNode', { in: 'b' }));
    gm.appendChild(el('feMergeNode', { in: 'SourceGraphic' }));
    glow.appendChild(gm);
    defs.appendChild(glow);

    /* gradient for progress line */
    var lg = el('linearGradient', { id: 'fp-lg', x1: '0%', y1: '0%', x2: '100%', y2: '0%' });
    lg.appendChild(el('stop', { offset: '0%', 'stop-color': domains[0].color }));
    lg.appendChild(el('stop', { offset: '100%', 'stop-color': domains[n - 1].color }));
    defs.appendChild(lg);

    svg.appendChild(defs);

    /* background ring */
    svg.appendChild(el('circle', {
      cx: cx, cy: cy, r: midR,
      fill: 'none', stroke: 'var(--border)', 'stroke-width': outerR - innerR, opacity: 0.08
    }));

    /* score segments + collect midpoints for progress line */
    var startAngle = -Math.PI / 2;
    var gap = 0.03;
    var midpoints = [];

    domains.forEach(function(d, i) {
      var sweep = (d.score / total) * Math.PI * 2 - gap;
      var endAngle = startAngle + sweep;

      var x1o = cx + outerR * Math.cos(startAngle);
      var y1o = cy + outerR * Math.sin(startAngle);
      var x1i = cx + innerR * Math.cos(startAngle);
      var y1i = cy + innerR * Math.sin(startAngle);
      var x2o = cx + outerR * Math.cos(endAngle);
      var y2o = cy + outerR * Math.sin(endAngle);
      var x2i = cx + innerR * Math.cos(endAngle);
      var y2i = cy + innerR * Math.sin(endAngle);
      var large = sweep > Math.PI ? 1 : 0;

      var path = 'M' + x1o + ',' + y1o +
        ' A' + outerR + ',' + outerR + ' 0 ' + large + ' 1 ' + x2o + ',' + y2o +
        ' L' + x2i + ',' + y2i +
        ' A' + innerR + ',' + innerR + ' 0 ' + large + ' 0 ' + x1i + ',' + y1i + ' Z';

      svg.appendChild(el('path', {
        d: path, fill: d.color, opacity: 0
      })).classList.add('fp-seg');

      /* midpoint of this segment for progress line */
      var midAngle = startAngle + sweep / 2;
      midpoints.push({
        x: cx + midR * Math.cos(midAngle),
        y: cy + midR * Math.sin(midAngle),
        color: d.color
      });

      /* label */
      var labelAngle = startAngle + sweep / 2;
      var labelR = outerR + 28;
      var lx = cx + labelR * Math.cos(labelAngle);
      var ly = cy + labelR * Math.sin(labelAngle);
      var anchor = lx > cx ? 'start' : 'end';

      var txt = el('text', {
        x: lx, y: ly, 'text-anchor': anchor, 'dominant-baseline': 'middle',
        fill: d.color, 'font-family': 'var(--ff-mono)', 'font-size': '11', opacity: 0
      });
      txt.textContent = d.name;
      txt.classList.add('fp-lbl');
      svg.appendChild(txt);

      startAngle = endAngle + gap;
    });

    /* progress line through all segment midpoints */
    if (midpoints.length > 1) {
      var linePath = 'M' + midpoints[0].x + ',' + midpoints[0].y;
      for (var i = 1; i < midpoints.length; i++) {
        linePath += ' L' + midpoints[i].x + ',' + midpoints[i].y;
      }
      linePath += ' L' + midpoints[0].x + ',' + midpoints[0].y;

      svg.appendChild(el('path', {
        d: linePath, fill: 'none', stroke: 'url(#fp-lg)', 'stroke-width': 1.5,
        'stroke-linecap': 'round', 'stroke-linejoin': 'round',
        'stroke-dasharray': '2000', 'stroke-dashoffset': '2000', opacity: 0
      })).classList.add('fp-line');

      midpoints.forEach(function(mp) {
        svg.appendChild(el('circle', {
          cx: mp.x, cy: mp.y, r: 3, fill: mp.color, opacity: 0
        })).classList.add('fp-node');
      });
    }

    /* center score */
    svg.appendChild(el('circle', {
      cx: cx, cy: cy, r: innerR - 4, fill: 'var(--bg)', opacity: 0
    })).classList.add('fp-center-bg');

    var scoreTxt = el('text', {
      x: cx, y: cy - 6, 'text-anchor': 'middle', 'dominant-baseline': 'middle',
      fill: 'var(--text)', 'font-family': 'var(--ff-display)', 'font-size': '32', 'font-weight': '700', opacity: 0
    });
    scoreTxt.textContent = Math.round(total / n);
    scoreTxt.classList.add('fp-center');
    svg.appendChild(scoreTxt);

    var subTxt = el('text', {
      x: cx, y: cy + 18, 'text-anchor': 'middle', 'dominant-baseline': 'middle',
      fill: 'var(--text-3)', 'font-family': 'var(--ff-mono)', 'font-size': '10', opacity: 0
    });
    subTxt.textContent = 'overall';
    subTxt.classList.add('fp-center');
    svg.appendChild(subTxt);

    container.appendChild(svg);
  }

  /* ---- PUBLIC API ---- */
  window.A = {
    buildRing: buildRing,
    buildStrip: buildStrip,
    buildRadar: buildRadar,
    buildLollipop: buildLollipop,
    buildBrain: buildBrain,
    buildFlow: buildFlow,
    buildBrainAbstract: buildBrainAbstract
  };

})();
