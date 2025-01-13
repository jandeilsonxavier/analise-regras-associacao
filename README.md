# Análise de Regras de Associação para Recomendação de Produtos

## Índice
1. [Descrição](#-descrição)
2. [Dataset](#-dataset)
3. [Ferramentas Utilizadas](#-ferramentas-utilizadas)
4. [Metodologia](#-metodologia)
5. [Resultados](#resultados)
6. [Próximos Passos](#-próximos-passos)
7. [Como Usar](#-como-executar)

## 📋 Descrição

🛒**Market Basket Analysis** é uma técnica amplamente utilizada por varejistas para identificar padrões e associações entre itens comprados em conjunto. Essa análise busca combinações de produtos que frequentemente aparecem juntas em transações, permitindo que os varejistas compreendam os relacionamentos entre os itens adquiridos por seus clientes. Essa abordagem é viabilizada por meio de regras de associação.

As **regras de associação** têm como objetivo encontrar elementos que implicam na presença de outros em uma mesma transação. Em outras palavras, elas identificam padrões frequentes e relacionamentos entre os conjuntos de dados. Essa técnica é aplicada tanto em mineração de dados quanto em aprendizado de máquina.

Em termos práticos, as regras de associação ajudam a descobrir relações entre itens em um conjunto de dados. Por exemplo, elas podem responder a perguntas como: "Se um cliente compra o produto A, qual é a probabilidade de ele também adquirir o produto B?"

**Métricas Importantes:**  
1. **Suporte (Support)**  
    Representa a frequência relativa com que dois produtos aparecem juntos nas transações totais. É uma proporção do total de vendas. É útil para identificar pares de produtos com alta popularidade conjunta.  

    $\text{Suporte} = \frac{\text{Número de transações com A e B}}{\text{Número total de transações}}$  
   
    Um suporte baixo pode indicar que a combinação de produtos não é muito comum, mesmo que tenha alta confiança ou lift. Quando você deseja promover produtos que já têm um volume significativo de vendas juntos.

2. **Confiança (Confidence):**  
   Representa a probabilidade de um produto ser comprado, dado que o outro foi comprado. É uma métrica condicional, útil para medir a força da relação entre dois produtos. 

   $\text{Confiança} = \frac{\text{Número de transações com A e B}}{\text{Número de transações com  A}}$

    Alta confiança indica que os clientes que compram o produto A têm grande probabilidade de comprar o produto B. Ideal quando o foco é em relações fortes e previsíveis para sugerir produtos altamente correlacionados.

   **Exemplo:** Se a confiança de "Se comprar A, então comprar B" é 0.8, significa que 80% dos clientes que compraram A também compraram B.

3. **Lift:**  
   Compara a probabilidade de os produtos serem comprados juntos com a probabilidade de serem comprados separadamente. Ela mede a força da relação entre A e B comparada ao que seria esperado por acaso.

   $\text{Lift} = \frac{\text{Confiança de A} \to B}{\text{Suporte de B}}$ 

   **Lift > 1:** Os itens têm uma associação positiva (mais provável de serem comprados juntos).  
   **Lift = 1:** Não há associação.  
   **Lift < 1:** Os itens têm uma associação negativa (menos provável de serem comprados juntos).

    Ideal quando o objetivo é descobrir associações surpreendentes ou não óbvias para promover combinações de produtos que têm potencial de venda conjunto, mesmo que não sejam os mais populares.

    **Exemplo:** Se o lift de "A + B" é 2.5, significa que os dois produtos são comprados juntos 2,5 vezes mais frequentemente do que o esperado pelo acaso.

**Apriori:**  
O **Apriori** é um dos algoritmos mais usados para encontrar conjuntos de itens frequentes e gerar regras de associação. Ele segue o princípio de que:
Se um conjunto de itens é frequente, todos os seus subconjuntos também são frequentes.

**Etapas do Apriori:**
1. **Gerar Conjuntos de Itens Frequentes:**
   - Ele começa analisando os itens individuais (ex.: "Camiseta Azul") e verifica se atendem a um suporte mínimo.
   - Depois, combina os itens em pares (ex.: {"Camiseta Azul", "Calça Jeans"}) e analisa novamente.

2. **Prune (Poda):**
   - Remove combinações que não atendem ao suporte mínimo, economizando tempo e recursos computacionais.

3. **Gerar Regras de Associação:**
   - Para cada conjunto de itens frequentes, o algoritmo calcula as métricas de confiança e lift para gerar regras como:  
     {"Camiseta Azul"} → {"Calça Jeans"}  
  
**Exemplo Prático:**  
| Transação | Itens Comprados                 |
|-----------|---------------------------------|
| 1         | {Camiseta Azul, Calça Jeans}    |
| 2         | {Tênis Esportivo, Calça Jeans}  |
| 3         | {Camiseta Azul, Tênis Esportivo}|
| 4         | {Camiseta Azul, Calça Jeans}    |

**Suporte:**
   - "Camiseta Azul" aparece em 3 transações (75% de suporte).

**Confiança:**
   - Dado que "Camiseta Azul" foi comprada, em 2 de 3 transações também foi comprada "Calça Jeans" (66.7% de confiança).

**Lift:**
   - Se "Calça Jeans" aparece em 50% das transações, o lift seria:  

     $\text{Lift} = \frac{0.667}{0.5} = 1.33$  

     Isso indica uma associação positiva.

## 📂 Dataset
Fonte: Dataset público no Kaggle referenta a vendas em uma Loja virtual. [link](https://www.kaggle.com/datasets/vincentcornlius/sales-orders?select=sales_data.csv)

## 🔧 Ferramentas Utilizadas
- Python (Pandas, Mlxtend, TransactionEncoder)
- Algoritmo Apriori
- Visualizações com Seaborn/Matplotlib

## 🧑‍🔬 Metodologia
1. **Pré-processamento**
- Agrupamento por número de pedido e criação de listas de produtos comprados juntos.
- Codificação binária das transações para uso no algoritmo Apriori.
2. **Geração de Regras**
- Aplicação do Apriori para identificar associações relevantes.
- Identificação de conjuntos frequentes de produtos.
- Geração de regras de associação com métricas de suporte, confiança e lift.
3. **Análise de Resultados**
- Foco em produtos específicos para identificar os itens mais fortemente associados.
4. **Implementação de Sistema Simples**
- Script para sugerir os 5 principais produtos relacionados ao item selecionado.

## Resultados
A análise revelou que 96% dos pedidos realizados na loja, durante o período analizado, contêm apenas um produto. Esse dado é um indicador claro do comportamento de compra predominante dos clientes, que tendem a adquirir itens de forma isolada. Essa característica explica os baixos valores de suporte e confiança observados nas associações entre produtos, já que a robabilidade de produtos serem comprados juntos é limitada pela ausência de itens adicionais na maioria dos pedidos.

| Qtd. Itens|Qtd. Pedidos |Porcentagem|
|-----------|-------------|-----------|
| 1         | 171301      |96.0%      |
| 2         | 6778        |3.8%       |
| 3         | 340         |0.19%      |
| 4         | 17          |0.01%      |
| 5         | 1           |0.0%       |

## 🚀 Próximos Passos
- **Automatização do Fluxo de Dados:** Desenvolver APIs que integrem o sistema de análise de vendas diretamente com o ERP ou com a loja.
- **Monitoramento em Tempo Real:** Habilitar a atualização em tempo real dos dados para oferecer insights instantâneos sobre tendências de compra e desempenho de produtos.
- **Testes A/B de Sugestões:** Realizar experimentos controlados para avaliar o impacto das recomendações sobre as taxas de conversão e o ticket médio.

## 💻 Como Executar

1. **Clone este repositório**
```bash
git clone https://github.com/jandeilsonxavier/analise-regras-associacao.git
cd restaurants-service-repository
```
2. **Crie o ambiente virtual**
```bash
python -m venv venv
```
3. **Ative o ambiente virtual**
```bash
No Windows:
venv\Scripts\activate

No Mac/Linux:
source venv/bin/activate
```
4. **Instale as dependências**
```bash
pip install -r requirements.txt
```
5. **Execute o script principal**
```bash
python run.py
```
