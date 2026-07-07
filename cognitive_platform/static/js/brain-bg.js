/* ============================================================
   RIAURA — Brain-Themed Background Visualizations
   Three.js WebGL · Cognitive Architecture
   ============================================================ */
(function(){
'use strict';

var COLORS={
  navy:'#080D18',blue:'#3D63DD',purple:'#7C5CFC',teal:'#1F9E96',
  gold:'#D4A72C',pink:'#E8607A',indigo:'#4B3F72',white:'#F0EDE8'
};
var hex=function(h){return parseInt(h.slice(1),16)};

function init(){
  if(typeof THREE==='undefined')return;

  var W=window.innerWidth,H=window.innerHeight;
  var canvas=document.createElement('canvas');
  canvas.id='brain-canvas';
  canvas.style.cssText='position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;opacity:0;transition:opacity 1.5s ease';
  document.body.prepend(canvas);

  /* Renderer */
  var renderer=new THREE.WebGLRenderer({canvas:canvas,antialias:true,alpha:true});
  renderer.setSize(W,H);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
  renderer.setClearColor(0x000000,0);

  /* Camera */
  var camera=new THREE.PerspectiveCamera(50,W/H,0.1,1000);
  camera.position.set(0,0,5);

  /* ---- SCENE 1: Wireframe Brain (Hero) ---- */
  var scene1=new THREE.Scene();
  var brainGeo=new THREE.IcosahedronGeometry(1.8,4);
  var pos=brainGeo.attributes.position;
  for(var i=0;i<pos.count;i++){
    var x=pos.getX(i),y=pos.getY(i),z=pos.getZ(i);
    var n=Math.sin(x*2.1)*0.12+Math.cos(y*3.7)*0.09+Math.sin(z*1.8)*0.11;
    var fold=Math.sin(y*6+x*2)*0.04+Math.cos(x*5+z*3)*0.03;
    var sc=1+n+fold;
    pos.setXYZ(i,x*sc,y*sc,z*sc);
  }
  brainGeo.computeVertexNormals();

  var brainMat=new THREE.MeshPhongMaterial({
    color:hex(COLORS.blue),emissive:hex(COLORS.indigo),emissiveIntensity:0.15,
    wireframe:true,transparent:true,opacity:0.18,depthWrite:false
  });
  var brainMesh=new THREE.Mesh(brainGeo,brainMat);
  scene1.add(brainMesh);

  /* Cortical fold lines — slightly larger wireframe */
  var foldGeo=new THREE.IcosahedronGeometry(1.88,3);
  var fp=foldGeo.attributes.position;
  for(var i=0;i<fp.count;i++){
    var x=fp.getX(i),y=fp.getY(i),z=fp.getZ(i);
    var n=Math.sin(x*2.1)*0.12+Math.cos(y*3.7)*0.09+Math.sin(z*1.8)*0.11;
    var fold=Math.sin(y*6+x*2)*0.04+Math.cos(x*5+z*3)*0.03;
    var sc=1+n+fold;
    fp.setXYZ(i,x*sc,y*sc,z*sc);
  }
  var foldMat=new THREE.MeshBasicMaterial({color:hex(COLORS.purple),transparent:true,opacity:0.06,wireframe:true,depthWrite:false});
  var foldMesh=new THREE.Mesh(foldGeo,foldMat);
  scene1.add(foldMesh);

  /* Inner glow sphere */
  var glowGeo=new THREE.SphereGeometry(1.2,16,16);
  var glowMat=new THREE.MeshBasicMaterial({color:hex(COLORS.blue),transparent:true,opacity:0.04,depthWrite:false});
  var glowMesh=new THREE.Mesh(glowGeo,glowMat);
  scene1.add(glowMesh);

  /* Ambient light */
  scene1.add(new THREE.AmbientLight(0xffffff,0.3));
  var pl=new THREE.PointLight(hex(COLORS.blue),0.6,10);
  pl.position.set(3,2,4);
  scene1.add(pl);
  var pl2=new THREE.PointLight(hex(COLORS.purple),0.3,10);
  pl2.position.set(-3,-1,3);
  scene1.add(pl2);

  /* ---- SCENE 2: Neural Network (Explorer) ---- */
  var scene2=new THREE.Scene();
  var NPARTICLES=200;
  var nPos=new Float32Array(NPARTICLES*3);
  var nVel=new Float32Array(NPARTICLES*3);
  var nCol=new Float32Array(NPARTICLES*3);
  var brainColors=[
    hex(COLORS.blue),hex(COLORS.purple),hex(COLORS.teal),
    hex(COLORS.gold),hex(COLORS.pink),hex(COLORS.indigo)
  ];

  for(var i=0;i<NPARTICLES;i++){
    var theta=Math.random()*Math.PI*2;
    var phi=Math.acos(2*Math.random()-1);
    var r=2+Math.random()*2.5;
    nPos[i*3]=r*Math.sin(phi)*Math.cos(theta);
    nPos[i*3+1]=r*Math.sin(phi)*Math.sin(theta);
    nPos[i*3+2]=r*Math.cos(phi);
    nVel[i*3]=(Math.random()-0.5)*0.003;
    nVel[i*3+1]=(Math.random()-0.5)*0.003;
    nVel[i*3+2]=(Math.random()-0.5)*0.003;
    var c=new THREE.Color(brainColors[i%brainColors.length]);
    nCol[i*3]=c.r;nCol[i*3+1]=c.g;nCol[i*3+2]=c.b;
  }
  var nGeo=new THREE.BufferGeometry();
  nGeo.setAttribute('position',new THREE.BufferAttribute(nPos,3));
  nGeo.setAttribute('color',new THREE.BufferAttribute(nCol,3));
  var nMat=new THREE.PointsMaterial({size:0.04,vertexColors:true,transparent:true,opacity:0.7,sizeAttenuation:true,depthWrite:false});
  var nPoints=new THREE.Points(nGeo,nMat);
  scene2.add(nPoints);

  /* Connection lines */
  var MAX_LINES=300;
  var lPos=new Float32Array(MAX_LINES*6);
  var lCol=new Float32Array(MAX_LINES*6);
  var lGeo=new THREE.BufferGeometry();
  lGeo.setAttribute('position',new THREE.BufferAttribute(lPos,3));
  lGeo.setAttribute('color',new THREE.BufferAttribute(lCol,3));
  var lMat=new THREE.LineBasicMaterial({vertexColors:true,transparent:true,opacity:0.12,depthWrite:false,blending:THREE.AdditiveBlending});
  var lLines=new THREE.LineSegments(lGeo,lMat);
  scene2.add(lLines);

  /* ---- SCENE 3: Cortical Surface (Brain section) ---- */
  var scene3=new THREE.Scene();
  var cortGeo=new THREE.IcosahedronGeometry(2,5);
  var cp=cortGeo.attributes.position;
  for(var i=0;i<cp.count;i++){
    var x=cp.getX(i),y=cp.getY(i),z=cp.getZ(i);
    var gy=Math.abs(y);
    var fold=(Math.sin(x*8+y*3)*0.06+Math.cos(z*6+x*4)*0.05)*(1+gy*0.3);
    var sulcus=Math.sin(y*12+x*5)*0.02;
    var sc=1+fold+sulcus;
    cp.setXYZ(i,x*sc,y*sc,z*sc);
  }
  cortGeo.computeVertexNormals();

  var cortMat=new THREE.MeshPhongMaterial({
    color:hex(COLORS.teal),emissive:hex(COLORS.indigo),emissiveIntensity:0.1,
    transparent:true,opacity:0.12,side:THREE.DoubleSide,depthWrite:false
  });
  var cortMesh=new THREE.Mesh(cortGeo,cortMat);
  scene3.add(cortMesh);

  var cortWireGeo=new THREE.IcosahedronGeometry(2.02,5);
  var cwp=cortWireGeo.attributes.position;
  for(var i=0;i<cwp.count;i++){
    var x=cwp.getX(i),y=cwp.getY(i),z=cwp.getZ(i);
    var gy=Math.abs(y);
    var fold=(Math.sin(x*8+y*3)*0.06+Math.cos(z*6+x*4)*0.05)*(1+gy*0.3);
    var sulcus=Math.sin(y*12+x*5)*0.02;
    var sc=1+fold+sulcus;
    cwp.setXYZ(i,x*sc,y*sc,z*sc);
  }
  var cortWireMat=new THREE.MeshBasicMaterial({color:hex(COLORS.teal),transparent:true,opacity:0.08,wireframe:true,depthWrite:false});
  cortMesh.add(new THREE.Mesh(cortWireGeo,cortWireMat));

  scene3.add(new THREE.AmbientLight(0xffffff,0.25));
  var pl3=new THREE.PointLight(hex(COLORS.teal),0.5,10);
  pl3.position.set(3,2,4);scene3.add(pl3);

  /* ---- SCENE 4: Neural Waves (Appendix) ---- */
  var scene4=new THREE.Scene();
  var waveGroup=new THREE.Group();
  scene4.add(waveGroup);

  var NWAVES=8;
  var waveCurves=[];
  for(var w=0;w<NWAVES;w++){
    var pts=[];
    for(var j=0;j<80;j++){
      pts.push(new THREE.Vector3((j/79)*12-6,0,0));
    }
    var wGeo=new THREE.BufferGeometry().setFromPoints(pts);
    var wMat=new THREE.LineBasicMaterial({
      color:w%2===0?hex(COLORS.blue):hex(COLORS.purple),
      transparent:true,opacity:0.06+w*0.005,depthWrite:false
    });
    var wLine=new THREE.Line(wGeo,wMat);
    wLine.position.z=(w-NWAVES/2)*0.4;
    waveGroup.add(wLine);
    waveCurves.push({line:wLine,geo:wGeo,offset:w*0.7});
  }

  /* Flow particles */
  var NFLOW=80;
  var fPos=new Float32Array(NFLOW*3);
  var fCol=new Float32Array(NFLOW*3);
  var flowColors=[hex(COLORS.gold),hex(COLORS.blue),hex(COLORS.purple)];
  for(var i=0;i<NFLOW;i++){
    fPos[i*3]=(Math.random()-0.5)*12;
    fPos[i*3+1]=(Math.random()-0.5)*4;
    fPos[i*3+2]=(Math.random()-0.5)*4;
    var fc=new THREE.Color(flowColors[i%flowColors.length]);
    fCol[i*3]=fc.r;fCol[i*3+1]=fc.g;fCol[i*3+2]=fc.b;
  }
  var fGeo=new THREE.BufferGeometry();
  fGeo.setAttribute('position',new THREE.BufferAttribute(fPos,3));
  fGeo.setAttribute('color',new THREE.BufferAttribute(fCol,3));
  var fMat=new THREE.PointsMaterial({size:0.03,vertexColors:true,transparent:true,opacity:0.5,sizeAttenuation:true,depthWrite:false});
  waveGroup.add(new THREE.Points(fGeo,fMat));

  /* ---- SCENES ARRAY ---- */
  var scenes=[
    {scene:scene1,camera:camera,init:function(){camera.position.set(0,0,5);camera.lookAt(0,0,0);}},
    {scene:scene2,camera:camera,init:function(){camera.position.set(0,0,6);camera.lookAt(0,0,0);}},
    {scene:scene3,camera:camera,init:function(){camera.position.set(0,0,5.5);camera.lookAt(0,0,0);}},
    {scene:scene4,camera:camera,init:function(){camera.position.set(0,0,5);camera.lookAt(0,0,0);}}
  ];
  var currentScene=0;

  /* ---- SCROLL-DRIVEN SCENE SWITCHING ---- */
  var sections=['cover','explorer','brain','appendix'];
  var secEls=[];
  sections.forEach(function(id){var el=document.getElementById(id);if(el)secEls.push(el);});

  function updateScene(){
    var sy=window.scrollY+H*0.5;
    var newScene=0;
    for(var i=secEls.length-1;i>=0;i--){
      if(sy>=secEls[i].offsetTop){newScene=i;break;}
    }
    if(newScene!==currentScene){
      currentScene=newScene;
      scenes[currentScene].init();
    }
  }

  /* Fade canvas in */
  setTimeout(function(){canvas.style.opacity='1';},100);

  /* ---- ANIMATION LOOP ---- */
  var clock=new THREE.Clock();
  var lineUpdateCounter=0;

  function animate(){
    requestAnimationFrame(animate);
    var t=clock.getElapsedTime();

    /* Scene 1: Rotate brain */
    brainMesh.rotation.y=t*0.08;
    brainMesh.rotation.x=Math.sin(t*0.05)*0.15;
    foldMesh.rotation.y=t*0.06;
    foldMesh.rotation.x=Math.sin(t*0.04)*0.1;
    glowMesh.scale.setScalar(1+Math.sin(t*0.3)*0.03);

    /* Scene 2: Move particles + update connections */
    var nPA=nGeo.attributes.position;
    for(var i=0;i<NPARTICLES;i++){
      nPA.array[i*3]+=nVel[i*3];
      nPA.array[i*3+1]+=nVel[i*3+1];
      nPA.array[i*3+2]+=nVel[i*3+2];
      for(var j=0;j<3;j++){
        if(Math.abs(nPA.array[i*3+j])>4.5)nVel[i*3+j]*=-1;
      }
    }
    nGeo.attributes.position.needsUpdate=true;
    nPoints.rotation.y=t*0.02;

    /* Update connections periodically */
    lineUpdateCounter++;
    if(lineUpdateCounter%3===0){
      var li=0;
      var pArr=nGeo.attributes.position.array;
      var cArr=nGeo.attributes.color.array;
      for(var i=0;i<NPARTICLES&&li<MAX_LINES;i++){
        for(var j=i+1;j<NPARTICLES&&li<MAX_LINES;j++){
          var dx=pArr[i*3]-pArr[j*3];
          var dy=pArr[i*3+1]-pArr[j*3+1];
          var dz=pArr[i*3+2]-pArr[j*3+2];
          var d2=dx*dx+dy*dy+dz*dz;
          if(d2<2.5){
            var alpha=1-d2/2.5;
            lPos[li*6]=pArr[i*3];lPos[li*6+1]=pArr[i*3+1];lPos[li*6+2]=pArr[i*3+2];
            lPos[li*6+3]=pArr[j*3];lPos[li*6+4]=pArr[j*3+1];lPos[li*6+5]=pArr[j*3+2];
            lCol[li*6]=cArr[i*3]*alpha;lCol[li*6+1]=cArr[i*3+1]*alpha;lCol[li*6+2]=cArr[i*3+2]*alpha;
            lCol[li*6+3]=cArr[j*3]*alpha;lCol[li*6+4]=cArr[j*3+1]*alpha;lCol[li*6+5]=cArr[j*3+2]*alpha;
            li++;
          }
        }
      }
      for(var k=li*6;k<MAX_LINES*6;k++)lPos[k]=0;
      lGeo.attributes.position.needsUpdate=true;
      lGeo.attributes.color.needsUpdate=true;
      lGeo.setDrawRange(0,li*2);
    }

    /* Scene 3: Rotate cortical surface */
    cortMesh.rotation.y=t*0.05;
    cortMesh.rotation.z=Math.sin(t*0.03)*0.08;

    /* Scene 4: Animate waves */
    waveCurves.forEach(function(w){
      var pts=w.line.geometry.attributes.position;
      for(var j=0;j<pts.count;j++){
        var x=(j/(pts.count-1))*12-6;
        var y=Math.sin(x*0.8+t*0.6+w.offset)*0.3*Math.sin(x*0.3+t*0.2)*0.5;
        y+=Math.sin(x*1.5+t*0.8+w.offset*1.3)*0.15;
        pts.setY(j,y);
      }
      pts.needsUpdate=true;
    });
    waveGroup.rotation.y=t*0.03;

    /* Move flow particles */
    var fPA=fGeo.attributes.position;
    for(var i=0;i<NFLOW;i++){
      fPA.array[i*3]+=0.005;
      if(fPA.array[i*3]>6)fPA.array[i*3]=-6;
      fPA.array[i*3+1]+=Math.sin(t+i)*0.001;
    }
    fGeo.attributes.position.needsUpdate=true;

    /* Render current scene */
    updateScene();
    renderer.render(scenes[currentScene].scene,scenes[currentScene].camera);
  }

  /* ---- RESIZE ---- */
  window.addEventListener('resize',function(){
    W=window.innerWidth;H=window.innerHeight;
    camera.aspect=W/H;
    camera.updateProjectionMatrix();
    renderer.setSize(W,H);
  });

  animate();
}

/* Wait for Three.js to load */
if(typeof THREE!=='undefined'){init();}
else{
  var check=setInterval(function(){
    if(typeof THREE!=='undefined'){clearInterval(check);init();}
  },100);
}

})();
