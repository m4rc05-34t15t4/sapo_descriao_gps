import psycopg2
import csv

# Lista de bancos de dados
db_list = [
    'v_1370-2-SE', 
    'v_1370-2-SO', 
    'v_1370-4-NO', 
    'v_1370-4-SE', 
    'v_1370-4-SO',
    'v_1371-3-SE',
    'v_1371-3-SO'
]  # Atualize com os nomes dos bancos reais

# Parâmetros de conexão (atualize conforme necessário)
conn_params = {
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',  # ou outro host
    'port': '5432'
}

# Função para conectar e executar a query em cada banco de dados
def execute_query_in_db(db_name, query, conn_params):
    try:
        conn = psycopg2.connect(dbname=db_name, **conn_params)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Erro ao conectar ou executar a query no banco {db_name}: {e}")
        return []

# Função principal para executar a query em cada banco e gerar o CSV
def generate_csv_for_multiple_dbs(db_list, query, conn_params, output_csv):
    # Define os cabeçalhos do CSV
    csv_headers = ["nome", "tipo", "classe", "banco"]

    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers)

        for db_name in db_list:
            # Executa a query no banco de dados atual
            results = execute_query_in_db(db_name, query, conn_params)

            # Adiciona o nome do banco a cada linha dos resultados
            for row in results:
                writer.writerow(list(row) + [db_name])

    print(f"CSV gerado com sucesso: {output_csv}")

# Query SQL fornecida
query = """
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'centroide_elemento_hidrografico_p' AS classe FROM edgv.centroide_elemento_hidrografico_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'centroide_ilha_p' AS classe FROM edgv.centroide_ilha_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'centroide_limite_especial_p' AS classe FROM edgv.centroide_limite_especial_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'centroide_massa_dagua_p' AS classe FROM edgv.centroide_massa_dagua_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'cobter_massa_dagua_a' AS classe FROM edgv.cobter_massa_dagua_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'constr_area_uso_especifico_a' AS classe FROM edgv.constr_area_uso_especifico_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'constr_deposito_a' AS classe FROM edgv.constr_deposito_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'constr_deposito_p' AS classe FROM edgv.constr_deposito_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'constr_edificacao_a' AS classe FROM edgv.constr_edificacao_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'constr_edificacao_p' AS classe FROM edgv.constr_edificacao_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'constr_extracao_mineral_a' AS classe FROM edgv.constr_extracao_mineral_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'constr_extracao_mineral_p' AS classe FROM edgv.constr_extracao_mineral_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'constr_ocupacao_solo_a' AS classe FROM edgv.constr_ocupacao_solo_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'constr_ocupacao_solo_l' AS classe FROM edgv.constr_ocupacao_solo_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'constr_ocupacao_solo_p' AS classe FROM edgv.constr_ocupacao_solo_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_elemento_fisiografico_a' AS classe FROM edgv.elemnat_elemento_fisiografico_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_elemento_fisiografico_l' AS classe FROM edgv.elemnat_elemento_fisiografico_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_elemento_fisiografico_p' AS classe FROM edgv.elemnat_elemento_fisiografico_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_elemento_hidrografico_a' AS classe FROM edgv.elemnat_elemento_hidrografico_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_elemento_hidrografico_l' AS classe FROM edgv.elemnat_elemento_hidrografico_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_elemento_hidrografico_p' AS classe FROM edgv.elemnat_elemento_hidrografico_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_ilha_a' AS classe FROM edgv.elemnat_ilha_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_ilha_p' AS classe FROM edgv.elemnat_ilha_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_toponimo_fisiografico_natural_l' AS classe FROM edgv.elemnat_toponimo_fisiografico_natural_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_toponimo_fisiografico_natural_p' AS classe FROM edgv.elemnat_toponimo_fisiografico_natural_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'elemnat_trecho_drenagem_l' AS classe FROM edgv.elemnat_trecho_drenagem_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_alteracao_fisiografica_antropica_l' AS classe FROM edgv.infra_alteracao_fisiografica_antropica_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_barragem_a' AS classe FROM edgv.infra_barragem_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_barragem_l' AS classe FROM edgv.infra_barragem_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_elemento_energia_a' AS classe FROM edgv.infra_elemento_energia_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_elemento_energia_l' AS classe FROM edgv.infra_elemento_energia_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_elemento_energia_p' AS classe FROM edgv.infra_elemento_energia_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_elemento_infraestrutura_a' AS classe FROM edgv.infra_elemento_infraestrutura_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_elemento_infraestrutura_l' AS classe FROM edgv.infra_elemento_infraestrutura_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_elemento_infraestrutura_p' AS classe FROM edgv.infra_elemento_infraestrutura_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_elemento_viario_l' AS classe FROM edgv.infra_elemento_viario_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_elemento_viario_p' AS classe FROM edgv.infra_elemento_viario_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_ferrovia_l' AS classe FROM edgv.infra_ferrovia_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_mobilidade_urbana_l' AS classe FROM edgv.infra_mobilidade_urbana_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_pista_pouso_a' AS classe FROM edgv.infra_pista_pouso_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_pista_pouso_l' AS classe FROM edgv.infra_pista_pouso_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_pista_pouso_p' AS classe FROM edgv.infra_pista_pouso_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_travessia_hidroviaria_l' AS classe FROM edgv.infra_travessia_hidroviaria_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_trecho_duto_l' AS classe FROM edgv.infra_trecho_duto_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'infra_via_deslocamento_l' AS classe FROM edgv.infra_via_deslocamento_l WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'llp_limite_especial_a' AS classe FROM edgv.llp_limite_especial_a WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome UNION 
SELECT TRIM(nome) AS nome, MIN(tipo) AS tipo, 'llp_localidade_p' AS classe FROM edgv.llp_localidade_p WHERE NOT TRIM(nome) IS NULL AND LENGTH(TRIM(nome)) >= 3 GROUP BY nome
ORDER BY CLASSE, NOME;
"""

# Nome do arquivo CSV de saída
output_csv = 'resultado_query.csv'

# Executa o script
generate_csv_for_multiple_dbs(db_list, query, conn_params, output_csv)
