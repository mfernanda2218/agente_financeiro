import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndicadoresDatabase:
    """Classe para consultar indicadores econômicos do PostgreSQL."""
    
    def __init__(self):
        """Inicializa a conexão com o banco de dados."""
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.db_name = os.getenv('DB_NAME', 'bd_pipeline_etl')
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_password = os.getenv('DB_PASSWORD', '')
        
        # String de conexão
        self.connection_string = (
            f'postgresql://{self.db_user}:{self.db_password}@'
            f'{self.db_host}:{self.db_port}/{self.db_name}'
        )
        
        self.engine = None
        self._connect()
    
    def _connect(self):
        """Estabelece conexão com o banco."""
        try:
            self.engine = create_engine(self.connection_string)
            logger.info("Conexão com banco de dados estabelecida.")
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco: {e}")
            self.engine = None
    
    def get_ultimos_indicadores(self, dias=30):
        """
        Obtém os indicadores dos últimos N dias.
        
        Args:
            dias: Número de dias para consultar (padrão: 30)
        
        Returns:
            DataFrame com os indicadores
        """
        if not self.engine:
            logger.error("Sem conexão com o banco.")
            return pd.DataFrame()
        
        try:
            data_corte = datetime.now() - timedelta(days=dias)
            query = text("""
                SELECT 
                    data_referencia,
                    indicador,
                    valor,
                    data_extracao
                FROM indicadores_economicos
                WHERE data_referencia >= :data_corte
                ORDER BY data_referencia DESC, indicador
            """)
            
            with self.engine.connect() as conn:
                df = pd.read_sql(query, conn, params={'data_corte': data_corte})
            
            logger.info(f"Carregados {len(df)} registros de indicadores.")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao consultar indicadores: {e}")
            return pd.DataFrame()
    
    def get_indicador_atual(self, indicador_nome):
        """
        Obtém o valor mais recente de um indicador específico.
        
        Args:
            indicador_nome: Nome do indicador (SELIC_META_ANUAL, IPCA_MENSAL)
        
        Returns:
            Dicionário com o valor mais recente
        """
        if not self.engine:
            return None
        
        try:
            query = text("""
                SELECT 
                    data_referencia,
                    indicador,
                    valor,
                    data_extracao
                FROM indicadores_economicos
                WHERE indicador = :indicador
                ORDER BY data_referencia DESC
                LIMIT 1
            """)
            
            with self.engine.connect() as conn:
                result = conn.execute(query, {'indicador': indicador_nome})
                row = result.fetchone()
            
            if row:
                return {
                    'data_referencia': row[0].strftime('%Y-%m-%d'),
                    'indicador': row[1],
                    'valor': float(row[2]),
                    'data_extracao': row[3].strftime('%Y-%m-%d %H:%M:%S')
                }
            return None
            
        except Exception as e:
            logger.error(f"Erro ao consultar {indicador_nome}: {e}")
            return None
    
    def get_selic_atual(self):
        """Obtém a Selic mais recente."""
        return self.get_indicador_atual('SELIC_META_ANUAL')
    
    def get_ipca_atual(self):
        """Obtém o IPCA mais recente."""
        return self.get_indicador_atual('IPCA_MENSAL')
    
    def get_todos_indicadores_recentes(self):
        """Retorna um dicionário com todos os indicadores recentes."""
        selic = self.get_selic_atual()
        ipca = self.get_ipca_atual()
        
        return {
            'selic': selic['valor'] if selic else None,
            'selic_data': selic['data_referencia'] if selic else None,
            'ipca': ipca['valor'] if ipca else None,
            'ipca_data': ipca['data_referencia'] if ipca else None,
            'data_consulta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def get_historico_indicador(self, indicador_nome, limite=12):
        """
        Obtém o histórico de um indicador.
        
        Args:
            indicador_nome: Nome do indicador
            limite: Número máximo de registros (padrão: 12)
        
        Returns:
            DataFrame com histórico
        """
        if not self.engine:
            return pd.DataFrame()
        
        try:
            query = text("""
                SELECT 
                    data_referencia,
                    valor,
                    data_extracao
                FROM indicadores_economicos
                WHERE indicador = :indicador
                ORDER BY data_referencia DESC
                LIMIT :limite
            """)
            
            with self.engine.connect() as conn:
                df = pd.read_sql(query, conn, params={
                    'indicador': indicador_nome,
                    'limite': limite
                })
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao consultar histórico: {e}")
            return pd.DataFrame()