// Interacción de la consola: información de conceptos y de cajas de diagrama (modal con enlaces), diagramas Mermaid
// (tema, animación), filtro del glosario, tema de color, cronómetro y «Ponme a prueba» (pregunta del apartado visible). Sin dependencias y compatible con la CSP (script-src 'self').
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
      if (clicPrueba(t)) return;
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
      if (ev.target && ev.target.id === "modal-pregunta" && prueba) {
        var b = prueba.boton;
        prueba = null;
        if (b && document.contains(b)) b.focus();
      }
    }, true);
    document.addEventListener("submit", function (ev) {
      if (ev.target && ev.target.id === "mp-form") { ev.preventDefault(); if (prueba && prueba.pregunta) responderPrueba(ev.target); }
    });
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


  // ------------------------------------------------------------------ «Ponme a prueba»: pregunta del apartado visible
  var vistas = {};          // módulo -> ids ya mostrados mientras dura la visita (no se guarda nada en el servidor)
  var prueba = null;        // { modulo, url, boton, pregunta }

  function el(etiqueta, clase, texto) {
    var e = document.createElement(etiqueta);
    if (clase) e.className = clase;
    if (texto !== undefined && texto !== null) e.textContent = texto;
    return e;
  }

  function tokenCsrf() {
    try { return JSON.parse(document.body.getAttribute("hx-headers") || "{}")["X-CSRF-Token"] || ""; }
    catch (e) { return ""; }
  }

  // Encabezado más cercano por encima del centro de la ventana y sus padres (de más concreto a más general)
  function anclasVisibles() {
    var art = $("article.md");
    if (!art) return [];
    var hs = $$("h1[id], h2[id], h3[id], h4[id]", art), centro = window.innerHeight / 2, k = -1;
    hs.forEach(function (h, i) { if (h.getBoundingClientRect().top <= centro) k = i; });
    if (k < 0) return [];
    var cadena = [hs[k].id], nivel = parseInt(hs[k].tagName.charAt(1), 10);
    for (var i = k - 1; i >= 0 && nivel > 1; i--) {
      var n = parseInt(hs[i].tagName.charAt(1), 10);
      if (n < nivel) { cadena.push(hs[i].id); nivel = n; }
    }
    return cadena;
  }

  function cuerpoPrueba() { return $("#mp-cuerpo"); }

  function avisoPrueba(texto) {
    var c = cuerpoPrueba();
    c.textContent = "";
    c.appendChild(el("p", "msg error", texto));
    var pie = el("div", "mp-pie");
    var b = el("button", "", "Reintentar"); b.type = "button"; b.setAttribute("data-mp-otra", "");
    pie.appendChild(b);
    c.appendChild(pie);
  }

  function pedirPregunta() {
    if (!prueba) return;
    var c = cuerpoPrueba();
    c.textContent = "";
    c.appendChild(el("p", "suave", "Buscando una pregunta…"));
    var vistasMod = vistas[prueba.modulo] || (vistas[prueba.modulo] = []);
    var q = new URLSearchParams({ modulo: prueba.modulo, anclas: anclasVisibles().join(","), excluir: vistasMod.join(",") });
    fetch(prueba.url + "/pregunta?" + q.toString(), { credentials: "same-origin", headers: { Accept: "application/json" } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (p) {
        if (p.reiniciado) vistasMod.length = 0;
        vistasMod.push(p.id);
        pintarPregunta(p);
      })
      .catch(function () { avisoPrueba("No se ha podido cargar una pregunta. Comprueba la conexión o vuelve a entrar."); });
  }

  function seleccion(nombre, id, opciones) {
    var s = el("select"); s.name = nombre; s.id = id; s.required = true;
    var vacia = el("option", "", "—"); vacia.value = ""; s.appendChild(vacia);
    opciones.forEach(function (o) { var op = el("option", "", o.texto); op.value = o.id; s.appendChild(op); });
    return s;
  }

  function pintarPregunta(p) {
    prueba.pregunta = p;
    var titulo = p.ancla && document.getElementById(p.ancla);
    $("#mp-origen").textContent = titulo ? "Apartado: " + titulo.textContent.trim() : "Pregunta del módulo";
    $("#mp-titulo").textContent = p.banco === "repaso" ? "Repaso de conocimientos" : "Pregunta de examen";
    var c = cuerpoPrueba();
    c.textContent = "";
    if (p.reiniciado) c.appendChild(el("p", "msg", "Ya has visto todas las preguntas de este módulo: empiezan de nuevo."));
    c.appendChild(el("p", "suave", p.id + " · " + (p.tarea === "CP" ? "Conocimientos previos" : "Tarea " + p.tarea)));
    c.appendChild(el("p", "mp-enunciado", p.enunciado));
    var f = el("form"); f.id = "mp-form"; f.noValidate = false;
    var opciones = p.opciones || [];
    if (p.tipo === "multiple_choice" || p.tipo === "multiple_response") {
      if (p.tipo === "multiple_response") f.appendChild(el("p", "suave", "Selecciona todas las respuestas correctas."));
      opciones.forEach(function (o) {
        var l = el("label", "opcion"), i = el("input");
        i.type = p.tipo === "multiple_choice" ? "radio" : "checkbox"; i.name = "r"; i.value = o.id;
        if (p.tipo === "multiple_choice") i.required = true;
        l.appendChild(i); l.appendChild(el("span", "", o.texto));
        f.appendChild(l);
      });
    } else if (p.tipo === "ordering") {
      f.appendChild(el("p", "suave", "Elige qué elemento va en cada posición, de primero a último."));
      for (var k = 1; k <= p.posiciones; k++) {
        var l = el("label", "", "Posición " + k); l.htmlFor = "mp-o" + k;
        f.appendChild(l); f.appendChild(seleccion("o" + k, "mp-o" + k, opciones));
      }
    } else {
      f.appendChild(el("p", "suave", "Empareja cada elemento con una opción."));
      (p.prompts || []).forEach(function (x) {
        var l = el("label", "", x.id + ". " + x.texto); l.htmlFor = "mp-m" + x.id;
        f.appendChild(l); f.appendChild(seleccion("m_" + x.id, "mp-m" + x.id, opciones));
      });
    }
    var err = el("p", "msg error"); err.id = "mp-error"; err.hidden = true;
    f.appendChild(err);
    var pie = el("div", "mp-pie");
    var b = el("button", "", "Responder"); b.type = "submit";
    var saltar = el("button", "sec", "Otra pregunta"); saltar.type = "button"; saltar.setAttribute("data-mp-otra", "");
    pie.appendChild(b); pie.appendChild(saltar);
    f.appendChild(pie);
    c.appendChild(f);
    $("#mp-titulo").focus();
  }

  function lista(lineas) {
    var ul = el("ul", "solucion");
    (lineas || []).forEach(function (t) { ul.appendChild(el("li", "", t)); });
    return ul;
  }

  function enlaceSeguro(url) {
    return typeof url === "string" && (url.indexOf("https://") === 0 || (url.charAt(0) === "/" && url.charAt(1) !== "/"));
  }

  function responderPrueba(form) {
    var datos = new FormData(form);
    datos.append("pid", prueba.pregunta.id);
    datos.append("modulo", prueba.modulo);
    var boton = form.querySelector("button[type=submit]");
    if (boton) boton.disabled = true;
    fetch(prueba.url + "/corregir", { method: "POST", body: datos, credentials: "same-origin",
                                      headers: { "X-CSRF-Token": tokenCsrf(), Accept: "application/json" } })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }, function () { return { ok: false, j: {} }; }); })
      .then(function (res) {
        if (!res.ok) {
          var e = $("#mp-error");
          e.textContent = res.j.error || "No se ha podido corregir. Recarga la página y vuelve a intentarlo.";
          e.hidden = false;
          if (boton) boton.disabled = false;
          return;
        }
        pintarCorreccion(form, res.j);
      })
      .catch(function () { avisoPrueba("No se ha podido corregir la respuesta. Comprueba la conexión."); });
  }

  function pintarCorreccion(form, r) {
    $$("input, select", form).forEach(function (x) { x.disabled = true; });
    var pie = form.querySelector(".mp-pie");
    if (pie) pie.remove();
    var c = cuerpoPrueba();
    var msg = el("div", "msg " + (r.correcta ? "ok" : "error"));
    msg.appendChild(el("strong", "", r.correcta ? "Correcto." : "Incorrecto."));
    if (!r.correcta) {
      msg.appendChild(el("p", "", "Solución:")); msg.appendChild(lista(r.solucion));
      msg.appendChild(el("p", "", "Tu respuesta:")); msg.appendChild(lista(r.respuesta));
    }
    c.appendChild(msg);
    var det = el("details", "explicacion");
    if (!r.correcta) det.open = true;
    det.appendChild(el("summary", "", "Ver explicación"));
    det.appendChild(el("p", "", r.explicacion));
    var ds = Object.keys(r.distractores || {});
    if (ds.length) {
      det.appendChild(el("p", "", "Por qué no son correctas las demás opciones:"));
      var ul = el("ul");
      ds.forEach(function (k) { var li = el("li"); li.appendChild(el("strong", "", k + ")")); li.appendChild(document.createTextNode(" " + r.distractores[k])); ul.appendChild(li); });
      det.appendChild(ul);
    }
    if (enlaceSeguro(r.referencia)) {
      var ref = el("p", "suave", "Referencia oficial: "), a = el("a", "", r.referencia);
      a.href = r.referencia; a.target = "_blank"; a.rel = "noopener noreferrer";
      ref.appendChild(a); det.appendChild(ref);
    }
    c.appendChild(det);
    var nuevo = el("div", "mp-pie");
    var otra = el("button", "", "Otra pregunta"); otra.type = "button"; otra.setAttribute("data-mp-otra", "");
    nuevo.appendChild(otra);
    if (enlaceSeguro(r.teoria) && r.teoria.charAt(0) === "/") {
      var t = el("a", "btn sec mc-enlace-interno", "Repasar en la teoría"); t.href = r.teoria; t.setAttribute("data-mp-teoria", "");
      nuevo.appendChild(t);
    }
    var cerrarB = el("button", "sec", "Cerrar"); cerrarB.type = "button"; cerrarB.setAttribute("data-mp-cerrar", "");
    nuevo.appendChild(cerrarB);
    c.appendChild(nuevo);
    otra.focus();
  }

  function abrirPrueba(boton) {
    var dlg = $("#modal-pregunta");
    if (!dlg || typeof dlg.showModal !== "function") return;
    prueba = { modulo: boton.getAttribute("data-modulo"), url: boton.getAttribute("data-url"), boton: boton, pregunta: null };
    if (!dlg.open) dlg.showModal();
    pedirPregunta();
  }

  function cerrarPrueba() {
    var dlg = $("#modal-pregunta");
    if (dlg && dlg.open) dlg.close();
  }

  // Devuelve true si el clic era del modal de preguntas
  function clicPrueba(t) {
    var b = t.closest("[data-ponme-a-prueba]");
    if (b) { abrirPrueba(b); return true; }
    var dlg = $("#modal-pregunta");
    if (!dlg || !dlg.contains(t)) return false;
    if (t === dlg || t.closest("[data-mp-cerrar]") || t.closest("[data-mp-teoria]")) { cerrarPrueba(); return !t.closest("[data-mp-teoria]"); }
    if (t.closest("[data-mp-otra]")) { pedirPregunta(); return true; }
    return true;
  }

  function iniciar() { registrarEventos(); leerDatos(); diagramas(); cronometro(); pintarEtiquetaTema(); }
  document.addEventListener("DOMContentLoaded", iniciar);
  document.addEventListener("htmx:load", iniciar);
})();
