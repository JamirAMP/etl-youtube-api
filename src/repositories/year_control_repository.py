import psycopg2
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

class YearControlRepository:
    """
    Repositorio para gestionar el control secuencial de años procesados.
    Maneja la tabla etl_year_control para tracking de progreso.
    """

    def __init__(self, conn_params):
        self.conn_params = conn_params

    def get_next_year(self) -> Optional[int]:
        """Obtiene el próximo año no procesado."""
        query = """
        SELECT year
        FROM etl_year_control
        WHERE processed = FALSE
        ORDER BY year
        LIMIT 1;
        """

        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    row = cur.fetchone()
                    
                    if row:
                        year = row[0]
                        logger.info(f"📅 Próximo año pendiente: {year}")
                        return year
                    else:
                        logger.warning("⚠️ No hay años pendientes para procesar")
                        return None
        except Exception as e:
            logger.error(f"Error obteniendo próximo año pendiente: {e}")
            return None

    def mark_year_as_processed(self, year: int) -> bool:
        """Marca un año como procesado."""
        query = """
        UPDATE etl_year_control
        SET processed = TRUE,
            processed_at = %s
        WHERE year = %s;
        """

        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (datetime.now(timezone.utc), year))
                    conn.commit()
                    logger.info(f"✅ Año {year} marcado como procesado")
                    return True
        except Exception as e:
            logger.error(f"Error marcando año {year} como procesado: {e}")
            return False
