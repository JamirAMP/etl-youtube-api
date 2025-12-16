import psycopg2
import psycopg2.extras
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class PostgresLoader:
    """
    Gestor de carga de datos a PostgreSQL.
    Maneja la creación de tablas y carga de datos con estrategia de upsert.
    """
    def __init__(self, host, port, dbname, user, password):
        self.conn_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password
        }

    def _get_connection(self):
        return psycopg2.connect(**self.conn_params)

    
    def create_tables(self):
        ddl_statements = {
            "videos": """
                CREATE TABLE IF NOT EXISTS raw_videos (
                    video_id TEXT PRIMARY KEY,
                    titulo TEXT,
                    descripcion TEXT,
                    canal_id TEXT,
                    canal_nombre TEXT,
                    fecha_publicacion TIMESTAMP,
                    duracion TEXT,
                    vistas INT,
                    likes INT,
                    comentarios INT,
                    tags TEXT[],
                    categoria_id TEXT,
                    thumbnail_url TEXT,
                    technology_id TEXT,
                    search_query TEXT,
                    fecha_extraccion TIMESTAMP
                );
            """,
            "comentarios": """
                CREATE TABLE IF NOT EXISTS raw_comments (
                    comment_id TEXT PRIMARY KEY,
                    video_id TEXT,
                    author TEXT,
                    text TEXT,
                    likes INT,
                    published_at TIMESTAMP,
                    fecha_extraccion TIMESTAMP
                );
            """,
            "canales": """
                CREATE TABLE IF NOT EXISTS raw_channels (
                    canal_id TEXT PRIMARY KEY,
                    nombre TEXT,
                    descripcion TEXT,
                    suscriptores INT,
                    total_videos INT,
                    vistas_totales INT,
                    fecha_creacion TIMESTAMP,
                    pais TEXT,
                    fecha_extraccion TIMESTAMP
                );
            """
        }

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                for table, ddl in ddl_statements.items():
                    try:
                        cur.execute(ddl)
                        logger.info(f"Tabla {table} creada o ya existe.")
                    except Exception as e:
                        logger.error(f"Error creando tabla {table}: {e}")
            conn.commit()
    
    def load_data(self, table: str, data: List[Dict]):
        if not data:
            logger.warning(f"No hay datos para insertar en {table}")
            return

        columns = data[0].keys()
        values_template = ", ".join([f"%({col})s" for col in columns])
        
        # Determinar la columna de conflicto según la tabla
        conflict_column = {
            "raw_videos": "video_id",
            "raw_comments": "comment_id",
            "raw_channels": "canal_id"
        }.get(table, "id")
        
        # Construir cláusula de actualización excluyendo la PK
        update_cols = [col for col in columns if col != conflict_column]
        update_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in update_cols])

        insert_sql = f"""
            INSERT INTO {table} ({", ".join(columns)})
            VALUES ({values_template})
            ON CONFLICT ({conflict_column}) 
            DO UPDATE SET {update_clause};
        """

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    psycopg2.extras.execute_batch(cur, insert_sql, data, page_size=500)
                    logger.info(f"{len(data)} registros procesados (insertados/actualizados) en {table}")
                except Exception as e:
                    logger.error(f"Error insertando datos en {table}: {e}")
                    raise
            conn.commit()
