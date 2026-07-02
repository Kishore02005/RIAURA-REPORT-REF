
(function(){
'use strict';
var d=window.__D;if(!d)return;

/* Theme */
var tb=document.getElementById('theme-btn');
if(tb)tb.addEventListener('click',function(){var c=document.documentElement.getAttribute('data-theme'),n=c==='light'?'dark':'light';document.documentElement.setAttribute('data-theme',n);localStorage.setItem('ahims-theme',n);/* re-render charts for theme */var cr2=document.getElementById('cover-ring');if(cr2){cr2.innerHTML='';var r2=document.createElement('div');r2.className='ring';A.buildRing(r2,d.overallScore,'var(--gold)',220);var t2=document.createElement('div');t2.className='ring__center';t2.innerHTML='<span class="ring__val ring__val--lg" data-count="'+d.overallScore+'" data-suffix="%">0</span><span class="ring__lbl">Overall Index</span>';r2.appendChild(t2);cr2.appendChild(r2);setTimeout(function(){var rf2=r2.querySelector('.ring__fill');if(rf2)rf2.classList.add('is-on');var cv2=r2.querySelector('[data-count]');if(cv2){var tgt=parseFloat(cv2.getAttribute('data-count'));var suf=cv2.getAttribute('data-suffix')||'';var dur=1300;var st=performance.now();(function step(now){var p=Math.min((now-st)/dur,1);cv2.textContent=Math.round(p*tgt)+suf;if(p<1)requestAnimationFrame(step);})(performance.now());}},100);}var rad2=document.getElementById('perf-radar');if(rad2){rad2.innerHTML='';A.buildRadar(rad2,d.domains,400);}var bal2=document.getElementById('balance-ring');if(bal2){bal2.innerHTML='';var br2=document.createElement('div');br2.className='ring';A.buildRing(br2,d.s4.balance_score,'var(--teal)',120);var bt2=document.createElement('div');bt2.className='ring__center';bt2.innerHTML='<span class="ring__val ring__val--sm" data-count="'+d.s4.balance_score+'" data-suffix="%">0</span><span class="ring__lbl">Balance</span>';br2.appendChild(bt2);bal2.appendChild(br2);setTimeout(function(){var bf2=br2.querySelector('.ring__fill');if(bf2)bf2.classList.add('is-on');var bv2=br2.querySelector('[data-count]');if(bv2){var tgt=parseFloat(bv2.getAttribute('data-count'));var suf=bv2.getAttribute('data-suffix')||'';var dur=1300;var st=performance.now();(function step(now){var p=Math.min((now-st)/dur,1);bv2.textContent=Math.round(p*tgt)+suf;if(p<1)requestAnimationFrame(step);})(performance.now());}},100);}});

/* Nav dots */
var secs=document.querySelectorAll('[data-section]'),dotsEl=document.getElementById('nav-dots'),lblEl=document.getElementById('nav-label');
secs.forEach(function(s){var a=document.createElement('a');a.href='#'+s.id;a.className='dot';a.setAttribute('aria-label',s.dataset.label||s.id);dotsEl.appendChild(a);});
var dots=dotsEl.querySelectorAll('.dot');
var navObs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){lblEl.textContent=e.target.dataset.label||'';dots.forEach(function(d,i){d.classList.toggle('is-on',secs[i]===e.target);});}});},{rootMargin:'-40% 0px -55% 0px'});
secs.forEach(function(s){navObs.observe(s);});

/* Nav bg */
var navEl=document.getElementById('nav'),covEl=document.getElementById('cover');
if(navEl&&covEl){var nbo=new IntersectionObserver(function(es){es.forEach(function(e){navEl.classList.toggle('nav--solid',!e.isIntersecting);});},{threshold:.1});nbo.observe(covEl);}

/* Reveal */
var rObs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-on');rObs.unobserve(e.target);}});},{threshold:.12});
document.querySelectorAll('.reveal').forEach(function(e){rObs.observe(e);});

/* Stagger */
var sObs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var k=e.target.children;for(var i=0;i<k.length;i++){(function(el,j){setTimeout(function(){el.classList.add('is-on');},j*70);})(k[i],i);}sObs.unobserve(e.target);}});},{threshold:.1});
document.querySelectorAll('.stagger').forEach(function(e){sObs.observe(e);});

/* Count */
var cObs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&!e.target.dataset.a){e.target.dataset.a='1';var el=e.target,t=parseFloat(el.getAttribute('data-count'));if(isNaN(t))t=0;var suf=el.getAttribute('data-suffix')||'',dur=1300,st=performance.now();(function step(now){var p=Math.min((now-st)/dur,1);el.textContent=Math.round(p*t)+suf;if(p<1)requestAnimationFrame(step);})(performance.now());cObs.unobserve(e.target);}});},{threshold:.3});
document.querySelectorAll('[data-count]').forEach(function(e){cObs.observe(e);});

/* Ring fill */
var rfObs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-on');rfObs.unobserve(e.target);}});},{threshold:.2});

/* Fingerprint reveal */
var baObs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var segs=e.target.querySelectorAll('.fp-seg');var lbls=e.target.querySelectorAll('.fp-lbl');var ctrs=e.target.querySelectorAll('.fp-center');segs.forEach(function(s,i){setTimeout(function(){s.classList.add('is-on');},i*80);});lbls.forEach(function(l,i){setTimeout(function(){l.classList.add('is-on');},i*80+400);});ctrs.forEach(function(c){c.classList.add('is-on');});baObs.unobserve(e.target);}});},{threshold:.3});
var baWrap=document.getElementById('brain-abstract');if(baWrap)baObs.observe(baWrap);

/* Parallel coordinates reveal */
var dbObs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var path=e.target.querySelector('.dc-path');var dots=e.target.querySelectorAll('.dc-dot');if(path)setTimeout(function(){path.classList.add('is-on');},200);dots.forEach(function(d,i){setTimeout(function(){d.classList.add('is-on');},i*120+400);});dbObs.unobserve(e.target);}});},{threshold:.2});
var dbWrap=document.getElementById('domain-bars');if(dbWrap)dbObs.observe(dbWrap);

/* ---- CHARTS ---- */

/* Cover ring */
var cr=document.getElementById('cover-ring');
if(cr){var r=document.createElement('div');r.className='ring';A.buildRing(r,d.overallScore,'var(--gold)',220);var t=document.createElement('div');t.className='ring__center';t.innerHTML='<span class="ring__val ring__val--lg" data-count="'+d.overallScore+'" data-suffix="%">0</span><span class="ring__lbl">Overall Index</span>';r.appendChild(t);cr.appendChild(r);/* trigger ring fill after reveal */var rf=r.querySelector('.ring__fill');if(rf)setTimeout(function(){rf.classList.add('is-on');},600);}

/* Abstract Brain */
var baEl=document.getElementById('brain-abstract');
if(baEl)A.buildBrainAbstract(baEl,d.domains,400);

/* Parallel Coordinates Chart */
var dbEl=document.getElementById('domain-bars');
if(dbEl){
  var sorted=d.domains.slice().sort(function(a,b){return b.score-a.score;});
  var W=1200,H=440,padL=100,padR=100,padT=32,padB=70;
  var usable=W-padL-padR;
  var n=sorted.length;
  var gap=usable/(n-1);
  var minV=0,maxV=100;
  var yScale=function(v){return padT+(1-(v-minV)/(maxV-minV))*(H-padT-padB);};
  var xPos=function(i){return padL+i*gap;};
  var shortNames={'Processing Speed':'Processing','Emotional Intelligence':'Emotional','Decision Integrity':'Decision','Attention':'Attention','Memory':'Memory','Reasoning':'Reasoning','Originality':'Originality','Metacognition':'Metacognitive'};
  var ns='http://www.w3.org/2000/svg';
  var svg=document.createElementNS(ns,'svg');
  svg.setAttribute('viewBox','0 0 '+W+' '+H);svg.setAttribute('preserveAspectRatio','xMidYMid meet');
  var gradId='dc-grad-'+Date.now();
  var defs=document.createElementNS(ns,'defs');
  var grad=document.createElementNS(ns,'linearGradient');grad.id=gradId;grad.setAttribute('x1','0');grad.setAttribute('y1','0');grad.setAttribute('x2','1');grad.setAttribute('y2','0');
  sorted.forEach(function(dd,i){
    var s=document.createElementNS(ns,'stop');s.setAttribute('offset',(i/(n-1)*100)+'%');s.setAttribute('stop-color',dd.color);grad.appendChild(s);
  });
  defs.appendChild(grad);svg.appendChild(defs);
  /* tick lines at 25,50,75 */
  [25,50,75].forEach(function(tv){
    var ty=yScale(tv);
    sorted.forEach(function(dd,i){
      var x=xPos(i);
      var tl=document.createElementNS(ns,'line');tl.setAttribute('x1',x-3);tl.setAttribute('y1',ty);tl.setAttribute('x2',x+3);tl.setAttribute('y2',ty);tl.classList.add('dc-tick-line');svg.appendChild(tl);
    });
  });
  /* axes + labels */
  sorted.forEach(function(dd,i){
    var x=xPos(i);
    var line=document.createElementNS(ns,'line');line.setAttribute('x1',x);line.setAttribute('y1',padT);line.setAttribute('x2',x);line.setAttribute('y2',H-padB);line.classList.add('dc-axis');svg.appendChild(line);
    var lbl=document.createElementNS(ns,'text');lbl.setAttribute('x',x);lbl.setAttribute('y',H-padB+14);lbl.setAttribute('transform','rotate(-25,'+x+','+(H-padB+14)+')');lbl.setAttribute('text-anchor','end');lbl.classList.add('dc-axis-label');lbl.textContent=shortNames[dd.name]||dd.name;svg.appendChild(lbl);
    [25,50,75].forEach(function(tv){
      var t=document.createElementNS(ns,'text');t.setAttribute('x',x-6);t.setAttribute('y',yScale(tv)+3);t.classList.add('dc-tick-label');t.textContent=tv;t.setAttribute('text-anchor','end');svg.appendChild(t);
    });
  });
  /* polyline */
  var pts=sorted.map(function(dd,i){return xPos(i)+','+yScale(dd.score);});
  var path=document.createElementNS(ns,'path');path.setAttribute('d','M'+pts.join(' L'));path.setAttribute('stroke','url(#'+gradId+')');path.classList.add('dc-path');svg.appendChild(path);
  /* dots */
  sorted.forEach(function(dd,i){
    var c=document.createElementNS(ns,'circle');c.setAttribute('cx',xPos(i));c.setAttribute('cy',yScale(dd.score));c.setAttribute('fill',dd.color);c.classList.add('dc-dot');svg.appendChild(c);
  });
  dbEl.appendChild(svg);
}

/* Performance */
var radEl=document.getElementById('perf-radar');if(radEl)A.buildRadar(radEl,d.domains,500);
var balEl=document.getElementById('balance-ring');
if(balEl){var br=document.createElement('div');br.className='ring';A.buildRing(br,d.s4.balance_score,'var(--teal)',120);var bt=document.createElement('div');bt.className='ring__center';bt.innerHTML='<span class="ring__val ring__val--sm" data-count="'+d.s4.balance_score+'" data-suffix="%">0</span><span class="ring__lbl">Balance</span>';br.appendChild(bt);balEl.appendChild(br);}
var lolEl=document.getElementById('perf-lollipop');if(lolEl)A.buildLollipop(lolEl,d.s4.domain_ranking,d.s4.avg_score);

/* Explorer */
var expEl=document.getElementById('explorer-cards');
if(expEl){d.s5.forEach(function(dom){var c=document.createElement('div');c.className='dcard reveal';c.id='dc-'+dom.key;c.style.setProperty('--c',dom.color);c.innerHTML='<div class="dcard__top"><div class="dcard__ring" id="ecr-'+dom.key+'"></div><div class="dcard__info"><h3 class="dcard__name">'+dom.name+'</h3><span class="dcard__region">'+dom.brain_region+'</span></div><svg class="dcard__chev" viewBox="0 0 20 20" fill="none"><path d="M6 8l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><div class="dcard__body"><p>'+dom.description+'</p><p>'+dom.narrative+'</p><div class="dcard__hint"><strong>Try:</strong> '+dom.development_hint+'</div></div>';expEl.appendChild(c);setTimeout(function(){var rc=document.getElementById('ecr-'+dom.key);if(rc){var rr=document.createElement('div');rr.className='ring';A.buildRing(rr,dom.score,dom.color,52);var rt=document.createElement('div');rt.className='ring__center';rt.innerHTML='<span class="ring__val ring__val--sm">'+Math.round(dom.score)+'</span>';rr.appendChild(rt);rc.appendChild(rr);}},50);});
expEl.addEventListener('click',function(e){var c=e.target.closest('.dcard');if(!c)return;var was=c.classList.contains('is-open');expEl.querySelectorAll('.dcard.is-open').forEach(function(x){x.classList.remove('is-open');});if(!was)c.classList.add('is-open');});}

/* Brain */
var brEl=document.getElementById('brain-main');if(brEl)A.buildBrain(brEl,d.domains);
var bcEl=document.getElementById('brain-cards');
if(bcEl){d.s6.forEach(function(b){var c=document.createElement('div');c.className='bcard reveal';c.innerHTML='<span class="bcard__dot" style="background:'+b.color+'"></span><div class="bcard__info"><h4 class="bcard__name">'+b.name+'</h4><span class="bcard__region">'+b.brain_region+'</span><span class="bcard__tier">'+b.tier+' &middot; '+b.score+'%</span></div>';bcEl.appendChild(c);});}

/* Architecture - Sankey + Parliament Transition */
var archSankey=document.getElementById('arch-sankey');
if(archSankey&&typeof echarts!=='undefined'){
  var allColors=['#F5A623','#1F9E96','#3D63DD','#7C5CFC','#2E8B57','#E8607A','#F0654A','#4B3F72','#D4A72C','#9B7CC8','#3498DB'];
  var nameColorMap={'Attention':allColors[0],'Memory':allColors[1],'Processing':allColors[2],'Reasoning':allColors[3],'Decision Integrity':allColors[4],'Emotional Intelligence':allColors[5],'Originality':allColors[6],'Metacognition':allColors[7],'Learning':allColors[8],'Problem Solving':allColors[9],'Daily Behaviour':allColors[10]};
  var sankeyNodes=[
    {name:'Attention',itemStyle:{color:allColors[0]}},
    {name:'Memory',itemStyle:{color:allColors[1]}},
    {name:'Processing',itemStyle:{color:allColors[2]}},
    {name:'Reasoning',itemStyle:{color:allColors[3]}},
    {name:'Decision Integrity',itemStyle:{color:allColors[4]}},
    {name:'Emotional Intelligence',itemStyle:{color:allColors[5]}},
    {name:'Originality',itemStyle:{color:allColors[6]}},
    {name:'Metacognition',itemStyle:{color:allColors[7]}},
    {name:'Learning',itemStyle:{color:allColors[8]}},
    {name:'Problem Solving',itemStyle:{color:allColors[9]}},
    {name:'Daily Behaviour',itemStyle:{color:allColors[10]}}
  ];
  var sankeyLinks=d.s7.flows.map(function(f){return{source:f.from,target:f.to,value:f.strength*100};});

  var sankeyChart=echarts.init(archSankey,null,{renderer:'svg'});
  sankeyChart.setOption({
    backgroundColor:'transparent',
    tooltip:{trigger:'item',triggerOn:'mousemove',formatter:function(p){if(p.dataType==='edge')return p.data.source+' → '+p.data.target+'<br/>Strength: '+Math.round(p.data.value)+'%';return p.name;}},
    series:[{type:'sankey',layout:'none',emphasis:{focus:'adjacency'},nodeAlign:'justify',layoutIterations:32,orient:'horizontal',nodeWidth:16,nodeGap:12,label:{show:true,color:'var(--text-2)',fontFamily:'var(--ff-mono)',fontSize:11},lineStyle:{color:'gradient',curveness:0.5,opacity:0.35},data:sankeyNodes,links:sankeyLinks}]
  });

  window.addEventListener('resize',function(){sankeyChart.resize();});
}

/* Functional */
var fuEl=document.getElementById('func-grid');
if(fuEl){d.s8.forEach(function(f){var c=document.createElement('div');c.className='xcard reveal';var pills=f.domains.map(function(dd){return'<span class="pill" style="background:'+dd.color+'">'+dd.name+'</span>';}).join('');c.innerHTML='<h3 class="xcard__title">'+f.title+'</h3><p class="xcard__text">'+f.narrative+'</p><div class="xcard__pills">'+pills+'</div>';fuEl.appendChild(c);});}

/* Interpersonal */
var inEl=document.getElementById('interp-cards');
if(inEl){var ICONS=['<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'];
d.s9.connections.forEach(function(c,i){var el=document.createElement('div');el.className='icard reveal';var icon=ICONS[i%ICONS.length];var pills=c.domains.map(function(dd){return'<span class="pill" style="background:'+dd.color+'">'+dd.name+'</span>';}).join('');el.innerHTML='<div class="icard__icon">'+icon+'</div><div class="icard__body"><h3 class="icard__title">'+c.skill+'</h3><p class="icard__desc">'+c.description+'</p><div class="icard__pills">'+pills+'</div></div>';inEl.appendChild(el);});}

/* Dev matrix */
/* Dev roadmap */
var rdEl=document.getElementById('dev-roadmap');
if(rdEl){
  var rh='<div class="timeline">';
  d.s11.roadmap.forEach(function(r,i){
    rh+='<div class="timeline__item">';
    rh+='<div class="timeline__marker"><span class="timeline__dot"></span>'+(i<d.s11.roadmap.length-1?'<span class="timeline__line"></span>':'')+'</div>';
    rh+='<div class="timeline__content"><span class="timeline__phase">'+r.phase+'</span><p class="timeline__text">'+r.action+'</p></div>';
    rh+='</div>';
  });
  rh+='</div>';
  rdEl.innerHTML=rh;
}

/* Dev focus cards */
var fcEl=document.getElementById('dev-focus');
if(fcEl){
  var fh='<div class="focus-grid">';
  d.s11.priorities.forEach(function(p){
    fh+='<div class="focus-card" style="--c:'+p.color+'">';
    fh+='<div class="focus-card__head"><span class="focus-card__rank">'+p.rank+'</span><span class="focus-card__name">'+p.name+'</span></div>';
    fh+='<div class="focus-card__bar"><div class="focus-card__fill" style="width:'+p.score+'%;background:'+p.color+'"></div></div>';
    fh+='<div class="focus-card__meta"><span class="focus-card__score">'+Math.round(p.score)+'%</span><span class="focus-card__impact '+p.impact.toLowerCase()+'">'+p.impact+' Impact</span></div>';
    fh+='<p class="focus-card__hint">'+p.hint+'</p>';
    fh+='</div>';
  });
  fh+='</div>';
  fcEl.innerHTML=fh;
}

/* Labs */
var lbEl=document.getElementById('labs-flow');
if(lbEl){var ARROW='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14m0 0l-6-6m6 6l6-6"/></svg>';d.s12.forEach(function(lab){var c=document.createElement('div');c.className='lcard reveal';c.style.setProperty('--c',lab.color);c.innerHTML='<div class="lcard__rank">'+lab.rank+'</div><div class="lcard__body"><span class="pill" style="background:'+lab.color+'">'+lab.domain_name+'</span><h3 class="lcard__title">'+lab.lab_name+'</h3><div class="lcard__flow"><div class="lcard__step"><span class="lcard__step-lbl">Activity</span><p>'+lab.lab_description+'</p></div><div class="lcard__arrow">'+ARROW+'</div><div class="lcard__step"><span class="lcard__step-lbl">Benefit</span><p>'+lab.expected_benefit+'</p></div><div class="lcard__arrow">'+ARROW+'</div><div class="lcard__step"><span class="lcard__step-lbl">Brain</span><p>'+lab.brain_function+'</p></div></div></div>';lbEl.appendChild(c);});}

/* Appendix */
var glEl=document.getElementById('glossary-grid');
if(glEl){d.glossary.forEach(function(g){var i=document.createElement('div');i.className='gloss';i.innerHTML='<span class="gloss__dot" style="background:'+g.color+'"></span><div><span class="gloss__name">'+g.name+'</span><p class="gloss__desc">'+g.description+'</p><span class="gloss__region">'+g.brain_region+'</span></div>';glEl.appendChild(i);});}
var blEl=document.getElementById('brain-legend');
if(blEl){var bl='';d.glossary.forEach(function(g){bl+='<div class="leg"><span class="leg__dot" style="background:'+g.color+'"></span><span class="leg__name">'+g.name+'</span><span class="leg__region">&mdash; '+g.brain_region+'</span></div>';});blEl.innerHTML=bl;}
var clEl=document.getElementById('color-legend');
if(clEl){var cl='';d.domains.forEach(function(dd){cl+='<div class="leg"><span class="leg__dot" style="background:'+dd.color+'"></span><span class="leg__name">'+dd.name+'</span></div>';});clEl.innerHTML=cl;}

/* Sticky */
var sf=document.getElementById('sticky-footer');
if(sf&&covEl){var sfo=new IntersectionObserver(function(es){es.forEach(function(e){sf.classList.toggle('is-on',!e.isIntersecting);});},{threshold:.1});sfo.observe(covEl);}
var dlB=document.getElementById('btn-download');if(dlB)dlB.addEventListener('click',function(){window.print();});
var shB=document.getElementById('btn-share');if(shB)shB.addEventListener('click',function(){if(navigator.share){navigator.share({title:'AHIMS Cognitive Report',url:window.location.href});}else if(navigator.clipboard){navigator.clipboard.writeText(window.location.href).then(function(){shB.textContent='Copied!';setTimeout(function(){shB.innerHTML='<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="14" cy="4" r="2.5"/><circle cx="5.5" cy="10" r="2.5"/><circle cx="14" cy="16" r="2.5"/><line x1="7.7" y1="8.8" x2="11.8" y2="5.2"/><line x1="7.7" y1="11.2" x2="11.8" y2="14.8"/></svg> Share';},1500);});}});

/* Re-observe dynamic elements */
document.querySelectorAll('[data-count]').forEach(function(e){cObs.observe(e);});
document.querySelectorAll('.ring__fill').forEach(function(e){rfObs.observe(e);});
})();
