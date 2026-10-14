// Valida la sintaxis de los diagramas Mermaid de los ficheros Markdown indicados.
// Uso: node validar-mermaid.mjs ../../cursos/aif-c01/modulos/*/README.md
import { JSDOM } from "jsdom";
import fs from "fs";
const dom = new JSDOM("<!doctype html><html><body></body></html>");
globalThis.window = dom.window; globalThis.document = dom.window.document; for (const k of ["Element","HTMLElement","SVGElement","Node","DOMParser","DocumentFragment","Text","MutationObserver"]) globalThis[k] = dom.window[k];
Object.defineProperty(globalThis, "navigator", { value: dom.window.navigator, configurable: true });
const mermaid = (await import("mermaid")).default;
let fallos = 0, total = 0;
for (const f of process.argv.slice(2)) {
  const txt = fs.readFileSync(f, "utf8");
  for (const m of txt.matchAll(/```mermaid\n([\s\S]*?)```/g)) {
    total++;
    try { await mermaid.parse(m[1]); console.log("OK   ", f.split("/").slice(-2).join("/"), "·", m[1].split("\n")[0]); }
    catch (e) { fallos++; console.log("ERROR", f, "·", m[1].split("\n")[0], "\n", String(e.message || e).slice(0, 300)); }
  }
}
console.log(`${total - fallos}/${total} diagramas válidos`);
process.exit(fallos ? 1 : 0);
