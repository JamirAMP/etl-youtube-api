import psycopg2
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class TechnologyRepository:
    """
    Repositorio para gestionar tecnologías y sus queries de búsqueda.
    Consulta la tabla dim_technology_queries para obtener tecnologías activas.
    """

    def __init__(self, conn_params: Dict):
        self.conn_params = conn_params

    def get_active_technologies(self) -> List[Dict]:
        query = """
        SELECT
            technology_id,            
            search_query
        FROM dim_technology_queries
        WHERE active = TRUE;
        """

        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

        technologies = [
            {
                "technology_id": row[0],                
                "search_query": row[1]
            }
            for row in rows
        ]

        logger.info(f"🔎 Tecnologías activas encontradas: {len(technologies)}")

        return technologies

    def get_one_active_technology(self, technology_id: str):
        query = """
        SELECT technology_id, search_query
        FROM dim_technology_queries
        WHERE active = TRUE
          AND technology_id = %s;
        """

        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (technology_id,))
                rows = cur.fetchall()

        return [
            {
                "technology_id": r[0],                
                "search_query": r[1]
            }
            for r in rows
        ]
