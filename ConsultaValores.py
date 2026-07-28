import os
import re
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from curl_cffi import requests

# 1. LISTA DE PRODUTOS PARA MONITORAR EM TEMPO REAL
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

NOME_ARQUIVO_HISTORICO = "historico_cotacoes_leroy.csv"

def buscar_preco_tempo_real(termo):
    """
    Busca o preço tentando a API de busca da Leroy e fallback no HTML.
    """
    # 1ª Tentativa: Endpoint da API interna de busca da Leroy
    api_url = f"https://www.leroymerlin.com.br/api/v2/products?term={termo.replace(' ', '%20')}&limit=1"
    
    try:
        res = requests.get(api_url, impersonate="chrome120", timeout=10)
        if res.status_code == 200:
            data = res.json()
            # Tenta navegar na estrutura da API
            if "products" in data and len(data["products"]) > 0:
                prod = data["products"][0]
                if "price" in prod:
                    return float(prod["price"].get("to", prod["price"].get("value", 0)))
                if "priceValue" in prod:
                    return float(prod["priceValue"])
    except Exception:
        pass

    # 2ª Tentativa: Regex avançada diretamente no código fonte da página
    url = f"https://www.leroymerlin.com.br/busca?q={termo.replace(' ', '%20')}"
    try:
        res = requests.get(url, impersonate="chrome120", timeout=12)
        if res.status_code == 200:
            # Procura padrões de preço JSON como "price": 129.9
            match_json = re.search(r'"price":\s*\{\s*"to":\s*([\d\.]+)', res.text) or re.search(r'"price":\s*([\d\.]+)', res.text)
            if match_json:
                return float(match_json.group(1))

            # Procura por padrões em texto (Ex: R$ 129,90)
            match_text = re.findall(r'R\$\s*([\d\.,]+)', res.text)
            for m in match_text:
                limpo = m.replace(".", "").replace(",", ".")
                try:
                    val = float(limpo)
                    if val > 1.0: # Ignora valores de centavos soltos
                        return val
                except ValueError:
                    continue
    except Exception as e:
        print(f"⚠️ Erro ao consultar '{termo}': {e}")
        
    return 0.0

# -----------------------------------------------------------------------------
# 2. EXECUÇÃO EM TEMPO REAL
# -----------------------------------------------------------------------------
agora = datetime.now()
data_hoje_str = agora.strftime("%Y-%m-%d")
hora_atual_str = agora.strftime("%H:%M:%S")

print(f"⚡ COTAÇÃO EM TEMPO REAL LEROY MERLIN ({data_hoje_str} às {hora_atual_str})\n")

novos_dados = []
for i, produto in enumerate(TERMOS_BUSCA, 1):
    print(f"[{i}/{len(TERMOS_BUSCA)}] Consultando: {produto}...")
    preco_hoje = buscar_preco_tempo_real(produto)
    
    print(f"   └─ Preço encontrado: R$ {preco_hoje:.2f}")
    
    novos_dados.append({
        "Data": data_hoje_str,
        "Hora": hora_atual_str,
        "Produto": produto,
        "Preco_Unitario_BRL": preco_hoje
    })
    time.sleep(0.5)

df_hoje = pd.DataFrame(novos_dados)

# -----------------------------------------------------------------------------
# 3. ATUALIZAÇÃO DO HISTÓRICO CSV
# -----------------------------------------------------------------------------
if os.path.exists(NOME_ARQUIVO_HISTORICO):
    df_historico = pd.read_csv(NOME_ARQUIVO_HISTORICO, sep=";")
    df_completo = pd.concat([df_historico, df_hoje], ignore_index=True)
else:
    df_completo = df_hoje

df_completo.to_csv(NOME_ARQUIVO_HISTORICO, index=False, encoding="utf-8-sig", sep=";")
print(f"\n📂 Dados gravados no histórico: '{NOME_ARQUIVO_HISTORICO}'")

# -----------------------------------------------------------------------------
# 4. GERAÇÃO DOS GRÁFICOS E ANÁLISE
# -----------------------------------------------------------------------------
df_validos = df_hoje[df_hoje["Preco_Unitario_BRL"] > 0]

if not df_validos.empty:
    plt.figure(figsize=(14, 8))
    sns.set_theme(style="whitegrid")

    df_sorted = df_validos.sort_values(by="Preco_Unitario_BRL", ascending=False)

    barplot = sns.barplot(
        data=df_sorted, 
        x="Preco_Unitario_BRL", 
        y="Produto", 
        palette="crest"
    )

    plt.title(f"Valores Unitários em Tempo Real ({data_hoje_str}) - Leroy Merlin", fontsize=15, fontweight="bold", pad=15)
    plt.xlabel("Preço Unitário (R$)", fontsize=12)
    plt.ylabel("Produto", fontsize=12)

    for index, value in enumerate(df_sorted["Preco_Unitario_BRL"]):
        barplot.text(value + (value * 0.01), index, f"R$ {value:.2f}", va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig("grafico_tempo_real.png", dpi=300)
    print("🖼️ Gráfico atualizado e salvo em 'grafico_tempo_real.png'")
    plt.show()
else:
    print("\n⚠️ Nenhum valor pôde ser extraído no momento. Verifique sua conexão com a internet.")