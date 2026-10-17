// Prueba de navegador de la consola (Chrome sin interfaz): conceptos, modal, diagramas, modo oscuro, movimiento reducido, móvil y tests (repaso y explicación).
// Uso: CONSOLA_USUARIO=... CONSOLA_CLAVE=... node consola.mjs   (genera capturas en tests/e2e/capturas)
import { chromium } from "playwright-core";
import { mkdirSync } from "node:fs";
const U = process.env.CONSOLA_URL || "http://127.0.0.1:8000";
const USUARIO = process.env.CONSOLA_USUARIO, CLAVE = process.env.CONSOLA_CLAVE;
if (!USUARIO || !CLAVE) { console.error("Define CONSOLA_USUARIO y CONSOLA_CLAVE (un estudiante matriculado en aif-c01)."); process.exit(2); }
const SH = process.env.CAPTURAS || "tests/e2e/capturas";
mkdirSync(SH, { recursive: true });
const ok = (c, m) => { console.log((c ? "OK    " : "FALLO ") + m); if (!c) process.exitCode = 1; };
const browser = await chromium.launch({ executablePath: process.env.CHROME || "/usr/bin/google-chrome", headless: true, args: ["--no-sandbox"] });

async function sesion(opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1100, height: 900 }, ...opts });
  const page = await ctx.newPage();
  const errores = [];
  page.on("pageerror", e => errores.push(String(e))); page.on("response", r => { if (r.status() >= 400) errores.push(`HTTP ${r.status()} ${r.url()}`); });
  page.on("console", m => { if (m.type() === "error") errores.push(m.text()); });
  await page.goto(U + "/login");
  await page.fill("#username", USUARIO); await page.fill("#password", CLAVE);
  await Promise.all([page.waitForURL(/\/c\/aif-c01\//), page.click("button[type=submit]")]);
  return { ctx, page, errores };
}
const RUTA = U + "/c/aif-c01/modulo/01-fundamentos-ia-ml/teoria";

// ---------------------------------------------------------------- claro, escritorio
{
  const { ctx, page, errores } = await sesion();
  await page.goto(RUTA);
  await page.waitForSelector("figure.diagrama svg", { timeout: 20000 });
  await page.waitForTimeout(1500);
  const botones = await page.locator("button.concepto").count();
  ok(botones > 20, `hay ${botones} conceptos pulsables en la teoría`);
  const nodos = await page.locator(".mermaid g.node, .mermaid g.cluster").count();
  const pulsables = await page.locator(".mermaid .caja-info").count();
  ok(nodos > 5 && pulsables === nodos, `diagramas: las ${nodos} cajas son pulsables (${pulsables})`);
  const flujo = await page.evaluate(() => { const l = document.querySelector(".mermaid .flowchart-link"); return l && getComputedStyle(l).animationName; });
  ok(flujo === "flujo", `flechas animadas (animation-name=${flujo})`);

  // aspecto: en reposo el concepto es texto normal; al pasar el ratón se resalta
  const primero = page.locator("button.concepto").first();
  await primero.scrollIntoViewIfNeeded();
  const reposo = await primero.evaluate(el => { const s = getComputedStyle(el); return { fondo: s.backgroundColor, borde: s.borderBottomWidth, cursor: s.cursor }; });
  ok(reposo.fondo === "rgba(0, 0, 0, 0)" && reposo.borde === "0px", `en reposo el concepto no tiene caja ni subrayado (${JSON.stringify(reposo)})`);
  await primero.hover();
  await page.waitForTimeout(300);
  const hover = await primero.evaluate(el => getComputedStyle(el).backgroundColor);
  ok(hover !== "rgba(0, 0, 0, 0)" && reposo.cursor === "pointer", `al pasar el ratón se resalta (${hover}) y el cursor es de mano`);
  const tema = await page.evaluate(() => document.documentElement.getAttribute("data-tema"));
  const fondoPagina = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  ok(tema === "claro" && fondoPagina === "rgb(248, 249, 252)", `tema claro por defecto (${tema}, fondo ${fondoPagina})`);

  // modal por clic
  const nombre = (await primero.textContent()).trim();
  await primero.scrollIntoViewIfNeeded();
  await primero.click();
  ok(await page.locator("dialog#modal-concepto[open]").count() === 1, `el modal se abre al pulsar «${nombre}»`);
  const titulo = (await page.locator("#mc-titulo").textContent()).trim();
  const def = (await page.locator("#mc-def").textContent()).trim();
  ok(titulo.length > 0 && def.length > 20, `modal con título «${titulo}» y definición (${def.length} car.)`);
  ok(await page.evaluate(() => document.activeElement && document.activeElement.id === "mc-titulo"), "el foco pasa al modal");
  await page.waitForTimeout(500); await page.screenshot({ path: `${SH}/modal-claro.png` });
  await page.keyboard.press("Escape");
  ok(await page.locator("dialog#modal-concepto[open]").count() === 0, "Esc cierra el modal");
  ok(await primero.evaluate(el => el === document.activeElement), "el foco vuelve al concepto de origen");

  // teclado
  await primero.focus(); await page.keyboard.press("Enter");
  ok(await page.locator("dialog#modal-concepto[open]").count() === 1, "Enter abre el modal desde el teclado");
  await page.click(".mc-cerrar");
  ok(await page.locator("dialog#modal-concepto[open]").count() === 0, "el botón ✕ cierra el modal");
  // clic en el fondo
  await primero.click();
  await page.mouse.click(5, 5);
  ok(await page.locator("dialog#modal-concepto[open]").count() === 0, "clic fuera cierra el modal");

  // nodo de diagrama
  const nodo = page.locator(".mermaid g.node.caja-info").first();
  await nodo.scrollIntoViewIfNeeded();
  await page.waitForTimeout(1200);
  const nodoTexto = (await nodo.textContent()).trim().replace(/\s+/g, " ");
  await nodo.click();
  ok(await page.locator("dialog#modal-concepto[open]").count() === 1, `el nodo «${nodoTexto.slice(0, 40)}…» abre el modal`);
  await page.keyboard.press("Escape");
  await nodo.focus(); await page.keyboard.press("Enter");
  ok(await page.locator("dialog#modal-concepto[open]").count() === 1, "Enter sobre un nodo abre el modal");
  await page.keyboard.press("Escape");

  // capturas de los diagramas ya animados
  const figs = page.locator("figure.diagrama");
  for (let i = 0; i < await figs.count(); i++) { await figs.nth(i).scrollIntoViewIfNeeded(); await page.waitForTimeout(1500); await figs.nth(i).screenshot({ path: `${SH}/diagrama-${i + 1}-claro.png` }); }
  await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(300);
  await page.screenshot({ path: `${SH}/pagina-claro.png` });

  // todas las cajas de todos los diagramas de los módulos: abren el modal con título y enlaces
  for (const modulo of ["00-base-aws", "01-fundamentos-ia-ml", "02-fundamentos-genai", "03-modelos-fundacionales", "04-ia-responsable", "05-seguridad-gobierno"]) {
    await page.goto(`${U}/c/aif-c01/modulo/${modulo}/teoria`);
    await page.waitForSelector("figure.diagrama svg", { timeout: 20000 });
    await page.waitForTimeout(1200);
    const total = await page.locator(".mermaid .caja-info").count();
    let sinTitulo = 0, sinEnlaces = 0, malEnlazados = 0;
    for (let i = 0; i < total; i++) {
      const caja = page.locator(".mermaid .caja-info").nth(i);
      await caja.scrollIntoViewIfNeeded(); await page.waitForTimeout(150);
      await caja.dispatchEvent("click");
      if (!(await page.locator("#mc-titulo").textContent()).trim()) sinTitulo++;
      const enlaces = await page.locator("#mc-enlaces a").evaluateAll(as => as.map(a => ({ href: a.getAttribute("href"), target: a.getAttribute("target"), rel: a.getAttribute("rel") })));
      if (!enlaces.length) sinEnlaces++;
      for (const e of enlaces) { const externo = e.href.startsWith("https://"); if (externo && !(e.target === "_blank" && /noopener/.test(e.rel || ""))) malEnlazados++; if (!externo && e.target) malEnlazados++; }
      await page.keyboard.press("Escape");
    }
    ok(total > 0 && sinTitulo === 0 && sinEnlaces === 0 && malEnlazados === 0, `${modulo}: ${total} cajas, todas abren su modal con título y enlaces correctos`);
  }
  // «Ver en el curso» lleva al apartado (ancla) y los enlaces del mapa de cobertura funcionan
  await page.goto(`${U}/c/aif-c01/modulo/01-fundamentos-ia-ml/teoria`);
  await page.waitForSelector("figure.diagrama svg"); await page.waitForTimeout(1200);
  await page.locator(".mermaid g.node.caja-info").first().dispatchEvent("click");
  await page.click("#mc-enlaces a.mc-enlace-interno");
  await page.waitForTimeout(800);
  ok(await page.locator("dialog#modal-concepto[open]").count() === 0, "el enlace interno cierra el modal");
  const url = page.url(); const hash = decodeURIComponent(new URL(url).hash.slice(1));
  ok(hash.length > 0 && await page.evaluate(h => !!document.getElementById(h), hash), `«Ver en el curso» lleva al apartado (#${hash})`);
  await page.goto(`${U}/c/aif-c01/modulo/01-fundamentos-ia-ml/teoria`);
  await page.click('a[href="#términos-básicos-de-ia"], a[href="#t%C3%A9rminos-b%C3%A1sicos-de-ia"]');
  ok(await page.evaluate(() => decodeURIComponent(location.hash) === "#términos-básicos-de-ia" && !!document.getElementById("términos-básicos-de-ia")), "los enlaces #ancla del mapa de cobertura funcionan");

  // navegación con hx-boost y modal en la página nueva
  await page.click('a:has-text("Servicios")');
  await page.waitForURL(/servicios/);
  await page.waitForTimeout(500);
  const b2 = page.locator("button.concepto").first();
  await b2.click();
  ok(await page.locator("dialog#modal-concepto[open]").count() === 1, "tras navegar con hx-boost el modal sigue funcionando");
  await page.keyboard.press("Escape");

  // glosario
  await page.goto(U + "/c/aif-c01/glosario");
  const total = await page.locator("#lista-glosario li").count();
  await page.fill("#filtro-glosario", "recall");
  const visibles = await page.locator("#lista-glosario li:visible").count();
  ok(total > 50 && visibles >= 1 && visibles < total, `glosario: ${total} entradas, filtro «recall» deja ${visibles}`);
  await page.locator("#lista-glosario li:visible button").first().click();
  ok(await page.locator("dialog#modal-concepto[open]").count() === 1, "una entrada del glosario abre el modal");
  await page.screenshot({ path: `${SH}/glosario-modal.png` });
  ok(errores.length === 0, `sin errores de JavaScript ni de consola${errores.length ? ": " + errores.join(" | ") : ""}`);
  await ctx.close();
}

// ---------------------------------------------------------------- oscuro
{
  const { ctx, page } = await sesion({ colorScheme: "light" });
  await page.evaluate(() => localStorage.setItem("tema", "oscuro"));
  await page.goto(RUTA); await page.waitForSelector("figure.diagrama svg", { timeout: 20000 });
  ok(await page.evaluate(() => document.documentElement.getAttribute("data-tema")) === "oscuro", "el tema oscuro se aplica desde las preferencias guardadas");
  const f = page.locator("figure.diagrama").first(); await f.scrollIntoViewIfNeeded(); await page.waitForTimeout(1800);
  await f.screenshot({ path: `${SH}/diagrama-1-oscuro.png` });
  const f2 = page.locator("figure.diagrama").nth(2); await f2.scrollIntoViewIfNeeded(); await page.waitForTimeout(1800);
  await f2.screenshot({ path: `${SH}/diagrama-3-oscuro.png` });
  await page.locator("button.concepto").first().click(); await page.waitForTimeout(500); await page.screenshot({ path: `${SH}/modal-oscuro.png` });
  await page.goto(U + "/c/aif-c01/modulo/00-base-aws/teoria"); await page.waitForSelector("figure.diagrama svg"); const g = page.locator("figure.diagrama"); for (let i = 0; i < await g.count(); i++) { await g.nth(i).scrollIntoViewIfNeeded(); await page.waitForTimeout(1600); await g.nth(i).screenshot({ path: `${SH}/m00-diagrama-${i + 1}-oscuro.png` }); }
  await ctx.close();
}

// ---------------------------------------------------------------- selector de tema y «sistema»
{
  const { ctx, page } = await sesion({ colorScheme: "dark" });
  await page.goto(U + "/c/aif-c01/");
  ok(await page.evaluate(() => document.documentElement.getAttribute("data-tema")) === "claro", "aunque el sistema esté en oscuro, la web empieza en claro");
  await page.click("[data-alternar-tema]");
  ok(await page.evaluate(() => document.documentElement.getAttribute("data-tema")) === "oscuro", "el botón cambia a oscuro");
  await page.click("[data-alternar-tema]");
  ok(await page.evaluate(() => document.documentElement.getAttribute("data-tema")) === "auto", "el segundo clic pasa a «Sistema» (sigue al sistema operativo)");
  const fondo = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  ok(fondo === "rgb(18, 22, 28)", `con «Sistema» y sistema oscuro el fondo es oscuro (${fondo})`);
  await page.reload();
  ok(await page.evaluate(() => document.documentElement.getAttribute("data-tema")) === "auto", "la preferencia se recuerda al recargar");
  await ctx.close();
}

// ---------------------------------------------------------------- movimiento reducido
{
  const { ctx, page } = await sesion({ reducedMotion: "reduce" });
  await page.goto(RUTA); await page.waitForSelector("figure.diagrama svg", { timeout: 20000 });
  await page.waitForTimeout(500);
  const r = await page.evaluate(() => {
    const l = document.querySelector(".mermaid .flowchart-link"), n = document.querySelector(".mermaid .node");
    return { flujo: getComputedStyle(l).animationName, op: getComputedStyle(n).opacity, nodoAnim: getComputedStyle(n).animationName,
             anim: !!document.querySelector("figure.diagrama.anim-lista") };
  });
  ok(r.flujo === "none" && r.op === "1" && r.nodoAnim === "none", `movimiento reducido: sin animación y todo visible (${JSON.stringify(r)})`);
  await ctx.close();
}

// ---------------------------------------------------------------- móvil
{
  const { ctx, page } = await sesion({ viewport: { width: 390, height: 800 }, isMobile: true, hasTouch: true });
  await page.goto(RUTA); await page.waitForSelector("figure.diagrama svg", { timeout: 20000 });
  const pista = await page.locator("button.concepto").first().evaluate(el => getComputedStyle(el).borderBottomStyle);
  ok(pista === "dotted", `en pantallas táctiles hay una pista discreta (subrayado ${pista})`);
  await page.locator("button.concepto").first().tap();
  await page.screenshot({ path: `${SH}/modal-movil.png` });
  const caja = await page.locator("dialog#modal-concepto").boundingBox();
  ok(caja && caja.width <= 390 && caja.x >= 0, `en móvil el modal cabe en la pantalla (${Math.round(caja.width)} px)`);
  const desborda = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  ok(!desborda, "sin desbordamiento horizontal de la página en móvil");
  await ctx.close();
}
// ---------------------------------------------------------------- tests: repaso y explicación tras responder
{
  const { ctx, page, errores } = await sesion();
  await page.goto(U + "/c/aif-c01/tests");
  for (const paso of ["1. Repaso de conocimientos", "2. Preguntas de examen", "3. Repetir falladas", "4. Simulacro"])
    ok(await page.getByRole("heading", { name: paso }).count() === 1, `la página de tests muestra «${paso}»`);
  ok(await page.locator('input[name="estudio"]').count() === 1, "el simulacro ofrece el modo estudio");
  const repaso = page.locator('form:has(input[name="modo"][value="repaso"])');
  await repaso.locator("select").selectOption("00-base-aws");
  await repaso.locator('input[name="n"]').fill("1");
  await Promise.all([page.waitForURL(/\/tests\/\d+\/p\/1/), repaso.locator("button").click()]);
  ok((await page.textContent("main")).includes("Repaso de conocimientos"), "la pregunta se identifica como de repaso");
  const marcar = page.locator("form[action$='/responder'] input[type=radio], form[action$='/responder'] input[type=checkbox]");
  if (await marcar.count()) await marcar.first().check();
  const listas = page.locator("form[action$='/responder'] select");
  for (let k = 0; k < await listas.count(); k++) await listas.nth(k).selectOption({ index: k + 1 });  // un elemento distinto en cada lista
  await page.click("form[action$='/responder'] button[type=submit]");
  await page.waitForSelector("details.explicacion", { timeout: 10000 }).catch(() => {});
  const det = page.locator("details.explicacion");
  ok(await det.count() === 1, "tras responder aparece el desplegable de explicación");
  if (!(await det.evaluate(d => d.open))) await det.locator("summary").click();
  ok(await det.evaluate(d => d.open) && (await det.textContent()).includes("Referencia oficial"), "«Ver explicación» muestra la explicación y la referencia");
  ok(await det.locator("a.btn", { hasText: "Repasar en la teoría" }).count() === 1, "la explicación enlaza a la teoría del objetivo");
  await page.screenshot({ path: `${SH}/repaso-explicacion.png`, fullPage: true });
  ok(errores.length === 0, `tests sin errores de consola ni HTTP (${errores.join(" | ")})`);
  await ctx.close();
}
{
  const { ctx, page } = await sesion({ viewport: { width: 390, height: 800 }, isMobile: true, hasTouch: true });
  await page.goto(U + "/c/aif-c01/tests");
  const desborda = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  ok(!desborda, "la página de tests no desborda en móvil");
  await ctx.close();
}
await browser.close();
