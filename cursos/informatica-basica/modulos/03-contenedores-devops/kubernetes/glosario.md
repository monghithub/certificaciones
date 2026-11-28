# Glosario: Kubernetes

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 19 términos.

## C

- **ConfigMap**. *Concepto.* Objeto que guarda configuración no confidencial en pares clave-valor, para inyectarla en los pods como variables de entorno o ficheros.
  - Referencia: <https://kubernetes.io/docs/concepts/configuration/configmap/>

## D

- **Deployment** (Deployments). *Concepto.* Objeto que declara cuántas réplicas de un pod deben ejecutarse y con qué plantilla, y gestiona las actualizaciones progresivas y las vueltas atrás mediante ReplicaSets.
  - Referencia: <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>

## E

- **Estado deseado** (bucle de control, reconciliación). *Concepto.* Modelo de Kubernetes en el que se declara cómo debe estar el sistema y unos controladores comparan continuamente el estado real con el deseado y actúan para acercarlos.
  - Referencia: <https://kubernetes.io/docs/concepts/architecture/controller/>
- **etcd**. *Herramienta.* Almacén clave-valor distribuido y consistente donde el plano de control guarda todo el estado del clúster.
  - Referencia: <https://kubernetes.io/docs/concepts/overview/components/>
- **Etiqueta** (etiquetas, label, labels, selector). *Concepto.* Par clave-valor que se asigna a los objetos (app=web). Los selectores usan las etiquetas para elegir objetos, por ejemplo qué pods gestiona un Deployment o a qué pods envía tráfico un Service.
  - Referencia: <https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/>

## H

- **HorizontalPodAutoscaler** (HPA, autoescalado horizontal). *Concepto.* Objeto que ajusta automáticamente el número de réplicas de un Deployment según métricas como el uso de CPU.
  - Referencia: <https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/>

## I

- **Ingress**. *Concepto.* Objeto que define reglas de enrutado HTTP y HTTPS desde fuera del clúster hacia Services, por nombre de host y ruta. Necesita un controlador de Ingress instalado. La Gateway API es su evolución.
  - Referencia: <https://kubernetes.io/docs/concepts/services-networking/ingress/>

## K

- **kubectl**. *Herramienta.* Herramienta de línea de comandos para hablar con la API de Kubernetes: aplicar manifiestos, consultar el estado, ver registros o ejecutar comandos en los pods.
  - Referencia: <https://kubernetes.io/docs/concepts/overview/components/>
- **kubelet**. *Herramienta.* Agente que se ejecuta en cada nodo, recibe las especificaciones de los pods asignados y se asegura de que sus contenedores estén en marcha y sanos.
  - Referencia: <https://kubernetes.io/docs/concepts/overview/components/>
- **Kubernetes** (K8s). *Herramienta.* Plataforma de código abierto para desplegar, escalar y gestionar aplicaciones en contenedores. Google la liberó en 2014; su nombre viene del griego «timonel».
  - Referencia: <https://kubernetes.io/docs/concepts/overview/>

## N

- **Namespace de Kubernetes** (namespace). *Concepto.* Partición lógica del clúster para agrupar recursos y separar equipos o entornos. Los nombres de los objetos son únicos dentro de cada namespace.
  - Referencia: <https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>

## P

- **PersistentVolumeClaim** (PVC, PersistentVolume, PV). *Concepto.* Petición de almacenamiento persistente que hace un pod. Kubernetes la vincula a un PersistentVolume, creado a mano o de forma dinámica por una StorageClass.
  - Referencia: <https://kubernetes.io/docs/concepts/storage/persistent-volumes/>
- **Pod** (pods). *Concepto.* Unidad mínima de despliegue en Kubernetes: uno o varios contenedores que comparten red (una IP) y almacenamiento, y que se planifican juntos en el mismo nodo.
  - Referencia: <https://kubernetes.io/docs/concepts/workloads/pods/>

## R

- **ReplicaSet**. *Concepto.* Controlador que mantiene un número fijo de pods idénticos. Normalmente no se crea a mano: lo gestiona un Deployment.
  - Referencia: <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>
- **Requests y limits** (requests, limits). *Concepto.* Recursos que pide un contenedor (requests, usados por el planificador para elegir nodo) y máximos que puede usar (limits). Superar el límite de memoria provoca que el contenedor muera con OOMKilled.
  - Referencia: <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>

## S

- **Secret** (Secrets). *Concepto.* Objeto para datos confidenciales (contraseñas, tokens). Sus valores van en base64, que es una codificación, no un cifrado; por defecto se guardan sin cifrar en etcd.
  - Referencia: <https://kubernetes.io/docs/concepts/configuration/secret/>
- **Service** (Services). *Concepto.* Objeto que da un nombre DNS y una IP estables a un conjunto de pods seleccionados por etiquetas y reparte el tráfico entre los que están listos.
  - Referencia: <https://kubernetes.io/docs/concepts/services-networking/service/>
- **Sonda** (sondas, probe, readinessProbe, livenessProbe, startupProbe). *Concepto.* Comprobación periódica que hace el kubelet sobre un contenedor. La de disponibilidad (readiness) decide si recibe tráfico; la de vida (liveness), si hay que reiniciarlo; la de arranque (startup) protege a las aplicaciones lentas en arrancar.
  - Referencia: <https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/>
- **StatefulSet**. *Concepto.* Controlador para aplicaciones con estado (bases de datos) que da a cada pod una identidad estable (nombre y almacenamiento propios) y un orden de arranque y parada.
  - Referencia: <https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/>
