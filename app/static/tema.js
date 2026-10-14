// Aplica el tema de color antes de pintar la página (evita parpadeos). Valores: claro (por defecto), oscuro, auto (sigue al sistema).
(function () {
  var t = "claro";
  try { t = localStorage.getItem("tema") || "claro"; } catch (e) { /* almacenamiento no disponible */ }
  if (["claro", "oscuro", "auto"].indexOf(t) === -1) t = "claro";
  document.documentElement.setAttribute("data-tema", t);
})();
