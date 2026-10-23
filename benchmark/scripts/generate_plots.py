#!/usr/bin/env python3
import sys
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    diretorio_saida = "benchmark/output" if os.path.exists("benchmark/output") else "output"
    caminho_csv = sys.argv[1] if len(sys.argv) > 1 else os.path.join(diretorio_saida, "results.csv")
    caminho_escala = os.path.join(diretorio_saida, "results_escala.csv")

    if not os.path.exists(caminho_csv):
        sys.exit(1)

    df = pd.read_csv(caminho_csv)

    coluna_teste = 'cenario_teste' if 'cenario_teste' in df.columns else 'test_name'
    coluna_algoritmo = 'algoritmo' if 'algoritmo' in df.columns else 'algorithm'
    coluna_tempo_ms = 'tempo_milissegundos' if 'tempo_milissegundos' in df.columns else 'time_milliseconds'
    coluna_fluxo = 'fluxo_maximo' if 'fluxo_maximo' in df.columns else 'max_flow'
    coluna_iter = 'iteracoes_ou_discharges' if 'iteracoes_ou_discharges' in df.columns else 'iterations_or_discharges'
    coluna_pushes = 'pushes'
    coluna_relabels = 'relabels'

    df[coluna_algoritmo] = df[coluna_algoritmo].replace({
        "Push-Relabel (Generico)": "Push-Relabel (Genérico)"
    })

    mapa_rotulos = {
        "01_exemplo_cormen": "01. Exemplo Cormen",
        "02_diamante_patologico": "02. Diamante Patológico",
        "03_emparelhamento_bipartido": "03. Emparelhamento Bipartido",
        "04_rede_densa": "04. Rede Densa",
        "05_abastecimento_urbano": "05. Abastecimento Urbano"
    }
    df['rotulo_teste'] = df[coluna_teste].map(mapa_rotulos).fillna(df[coluna_teste])

    cores = {
        "Ford-Fulkerson (DFS)": "#EF553B",
        "Edmonds-Karp (BFS)": "#636EFA",
        "Push-Relabel (Genérico)": "#00CC96",
        "Push-Relabel (Generico)": "#00CC96",
        "Relabel-to-Front": "#AB63FA"
    }

    fig_tempo = go.Figure()
    for algo in df[coluna_algoritmo].unique():
        sub = df[df[coluna_algoritmo] == algo]
        fig_tempo.add_trace(go.Bar(
            x=sub['rotulo_teste'],
            y=sub[coluna_tempo_ms],
            name=algo,
            marker_color=cores.get(algo, '#333333'),
            text=[f"{val:.4f} ms" for val in sub[coluna_tempo_ms]],
            textposition='auto'
        ))

    fig_tempo.update_layout(
        title=dict(
            text="<b>Comparação de Tempo de Execução (Escala Logarítmica)</b>",
            subtitle=dict(text="Ford-Fulkerson vs. Edmonds-Karp vs. Push-Relabel vs. Relabel-to-Front", font=dict(size=13, color="#555555")),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title="Cenário de Teste",
        yaxis_title="Tempo de Execução (ms - escala log)",
        yaxis_type="log",
        barmode='group',
        template='plotly_white',
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
        font=dict(family="Arial, sans-serif", size=13),
        margin=dict(l=70, r=40, t=90, b=100)
    )

    saida_barras_tempo = os.path.join(diretorio_saida, "grafico_barras_tempo.png")
    fig_tempo.write_image(saida_barras_tempo, width=1200, height=700, scale=2)

    fig_ops = go.Figure()
    for algo in df[coluna_algoritmo].unique():
        sub = df[df[coluna_algoritmo] == algo]
        metrica_ops = sub[coluna_iter] + sub[coluna_pushes] + sub[coluna_relabels]
        fig_ops.add_trace(go.Bar(
            x=sub['rotulo_teste'],
            y=metrica_ops,
            name=algo,
            marker_color=cores.get(algo, '#333333'),
            text=metrica_ops,
            textposition='auto'
        ))

    fig_ops.update_layout(
        title=dict(
            text="<b>Volume de Operações Internas Executadas</b>",
            subtitle=dict(text="Caminhos aumentadores no FF/EK vs. Pushes, Relabels e Discharges no PR/R2F", font=dict(size=13, color="#555555")),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title="Cenário de Teste",
        yaxis_title="Total de Operações (escala log)",
        yaxis_type="log",
        barmode='group',
        template='plotly_white',
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
        font=dict(family="Arial, sans-serif", size=13),
        margin=dict(l=70, r=40, t=90, b=100)
    )

    saida_barras_ops = os.path.join(diretorio_saida, "grafico_barras_operacoes.png")
    fig_ops.write_image(saida_barras_ops, width=1200, height=700, scale=2)

    if os.path.exists(caminho_escala):
        df_esc = pd.read_csv(caminho_escala)
        df_esc['algoritmo'] = df_esc['algoritmo'].replace({
            "Push-Relabel (Generico)": "Push-Relabel (Genérico)"
        })

        estilos = {
            "Ford-Fulkerson (DFS)": dict(dash="solid", marker="circle", size=8),
            "Edmonds-Karp (BFS)": dict(dash="dash", marker="square", size=8),
            "Push-Relabel (Genérico)": dict(dash="dot", marker="diamond", size=8),
            "Relabel-to-Front": dict(dash="dashdot", marker="triangle-up", size=8)
        }

        fig_linhas = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Tempo de Execução (ms) vs. Capacidade M", "Iterações / Operações vs. Capacidade M"),
            horizontal_spacing=0.1
        )

        for algo in df_esc['algoritmo'].unique():
            sub_esc = df_esc[df_esc['algoritmo'] == algo]
            cor = cores.get(algo, '#333333')
            est = estilos.get(algo, dict(dash="solid", marker="circle", size=8))

            fig_linhas.add_trace(go.Scatter(
                x=sub_esc['capacidade_m'],
                y=sub_esc['tempo_milissegundos'],
                mode='lines+markers',
                name=algo,
                line=dict(color=cor, width=2.5, dash=est['dash']),
                marker=dict(size=est['size'], symbol=est['marker'])
            ), row=1, col=1)

            fig_linhas.add_trace(go.Scatter(
                x=sub_esc['capacidade_m'],
                y=sub_esc['iteracoes'],
                mode='lines+markers',
                name=algo,
                line=dict(color=cor, width=2.5, dash=est['dash']),
                marker=dict(size=est['size'], symbol=est['marker']),
                showlegend=False
            ), row=1, col=2)

        fig_linhas.update_layout(
            title=dict(
                text="<b>Escalabilidade Assintótica: Sensibilidade à Capacidade M no Caso Patológico</b>",
                subtitle=dict(
                    text="Escala logarítmica: Ford-Fulkerson O(E · |f*|) cresce linearmente com o fluxo enquanto os demais permanecem constantes",
                    font=dict(size=13, color="#555555")
                ),
                x=0.5,
                xanchor='center'
            ),
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.20,
                xanchor="center",
                x=0.5,
                font=dict(size=12)
            ),
            font=dict(family="Arial, sans-serif", size=13),
            margin=dict(l=70, r=40, t=110, b=110)
        )
        fig_linhas.update_xaxes(title_text="Capacidade M da Rede (escala log)", type="log", row=1, col=1)
        fig_linhas.update_xaxes(title_text="Capacidade M da Rede (escala log)", type="log", row=1, col=2)
        fig_linhas.update_yaxes(title_text="Tempo de Execução (ms - escala log)", type="log", row=1, col=1)
        fig_linhas.update_yaxes(title_text="Iterações / Operações (escala log)", type="log", row=1, col=2)

        saida_linhas = os.path.join(diretorio_saida, "grafico_linhas_escalabilidade.png")
        fig_linhas.write_image(saida_linhas, width=1400, height=750, scale=2)

    caminho_html_antigo = os.path.join(diretorio_saida, "benchmark_report.html")
    if os.path.exists(caminho_html_antigo):
        os.remove(caminho_html_antigo)

if __name__ == "__main__":
    main()
