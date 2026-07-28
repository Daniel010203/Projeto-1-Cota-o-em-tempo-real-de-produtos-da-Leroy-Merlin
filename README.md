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
