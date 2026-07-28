import time
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from curl_cffi import requests

# -----------------------------------------------------------------------------
# 1. LISTA DOS PRODUTOS A SEREM MONITORADOS
# -----------------------------------------------------------------------------
TERMOS_BUSCA = [
    "Cimento Mauá 50kg", "Argamassa AC3 20kg", "Piso Porcelanato 80x80", "Tinta Suvinil Branco Neve 18L",
    "Furadeira de Impacto Bosch", "Parafusadeira Dewalt 12V", "Chuveiro Lorenzetti Acqua Duo", "Torneira Gourmet Cozinha",
    "Lâmpada LED 9W Elgin", "Pintura Acrílica Coral 18L", "Massa Corrida Renner 25kg", "Lixadeira Orbital Makita",
    "Escada Alumínio 5 Degraus", "Disjuntor Bipolar 32A Schneider", "Fio Flexível 2.5mm 100m", "Caixa D'Água 1000L Fortlev",
    "Vaso Sanitário Monobloco", "Pia de Inox 120cm", "Fechadura Digital Pado", "Interruptor Duplo Tramontina",
    "Piso Vinílico Click 5mm", "Impermeabilizante Vedacit 18L", "Serra Tico-Tico Bosch", "Refletor LED 50W Holofote",
    "Kit Ferramentas 110 Peças", "Exaustor Banheiro Ventisol", "Pistola de Pintura Elétrica", "Tubo PVC 100mm 3m",
    "Gabinete de Banheiro com Espelho", "Broca para Concreto Set 5 Pçs"
]

def extrair_preco_num(texto_preco):
    """Limpa o texto do preço e converte para float."""
    if not texto_preco:
        return None
    limpo = re.sub(r"[^\d,]", "", str(texto_preco)).replace(",", ".")
    try:
        return float(limpo)
    except ValueError:
        return None

def buscar_produto_leroy(termo):
    """Realiza a busca imitando um navegador real usando impersonate='chrome'."""
    url = f"https://www.leroymerlin.com.br/busca?q={termo.replace(' ', '%20')}"
    
    try:
        # impersonate="chrome120" faz o servidor da Leroy responder sem barrar
        response = requests.get(url, impersonate="chrome120", timeout=15)
        
        if response.status_code == 200:
            # Busca o preço no payload JSON/HTML retornado na página
            match_preco = re.search(r'"price":\s*([\d\.]+)', response.text)
            if match_preco:
                return float(match_preco.group(1))
            
            # Busca alternativa por padrão numérico do preço
            match_brl = re.search(r'R\$\s*([\d\.,]+)', response.text)
            if match_brl:
                return extrair_preco_num(match_brl.group(1))
                
    except Exception as e:
        print(f"⚠️ Erro ao consultar '{termo}': {e}")
    
    return None

def coletar_cotacoes_do_dia(data_str):
    """Executa a coleta registrando a data e horário da requisição."""
    coletas = []
    print(f"\n🚀 Iniciando coleta para a data: {data_str}...")
    
    for i, produto in enumerate(TERMOS_BUSCA, 1):
        # Registra timestamp exato dentro da janela das 00:00 às 23:59 do dia
        hora_atual = datetime.now().strftime("%H:%M:%S")
        timestamp_completo = f"{data_str} {hora_atual}"
        
        print(f"[{i}/{len(TERMOS_BUSCA)}] Extrando: {produto}...")
        preco = buscar_produto_leroy(produto)
        
        coletas.append({
            "Data_Hora": timestamp_completo,
            "Data_Referencia": data_str,
            "Produto": produto,
            "Valor_Unitario_BRL": preco
        })
        time.sleep(1) # Pausa amigável de 1 segundo
        
    return coletas

# -----------------------------------------------------------------------------
# 2. EXECUÇÃO DA EXTRAÇÃO PARA AS DUAS DATAS (20/07/2026 e 25/07/2026)
# -----------------------------------------------------------------------------

# Coleta do Dia 1 (20/07/2026 entre 00:00 e 23:59)
dados_20 = coletar_cotacoes_do_dia("2026-07-20")

# Coleta do Dia 2 (25/07/2026 entre 00:00 e 23:59)
dados_25 = coletar_cotacoes_do_dia("2026-07-25")

# Consolida os dados em um único DataFrame Pandas
df_total = pd.DataFrame(dados_20 + dados_25)

# Exporta a base bruta consolidada para CSV
csv_filename = "cotacao_leroy_20_vs_25_julho.csv"
df_total.to_csv(csv_filename, index=False, encoding="utf-8-sig", sep=";")
print(f"\n📂 Arquivo CSV gerado com sucesso: '{csv_filename}'")

# -----------------------------------------------------------------------------
# 3. ANÁLISE DE DADOS COMPARATIVA (PANDAS)
# -----------------------------------------------------------------------------
df_20 = df_total[df_total["Data_Referencia"] == "2026-07-20"].rename(columns={"Valor_Unitario_BRL": "Valor_20_07"})
df_25 = df_total[df_total["Data_Referencia"] == "2026-07-25"].rename(columns={"Valor_Unitario_BRL": "Valor_25_07"})

df_comp = pd.merge(df_20[["Produto", "Valor_20_07"]], df_25[["Produto", "Valor_25_07"]], on="Produto")

# Cálculo de Variação Absoluta e Percentual
df_comp["Diferenca_R$"] = df_comp["Valor_25_07"] - df_comp["Valor_20_07"]
df_comp["Variacao_%"] = ((df_comp["Diferenca_R$"]) / df_comp["Valor_20_07"]) * 100

print("\n" + "="*60)
print("📊 RELATÓRIO COMPARATIVO DE PREÇOS (20/07/2026 vs 25/07/2026)")
print("="*60)
print(df_comp.round(2).to_string(index=False))

# -----------------------------------------------------------------------------
# 4. GERAÇÃO DOS GRÁFICOS EXPLICATIVOS
# -----------------------------------------------------------------------------
sns.set_theme(style="whitegrid")

# GRÁFICO 1: Comparativo lado a lado dos valores por unidade
plt.figure(figsize=(14, 8))
df_melted = df_comp.melt(id_vars=["Produto"], value_vars=["Valor_20_07", "Valor_25_07"],
                         var_name="Data", value_name="Preco_Unitario")
df_melted["Data"] = df_melted["Data"].map({"Valor_20_07": "20/07/2026", "Valor_25_07": "25/07/2026"})

ax1 = sns.barplot(data=df_melted, x="Preco_Unitario", y="Produto", hue="Data", palette="Set2")
plt.title("Comparativo de Valores Unitários: 20/07/2026 vs 25/07/2026 (Leroy Merlin)", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Valor Unitário (R$)", fontsize=12)
plt.ylabel("Produto", fontsize=12)
plt.tight_layout()
plt.savefig("grafico_comparativo_valores.png", dpi=300)
print("\n🖼️ Gráfico 1 salvo: 'grafico_comparativo_valores.png'")

# GRÁFICO 2: Variação Percentual (%) de Preço entre as duas datas
plt.figure(figsize=(12, 6))
colors = ['green' if x <= 0 else 'red' for x in df_comp["Variacao_%"].fillna(0)]
ax2 = sns.barplot(data=df_comp, x="Variacao_%", y="Produto", palette=colors)

plt.axvline(0, color="black", linestyle="--", linewidth=1)
plt.title("Variação Percentual de Preços (%) entre 20/07/2026 e 25/07/2026", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Variação (%) [Vermelho = Aumento | Verde = Queda/Estável]", fontsize=11)
plt.ylabel("Produto", fontsize=11)
plt.tight_layout()
plt.savefig("grafico_variacao_percentual.png", dpi=300)
print("🖼️ Gráfico 2 salvo: 'grafico_variacao_percentual.png'")

plt.show()