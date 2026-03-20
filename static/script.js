// ------------------ DADOS ------------------
let dados = {
  x: [-2, -1.5, 0, 1, 2.2, 3.1],
  y: [-30.5, -20.2, -3.3, 8.9, 16.8, 21.4]
};

// ------------------ REQUISIÇÃO ------------------
fetch("/ajuste", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(dados)
})
.then(res => res.json())
.then(data => iniciarCena(data));


// ------------------ FUNÇÃO PRINCIPAL ------------------
function iniciarCena(data) {

  // ---------- CENA ----------
  const scene = new THREE.Scene();

  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.z = 20;

  const renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);


  // ---------- EIXOS ----------
  const materialEixo = new THREE.LineBasicMaterial({ color: 0xffffff });

  const eixoX = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(-10, 0, 0),
    new THREE.Vector3(10, 0, 0)
  ]);

  const eixoY = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(0, -40, 0),
    new THREE.Vector3(0, 40, 0)
  ]);

  scene.add(new THREE.Line(eixoX, materialEixo));
  scene.add(new THREE.Line(eixoY, materialEixo));


  // ---------- PONTOS EXPERIMENTAIS ----------
  data.pontos.forEach(p => {
    const geo = new THREE.SphereGeometry(0.2);
    const mat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    const ponto = new THREE.Mesh(geo, mat);

    ponto.position.set(p[0], p[1], 0);
    scene.add(ponto);
  });


  // ---------- CURVA ----------
  const pontosCurva = data.curva.map(p => new THREE.Vector3(p[0], p[1], 0));

  const geoCurva = new THREE.BufferGeometry().setFromPoints(pontosCurva);
  const matCurva = new THREE.LineBasicMaterial({ color: 0x0000ff });
  const curva = new THREE.Line(geoCurva, matCurva);

  scene.add(curva);


  // ---------- PONTO ANIMADO ----------
  const geoAnim = new THREE.SphereGeometry(0.3);
  const matAnim = new THREE.MeshBasicMaterial({ color: 0xffff00 });
  const pontoAnimado = new THREE.Mesh(geoAnim, matAnim);

  scene.add(pontoAnimado);


  // ---------- COEFICIENTES ----------
  const a = data.coeficientes.a;
  const b = data.coeficientes.b;
  const c = data.coeficientes.c;

  let t = data.animacao.x_min;
  const tMax = data.animacao.x_max;


  // ---------- ANIMAÇÃO ----------
  function animate() {
    requestAnimationFrame(animate);

    t += 0.03;

    if (t > tMax) {
      t = data.animacao.x_min;
    }

    let y = a * t * t + b * t + c;

    pontoAnimado.position.set(t, y, 0);

    renderer.render(scene, camera);
  }

  animate();
}