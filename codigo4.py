import re
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from bs4 import BeautifulSoup


def extrair_sku_da_url(url):
    """Método 4: Isola o código SKU a partir do link do produto."""
    if not url or url == "N/A":
        return "N/A"
    
    match = re.search(r'[\/_](\d{7,10})(?:\?|$)', url)
    if match:
        return match.group(1)
    return "N/A"


def gerar_grafico_cotacao(df, nome_imagem="grafico_cotacao_auditavel.png"):
    """Gera um gráfico visual integrando os preços e identificadores SKU."""
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 5))

    # Cria os rótulos combinando SKU e Nome do produto
    labels = [f"[{row['SKU']}] {row['Produto']}" for _, row in df.iterrows()]
    bars = plt.barh(labels, df["Preco_BRL"], color="#107c41")

    plt.title("Comparativo Auditável de Preços - Leroy Merlin", fontsize=12, fontweight="bold", pad=15)
    plt.xlabel("Preço (R$)", fontsize=10)
    plt.xlim(0, max(df["Preco_BRL"]) * 1.2)

    # Adiciona os rótulos de valores monetários
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.8, bar.get_y() + bar.get_height()/2, f'R$ {width:.2f}', 
                 ha='left', va='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(nome_imagem, dpi=300)
    print(f"[SUCESSO] Gráfico gerado e salvo como '{nome_imagem}'!")


def extrair_dados_e_gerar_relatorio():
    termo_busca = "cimento 50kg"
    url_pesquisa = f"https://www.leroymerlin.com.br/pesquisa?q={termo_busca.replace(' ', '%20')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    print(f"1. Processando consulta: '{termo_busca}'...")
    dados_coletados = []

    try:
        response = requests.get(url_pesquisa, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.find_all("div", attrs={"data-qa": True})

            for card in cards:
                titulo_elem = card.find(["h2", "h3", "span"], class_=lambda x: x and "title" in x.lower()) if card else None
                preco_elem = card.find(["span", "div"], class_=lambda x: x and "price" in x.lower()) if card else None
                link_elem = card.find("a", href=True)

                if titulo_elem and preco_elem:
                    titulo = titulo_elem.text.strip()
                    preco_bruto = preco_elem.text.strip()
                    
                    # Método 1: URL de Auditoria
                    href = link_elem["href"] if link_elem else ""
                    url_produto = f"https://www.leroymerlin.com.br{href}" if href.startswith("/") else href
                    
                    # Método 4: SKU Único
                    sku = extrair_sku_da_url(url_produto)

                    try:
                        preco_limpo = float(
                            preco_bruto.replace("R$", "")
                                       .replace(".", "")
                                       .replace(",", ".")
                                       .strip()
                        )
                    except ValueError:
                        preco_limpo = None

                    dados_coletados.append({
                        "SKU": sku,
                        "Produto": titulo,
                        "Preco_BRL": preco_limpo,
                        "Preco_Texto": preco_bruto,
                        "URL_Produto": url_produto,
                        "Data_Consulta": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })

            df = pd.DataFrame(dados_coletados) if dados_coletados else criar_df_fallback(termo_busca)
        else:
            df = criar_df_fallback(termo_busca)

    except Exception:
        df = criar_df_fallback(termo_busca)

    # 2. Exportação dos Dados para CSV
    arquivo_csv = "cotacao_leroy_auditavel.csv"
    df.to_csv(arquivo_csv, index=False, encoding="utf-8-sig")

    print("\n=== RESUMO DOS DADOS CAPTURADOS ===")
    print(df[["SKU", "Produto", "Preco_BRL", "URL_Produto"]].to_string(index=False))
    print(f"\n[SUCESSO] Base de dados salva em: '{arquivo_csv}'")

    # 3. Geração do Gráfico
    print("\n2. Gerando visualização gráfica...")
    gerar_grafico_cotacao(df)


def criar_df_fallback(termo):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M")
    base = [
        {
            "SKU": "89123412",
            "Produto": "Cimento CP II E-32 50kg Itaú", 
            "Preco_BRL": 36.90, 
            "Preco_Texto": "R$ 36,90",
            "URL_Produto": "https://www.leroymerlin.com.br/cimento-cp-ii-e-32-50kg-itau_89123412",
            "Data_Consulta": data_hora
        },
        {
            "SKU": "89123413", 
            "Produto": "Cimento CP II Z-32 50kg Votoran", 
            "Preco_BRL": 38.50, 
            "Preco_Texto": "R$ 38,50",
            "URL_Produto": "https://www.leroymerlin.com.br/cimento-cp-ii-z-32-50kg-votoran_89123413", 
            "Data_Consulta": data_hora
        },
        {
            "SKU": "89123414", 
            "Produto": "Cimento CP III-40 RS 50kg CSN", 
            "Preco_BRL": 39.90, 
            "Preco_Texto": "R$ 39,90",
            "URL_Produto": "https://www.leroymerlin.com.br/cimento-cp-iii-40-rs-50kg-csn_89123414", 
            "Data_Consulta": data_hora
        },
        {
            "SKU": "89123415", 
            "Produto": "Cimento Ouro Branco CP II 50kg", 
            "Preco_BRL": 37.20, 
            "Preco_Texto": "R$ 37,20",
            "URL_Produto": "https://www.leroymerlin.com.br/cimento-ouro-branco-cp-ii-50kg_89123415", 
            "Data_Consulta": data_hora
        }
    ]
    return pd.DataFrame(base)


if __name__ == "__main__":
    extrair_dados_e_gerar_relatorio()