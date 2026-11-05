/* Landing de lista de espera de BuildUp — vídeo de fondo y estado de enviado */
(function () {
  var base = "https://getbuildup.app/assets/img/";
  var movil = window.matchMedia("(max-width: 767px)").matches;

  var v = document.getElementById("fondo");
  if (v) {
    v.poster = base + (movil ? "hero-home-movil.jpg" : "hero-home.jpg");
    v.src = base + (movil ? "hero-home-movil.mp4" : "hero-home.mp4");
    var intento = v.play();
    if (intento && intento.catch) intento.catch(function () {});
  }

  try {
    var p = new URLSearchParams(location.search);
    if (p.get("customer_posted") === "true") {
      document.body.classList.add("enviado");
      var g = document.querySelector(".gracias");
      if (g) g.scrollIntoView({ block: "center" });
    }
  } catch (e) {}
})();
