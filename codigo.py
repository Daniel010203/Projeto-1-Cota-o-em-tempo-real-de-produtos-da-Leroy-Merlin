import pandas as pd
import numpy as np

def gerar_relatorio_leroy_merlin():
    print("=== GERANDO DADOS DE COTAÇÃO - LEROY MERLIN ===")

    # Lista de insumos com faixa de preço de referência (em R$)
    base_produtos = [
        {"categoria": "Saco de Cimento 50kg", "nome": "Cimento CP II E-32 50kg Itaú", "preco_base": 36.90},
        {"categoria": "Saco de Cimento 50kg", "nome": "Cimento CP II Z-32 50kg Votoran", "preco_base": 38.50},
        {"categoria": "Tinta Acrílica Branca 18L", "nome": "Tinta Acrílica Fosca Rende Muito Branco 18L Coral", "preco_base": 389.90},
        {"categoria": "Tinta Acrílica Branca 18L", "nome": "Tinta Acrílica Fosca Suvinil Clássico Branco 18L", "preco_base": 429.90},
        {"categoria": "Tubo PVC Esgoto 100mm", "nome": "Tubo de Esgoto Série Normal 100mm 6m Tigre", "preco_base": 78.90},
        {"categoria": "Tubo PVC Esgoto 100mm", "nome": "Tubo de Esgoto Série Normal 100mm 6m Amanco", "preco_base": 72.50},
        {"categoria": "Cabo Flexível 2.5mm 100m", "nome": "Cabo Flexível 750V 2,5mm² 100m Azul SIL", "preco_base": 185.00},
        {"categoria": "Cabo Flexível 2.5mm 100m", "nome": "Cabo Flexível 750V 2,5mm² 100m Vermelho Prysmian", "preco_base": 210.00}
    ]

    dados_coletados = []
    data_atual = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")

    # Gera registros simulando variações e promoções
    for item in base_produtos:
        # Adiciona uma variação aleatória de até ±5% para simular oscilações regionais
        variacao = np.random.uniform(-0.05, 0.05)
        preco_final = round(item["preco_base"] * (1 + variacao), 2)

        dados_coletados.append({
            "Categoria_Insumo": item["categoria"],
            "Produto_Leroy": item["nome"],
            "Preco_BRL": preco_final,
            "Loja": "Leroy Merlin",
            "Data_Consulta": data_atual
        })

    # 1. Criando o DataFrame do Pandas
    df = pd.DataFrame(dados_coletados)

    print("\n--- VISUALIZAÇÃO DOS DADOS ESTRUTURADOS ---")
    print(df.to_string(index=False))
    print("-" * 65)

    # 2. Análise Estatística / Agrupamento
    print("\n=== RESUMO ESTATÍSTICO DA COTAÇÃO LEROY MERLIN ===")
    resumo = df.groupby("Categoria_Insumo")["Preco_BRL"].agg(
        Menor_Preco="min",
        Preco_Medio="mean",
        Maior_Preco="max"
    ).reset_index()

    resumo.columns = ["Insumo", "Menor Preço (R$)", "Preço Médio (R$)", "Maior Preço (R$)"]
    print(resumo.to_string(index=False))
    print("-" * 65)

    # 3. Exportação para CSV
    nome_arquivo = "cotacao_leroy_merlin_simulado.csv"
    df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
    print(f"\n[SUCESSO] Arquivo '{nome_arquivo}' criado no seu diretório local!")

if __name__ == "__main__":
    gerar_relatorio_leroy_merlin()