// Interacción de la consola: información de conceptos y de cajas de diagrama (modal con enlaces), diagramas Mermaid
// (tema, animación), filtro del glosario, tema de color y cronómetro. Sin dependencias y compatible con la CSP (script-src 'self').
(function () {
  "use strict";

  var CATEGORIAS = { servicio: "Servicio", concepto: "Concepto", tecnica: "Técnica", metrica: "Métrica" };
  var datos = { conceptos: {}, diagramas: {} };   // datos incrustados en la página
  var origen = null;                              // elemento que abrió el modal, para devolverle el foco
  var reducido = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function $(sel, raiz) { return (raiz || document).querySelector(sel); }
  function $$(sel, raiz) { return Array.prototype.slice.call((raiz || document).querySelectorAll(sel)); }

  // ------------------------------------------------------------------ datos de la página
  function leerDatos() {
    datos = { conceptos: {}, diagramas: {} };
    var el = $("#datos-glosario");
    if (!el) return;
    try {
      var d = JSON.parse(el.textContent);
      datos.conceptos = d.conceptos || {};
      datos.diagramas = d.diagramas || {};
    } catch (e) { /* datos dañados: la página sigue siendo legible, sin modal */ }
  }

  // ------------------------------------------------------------------ modal de información
  function fila(dl, titulo, texto) {
    var dt = document.createElement("dt"), dd = document.createElement("dd");
    dt.textContent = titulo; dd.textContent = texto;
    dl.appendChild(dt); dl.appendChild(dd);
  }

  function pintarEnlaces(enlaces) {
    var ul = $("#mc-enlaces"), caja = $("#mc-enlaces-caja");
    ul.textContent = "";
    var validos = (enlaces || []).filter(function (e) {
      return e && typeof e.url === "string" && (e.url.indexOf("https://") === 0 || (e.url.charAt(0) === "/" && e.url.charAt(1) !== "/"));
    });
    caja.hidden = validos.length === 0;
    validos.forEach(function (e) {
      var li = document.createElement("li"), a = document.createElement("a");
      a.textContent = e.texto || e.url;
      a.setAttribute("href", e.url);
      if (e.url.indexOf("https://") === 0) {      // externo: pestaña nueva, sin acceso a la ventana de origen
        a.setAttribute("target", "_blank");
        a.setAttribute("rel", "noopener noreferrer");
        a.textContent += " ↗";
      } else {                                    // interno: se cierra el modal y se navega en la misma pestaña
        a.className = "mc-enlace-interno";
      }
      li.appendChild(a);
      ul.appendChild(li);
    });
  }

  function mostrar(info, desde) {
    var dlg = $("#modal-concepto");
    if (!info || !dlg || typeof dlg.showModal !== "function") return;
    origen = desde || null;
    $("#mc-titulo").textContent = info.titulo || "";
    var cat = $("#mc-cat");
    cat.hidden = !info.categoria;
    cat.textContent = CATEGORIAS[info.categoria] || info.categoria || "";
    cat.className = "mc-cat cat cat-" + (info.categoria || "");
    var def = $("#mc-def");
    def.textContent = info.texto || "";
    def.hidden = !info.texto;
    var extra = $("#mc-extra");
    extra.textContent = "";
    if (info.usar_cuando) fila(extra, "Cuándo usarlo", info.usar_cuando);
    if (info.no_usar_cuando) fila(extra, "Cuándo no usarlo", info.no_usar_cuando);
    pintarEnlaces(info.enlaces);
    if (!dlg.open) dlg.showModal();
    $("#mc-titulo").focus();
  }

  function cerrar() {
    var dlg = $("#modal-concepto");
    if (dlg && dlg.open) dlg.close();
  }

  function alCerrarModal() {
    if (origen && document.contains(origen) && typeof origen.focus === "function") origen.focus();
    origen = null;
  }

  function infoDeCaja(el) {                       // el = elemento con data-caja="<diagrama>|<id>"
    var partes = (el.getAttribute("data-caja") || "").split("|");
    var d = datos.diagramas[partes[0]];
    return d ? d[partes[1]] : null;
  }

  // Eventos globales: se registran una sola vez (la navegación con hx-boost sustituye el cuerpo, no el documento)
  function registrarEventos() {
    if (window.__eventosConsola) return;
    window.__eventosConsola = true;
    document.addEventListener("click", function (ev) {
      var t = ev.target;
      if (!t.closest) return;
      if (t.closest("[data-alternar-tema]")) { alternarTema(); return; }
      var c = t.closest("[data-concepto]");
      if (c) { ev.preventDefault(); mostrar(datos.conceptos[c.getAttribute("data-concepto")], c); return; }
      var caja = t.closest("[data-caja]");           // la caja más interna que se haya pulsado
      if (caja) { ev.preventDefault(); mostrar(infoDeCaja(caja), caja); return; }
      var dlg = $("#modal-concepto");
      if (dlg && t === dlg) cerrar();                // clic en el fondo
      else if (t.closest(".mc-cerrar") || t.closest(".mc-enlace-interno")) cerrar();
    });
    document.addEventListener("keydown", function (ev) {
      var caja = ev.target.closest && ev.target.closest("[data-caja]");
      if (caja && (ev.key === "Enter" || ev.key === " ")) { ev.preventDefault(); mostrar(infoDeCaja(caja), caja); }
    });
    document.addEventListener("input", function (ev) {
      if (ev.target.matches && ev.target.matches("[data-filtro-glosario]")) filtrarGlosario(ev.target.value);
    });
    document.addEventListener("close", function (ev) {
      if (ev.target && ev.target.id === "modal-concepto") alCerrarModal();
    }, true);
  }

  function filtrarGlosario(texto) {
    var q = texto.trim().toLowerCase(), visibles = 0;
    $$("#lista-glosario li").forEach(function (li) {
      var ok = !q || (li.getAttribute("data-buscar") || "").indexOf(q) !== -1;
      li.hidden = !ok;
      if (ok) visibles++;
    });
    var vacio = $("#sin-resultados");
    if (vacio) vacio.hidden = visibles !== 0;
  }

  // ------------------------------------------------------------------ diagramas
  function tema() {
    var cs = getComputedStyle(document.documentElement);
    var v = function (n) { return cs.getPropertyValue(n).trim() || undefined; };
    return {
      fontFamily: v("--fuente-diagrama"), fontSize: "16px", background: "transparent",
      primaryColor: v("--dg-nodo"), primaryTextColor: v("--texto"), primaryBorderColor: v("--dg-borde"),
      secondaryColor: v("--dg-nodo"), tertiaryColor: v("--dg-nodo"), lineColor: v("--dg-linea"),
      mainBkg: v("--dg-nodo"), nodeBorder: v("--dg-borde"), clusterBkg: v("--dg-grupo"), clusterBorder: v("--dg-borde"),
      edgeLabelBackground: v("--dg-grupo"), titleColor: v("--texto"), textColor: v("--texto")
    };
  }

  // Hace pulsable una caja (nodo o subgrupo) si el autor ha definido su información
  function hacerPulsable(g, indice, id) {
    var info = (datos.diagramas[indice] || {})[id];
    if (!info) return;
    g.classList.add("caja-info");
    g.setAttribute("data-caja", indice + "|" + id);
    g.setAttribute("role", "button");
    g.setAttribute("tabindex", "0");
    g.setAttribute("aria-label", "Ver información de " + (info.titulo || id));
  }

  function prepararDiagrama(fig) {
    var indice = fig.getAttribute("data-diagrama");
    $$("g.node", fig).forEach(function (n, i) {
      n.style.setProperty("--i", String(i));
      var m = /^flowchart-(.+)-\d+$/.exec(n.id || "");
      if (m) hacerPulsable(n, indice, m[1]);
    });
    $$("g.cluster", fig).forEach(function (c) { if (c.id) hacerPulsable(c, indice, c.id); });
    if (reducido) { fig.classList.add("visible"); return; }
    fig.classList.add("anim-lista");
    if (!("IntersectionObserver" in window)) { fig.classList.add("visible"); return; }
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) { if (e.isIntersecting) { fig.classList.add("visible"); obs.disconnect(); } });
    }, { threshold: 0.2 });
    obs.observe(fig);
  }

  function diagramas() {
    var pendientes = $$("figure.diagrama pre.mermaid:not([data-processed])");
    if (!window.mermaid || !pendientes.length) return;
    window.mermaid.initialize({
      startOnLoad: false, securityLevel: "strict", theme: "base", themeVariables: tema(),
      flowchart: { curve: "basis", htmlLabels: true, padding: 16, nodeSpacing: 40, rankSpacing: 48, useMaxWidth: true }
    });
    var ps = window.mermaid.run({ nodes: pendientes });
    (ps && ps.then ? ps : Promise.resolve()).then(function () {
      $$("figure.diagrama").forEach(function (f) { if (!f.hasAttribute("data-lista")) { f.setAttribute("data-lista", ""); prepararDiagrama(f); } });
    }).catch(function () { /* un diagrama inválido no debe romper la página: se deja el código visible */ });
  }

  // ------------------------------------------------------------------ tema de color
  var ETIQUETAS = { claro: "Claro", oscuro: "Oscuro", auto: "Sistema" };
  function temaActual() { return document.documentElement.getAttribute("data-tema") || "claro"; }
  function pintarEtiquetaTema() {
    $$("[data-tema-etiqueta]").forEach(function (el) { el.textContent = ETIQUETAS[temaActual()]; });
  }
  function alternarTema() {
    var orden = ["claro", "oscuro", "auto"], siguiente = orden[(orden.indexOf(temaActual()) + 1) % orden.length];
    try { localStorage.setItem("tema", siguiente); } catch (e) { /* sin almacenamiento: vale solo para esta página */ }
    document.documentElement.setAttribute("data-tema", siguiente);
    pintarEtiquetaTema();
    // los diagramas ya dibujados llevan sus colores incrustados: se vuelve a cargar para repintarlos con el tema nuevo
    if ($("figure.diagrama")) window.location.reload();
  }

  // ------------------------------------------------------------------ cronómetro del simulacro
  var reloj = null;
  function cronometro() {
    if (reloj) { clearInterval(reloj); reloj = null; }
    var el = document.getElementById("cronometro");
    if (!el) return;
    var restante = parseInt(el.dataset.segundos, 10);
    function pintar() {
      var m = Math.floor(restante / 60), s = restante % 60;
      el.textContent = m + ":" + (s < 10 ? "0" : "") + s;
      if (restante <= 0) { clearInterval(reloj); window.location.href = el.dataset.fin; }
      restante -= 1;
    }
    pintar();
    reloj = setInterval(pintar, 1000);
  }

  function iniciar() { registrarEventos(); leerDatos(); diagramas(); cronometro(); pintarEtiquetaTema(); }
  document.addEventListener("DOMContentLoaded", iniciar);
  document.addEventListener("htmx:load", iniciar);
})();
