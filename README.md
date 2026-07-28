# 🛒 Análise de Dados e Cotação de Produtos em Tempo Real (Leroy Merlin)

Este projeto realiza a **coleta, monitoramento e análise de preços em tempo real** de produtos no e-commerce da Leroy Merlin. O sistema automatiza o acompanhamento de variações de preços, permitindo comparações temporais e auditorias detalhadas para suporte na tomada de decisões comerciais e estratégicas de precificação.

---

## 💡 Valor Agregado para as Empresas

A automação de monitoramento de preços (Price Intelligence) traz vantagens competitivas diretas para negócios do varejo, distribuidores e compradores corporativos:

* **Inteligência de Mercado e Precificação Dinâmica:** Permite acompanhar a variação de preços da concorrência/fornecedores para reajustes ágeis de tabela e estratégias de *pricing*.
* **Auditoria e Transparência em Compras:** Cria um histórico auditável de cotações para garantir que suprimentos e materiais sejam adquiridos na melhor janela de oportunidade.
* **Economia de Tempo e Escala:** Substitui o processo manual e suscetível a erros de pesquisa de preços por rotinas automatizadas em Python.
* **Detecção de Tendências e Promoções:** Identifica rapidamente variações percentuais e ofertas, otimizando o orçamento de compras.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Análise e Manipulação de Dados:** `pandas`, `numpy`
* **Visualização de Dados:** `matplotlib`, `seaborn`
* **Armazenamento e Exportação:** Arquivos estruturados em CSV

---

## ⚙️ Funcionalidades do Projeto

* **Consulta e Coleta de Valores:** Scripts focados na busca e extração de cotações atualizadas.
* **Comparação Temporal de Preços:**
  * Comparativo de preços entre períodos distintos (ex: variação observada entre 20 e 25 de julho).
  * Cálculo automatizado da variação percentual dos produtos monitorados.
* **Base de Dados Auditável:** Exportação de planilhas de cotações com registros estruturados para auditoria.
* **Geração Automática de Gráficos Analíticos:**
  * **Gráfico Comparativo de Valores:** Comparação direta de preços entre datas/produtos.
  * **Gráfico de Variação Percentual:** Destaque para altas e baixas de preço no período.
  * **Visualização Auditável de Cotações:** Gráficos prontos para apresentação em relatórios comerciais.

---

## 📁 Estrutura de Arquivos Principais

```text
.
├── ConsultaValores.py                 # Script para coleta/consulta dos preços
├── ComparacaoPreços.py                # Script para cruzamento e comparação de preços
├── codigo.py / codigo2.py / ...       # Scripts complementares de análise e automação
├── cotacao_leroy_20_vs_25_julho.csv   # Base comparativa de preços entre períodos
├── cotacao_leroy_auditavel.csv        # Histórico de cotações formatado para auditoria
├── grafico_comparativo_valores.png    # Gráfico com comparação direta de preços
├── grafico_variacao_percentual.png    # Gráfico destacando oscilações percentuais
└── grafico_cotacao_auditavel.png      # Visualização consolidada para relatórios


O repositório **[Projeto-1-Cota-o-em-tempo-real-de-produtos-da-Leroy-Merlin](https://github.com/Daniel010203/Projeto-1-Cota-o-em-tempo-real-de-produtos-da-Leroy-Merlin.git)** foi construído para realizar a **automação de coleta, comparação e análise visual de preços de produtos** no e-commerce da Leroy Merlin.

Abaixo está a explicação detalhada do funcionamento dos componentes e do fluxo do código:

---

## ⚙️ Arquitetura e Fluxo do Código

O projeto combina scripts de extração de dados com scripts de análise temporal e plotagem gráfica:

```text
  1. Consulta / Coleta            2. Processamento & Cruzamento           3. Análise Visual
  ┌──────────────────────┐        ┌───────────────────────────┐         ┌───────────────────────┐
  │ ConsultaValores.py   │ ─────> │ ComparacaoPreços.py       │ ──────> │ Plotagem de Gráficos  │
  └──────────────────────┘        └───────────────────────────┘         └───────────────────────┘
             │                                  │                                   │
             ▼                                  ▼                                   ▼
  (Coleta cotações atuais)       (Calcula variação % entre     (Gera relatórios em imagem)
                                  datas: ex. 20 vs 25 de Julho)

```

---

## 🔍 Detalhamento dos Arquivos e Scripts

### 1. Coleta de Preços (`ConsultaValores.py`)

* **O que faz:** Realiza a busca/extração das cotações atualizadas dos produtos diretamente da fonte.
* **Como funciona:** Coleta os nomes e valores dos produtos e organiza esses registros em uma tabela estruturada.

### 2. Comparação Temporal (`ComparacaoPreços.py`)

* **O que faz:** Cruza bases de cotações obtidas em datas distintas (por exemplo, os arquivos `cotacao_leroy_20_vs_25_julho.csv` e `cotacao_leroy_auditavel.csv`).
* **Como funciona:**
* Utliza `pandas` para ler e mesclar (*merge/join*) as bases por produto.
* Calcula a variação bruta (diferença em R$) e a variação percentual (%) no preço de cada item entre as duas datas.



### 3. Visualização de Dados e Relatórios (`codigo.py`, `codigo2.py`, etc.)

* **O que faz:** Transforma os dados comparativos em gráficos analíticos prontos para relatórios comerciais.
* **Como funciona:**
* Utiliza `matplotlib` e `seaborn` para gerar gráficos que destacam:
1. **Preço do produto em datas distintas** (`grafico_comparativo_valores.png`).
2. **Oscilações de alta e queda percentual** (`grafico_variacao_percentual.png`).
3. **Visão consolidada auditável** (`grafico_cotacao_auditavel.png`).





---

## 🛠️ Tecnologias Envolvidas

* **`pandas`:** Manipulação das tabelas de cotação, cruzamento de dados temporais e cálculo de variações de preços.
* **`numpy`:** Suporte a cálculos matemáticos/estatísticos de variação.
* **`matplotlib` e `seaborn`:** Construção, estilização e exportação dos gráficos comparativos em formato PNG.

