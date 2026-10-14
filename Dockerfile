# syntax=docker/dockerfile:1
FROM python:3.12-slim AS construccion
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /src
COPY requirements.txt requirements-app.txt ./
RUN python -m venv /opt/venv && /opt/venv/bin/pip install -r requirements-app.txt

FROM python:3.12-slim
ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    DATABASE_URL=sqlite:////data/app.db COURSES_DIR=/cursos
RUN useradd --system --uid 10001 --home-dir /nonexistent --shell /usr/sbin/nologin app \
    && mkdir /data /cursos && chown app /data
COPY --from=construccion /opt/venv /opt/venv
WORKDIR /srv
COPY app ./app
COPY curso ./curso
COPY migrations ./migrations
COPY schemas ./schemas
COPY alembic.ini ./
USER app
VOLUME ["/data"]
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s \
    CMD python -c "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/login', timeout=3)" || exit 1
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
