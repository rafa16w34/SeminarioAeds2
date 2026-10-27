import os
import sys
import json
import csv
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

def carregar_txt_ou_dat(caminho):
    g = nx.DiGraph()
    fonte = None
    sorvedouro = None
    with open(caminho, 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f if linha.strip() and not linha.startswith('#') and not linha.startswith('//')]
    if not linhas:
        return g, fonte, sorvedouro
    primeira = linhas[0].split()
    if len(primeira) == 2:
        fonte = primeira[0]
        sorvedouro = primeira[1]
        linhas = linhas[1:]
    for linha in linhas:
        partes = linha.split()
        if len(partes) >= 3:
            u, v, cap = partes[0], partes[1], int(partes[2])
            g.add_edge(u, v, capacity=cap)
    return g, fonte, sorvedouro

def carregar_csv(caminho):
    g = nx.DiGraph()
    fonte = 's'
    sorvedouro = 't'
    with open(caminho, 'r', encoding='utf-8') as f:
        leitor = csv.reader(f)
        cabecalho = next(leitor, None)
        for linha in leitor:
            if len(linha) >= 3:
                u, v, cap = linha[0].strip(), linha[1].strip(), int(linha[2].strip())
                g.add_edge(u, v, capacity=cap)
    return g, fonte, sorvedouro

def carregar_json(caminho):
    g = nx.DiGraph()
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    fonte = dados.get('source', 's')
    sorvedouro = dados.get('sink', 't')
    for aresta in dados.get('edges', []):
        u = aresta.get('from', aresta.get('origem'))
        v = aresta.get('to', aresta.get('destino'))
        cap = int(aresta.get('capacity', aresta.get('capacidade', 0)))
        g.add_edge(u, v, capacity=cap)
    return g, fonte, sorvedouro

def obter_posicoes_cormen():
    return {
        's': (0.0, 1.5),
        'v1': (2.0, 2.7),
        'v2': (2.0, 0.3),
        'v3': (4.5, 2.7),
        'v4': (4.5, 0.3),
        't': (6.5, 1.5)
    }

def obter_posicoes_diamante():
    return {
        's': (0.0, 1.5),
        'u': (2.5, 2.8),
        'v': (2.5, 0.2),
        't': (5.0, 1.5)
    }

def obter_posicoes_bipartido():
    pos = {'s': (0.0, 3.0), 't': (6.0, 3.0)}
    candidatos = [f'Cand_{i}' for i in range(1, 6)]
    temas = [f'Tema_{chr(ord("A") + i)}' for i in range(5)]
    y_coords = [5.0, 4.0, 3.0, 2.0, 1.0]
    for c, y in zip(candidatos, y_coords):
        pos[c] = (2.0, y)
    for t, y in zip(temas, y_coords):
        pos[t] = (4.0, y)
    return pos

def obter_posicoes_densa():
    pos = {'s': (0.0, 2.5), 't': (8.0, 2.5)}
    l1 = ['L1_1', 'L1_2', 'L1_3']
    for idx, no in enumerate(l1):
        pos[no] = (2.0, 4.0 - idx * 1.5)
    l2 = ['L2_1', 'L2_2', 'L2_3', 'L2_4']
    for idx, no in enumerate(l2):
        pos[no] = (4.0, 4.2 - idx * 1.1)
    l3 = ['L3_1', 'L3_2', 'L3_3']
    for idx, no in enumerate(l3):
        pos[no] = (6.0, 4.0 - idx * 1.5)
    return pos

def obter_posicoes_abastecimento():
    return {
        'Represa_Central': (0.0, 2.5),
        'ETA_Norte': (2.2, 4.0),
        'ETA_Sul': (2.2, 1.0),
        'Elevatoria_1': (4.5, 4.6),
        'Reservatorio_R1': (4.5, 3.2),
        'Reservatorio_R2': (4.5, 1.8),
        'Elevatoria_2': (4.5, 0.4),
        'Polo_Industrial': (7.0, 3.7),
        'Setor_Leste': (7.0, 1.3),
        'Bairro_Central': (9.2, 2.5)
    }

def calcular_ponto_rotulo(p1, p2, rad):
    mx = (p1[0] + p2[0]) / 2.0
    my = (p1[1] + p2[1]) / 2.0
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = math.hypot(dx, dy)
    if dist > 0 and rad != 0:
        nx = -dy / dist
        ny = dx / dist
        mx += nx * (rad * dist * 0.32)
        my += ny * (rad * dist * 0.32)
    return mx, my

def desenhar_grafo(g, fonte, sorvedouro, pos, titulo, subtitulo, caminho_saida, tamanho=(13, 8), node_size=2400, font_size=10):
    fig, ax = plt.subplots(figsize=tamanho, dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')

    arestas_bidirecionais = set()
    for u, v in g.edges():
        if g.has_edge(v, u):
            arestas_bidirecionais.add((min(u, v), max(u, v)))

    cores_nos = []
    bordas_nos = []
    larguras_bordas = []

    for no in g.nodes():
        if no == fonte:
            cores_nos.append('#2ecc71')
            bordas_nos.append('#196f3d')
            larguras_bordas.append(3.0)
        elif no == sorvedouro:
            cores_nos.append('#e74c3c')
            bordas_nos.append('#922b21')
            larguras_bordas.append(3.0)
        elif 'ETA' in no or 'Reservatorio' in no:
            cores_nos.append('#3498db')
            bordas_nos.append('#1b4f72')
            larguras_bordas.append(2.5)
        elif 'Elevatoria' in no:
            cores_nos.append('#f39c12')
            bordas_nos.append('#b9770e')
            larguras_bordas.append(2.5)
        elif 'Setor' in no or 'Polo' in no:
            cores_nos.append('#9b59b6')
            bordas_nos.append('#5b2c6f')
            larguras_bordas.append(2.5)
        else:
            cores_nos.append('#34495e')
            bordas_nos.append('#1c2833')
            larguras_bordas.append(2.0)

    nx.draw_networkx_nodes(
        g, pos, ax=ax,
        node_size=node_size,
        node_color=cores_nos,
        edgecolors=bordas_nos,
        linewidths=larguras_bordas
    )

    rotulos_nos = {}
    for no in g.nodes():
        rotulo_formatado = no.replace('_', '\n')
        rotulos_nos[no] = rotulo_formatado

    nx.draw_networkx_labels(
        g, pos, labels=rotulos_nos, ax=ax,
        font_size=font_size,
        font_color='#ffffff',
        font_family='sans-serif',
        font_weight='bold'
    )

    for u, v, dados in g.edges(data=True):
        cap = dados.get('capacity', 0)
        p1 = pos[u]
        p2 = pos[v]
        e_bidi = (min(u, v), max(u, v)) in arestas_bidirecionais

        if e_bidi:
            rad = 0.22 if u < v else 0.22
            estilo = f'arc3,rad={rad}'
        else:
            rad = 0.0
            estilo = 'arc3,rad=0.0'

        ax.annotate(
            '',
            xy=p2,
            xytext=p1,
            arrowprops=dict(
                arrowstyle='-|>',
                connectionstyle=estilo,
                color='#475569',
                lw=2.0,
                shrinkA=22,
                shrinkB=22,
                mutation_scale=18
            )
        )

        mx, my = calcular_ponto_rotulo(p1, p2, rad)
        texto_cap = f'c = {cap}'

        ax.text(
            mx, my, texto_cap,
            fontsize=8.5,
            fontweight='bold',
            color='#1e293b',
            ha='center', va='center',
            bbox=dict(
                boxstyle='round,pad=0.25',
                facecolor='#ffffff',
                edgecolor='#94a3b8',
                linewidth=1.0,
                alpha=0.95
            ),
            zorder=5
        )

    patches_legenda = [
        mpatches.Patch(facecolor='#2ecc71', edgecolor='#196f3d', label=f'Fonte s ({fonte})'),
        mpatches.Patch(facecolor='#e74c3c', edgecolor='#922b21', label=f'Sorvedouro t ({sorvedouro})'),
        mpatches.Patch(facecolor='#34495e', edgecolor='#1c2833', label='Vértices Intermediários')
    ]
    if 'abastecimento' in caminho_saida:
        patches_legenda = [
            mpatches.Patch(facecolor='#2ecc71', edgecolor='#196f3d', label='Captação / Represa (Fonte s)'),
            mpatches.Patch(facecolor='#3498db', edgecolor='#1b4f72', label='Tratamento e Reservatórios'),
            mpatches.Patch(facecolor='#f39c12', edgecolor='#b9770e', label='Estações Elevatórias / Bombas'),
            mpatches.Patch(facecolor='#9b59b6', edgecolor='#5b2c6f', label='Polos / Setores de Distribuição'),
            mpatches.Patch(facecolor='#e74c3c', edgecolor='#922b21', label='Centro de Consumo (Sorvedouro t)')
        ]

    ax.legend(
        handles=patches_legenda,
        loc='upper center',
        bbox_to_anchor=(0.5, -0.05),
        ncol=len(patches_legenda) if len(patches_legenda) <= 3 else 3,
        fontsize=9.5,
        frameon=True,
        facecolor='#ffffff',
        edgecolor='#cbd5e1'
    )

    plt.title(titulo, fontsize=15, fontweight='bold', color='#0f172a', pad=24)
    plt.suptitle(subtitulo, fontsize=10.5, color='#475569', y=0.92)

    xs = [coord[0] for coord in pos.values()]
    ys = [coord[1] for coord in pos.values()]
    margem_x = (max(xs) - min(xs)) * 0.12 if max(xs) > min(xs) else 1.0
    margem_y = (max(ys) - min(ys)) * 0.18 if max(ys) > min(ys) else 1.0
    ax.set_xlim(min(xs) - margem_x, max(xs) + margem_x)
    ax.set_ylim(min(ys) - margem_y, max(ys) + margem_y)

    ax.axis('off')
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, bottom=0.12)
    plt.savefig(caminho_saida, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()

def gerar_todos_grafos(dir_entrada, dir_saida):
    os.makedirs(dir_saida, exist_ok=True)

    caminho1 = os.path.join(dir_entrada, '01_exemplo_cormen.txt')
    if os.path.exists(caminho1):
        g1, f1, s1 = carregar_txt_ou_dat(caminho1)
        pos1 = obter_posicoes_cormen()
        desenhar_grafo(
            g1, f1, s1, pos1,
            'Grafo 1: Exemplo Clássico de Cormen (Capítulo 26)',
            'Topologia de 6 vértices com arestas antiparalelas (v1 ⇄ v2) | Fluxo Máximo = 23',
            os.path.join(dir_saida, 'grafo_01_exemplo_cormen.png'),
            tamanho=(11, 7), node_size=2600, font_size=12
        )

    caminho2 = os.path.join(dir_entrada, '02_diamante_patologico.dat')
    if os.path.exists(caminho2):
        g2, f2, s2 = carregar_txt_ou_dat(caminho2)
        pos2 = obter_posicoes_diamante()
        desenhar_grafo(
            g2, f2, s2, pos2,
            'Grafo 2: Diamante Patológico (Pior Caso de Ford-Fulkerson)',
            'Aresta central (u → v, cap=1) causa 20.000 iterações com caminhos alternantes no pior caso',
            os.path.join(dir_saida, 'grafo_02_diamante_patologico.png'),
            tamanho=(10, 6.5), node_size=2600, font_size=12
        )

    caminho3 = os.path.join(dir_entrada, '03_emparelhamento_bipartido.csv')
    if os.path.exists(caminho3):
        g3, f3, s3 = carregar_csv(caminho3)
        pos3 = obter_posicoes_bipartido()
        desenhar_grafo(
            g3, f3, s3, pos3,
            'Grafo 3: Emparelhamento Bipartido Máximo (Redução de Fluxo)',
            'Atribuição de 5 Candidatos a 5 Temas com capacidades unitárias (c = 1)',
            os.path.join(dir_saida, 'grafo_03_emparelhamento_bipartido.png'),
            tamanho=(12, 8), node_size=2200, font_size=9.5
        )

    caminho4 = os.path.join(dir_entrada, '04_rede_densa.json')
    if os.path.exists(caminho4):
        g4, f4, s4 = carregar_json(caminho4)
        pos4 = obter_posicoes_densa()
        desenhar_grafo(
            g4, f4, s4, pos4,
            'Grafo 4: Rede Densa em Camadas (DAG com Arestas Cruzadas)',
            'Múltiplas camadas intermediárias com arestas paralelas e cruzadas para estresse de push e relabel',
            os.path.join(dir_saida, 'grafo_04_rede_densa.png'),
            tamanho=(14, 8), node_size=2000, font_size=9.5
        )

    caminho5 = os.path.join(dir_entrada, '05_abastecimento_urbano.txt')
    if os.path.exists(caminho5):
        g5, f5, s5 = carregar_txt_ou_dat(caminho5)
        pos5 = obter_posicoes_abastecimento()
        desenhar_grafo(
            g5, f5, s5, pos5,
            'Grafo 5: Rede de Abastecimento Hídrico Urbano',
            'Modelagem realista de captação, tratamento, reservatórios, elevatórias e zonas de consumo',
            os.path.join(dir_saida, 'grafo_05_abastecimento_urbano.png'),
            tamanho=(15, 8.5), node_size=2400, font_size=8.0
        )

    gerar_painel_consolidado(dir_entrada, dir_saida)

def gerar_painel_consolidado(dir_entrada, dir_saida):
    fig, axes = plt.subplots(2, 3, figsize=(22, 14), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    configs = [
        ('01_exemplo_cormen.txt', carregar_txt_ou_dat, obter_posicoes_cormen(), 'Grafo 1: Exemplo Cormen (Cap. 26)', 2000, 9),
        ('02_diamante_patologico.dat', carregar_txt_ou_dat, obter_posicoes_diamante(), 'Grafo 2: Diamante Patológico', 2000, 9),
        ('03_emparelhamento_bipartido.csv', carregar_csv, obter_posicoes_bipartido(), 'Grafo 3: Emparelhamento Bipartido', 1600, 7.5),
        ('04_rede_densa.json', carregar_json, obter_posicoes_densa(), 'Grafo 4: Rede Densa em Camadas', 1500, 7.5),
        ('05_abastecimento_urbano.txt', carregar_txt_ou_dat, obter_posicoes_abastecimento(), 'Grafo 5: Abastecimento Urbano', 1600, 6.5)
    ]

    for idx, (nome_arq, carregador, pos, titulo, tam_no, tam_fonte) in enumerate(configs):
        linha = idx // 3
        coluna = idx % 3
        ax = axes[linha, coluna]
        ax.set_facecolor('#f8fafc')

        caminho = os.path.join(dir_entrada, nome_arq)
        if not os.path.exists(caminho):
            continue

        g, fonte, sorvedouro = carregador(caminho)

        cores_nos = []
        bordas_nos = []
        for no in g.nodes():
            if no == fonte:
                cores_nos.append('#2ecc71')
                bordas_nos.append('#196f3d')
            elif no == sorvedouro:
                cores_nos.append('#e74c3c')
                bordas_nos.append('#922b21')
            else:
                cores_nos.append('#3498db')
                bordas_nos.append('#1b4f72')

        nx.draw_networkx_nodes(
            g, pos, ax=ax,
            node_size=tam_no,
            node_color=cores_nos,
            edgecolors=bordas_nos,
            linewidths=1.8
        )

        rotulos = {no: no.replace('_', '\n') for no in g.nodes()}
        nx.draw_networkx_labels(
            g, pos, labels=rotulos, ax=ax,
            font_size=tam_fonte,
            font_color='#ffffff',
            font_family='sans-serif',
            font_weight='bold'
        )

        arestas_bidi = set()
        for u, v in g.edges():
            if g.has_edge(v, u):
                arestas_bidi.add((min(u, v), max(u, v)))

        for u, v, d in g.edges(data=True):
            cap = d.get('capacity', 0)
            p1 = pos[u]
            p2 = pos[v]
            e_bidi = (min(u, v), max(u, v)) in arestas_bidi
            rad = 0.22 if e_bidi else 0.0

            ax.annotate(
                '',
                xy=p2,
                xytext=p1,
                arrowprops=dict(
                    arrowstyle='-|>',
                    connectionstyle=f'arc3,rad={rad}',
                    color='#475569',
                    lw=1.3,
                    shrinkA=16,
                    shrinkB=16,
                    mutation_scale=12
                )
            )

            mx, my = calcular_ponto_rotulo(p1, p2, rad)
            ax.text(
                mx, my, str(cap),
                fontsize=7,
                fontweight='bold',
                color='#1e293b',
                ha='center', va='center',
                bbox=dict(
                    boxstyle='round,pad=0.18',
                    facecolor='#ffffff',
                    edgecolor='#94a3b8',
                    linewidth=0.8,
                    alpha=0.9
                )
            )

        ax.set_title(titulo, fontsize=12, fontweight='bold', color='#0f172a', pad=12)
        xs = [coord[0] for coord in pos.values()]
        ys = [coord[1] for coord in pos.values()]
        mx_range = (max(xs) - min(xs)) * 0.12 if max(xs) > min(xs) else 1.0
        my_range = (max(ys) - min(ys)) * 0.18 if max(ys) > min(ys) else 1.0
        ax.set_xlim(min(xs) - mx_range, max(xs) + mx_range)
        ax.set_ylim(min(ys) - my_range, max(ys) + my_range)
        ax.axis('off')

    ax_info = axes[1, 2]
    ax_info.set_facecolor('#ffffff')
    ax_info.axis('off')

    resumo = (
        "SUÍTE DE BENCHMARK DE FLUXO MÁXIMO\n"
        "Algoritmos em Avaliação:\n"
        " • Ford-Fulkerson (DFS residual)\n"
        " • Edmonds-Karp (BFS caminho mais curto)\n"
        " • Push-Relabel (Genérico O(V²E))\n"
        " • Relabel-to-Front (Descarregamento O(V³))\n\n"
        "Topologias Projetadas:\n"
        " 1. Cormen: Caso clássico do livro-texto\n"
        " 2. Diamante: Pior caso assintótico de FF\n"
        " 3. Bipartido: Problema de atribuição unitária\n"
        " 4. Rede Densa: DAG estratificado complexo\n"
        " 5. Abastecimento: Malha hídrica real da cidade"
    )

    ax_info.text(
        0.5, 0.5, resumo,
        fontsize=11.5,
        fontweight='normal',
        color='#1e293b',
        ha='center', va='center',
        bbox=dict(
            boxstyle='round,pad=0.8',
            facecolor='#f1f5f9',
            edgecolor='#cbd5e1',
            linewidth=1.5
        )
    )

    plt.suptitle('Topologias dos Grafos Utilizados no Benchmark Comparativo', fontsize=18, fontweight='bold', color='#0f172a', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    caminho_painel = os.path.join(dir_saida, 'grafos_todos_benchmarks.png')
    plt.savefig(caminho_painel, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    dir_entrada = sys.argv[1] if len(sys.argv) > 1 else 'benchmark/input'
    dir_saida = sys.argv[2] if len(sys.argv) > 2 else 'benchmark/output'
    gerar_todos_grafos(dir_entrada, dir_saida)
