## 1. Manifiesto y validación

- [x] 1.1 Añadir `proveedor` y `fuentes_oficiales` a `schemas/curso.schema.json` y a `curso/manifiesto.py`
- [x] 1.2 Generalizar `referencia` en `schemas/pregunta.schema.json` (https) y comprobar el host en `validar_preguntas.py`
- [x] 1.3 Declarar `proveedor` y `fuentes_oficiales` en `cursos/aif-c01/curso.yaml`
- [x] 1.4 Tests: referencia fuera de las fuentes, subdominio, curso de otro proveedor y URL no https

## 2. Reglas y documentación

- [x] 2.1 `AGENTS.md` raíz genérico y `cursos/aif-c01/AGENTS.md` con lo propio de AWS y AIF-C01
- [x] 2.2 Mover `promt.md` a `cursos/aif-c01/promt.md` y actualizar markdownlint y lychee
- [x] 2.3 README raíz con la visión multicertificación y `docs/consola.md`

## 3. Consola y despliegue

- [x] 3.1 Marca «Certificaciones» en la plantilla y título de la API
- [x] 3.2 Imagen Docker `certificaciones-consola` en `compose.yaml` y CI

## 4. Cierre

- [x] 4.1 Validador, cobertura, markdownlint y pytest en verde
- [x] 4.2 `CHANGELOG.md` y `docs/journal.md`
- [ ] 4.3 PR a `main`, CI en verde, integración y archivo del cambio
