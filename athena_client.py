import pandas as pd
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor

REGION = 'us-east-1'
S3_STAGING = 's3://sus-data-pipeline-kvgs/athena-results/'
DATABASE = 'sus_pipeline'

def query(sql: str) -> pd.DataFrame:
    conn = connect(
        region_name=REGION,
        s3_staging_dir=S3_STAGING,
        schema_name=DATABASE,
        cursor_class=PandasCursor
    )
    return conn.cursor().execute(sql).as_pandas()

def get_internacoes_por_ano():
    return query("SELECT * FROM internacoes_por_ano ORDER BY ano")

def get_internacoes_por_cid():
    return query("SELECT * FROM internacoes_por_cid ORDER BY ano, total_internacoes DESC")

def get_saude_mental_municipios(ano='2023'):
    return query(f"""
        SELECT * FROM saude_mental_municipios
        WHERE ano = '{ano}'
        AND populacao_total > 0
    """)

def get_atendimentos_por_ano():
    return query("SELECT * FROM atendimentos_por_ano ORDER BY ano")

def get_suicidios_por_ano():
    return query("""
        SELECT ano, SUM(total_suicidios) as total_suicidios,
               SUM(total_masculino) as masculino,
               SUM(total_feminino) as feminino,
               SUM(por_enforcamento) as enforcamento,
               SUM(por_arma_fogo) as arma_fogo
        FROM suicidios_por_ano
        GROUP BY ano ORDER BY ano
    """)