# Glosario: CI/CD y GitOps

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 15 términos.

## A

- **Argo CD** (Application, selfHeal, prune). *Herramienta.* Herramienta de GitOps para Kubernetes que compara los manifiestos de un repositorio con el clúster y los sincroniza.
  - Referencia: <https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/>
- **Artefacto inmutable** (build once). *Patrón.* El resultado de la compilación (por ejemplo, una imagen identificada por su digest) se construye una vez y se promociona sin cambios entre entornos; solo cambia la configuración.
  - Referencia: <https://12factor.net/es/build-release-run>

## D

- **Deriva de configuración** (drift, OutOfSync). *Concepto.* Diferencia entre el estado real de un sistema y el declarado, causada por cambios manuales o fallos.
  - Referencia: <https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/>
- **Desarrollo basado en el tronco** (trunk-based development). *Técnica.* Modelo de ramas en el que todos integran en la rama principal con ramas de vida muy corta (horas o pocos días).
  - Referencia: <https://trunkbaseddevelopment.com/>
- **Despliegue azul-verde** (blue-green). *Patrón.* Se mantienen dos entornos de producción; la versión nueva se despliega en el inactivo y se cambia el tráfico de golpe, con vuelta atrás inmediata.
  - Referencia: <https://martinfowler.com/bliki/BlueGreenDeployment.html>
- **Despliegue canario** (canary release). *Patrón.* La versión nueva recibe primero una pequeña parte del tráfico y, si sus métricas son buenas, se amplía progresivamente.
  - Referencia: <https://martinfowler.com/bliki/CanaryRelease.html>
- **Despliegue continuo** (continuous deployment). *Técnica.* Cada cambio que supera la tubería llega a producción automáticamente, sin aprobación manual.
  - Referencia: <https://martinfowler.com/bliki/ContinuousDelivery.html>

## E

- **Entrega continua** (continuous delivery). *Técnica.* Mantener el software siempre listo para desplegarse en producción, de forma que desplegar sea una decisión de negocio y no un esfuerzo técnico.
  - Referencia: <https://martinfowler.com/bliki/ContinuousDelivery.html>

## G

- **GitHub Actions** (workflow, flujo de trabajo). *Herramienta.* Plataforma de CI/CD de GitHub: flujos de trabajo en YAML dentro de .github/workflows, con trabajos y pasos que se ejecutan ante eventos del repositorio.
  - Referencia: <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- **GITHUB_TOKEN** (permissions). *Herramienta.* Credencial temporal que GitHub da a cada ejecución de un flujo de trabajo; sus permisos se limitan con la clave permissions.
  - Referencia: <https://docs.github.com/en/actions/tutorials/authenticate-with-github_token>
- **GitOps**. *Técnica.* Gestión de sistemas en la que el estado deseado se declara y versiona en Git, y unos agentes lo traen y reconcilian continuamente con el estado real.
  - Referencia: <https://opengitops.dev/>

## I

- **Integración continua** (CI, continuous integration). *Técnica.* Práctica de integrar los cambios en la rama principal al menos a diario, con una compilación y unas pruebas automáticas que avisan enseguida si algo se rompe.
  - Referencia: <https://martinfowler.com/articles/continuousIntegration.html>
- **Interruptor de funcionalidad** (feature flag, feature toggle). *Patrón.* Condición configurable que activa o desactiva una funcionalidad sin desplegar, para separar el despliegue del lanzamiento.
  - Referencia: <https://martinfowler.com/articles/feature-toggles.html>
- **Inyección de script** (script injection). *Concepto.* Ataque en el que un dato controlado por un tercero, como el título de un pull request, se inserta con ${{ }} en un run y se ejecuta como código en el runner.
  - Referencia: <https://docs.github.com/en/actions/reference/security/secure-use>

## M

- **Métricas DORA** (DORA). *Métrica.* Métricas de rendimiento de la entrega de software: tiempo de entrega de un cambio, frecuencia de despliegue, tiempo de recuperación de un despliegue fallido, tasa de fallo de cambios y tasa de retrabajo de despliegues.
  - Referencia: <https://dora.dev/guides/dora-metrics/>
