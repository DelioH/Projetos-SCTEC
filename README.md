# Projetos-SCTEC

Este é um projeto que foi escrito para fazer uma limpeza em um conjunto de dados de vendas, estruturado da seguinte forma:
DATA: Data da compra;
CO_ID: Identificação do número de compra (número da nota fiscal);
CL_ID: Identificação do cliente (número do cliente);
CL_GENERO: Sexo biológico informado pelo cliente;
CL_EC: Estado civil do cliente:
1: Casado ou união estável;
2: Divorciado;
3: Separado;
4: Solteiro;
5: Viúvo.
CL_FHL: Número de filhos do cliente;
CL_SEG: Segmentação econômica do cliente (classe A, B ou C);
PR_ID: Código do produto (SKU) adquirido;
PR_CAT: Categoria do produto adquirido;
PR_NOME: Nome do produto adquirido.

O arquivo lido tem o nome: Base_Varejo.csv e está na pasta dados.

Os seguintes passos foram realizados para limpeza e extração dos dados:
1 - Avaliação dos dados

2 - Validação e exclusão de colunas sem nenhum valor

3 - Validação de duplicatas - Na análise, foram identificadas várias colunas duplicadas; porém, pelo formato dos registros identificado (ausência do campo quantidade), foram mantidas essas duplicatas por entender que elas suprem a ausência de um campo quantidade. Ou seja, se tem 2 linhas iguais, significa a venda de 2 produtos e assim por diante. Foi criada uma coluna contagem, contendo a quantidade que os registros se repetem e a coluna 'duplicata' eu exibe 1 caso a coluna tenha duplicata e 0 caso não possua.

4 - Ajuste dos tipos de dados - Foi ajustado o campo 'DATA' para o formato datetime e, todas as colunas com formato int64 que não representavam dados numéricos foram convertidos para o formato string.

5 - Verificando inconsistências de dados - Como existiam para cada produto e para cada cliente as descrições do mesmo, foi verificado se existiam dados divergentes. Exemplo: Cliente com ID igual, porém sexo diferente ou quantidade de filhos diferentes, e assim por diante. 

6 - Gerados dados estatísticos - Foram gerados dados estatísticos com a coluna 'CL_FHL' já que a mesma apresentava dados numéricos.

7 - Agrupamento de dados - Foram gerados alguns agrupamentos de dados para entender melhor a base, sendo: Quantidade de vendas por cliente, Genero por clientes cadastrados, Quantidade de itens vendidos por genero de cliente, Quantidade de itens comprados por quantidade de filhos.

Para cada passo executado, foi adicionado um cabeçalho e ao final uma pequena análise. Para cada etapa, o script pára afim de ser visualizado por quem estiver executando o script, bastando um <enter> para ir para o próximo passo.

Ao fim, foi gerado um novo arquivo chamado df_limpo.csv na pasta dados.


Insights obtidos:
Considerações sobre a base e melhorias:
- Base possuía 3 colunas sem nenhum dado (Essa informação não constava na documentação). Os dados foram excluídos, mas deve-se atentar a próxima carga de dados se estas colunas virão, pois pode gerar erro no código caso não virem.
- Esta base deveria ter sido divida em 3 tabelas separadas: Vendas, Clientes e produtos (para evitar repetição de dados). Validar com o gestor da base se a informação vem assim mesmo; caso sim, fazer a divisão das colunas (tabela dimensão: produtos, tabela dimensão: clientes e tabela fato: vendas). Desta forma economizamos espaço de armazenamento de dados (parando de repetir os dados), além de evitarmos inconsistências - que foram analisadas no script.
- Não há campo quantidade; ou seja, se o cliente precisar comprar mais do mesmo produto, deverão ser criados 2 ou mais registros (de acordo com a quantidade). Validar com o gestor da base essa sobre informação. Caso ela não exista mesmo e, considerando que existe um sistema gerando esses dados fazer testes para validar o comportamente do mesmo. Fazer um teste de venda com 3 produtos, 2 duplicados: 1 na sequencia, e outro com um produto diferente entre a duplicata. 
- Melhorias na análise: Utilização de algoritmos para identificar correlações entre dados e entender alguns padrões.