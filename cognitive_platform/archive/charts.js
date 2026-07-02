/**
 * COGNITIVE PLATFORM — CHART INITIALIZATION
 * Apache ECharts (SVG renderer only)
 * All charts answer a cognitive question. No decorative elements.
 */

(function () {
  'use strict';

  const COLORS = {
    attention: '#3B82F6',
    memory: '#4338CA',
    processing: '#14B8A6',
    reasoning: '#8B5CF6',
    decision_integrity: '#475569',
    emotional_intelligence: '#F87171',
    originality: '#D97706',
    metacognition: '#6B7280',
  };

  const FONT = {
    family: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    mono: "'JetBrains Mono', monospace",
  };

  // ---------------------------------------------------------------------------
  // Initialize all charts when DOM is ready
  // ---------------------------------------------------------------------------

  function initCharts() {
    if (!window.__CHART_DATA__) return;

    initRadarChart();
    initGaugeChart();
    initParallelChart();
    initFingerprintChart();
  }

  // ---------------------------------------------------------------------------
  // RADAR CHART — Domain structure visualization
  // Answers: "What is the shape of my cognitive profile?"
  // ---------------------------------------------------------------------------

  function initRadarChart() {
    const container = document.getElementById('chart-radar');
    if (!container) return;

    const chart = echarts.init(container, null, { renderer: 'svg' });
    const data = window.__CHART_DATA__.radar;

    const option = {
      animation: true,
      animationDuration: 1200,
      animationEasing: 'cubicOut',
      radar: {
        indicator: data.indicators,
        shape: 'polygon',
        radius: '70%',
        center: ['50%', '52%'],
        axisName: {
          color: '#8892A0',
          fontSize: 11,
          fontFamily: FONT.family,
          fontWeight: 500,
        },
        splitArea: {
          areaStyle: {
            color: ['#FAFBFC', '#F1F3F5', '#FAFBFC', '#F1F3F5'],
          },
        },
        splitLine: {
          lineStyle: {
            color: '#E8EBF0',
            width: 1,
          },
        },
        axisLine: {
          lineStyle: {
            color: '#E8EBF0',
            width: 1,
          },
        },
      },
      series: [
        {
          type: 'radar',
          symbol: 'circle',
          symbolSize: 6,
          data: [
            {
              value: data.values,
              name: 'Your Profile',
              areaStyle: {
                color: 'rgba(37, 99, 235, 0.08)',
              },
              lineStyle: {
                color: '#2563EB',
                width: 2,
              },
              itemStyle: {
                color: '#2563EB',
                borderColor: '#fff',
                borderWidth: 2,
              },
            },
          ],
        },
      ],
      tooltip: {
        trigger: 'item',
        backgroundColor: '#fff',
        borderColor: '#E8EBF0',
        borderWidth: 1,
        padding: [8, 12],
        textStyle: {
          color: '#1A1D23',
          fontSize: 13,
          fontFamily: FONT.family,
        },
        formatter: function (params) {
          if (!params.value) return '';
          let html = '<div style="font-weight:600;margin-bottom:4px;">Cognitive Domain Scores</div>';
          data.indicators.forEach(function (ind, i) {
            html += '<div style="display:flex;justify-content:space-between;gap:16px;padding:2px 0;">';
            html += '<span style="color:#8892A0;">' + ind.name + '</span>';
            html += '<span style="font-weight:600;font-family:' + FONT.mono + ';">' + params.value[i] + '%</span>';
            html += '</div>';
          });
          return html;
        },
      },
    };

    chart.setOption(option);
    window.addEventListener('resize', function () { chart.resize(); });
  }

  // ---------------------------------------------------------------------------
  // GAUGE CHART — Overall score indicator
  // Answers: "What is my overall cognitive performance level?"
  // ---------------------------------------------------------------------------

  function initGaugeChart() {
    const container = document.getElementById('chart-gauge');
    if (!container) return;

    const chart = echarts.init(container, null, { renderer: 'svg' });
    const data = window.__CHART_DATA__.gauge;

    const tierColors = {
      distinguished: '#1E40AF',
      high: '#047857',
      moderate: '#B45309',
      developing: '#6B7280',
    };

    const tierColor = tierColors[data.tier.toLowerCase()] || '#2563EB';

    const option = {
      animation: true,
      animationDuration: 1500,
      animationEasing: 'cubicOut',
      series: [
        {
          type: 'gauge',
          startAngle: 220,
          endAngle: -40,
          radius: '85%',
          center: ['50%', '55%'],
          min: 0,
          max: 100,
          splitNumber: 5,
          axisLine: {
            lineStyle: {
              width: 12,
              color: [
                [0.5, '#F1F3F5'],
                [0.7, '#F1F3F5'],
                [0.85, '#F1F3F5'],
                [1, '#F1F3F5'],
              ],
            },
            roundCap: true,
          },
          progress: {
            show: true,
            width: 12,
            roundCap: true,
            itemStyle: {
              color: tierColor,
            },
          },
          pointer: {
            show: false,
          },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
          title: {
            show: true,
            offsetCenter: [0, '30%'],
            fontSize: 12,
            fontWeight: 600,
            fontFamily: FONT.family,
            color: '#8892A0',
            textTransform: 'uppercase',
          },
          detail: {
            valueAnimation: true,
            offsetCenter: [0, '-5%'],
            fontSize: 42,
            fontWeight: 700,
            fontFamily: FONT.family,
            color: '#1A1D23',
            formatter: function (val) {
              return val.toFixed(0) + '%';
            },
          },
          data: [
            {
              value: data.value,
              name: data.tier.toUpperCase(),
            },
          ],
        },
      ],
    };

    chart.setOption(option);
    window.addEventListener('resize', function () { chart.resize(); });
  }

  // ---------------------------------------------------------------------------
  // PARALLEL COORDINATES — Cognitive balance visualization
  // Answers: "How balanced is my cognitive profile across domains?"
  // ---------------------------------------------------------------------------

  function initParallelChart() {
    const container = document.getElementById('chart-parallel');
    if (!container) return;

    const chart = echarts.init(container, null, { renderer: 'svg' });
    const data = window.__CHART_DATA__.parallel;

    const option = {
      animation: true,
      animationDuration: 1000,
      parallelAxis: data.dimensions.map(function (dim, i) {
        return {
          dim: i,
          name: dim.name,
          min: dim.min,
          max: dim.max,
          nameTextStyle: {
            color: '#8892A0',
            fontSize: 11,
            fontFamily: FONT.family,
            fontWeight: 500,
            padding: [0, 0, 8, 0],
          },
          axisLine: {
            lineStyle: {
              color: '#E8EBF0',
              width: 1,
            },
          },
          axisTick: { show: false },
          axisLabel: {
            color: '#B0B8C4',
            fontSize: 10,
            fontFamily: FONT.mono,
          },
        };
      }),
      parallel: {
        left: 60,
        right: 60,
        top: 40,
        bottom: 40,
        parallelAxisDefault: {
          type: 'value',
          nameLocation: 'start',
          nameGap: 25,
        },
      },
      series: [
        {
          type: 'parallel',
          lineStyle: {
            width: 2,
            color: '#2563EB',
            opacity: 0.8,
          },
          emphasis: {
            lineStyle: {
              width: 3,
              opacity: 1,
            },
          },
          data: [
            {
              value: data.values,
            },
          ],
          smooth: true,
        },
        // Background reference lines for context
        {
          type: 'parallel',
          lineStyle: {
            width: 1,
            color: '#E8EBF0',
            opacity: 0.4,
            type: 'dashed',
          },
          silent: true,
          data: [
            { value: [50, 50, 50, 50, 50, 50, 50, 50] },
          ],
        },
      ],
      tooltip: {
        trigger: 'item',
        backgroundColor: '#fff',
        borderColor: '#E8EBF0',
        borderWidth: 1,
        padding: [8, 12],
        textStyle: {
          color: '#1A1D23',
          fontSize: 13,
          fontFamily: FONT.family,
        },
        formatter: function (params) {
          if (!params.value) return '';
          let html = '<div style="font-weight:600;margin-bottom:4px;">Domain Scores</div>';
          data.dimensions.forEach(function (dim, i) {
            const val = params.value[i];
            if (val === undefined) return;
            html += '<div style="display:flex;justify-content:space-between;gap:16px;padding:2px 0;">';
            html += '<span style="color:#8892A0;">' + dim.name + '</span>';
            html += '<span style="font-weight:600;font-family:' + FONT.mono + ';">' + val + '%</span>';
            html += '</div>';
          });
          return html;
        },
      },
    };

    chart.setOption(option);
    window.addEventListener('resize', function () { chart.resize(); });
  }

  // ---------------------------------------------------------------------------
  // FINGERPRINT CHART — Cluster-based cognitive visualization
  // Answers: "What shape is my cognitive identity?"
  // ---------------------------------------------------------------------------

  function initFingerprintChart() {
    const container = document.getElementById('chart-fingerprint');
    if (!container) return;

    const chart = echarts.init(container, null, { renderer: 'svg' });
    const data = window.__CHART_DATA__.fingerprint;

    // Create a scatter-based fingerprint visualization
    const scatterData = data.points.map(function (point, i) {
      const angle = (i / data.points.length) * 2 * Math.PI - Math.PI / 2;
      const radius = (point.value / 100) * 0.85;
      return {
        value: [
          Math.cos(angle) * radius,
          Math.sin(angle) * radius,
          point.value,
        ],
        name: point.name,
        itemStyle: {
          color: point.color,
        },
        symbolSize: Math.max(8, point.value / 5),
      };
    });

    // Create polygon path from data points
    const polygonData = data.points.map(function (point, i) {
      const angle = (i / data.points.length) * 2 * Math.PI - Math.PI / 2;
      const radius = (point.value / 100) * 0.85;
      return [
        Math.cos(angle) * radius,
        Math.sin(angle) * radius,
      ];
    });

    const option = {
      animation: true,
      animationDuration: 1200,
      animationEasing: 'cubicOut',
      grid: {
        left: 40,
        right: 40,
        top: 40,
        bottom: 40,
      },
      xAxis: {
        type: 'value',
        min: -1,
        max: 1,
        show: false,
      },
      yAxis: {
        type: 'value',
        min: -1,
        max: 1,
        show: false,
      },
      series: [
        // Grid lines (subtle radial guides)
        {
          type: 'lines',
          coordinateSystem: 'cartesian2d',
          silent: true,
          lineStyle: {
            color: '#E8EBF0',
            width: 0.5,
            opacity: 0.5,
          },
          data: [
            [{ coord: [0, 0] }, { coord: [0.9, 0] }],
            [{ coord: [0, 0] }, { coord: [-0.9, 0] }],
            [{ coord: [0, 0] }, { coord: [0, 0.9] }],
            [{ coord: [0, 0] }, { coord: [0, -0.9] }],
          ],
        },
        // Polygon shape
        {
          type: 'custom',
          coordinateSystem: 'cartesian2d',
          silent: true,
          renderItem: function (params, api) {
            const points = polygonData.map(function (p) {
              return api.coord(p);
            });
            return {
              type: 'polygon',
              shape: { points: points },
              style: {
                fill: 'rgba(37, 99, 235, 0.06)',
                stroke: 'rgba(37, 99, 235, 0.3)',
                lineWidth: 1.5,
              },
            };
          },
          data: [{ value: polygonData }],
        },
        // Domain points
        {
          type: 'scatter',
          coordinateSystem: 'cartesian2d',
          data: scatterData,
          label: {
            show: true,
            formatter: '{b}',
            position: 'top',
            distance: 8,
            fontSize: 10,
            fontFamily: FONT.family,
            fontWeight: 500,
            color: '#8892A0',
          },
          emphasis: {
            scale: 1.3,
            itemStyle: {
              borderColor: '#fff',
              borderWidth: 2,
              shadowBlur: 8,
              shadowColor: 'rgba(0,0,0,0.1)',
            },
          },
        },
      ],
      tooltip: {
        trigger: 'item',
        backgroundColor: '#fff',
        borderColor: '#E8EBF0',
        borderWidth: 1,
        padding: [8, 12],
        textStyle: {
          color: '#1A1D23',
          fontSize: 13,
          fontFamily: FONT.family,
        },
        formatter: function (params) {
          if (!params.data || !params.data.name) return '';
          return '<span style="font-weight:600;">' + params.data.name + '</span><br>' +
            '<span style="font-family:' + FONT.mono + ';">' + params.data.value[2] + '%</span>';
        },
      },
    };

    chart.setOption(option);
    window.addEventListener('resize', function () { chart.resize(); });
  }

  // ---------------------------------------------------------------------------
  // Boot
  // ---------------------------------------------------------------------------

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCharts);
  } else {
    initCharts();
  }
})();
