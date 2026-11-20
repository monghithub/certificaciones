## 1. Consola

- [ ] 1.1 `CONSULTAS_TOKEN` en `Settings`; sin él, ni panel ni rutas
- [ ] 1.2 Modelos `Consulta` y `ConsultaMensaje` y migración `0003`
- [ ] 1.3 Rutas: enviar duda, ver panel (htmx), «Mis dudas»; solo `admin`
- [ ] 1.4 API interna con token: pendientes (con el contexto de la pregunta) y respuesta
- [ ] 1.5 Panel en `pregunta.html` y `resultado.html`; enlace «Mis dudas»
- [ ] 1.6 Pruebas: permisos, CSRF, token, cola, conversación, desactivado por defecto

## 2. Trabajador

- [ ] 2.1 `scripts/consultas_trabajador.py`: sondeo, prompt, `claude -p`/`--resume`, herramientas de solo lectura, límites y reintentos
- [ ] 2.2 Pruebas con un `claude` simulado

## 3. Cierre y despliegue

- [ ] 3.1 `docs/consola.md`, `.env.example`, CHANGELOG y journal
- [ ] 3.2 PR, CI y fusión
- [ ] 3.3 titan: `CONSULTAS_TOKEN` en `.env`, servicio de usuario de systemd del trabajador, prueba de extremo a extremo; inventario de `Sistema`
