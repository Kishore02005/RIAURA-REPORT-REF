/**
 * NeuroSpectrum — Constellation Chart
 * Custom SVG visualization replacing traditional radar charts.
 * Each node represents a cognitive domain positioned by score intensity.
 */
(function () {
  'use strict';

  function init() {
    var container = document.getElementById('constellation-chart');
    if (!container) return;

    var data = window.__REPORT_DATA__;
    if (!data || !data.constellation) return;

    var size = Math.min(container.offsetWidth || 480, 480);
    var cx = size / 2;
    var cy = size / 2;
    var maxR = (size / 2) - 60;

    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 ' + size + ' ' + size);
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '100%');
    svg.style.maxWidth = size + 'px';

    // Background rings
    [0.25, 0.5, 0.75, 1.0].forEach(function (frac) {
      var ring = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      ring.setAttribute('cx', cx);
      ring.setAttribute('cy', cy);
      ring.setAttribute('r', maxR * frac);
      ring.setAttribute('fill', 'none');
      ring.setAttribute('stroke', '#E7E5E4');
      ring.setAttribute('stroke-width', '0.5');
      ring.setAttribute('opacity', '0.5');
      svg.appendChild(ring);
    });

    // Axis lines
    var points = data.constellation.points;
    points.forEach(function (p, i) {
      var angle = (i / points.length) * 2 * Math.PI - Math.PI / 2;
      var line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', cx);
      line.setAttribute('y1', cy);
      line.setAttribute('x2', cx + Math.cos(angle) * maxR);
      line.setAttribute('y2', cy + Math.sin(angle) * maxR);
      line.setAttribute('stroke', '#E7E5E4');
      line.setAttribute('stroke-width', '0.5');
      line.setAttribute('opacity', '0.3');
      svg.appendChild(line);
    });

    // Connections
    var connections = data.constellation.connections;
    connections.forEach(function (conn) {
      var p1 = points[conn.from];
      var p2 = points[conn.to];
      var line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', cx + p1.x * maxR);
      line.setAttribute('y1', cy + p1.y * maxR);
      line.setAttribute('x2', cx + p2.x * maxR);
      line.setAttribute('y2', cy + p2.y * maxR);
      line.setAttribute('stroke', '#D6D3D1');
      line.setAttribute('stroke-width', (conn.strength * 2).toString());
      line.setAttribute('opacity', (conn.strength * 0.4).toString());
      svg.appendChild(line);
    });

    // Nodes with glow
    points.forEach(function (p, i) {
      var nx = cx + p.x * maxR;
      var ny = cy + p.y * maxR;
      var nodeR = 4 + (p.value / 100) * 8;

      // Glow
      var glow = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      glow.setAttribute('cx', nx);
      glow.setAttribute('cy', ny);
      glow.setAttribute('r', nodeR + 6);
      glow.setAttribute('fill', p.color);
      glow.setAttribute('opacity', '0.12');
      svg.appendChild(glow);

      // Node
      var node = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      node.setAttribute('cx', nx);
      node.setAttribute('cy', ny);
      node.setAttribute('r', nodeR);
      node.setAttribute('fill', p.color);
      node.setAttribute('opacity', '0.85');
      node.setAttribute('class', 'constellation__node');
      node.style.cursor = 'pointer';
      node.style.transition = 'transform 0.2s ease, opacity 0.2s ease';

      // Hover tooltip
      node.addEventListener('mouseenter', function () {
        node.setAttribute('opacity', '1');
        node.setAttribute('r', nodeR + 2);
        showTooltip(p.name, p.value + '%', p.color);
      });
      node.addEventListener('mouseleave', function () {
        node.setAttribute('opacity', '0.85');
        node.setAttribute('r', nodeR);
        hideTooltip();
      });

      svg.appendChild(node);

      // Label
      var labelAngle = (i / points.length) * 2 * Math.PI - Math.PI / 2;
      var labelR = maxR + 28;
      var lx = cx + Math.cos(labelAngle) * labelR;
      var ly = cy + Math.sin(labelAngle) * labelR;

      var label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      label.setAttribute('x', lx);
      label.setAttribute('y', ly);
      label.setAttribute('text-anchor', 'middle');
      label.setAttribute('dominant-baseline', 'central');
      label.setAttribute('font-family', "'Inter', sans-serif");
      label.setAttribute('font-size', '10');
      label.setAttribute('font-weight', '500');
      label.setAttribute('fill', '#78716C');
      label.textContent = p.name;
      svg.appendChild(label);

      // Value
      var val = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      val.setAttribute('x', lx);
      val.setAttribute('y', ly + 14);
      val.setAttribute('text-anchor', 'middle');
      val.setAttribute('font-family', "'JetBrains Mono', monospace");
      val.setAttribute('font-size', '11');
      val.setAttribute('font-weight', '700');
      val.setAttribute('fill', '#1C1917');
      val.textContent = p.value + '%';
      svg.appendChild(val);
    });

    container.appendChild(svg);
  }

  // Tooltip
  var tooltipEl = null;

  function showTooltip(name, value, color) {
    if (!tooltipEl) {
      tooltipEl = document.createElement('div');
      tooltipEl.style.cssText = 'position:fixed;padding:8px 14px;background:#fff;border:1px solid #E7E5E4;border-radius:8px;font-size:13px;color:#1C1917;pointer-events:none;z-index:1000;box-shadow:0 4px 12px rgba(0,0,0,0.06);font-family:Inter,sans-serif;transition:opacity 0.15s ease;';
      document.body.appendChild(tooltipEl);
    }
    tooltipEl.innerHTML = '<span style="font-weight:600;">' + name + '</span> <span style="font-family:JetBrains Mono,monospace;color:' + color + ';">' + value + '</span>';
    tooltipEl.style.opacity = '1';

    document.addEventListener('mousemove', moveTooltip);
  }

  function moveTooltip(e) {
    if (tooltipEl) {
      tooltipEl.style.left = (e.clientX + 12) + 'px';
      tooltipEl.style.top = (e.clientY - 10) + 'px';
    }
  }

  function hideTooltip() {
    if (tooltipEl) {
      tooltipEl.style.opacity = '0';
    }
    document.removeEventListener('mousemove', moveTooltip);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
