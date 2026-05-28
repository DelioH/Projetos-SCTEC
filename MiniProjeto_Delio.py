# Script para análise da base de Vendas
# Mini Projeto

import pandas as pd
import openpyxl

# Importando os dados
# Usando separador ;
caminho = "MOD1_SEM7_MiniProjeto\dados\Base_Varejo.csv"
df_varejo = pd.read_csv(caminho, sep=";")

# Mostrar os primeiros registors (por padrão, 5)
print(df_varejo.head())
# Mostra os ultimos registro (por padrão, 5)
print(df_varejo.tail())
#mostrar informações (tipos de dados)
print(df_varejo.info())
# disposição    
print(df_varejo.shape)
# Mostrar todas as colunas já que nãoestão aparecendo todas
print("Lista de Colunas")
print(df_varejo.columns.tolist())
for col in df_varejo.columns:
    print(col)

# Verificar quantos NaN tem nas colunas 10, 11, 12 e 13 prá ver se tem algum dado.
# Caso contrário excluir essas colunas
print("Quantidade de NaN nas colunas 10, 11, 12 e 13")
print(df_varejo["Unnamed: 10"].isna().sum())
print(df_varejo["Unnamed: 11"].isna().sum())
print(df_varejo["Unnamed: 12"].isna().sum())
print(df_varejo["Unnamed: 13"].isna().sum())

# Verificado que nas colunas não nomeadas 10, 11, 12 e 13 a quantidade de Nan é a mesma
# quantidade de registros (830000), excluir essas colunas. Usar a função que exclui todas
# as colunas que só tem valores NaN
df_varejo = df_varejo.dropna(axis=1, how="all")

# verificar se as colunas foram removidas
print(df_varejo.head())





# Escreve os dados no arquivo de destino
df_varejo.to_csv(r"MOD1_SEM7_MiniProjeto\df_limpo.csv", index=False)