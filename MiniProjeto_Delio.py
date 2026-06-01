# Script para análise da base de Vendas
# Mini Projeto

import pandas as pd
import openpyxl

# Importando os dados
# Usando separador ;
caminho = "dados\\Base_Varejo.csv"
df_varejo = pd.read_csv(caminho, sep=";")
"""
Colunas da base:
['DATA', 'CO_ID', 'CL_ID', 'CL_GENERO', 'CL_EC', 'CL_FHL', 'CL_SEG', 'PR_ID', 
'PR_CAT', 'PR_NOME', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13']
"""

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
# Verificar se as colunas foram removidas
print(df_varejo.head())
# Colunas foram removidas com sucesso

# Validar quantas duplicas existem. Considerando somente as colunas chaves que são:
# DATA  CO_ID  CL_ID PR_ID
# Importante, a base não possui uma coluna com a quantidade de itens, logo, se o cliente comprar mais de um item,
# a base irá criar uma duplicata. Então, será contabilizada a quantidade de duplicatas e será criado uma coluna
# chamada 'duplicata', que irá assumir 1 caso a linha seja duplicada ou 0 quando não.
print("Duplicatas reais: ")
duplicatas=(df_varejo
      .groupby(['DATA','CO_ID','CL_ID','PR_ID'])
      .size()
      .reset_index(name='contagem'))
duplicatas_reais = duplicatas[duplicatas['contagem'] >= 2]
print(duplicatas_reais)
# Verificado que existem registro com mais de 2 duplicatas. Criar, além da coluna duplicata, a coluna contagem
# que irá informar quantas duplicatas existem da mesma
# Criar um dataframe com as contagens:
contagens = (
    df_varejo
    .groupby(['DATA', 'CO_ID', 'CL_ID', 'PR_ID'])
    .size()
    .reset_index(name='contagem')
)
print(contagens)
# Juntar ao dataframe original
df_varejo = df_varejo.merge(
    contagens,
    on=['DATA', 'CO_ID', 'CL_ID', 'PR_ID'],
    how='left'
)
# Criar a coluna 'contagem' e incluir a mesma no dataframe
df_varejo['duplicata'] = df_varejo['contagem'].apply(lambda x: 1 if x >= 2 else 0)

# Ajuste de tipos de dados
# Verificar os tipos de dados
df_varejo.info()
# Ajustar a data no formato datetime
df_varejo['DATA'] = pd.to_datetime(df_varejo['DATA'], format='%d/%m/%Y', errors='coerce')
# Com exceção da coluna CL_FHL, do campo DATA e das colunas que foram criadas,
# o restante dos campos que estão como inteiro devem ser convertidos
# para string. Campos a serem convertidos: CO_ID, CL_ID, CL_EC, PR_ID
colunas = ['CO_ID', 'CL_ID', 'CL_EC', 'PR_ID']
df_varejo[colunas] = df_varejo[colunas].astype(str)
# Validando se foi convertido.
df_varejo.info()
# Validando como ficaram os dados
print(df_varejo.head())

# Como a base atual tem os campos descritivos de clientes e de produtos, validar se existe alguma inconsistência nos dados. Exemplo:
# Cliente com ID igual, porém sexo diferente ou quantidade de filhos diferentes, e assim por diante.
# Detectar inconsistencias de dados de clientes
inconsistencias_cli = (
    df_varejo
    .groupby('CL_ID')
    .agg({
        'CL_GENERO': 'nunique',
        'CL_EC': 'nunique',
        'CL_FHL': 'nunique',
        'CL_SEG': 'nunique'
    })
)
#Exibir inconsistencias (caso qualquer um dos campos descritivos de clientes for maior que 1)
clientes_inconsistentes = inconsistencias_cli[
    (inconsistencias_cli['CL_GENERO'] > 1) |
    (inconsistencias_cli['CL_EC'] > 1) |
    (inconsistencias_cli['CL_FHL'] > 1) |
    (inconsistencias_cli['CL_SEG'] > 1)
]
print("Clientes inconscistentes: ")
print(clientes_inconsistentes)
# Verificado que não há inconsistencias

# Detectar inconsistencias de dados de produtos
inconsistencias_prod = (
    df_varejo
    .groupby('PR_ID')
    .agg({
        'PR_CAT': 'nunique',
        'PR_NOME': 'nunique'
    })
)
#Exibir inconsistencias (caso qualquer um dos campos descritivos de clientes for maior que 1)
produtos_inconsistentes = inconsistencias_prod[
    (inconsistencias_prod['PR_CAT'] > 1) |
    (inconsistencias_prod['PR_NOME'] > 1)
]
print("Produtos Inconsistentes: ")
print(produtos_inconsistentes)
# Verificado que não há inconsistencias.

# Agora que já temos os dados validados quanto a consistencia (clientes e produtos), gerar estatísticas (utilizar os dados numéricos)
print(df_varejo['CL_FHL'].describe())
# Considerando os dados estatístico,
# o máximo de número de filhos é 4,
# a média é 1,15 (mean)
# tem pessoas sem filhos,
# Pelo menos metade dos clientes não tem filhos (mediana)

# Agora vou agrupar os dados para explorar melhor os dados
# Antes de fazer os agrupamentos por genero, classe social, vamos fazer um agrupamento por cliente e quantidade de vendas, pois clientes
# que compram muito podem distorcer os dados (dependendo da pergunta que iremos fazer). E também assim entendemnos melhor o negócio.
# Vendas por cliente
vendas_unicas = (
    df_varejo[['CL_ID', 'CO_ID']]
    .drop_duplicates()
    .groupby('CL_ID')
    .size()
    .reset_index(name='qtd_vendas')
    .sort_values('qtd_vendas', ascending=False)
)

print(vendas_unicas)
# O cliente que tem mais vendas, é o cliente com id 41, e tem 34 vendas, e o cliente que tem menos vendas, tem 7 vendas.
# Considerando a distorção que eu achei que poderia ter, na verdade ela está mais relacionada ao tipo de pergunta que irei fazer:
# Se é sobre vendas ou se é sobre clientes. Quando eu falo de vendas, e perfil dos clientes das vendas, ele sempre vai ser puxado pelos 
# clientes que tiveram mais compras. Mas quando eu falo de clientes, e perfis deles, mesmo que o cliente tenha feito 34 vendas como é o 
# caso do cliente 41, a quantidade de vendas dele não altera o meu resultado. Dito isto, vamos as perguntas:
# Quem são os clientes cadastrados? Mais homens ou mulheres?
clientes_unicos = df_varejo.drop_duplicates(subset='CL_ID')

clientes_por_genero = (
    clientes_unicos
    .groupby('CL_GENERO')
    .size()
    .reset_index(name='qtd_clientes')
    .sort_values('qtd_clientes', ascending=False)
)

print(clientes_por_genero)
# Agora percentual
percentual_clientes = (
    clientes_unicos['CL_GENERO']
    .value_counts(normalize=True) * 100
)
print(percentual_clientes)
# Resultado: 52,9% Mulheres, 48,1% Homens

# Tem mais clientes homens que mulheres.
# E agora sim, falando em vendas:
# Quem compra mais itens: homens ou mulheres? (aqui vamos levar em consideração os itens separados)
itens_por_genero = (
    df_varejo
    .groupby('CL_GENERO')
    .size()
    .reset_index(name='qtd_itens')
    .sort_values('qtd_itens', ascending=False)
)

print(itens_por_genero)

# Agora em percentual prá ter uma melhor noção
percentual_vendas = (
    df_varejo['CL_GENERO']
    .value_counts(normalize=True) * 100
)
print(percentual_vendas)
# Resultado: 52,3% para Homens e 47,7% para Mulheres
# Considerando a comparação de quantidade de homens e mulheres cadastrados com a quantidade de itens vendidos por homens e mulheres, os
# valores se inverteram, mas ambos ficaram próximos de 50%.

# Agora, uma dúvida: dos que compraram, a quantidade comprada tem alguma relação com a quantidade de filhos?
# Etapa 1 - quantidade de itens que cada cliente comprou
itens_por_cliente = (
    df_varejo
    .groupby('CL_ID')
    .size()
    .reset_index(name='qtd_itens')
)

# Etapa 2 - quantidade de números de filhos
clientes_unicos = df_varejo[['CL_ID', 'CL_FHL']].drop_duplicates(subset='CL_ID')

# Etapa 3 - Juntar as 2 informações
df_clientes = itens_por_cliente.merge(clientes_unicos, on='CL_ID', how='left')


# Etapa final - agrupar por quantidade defilhos
itens_por_filhos = (
    df_clientes
    .groupby('CL_FHL')['qtd_itens']
    .sum()
    .reset_index()
    .sort_values('qtd_itens', ascending=False)
)
print(itens_por_filhos)
# analise


# vendas por data






# verificado que temos 1.000
# Verificar qtde de itens por venda





















"""
Considerações sobre a base e melhorias
- Base possuía 3 colunas sem nenhum dado
- Esta base deveria ter sido divida em 3 tabelas separadas: Vendas, Clientes e produtos (para evitar a dados repetidos). Validar com o gestor da base
se a informação vem assim mesmo; caso sim, fazer a divisão das colunas (tabela dimensão: produtos, tabela dimensão: clientes e tabela fato: vendas).
Desta forma economizamos espaço de armazenamento de dados (parando de repetir os dados)
- Não há campo quantidade; ou seja, se o cliente precisar comprar mais do mesmo produto, deverão ser criados 2 ou mais registros (de acordo com a quantidade).
Validar com o gestor da base essa informação, caso ela não a tenha e considerando que existe um sistema que gere esses dados,
Fazer um teste de venda com 3 produtos, 2 duplicados: 1 na sequencia, e outro com um produto diferente entre a duplicata.
"""






# Escreve os dados no arquivo de destino
df_varejo.to_csv(r"dados\df_limpo.csv", index=False)