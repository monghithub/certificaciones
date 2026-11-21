import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402

from app.db import crear_motor  # noqa: E402
from app.migraciones import RAIZ, migrar  # noqa: E402


def _cfg(conn):
    cfg = Config(str(RAIZ / "alembic.ini"))
    cfg.set_main_option("script_location", str(RAIZ / "migrations"))
    cfg.attributes["connection"] = conn
    return cfg


def _base_0001(url):
    motor = crear_motor(url)
    with motor.begin() as conn:
        command.upgrade(_cfg(conn), "0001")
    with sqlite3.connect(url.removeprefix("sqlite:///")) as db:
        db.executescript("""
        INSERT INTO usuario VALUES (1,'root','Root','admin','h',1,0,'2026-01-01 00:00:00',NULL);
        INSERT INTO usuario VALUES (2,'ana','Ana','estudiante','h',1,0,'2026-01-01 00:00:00',NULL);
        INSERT INTO usuario VALUES (3,'bea','Bea','estudiante','h',0,0,'2026-01-01 00:00:00',NULL);
        INSERT INTO progreso_lectura VALUES (1,2,'03-m','teoria',1,'2026-01-02 10:00:00');
        INSERT INTO progreso_lectura VALUES (2,2,'03-m','servicios',0,'2026-01-02 11:00:00');
        INSERT INTO progreso_lectura VALUES (3,3,'03-m','teoria',1,'2026-01-03 10:00:00');
        INSERT INTO intento VALUES (1,2,'mixto','','2026-01-02 12:00:00',NULL,NULL,'["D3-001"]');
        INSERT INTO intento VALUES (2,3,'dominio','3','2026-01-03 12:00:00','2026-01-03 12:05:00',NULL,'["D3-001","D3-002"]');
        INSERT INTO intento_respuesta VALUES (1,1,'D3-001',3,'3.1','multiple_choice','["b"]',1);
        """)
    return motor


def test_migracion_0002_conserva_datos_y_matricula(tmp_path):
    url = f"sqlite:///{tmp_path}/v1.db"
    motor = _base_0001(url)
    migrar(motor)
    with sqlite3.connect(tmp_path / "v1.db") as db:
        assert db.execute("SELECT version_num FROM alembic_version").fetchone() == ("0003",)
        assert db.execute("SELECT COUNT(*), COUNT(DISTINCT curso) FROM progreso_lectura WHERE curso='aif-c01'").fetchone() == (3, 1)
        assert db.execute("SELECT COUNT(*) FROM intento WHERE curso='aif-c01'").fetchone() == (2,)
        assert db.execute("SELECT usuario_id, curso FROM matricula ORDER BY usuario_id").fetchall() == [(2, "aif-c01"), (3, "aif-c01")]
        assert db.execute("SELECT correcta FROM intento_respuesta").fetchone() == (1,)
        assert db.execute("SELECT completada, actualizado FROM progreso_lectura WHERE id=1").fetchone() == (1, "2026-01-02 10:00:00")
        # la nueva restricción única admite la misma sección en otro curso
        db.execute("INSERT INTO progreso_lectura (usuario_id, curso, modulo, seccion, completada, actualizado) VALUES (2,'otro','03-m','teoria',0,'2026-02-01 00:00:00')")
        try:
            db.execute("INSERT INTO progreso_lectura (usuario_id, curso, modulo, seccion, completada, actualizado) VALUES (2,'otro','03-m','teoria',0,'2026-02-01 00:00:00')")
            assert False, "debería violar la restricción única"
        except sqlite3.IntegrityError:
            pass


def test_migracion_idempotente_y_bd_nueva(tmp_path):
    motor = crear_motor(f"sqlite:///{tmp_path}/nueva.db")
    migrar(motor)
    migrar(motor)  # segunda vez: no hace nada
    with sqlite3.connect(tmp_path / "nueva.db") as db:
        assert db.execute("SELECT version_num FROM alembic_version").fetchone() == ("0003",)


def test_downgrade_a_0001(tmp_path):
    url = f"sqlite:///{tmp_path}/d.db"
    motor = _base_0001(url)
    migrar(motor)
    with motor.begin() as conn:
        command.downgrade(_cfg(conn), "0001")
    with sqlite3.connect(tmp_path / "d.db") as db:
        assert db.execute("SELECT COUNT(*) FROM progreso_lectura").fetchone() == (3,)
        assert "curso" not in [c[1] for c in db.execute("PRAGMA table_info(intento)")]
        assert db.execute("SELECT name FROM sqlite_master WHERE name='matricula'").fetchone() is None


def test_migracion_0003_consultas_y_downgrade(tmp_path):
    url = f"sqlite:///{tmp_path}/c.db"
    motor = _base_0001(url)
    migrar(motor)
    with sqlite3.connect(tmp_path / "c.db") as db:
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("INSERT INTO consulta (usuario_id, curso, pregunta_id, intento_id, creada, actualizada) "
                   "VALUES (1,'aif-c01','D3-001',1,'2026-11-21 10:00:00','2026-11-21 10:00:00')")
        db.execute("INSERT INTO consulta_mensaje (consulta_id, rol, texto, estado, creado, actualizado) "
                   "VALUES (1,'usuario','¿Por qué?','pendiente','2026-11-21 10:00:00','2026-11-21 10:00:00')")
        assert db.execute("SELECT intentos FROM consulta_mensaje").fetchone() == (0,)
        try:
            db.execute("INSERT INTO consulta (usuario_id, curso, pregunta_id, creada, actualizada) "
                       "VALUES (1,'aif-c01','D3-001','2026-11-21 10:00:00','2026-11-21 10:00:00')")
            assert False, "debería violar la restricción única (una conversación por pregunta y usuario)"
        except sqlite3.IntegrityError:
            pass
        db.execute("DELETE FROM intento WHERE id=1")  # el intento se borra: la consulta se conserva sin él
        assert db.execute("SELECT intento_id FROM consulta").fetchone() == (None,)
        db.execute("DELETE FROM consulta")
        assert db.execute("SELECT COUNT(*) FROM consulta_mensaje").fetchone() == (0,)
        db.commit()
    with motor.begin() as conn:
        command.downgrade(_cfg(conn), "0002")
    with sqlite3.connect(tmp_path / "c.db") as db:
        assert db.execute("SELECT name FROM sqlite_master WHERE name LIKE 'consulta%'").fetchall() == []
        assert db.execute("SELECT version_num FROM alembic_version").fetchone() == ("0002",)
