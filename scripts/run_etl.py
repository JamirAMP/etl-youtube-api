from src.config import Config
from src.youtube_api import YouTubeAPI
from src.postgres_loader import PostgresLoader
from src.repositories.technology_repository import TechnologyRepository
from src.repositories.year_control_repository import YearControlRepository
from src.transformers.clean_data import CleanData
from src.services.etl_service import YouTubeETLService
import logging
import sys

logging.basicConfig(level=logging.INFO)

def main(technology_id: str | None = None, year=None):

    youtube_api = YouTubeAPI(Config.YOUTUBE_API_KEY)

    loader = PostgresLoader(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )

    # Crear tablas si no existen
    loader.create_tables()

    conn_params = {
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
        "dbname": Config.DB_NAME,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD
    }

    tech_repo = TechnologyRepository(conn_params)
    year_control = YearControlRepository(conn_params)

    # Si no se especifica año, obtener el próximo pendiente
    if year is None:
        year = year_control.get_next_year()
        if year is None:
            logging.error("❌ No hay años pendientes para procesar. Todos los años están completos.")
            sys.exit(0)
    
    logging.info(f"🎯 Procesando año: {year}")

    cleaner = CleanData()

    etl = YouTubeETLService(
        video_extractor=youtube_api,
        comment_extractor=youtube_api,
        channel_extractor=youtube_api,
        loader=loader,
        cleaner=cleaner
    )

    if technology_id:
        technologies = tech_repo.get_one_active_technology(technology_id)
    else:
        technologies = tech_repo.get_active_technologies()
    
    if not technologies:
        logging.error("❌ No se encontraron tecnologías activas para procesar")
        sys.exit(1)
        
    logging.info(f"📋 Tecnologías a procesar: {len(technologies)} queries con {len(set(t['technology_id'] for t in technologies))} tecnologías únicas")

    settings = {
        "max_videos": Config.MAX_VIDEOS,
        "max_comments": Config.MAX_COMENTARIOS,
        "extract_comments": Config.EXTRACT_COMMENTS
    }

    try:
        etl.run(technologies, settings, year=year)
        
        # Marcar el año como procesado solo si:
        # 1. No se especificó manualmente como argumento
        # 2. No es el año actual (ya que el año actual aún no termina)
        from datetime import datetime
        current_year = datetime.now().year
        
        if sys.argv[2:3] == [] and year != current_year:  # No se pasó year como argumento y no es el año actual
            year_control.mark_year_as_processed(year)
            logging.info(f"✅ ETL completado exitosamente para el año {year} (marcado como procesado)")
        else:
            if year == current_year:
                logging.info(f"✅ ETL completado exitosamente para el año {year} (NO marcado como procesado - año en curso)")
            else:
                logging.info(f"✅ ETL completado exitosamente para el año {year}")
    except Exception as e:
        logging.error(f"❌ Error durante el ETL del año {year}: {e}")
        raise

if __name__ == "__main__":
    tech_id = sys.argv[1] if len(sys.argv) > 1 else None
    year = int(sys.argv[2]) if len(sys.argv) > 2 else None
    main(tech_id, year)