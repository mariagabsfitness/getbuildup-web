/* BuildUp — interacciones del sitio. Generado desde el mockup, no editar a mano. */
(function(){
  var app = document;
/* ============================ INTERACTIONS ============================ */
function wire(){
  /* membership plan selector */
  app.querySelectorAll("[data-plan]").forEach(el=>{
    const pick = ()=>{
      el.parentElement.querySelectorAll("[data-plan]").forEach(x=>x.classList.remove("sel"));
      el.classList.add("sel");
      const after = app.querySelector("[data-after]");
      if(after && el.dataset.price) after.textContent = el.dataset.price;
    };
    el.addEventListener("click", pick);
    el.addEventListener("keydown", e=>{ if(e.key==="Enter"||e.key===" "){e.preventDefault();pick();} });
  });

  /* before / after comparator */
  app.querySelectorAll("[data-compare]").forEach(box=>{
    const before = box.querySelector(".before");
    const handle = box.querySelector(".handle");
    const set = pct=>{
      pct = Math.max(0, Math.min(100, pct));
      before.style.clipPath = `inset(0 ${100-pct}% 0 0)`;
      handle.style.left = pct + "%";
      box.setAttribute("aria-valuenow", Math.round(pct));
    };
    const fromEvent = e=>{
      const r = box.getBoundingClientRect();
      const x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      set(x / r.width * 100);
    };
    let dragging = false;
    box.addEventListener("pointerdown", e=>{ dragging = true; box.setPointerCapture(e.pointerId); fromEvent(e); });
    box.addEventListener("pointermove", e=>{ if(dragging) fromEvent(e); });
    box.addEventListener("pointerup", ()=>{ dragging = false; });
    box.addEventListener("pointercancel", ()=>{ dragging = false; });
    box.addEventListener("keydown", e=>{
      const cur = parseFloat(box.getAttribute("aria-valuenow"));
      if(e.key === "ArrowLeft"){ e.preventDefault(); set(cur - 4); }
      if(e.key === "ArrowRight"){ e.preventDefault(); set(cur + 4); }
    });
    set(50);
  });

  /* video tiles — placeholder playback */
  app.querySelectorAll("[data-video]").forEach(v=>{
    const bar = v.querySelector(".bar i");
    let t = null, p = 0;
    v.addEventListener("click", ()=>{
      if(t){ clearInterval(t); t = null; v.classList.remove("playing"); bar.style.width = "0%"; p = 0; return; }
      v.classList.add("playing");
      t = setInterval(()=>{
        p += 1.6;
        bar.style.width = Math.min(p,100) + "%";
        if(p >= 100){ clearInterval(t); t = null; v.classList.remove("playing"); bar.style.width = "0%"; p = 0; }
      }, 60);
    });
  });
}
  wire();
  var b = document.getElementById("burger"), n = document.getElementById("nav");
  if (b && n) b.addEventListener("click", function(){ n.classList.toggle("open"); });
})();
