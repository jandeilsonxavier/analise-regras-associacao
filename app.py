import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Título da aplicação
st.title("Recomendações de Produtos")

# Carregar os datasets
df = pd.read_csv('sales_data.csv')

# Agrupar os produtos por pedido em uma única lista
basket = df.groupby('Order ID')['Product'].apply(list).reset_index()

# Converte as listas de produtos em um formato binário One-Hot Encoding, uma matriz onde 1 significa que o produto foi comprado no pedido).
te = TransactionEncoder()
te_data = te.fit(basket['Product']).transform(basket['Product'])
df_encoded = pd.DataFrame(te_data, columns=te.columns_)

# Gerar conjuntos de itens frequentes
frequent_itemsets = apriori(df_encoded, min_support=0.001, use_colnames=True)

# Gerar regras de associação
rules = association_rules(frequent_itemsets, metric='confidence',min_threshold=0.001, num_itemsets=2)

# Transformar conjuntos em strings para exibição mais clara
rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x)[0])
rules['consequents'] = rules['consequents'].apply(lambda x: list(x)[0])

lista_produtos = ['iPhone', 'Google Phone', 'USB-C Charging Cable', 'Wired Headphones']

produto_para_analise = st.selectbox(
    "Selecione o produto para análise:",
    (lista_produtos)
)

# Filtrar as regras de associação onde o produto está como antecedente
regras_produto = rules[rules['antecedents'] == produto_para_analise]

# Ordenar as regras por suporte em ordem decrescente e pegar os 5 primeiros produtos
regras_produto = regras_produto.sort_values(by='confidence', ascending=False).reset_index()

# Exibir os 5 primeiros produtos com maior suporte
st.dataframe(regras_produto[['consequents','support', 'confidence', 'lift']])

suporte = regras_produto['support'][0].astype(float).round(4)
confianca = regras_produto['confidence'][0].astype(float).round(4)
lift = regras_produto['lift'][0].astype(float).round(4)


st.write(f'''**Explicaçao da primeira linha da tabela:**   
        O valor do :blue[suporte] = {suporte} indica que há uma probabilidade de **{suporte*100:.2f}%** de os produtos 
        **"{produto_para_analise}"** e **"{regras_produto['consequents'][0]}"** serem comprados juntos em relação ao total de vendas.''')

st.write(f'''O valor da :blue[confiança] = {confianca} indica que, sempre que o produto **"{produto_para_analise}"** é comprado, 
        há uma probabilidade de **{confianca*100:.2f}%** de que o produto **"{regras_produto['consequents'][0]}"** também seja comprado.''')

st.write(f'''O valor do :blue[lift] = {lift} indica que a compra do produto **"{produto_para_analise}"** aumenta em **{lift:.2f}** vezes 
        a probabilidade de o produto **"{regras_produto['consequents'][0]}"** ser comprado, em comparação com uma compra aleatória.''')

st.divider()

# Calcula a frequência de cada 'Order ID'
pedidos_counts = df['Order ID'].value_counts()
pedidos_freq = pedidos_counts.value_counts()

# Calcula as porcentagens
percentagens = (pedidos_freq / pedidos_freq.sum()) * 100

# Junte as Series "pedidos_freq" e "percentagens"
produtos_por_pedido = pd.concat([pedidos_freq, percentagens.round(2).astype(str) + '%'], axis=1)

# Renomeie as colunas
produtos_por_pedido.columns = ['Frequencia', 'Porcentagem']

# Renomeie a coluna dos índices
produtos_por_pedido.index.name = 'Num. de produtos'

st.write(f'''**Conclusão**:   
         O dataset possui :blue[{df['Order ID'].nunique()}] pedidos, a quantidade de produtos por pedido está distribuido da seguinte forma:''')

st.dataframe(produtos_por_pedido)

st.write(f'''A análise revelou que :blue[96%] dos pedidos realizados na loja contêm apenas um produto. Esse dado é um indicador claro 
         do comportamento de compra predominante dos clientes, que tendem a adquirir itens de forma isolada.   
         Essa característica explica os baixos valores de suporte e confiança observados nas associações entre produtos, 
         já que a probabilidade de produtos serem comprados juntos é limitada pela ausência de itens adicionais na maioria dos pedidos.''')
