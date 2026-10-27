# -*- coding: utf-8 -*-
"""Saca de _mockup.html el CSS y el JS de interacciones hacia assets/."""
import re, os, io
src = io.open("_mockup.html", encoding="utf-8").read()
os.makedirs("assets", exist_ok=True)

css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
io.open("assets/styles.css", "w", encoding="utf-8").write(css.strip() + "\n")

js = re.search(r"<script>(.*?)</script>", src, re.S).group(1)
i = js.index("/* ============================ INTERACTIONS ============================ */")
j = js.index("document.getElementById(\"burger\")")
wire = js[i:j].strip()

runtime = """/* BuildUp — interacciones del sitio. Generado desde el mockup, no editar a mano. */
(function(){
  var app = document;
""" + wire + """
  wire();
  var b = document.getElementById("burger"), n = document.getElementById("nav");
  if (b && n) b.addEventListener("click", function(){ n.classList.toggle("open"); });
})();
"""
io.open("assets/app.js", "w", encoding="utf-8").write(runtime)
print("styles.css:", len(css), "bytes | app.js:", len(runtime), "bytes")
