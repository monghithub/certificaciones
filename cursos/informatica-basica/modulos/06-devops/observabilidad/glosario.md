# Glosario: Observabilidad: logs, métricas y trazas

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 15 términos.

## C

- **Cardinalidad** (cardinality). *Concepto.* Número de combinaciones distintas de valores de etiquetas de una métrica. Cada combinación es una serie temporal; etiquetas como el id de usuario la disparan.
  - Referencia: <https://prometheus.io/docs/practices/naming/>

## H

- **Histograma** (histogram, buckets). *Métrica.* Métrica que cuenta observaciones (como duraciones) en intervalos o buckets, de la que se calculan percentiles. Los límites de los buckets deben ajustarse a la unidad y al rango de los valores.
  - Referencia: <https://prometheus.io/docs/practices/histograms/>

## L

- **Log estructurado** (structured logging, logs en JSON). *Técnica.* Registro en el que cada evento es un objeto con campos (normalmente JSON) en lugar de una línea de texto libre, para poder filtrarlo y agregarlo.
  - Referencia: <https://opentelemetry.io/docs/concepts/signals/logs/>

## M

- **Método RED** (RED). *Técnica.* Para cada servicio, medir la tasa de peticiones (Rate), los errores (Errors) y la duración (Duration).
  - Referencia: <https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/>
- **Método USE** (USE). *Técnica.* Para cada recurso (CPU, memoria, disco, red), medir su utilización (Utilization), saturación (Saturation) y errores (Errors).
  - Referencia: <https://www.brendangregg.com/usemethod.html>
- **Muestreo** (sampling). *Técnica.* Guardar solo una parte de las trazas para reducir el coste. Puede decidirse al empezar la traza (head) o al terminar, viendo su resultado (tail).
  - Referencia: <https://opentelemetry.io/docs/concepts/sampling/>

## O

- **Observabilidad** (observability). *Concepto.* Capacidad de entender el estado interno de un sistema a partir de lo que emite (logs, métricas y trazas), incluso ante problemas que no se habían previsto.
  - Referencia: <https://opentelemetry.io/docs/concepts/observability-primer/>
- **OpenTelemetry** (OTel, OTLP). *Herramienta.* Estándar abierto, con API, SDK y protocolo (OTLP), para generar y enviar trazas, métricas y logs sin depender de un proveedor concreto.
  - Referencia: <https://opentelemetry.io/docs/concepts/signals/>
- **OpenTelemetry Collector** (Collector). *Herramienta.* Servicio que recibe telemetría, la procesa (lotes, filtros, muestreo) y la exporta a uno o varios destinos mediante tuberías de receptores, procesadores y exportadores.
  - Referencia: <https://opentelemetry.io/docs/collector/configuration/>

## P

- **PromQL** (rate, histogram_quantile). *Lenguaje.* Lenguaje de consulta de Prometheus, con funciones como rate (ritmo por segundo de un contador) o histogram_quantile (percentil de un histograma).
  - Referencia: <https://prometheus.io/docs/prometheus/latest/querying/functions/>

## S

- **Señales doradas** (golden signals, cuatro señales doradas). *Métrica.* Las cuatro métricas que el libro de SRE de Google recomienda vigilar en un servicio de cara al usuario: latencia, tráfico, errores y saturación.
  - Referencia: <https://sre.google/sre-book/monitoring-distributed-systems/>
- **SLI y SLO** (SLI, SLO, objetivo de nivel de servicio). *Métrica.* Un SLI es una medida del servicio tal como lo percibe el usuario (por ejemplo, la proporción de peticiones correctas); un SLO es el objetivo para ese indicador (por ejemplo, el 99,9 % en 30 días).
  - Referencia: <https://sre.google/sre-book/service-level-objectives/>
- **Span** (spans). *Concepto.* Unidad de trabajo dentro de una traza, con nombre, inicio, duración, atributos, estado y el span padre del que depende.
  - Referencia: <https://opentelemetry.io/docs/concepts/signals/traces/>

## T

- **traceparent** (W3C Trace Context, propagación de contexto). *Protocolo.* Cabecera HTTP del estándar W3C Trace Context que transmite la versión, el identificador de traza, el del span padre y los indicadores, para continuar la traza en otro servicio.
  - Referencia: <https://www.w3.org/TR/trace-context-2/>
- **Traza** (trace, traza distribuida). *Concepto.* Recorrido de una petición por todos los servicios que atraviesa, formado por spans con un mismo identificador de traza.
  - Referencia: <https://opentelemetry.io/docs/concepts/signals/traces/>
