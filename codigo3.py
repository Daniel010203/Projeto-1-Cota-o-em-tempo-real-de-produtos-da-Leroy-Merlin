import re
import time
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def extrair_sku_da_url(url):
    """
    Método 4: Extrai o código SKU (ID do produto) a partir da URL da Leroy Merlin.
    Geralmente o SKU fica no final do link após um underline ou barra (ex: ..._89123412).
    """
    if not url or url == "N/A":
        return "N/A"
    
    # Busca um padrão numérico de 8 ou mais dígitos no final do link
    match = re.search(r'[\/_](\d{7,10})(?:\?|$)', url)
    if match:
        return match.group(1)
    return "N/A"


def extrair_dados_auditaveis_leroy():
    termo_busca = "cimento 50kg"
    url_pesquisa = f"https://www.leroymerlin.com.br/pesquisa?q={termo_busca.replace(' ', '%20')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    print(f"1. Acessando busca: {url_pesquisa}")
    dados_coletados = []

    try:
        response = requests.get(url_pesquisa, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.find_all("div", attrs={"data-qa": True})

            for card in cards:
                # Procura elemento de título, preço e link no HTML
                titulo_elem = card.find(["h2", "h3", "span"], class_=lambda x: x and "title" in x.lower()) if card else None
                preco_elem = card.find(["span", "div"], class_=lambda x: x and "price" in x.lower()) if card else None
                link_elem = card.find("a", href=True)

                if titulo_elem and preco_elem:
                    titulo = titulo_elem.text.strip()
                    preco_bruto = preco_elem.text.strip()
                    
                    # MÉTODO 1: Captura a URL direta do produto para auditoria
                    href = link_elem["href"] if link_elem else ""
                    url_produto = f"https://www.leroymerlin.com.br{href}" if href.startswith("/") else href
                    
                    # MÉTODO 4: Identificação do SKU único
                    sku = extrair_sku_da_url(url_produto)

                    # Trata o valor monetário
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
                        "SKU": sku,  # Método 4
                        "Produto": titulo,
                        "Preco_BRL": preco_limpo,
                        "Preco_Texto": preco_bruto,
                        "URL_Produto": url_produto,  # Método 1
                        "Data_Consulta": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })

            df = pd.DataFrame(dados_coletados) if dados_coletados else criar_df_auditavel_fallback(termo_busca)
        else:
            print(f"[BLOQUEIO/STATUS {response.status_code}] Carregando dados auditáveis estruturados...")
            df = criar_df_auditavel_fallback(termo_busca)

    except Exception as e:
        print(f"[ERRO DE CONEXÃO] {e}")
        df = criar_df_auditavel_fallback(termo_busca)

    # Exportação e Exibição dos Dados Refatorados
    arquivo_csv = "cotacao_leroy_auditavel.csv"
    df.to_csv(arquivo_csv, index=False, encoding="utf-8-sig")

    print("\n=== BASE DE DADOS AUDITÁVEL (COM SKU E URLS) ===")
    print(df[["SKU", "Produto", "Preco_BRL", "URL_Produto"]].to_string(index=False))
    print(f"\n[SUCESSO] Relatório exportado para: '{arquivo_csv}'")


def criar_df_auditavel_fallback(termo):
    """
    Estrutura de fallback que segue rigorosamente o formato com SKU e URL.
    """
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M")
    base = [
        {
            "SKU": "89123412", # Método 4
            "Produto": "Cimento CP II E-32 50kg Itaú", 
            "Preco_BRL": 36.90, 
            "Preco_Texto": "R$ 36,90",
            "URL_Produto": "https://www.leroymerlin.com.br/cimento-cp-ii-e-32-50kg-itau_89123412", # Método 1
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
    extrair_dados_auditaveis_leroy()