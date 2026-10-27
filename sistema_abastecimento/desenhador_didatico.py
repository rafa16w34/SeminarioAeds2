import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

def obter_estilo_no_didatico(id_no):
    if id_no == 's':
        return '#059669', '#047857', '#ffffff'
    elif id_no == 't':
        return '#dc2626', '#991b1b', '#ffffff'
    elif id_no in ('A', 'B'):
        return '#0284c7', '#0369a1', '#ffffff'
    elif id_no in ('C', 'D'):
        return '#2563eb', '#1d4ed8', '#ffffff'
    return '#475569', '#334155', '#ffffff'

def desenhar_slide_problema(rede, caminho_saida):
    fig = plt.figure(figsize=(15, 8.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    ax_grafo = fig.add_axes([0.05, 0.28, 0.90, 0.62])
    ax_grafo.set_facecolor('#f8fafc')

    pos = {no.id: (no.x, no.y) for no in rede.nos.values()}
    g = nx.DiGraph()
    for no in rede.nos.values():
        g.add_node(no.id)

    for no in rede.nos.values():
        cor_fundo, cor_borda, cor_txt = obter_estilo_no_didatico(no.id)
        nx.draw_networkx_nodes(
            g, pos, nodelist=[no.id], ax=ax_grafo,
            node_size=3200, node_color=cor_fundo,
            edgecolors=cor_borda, linewidths=2.8
        )
        rotulo_formatado = f"{no.id}\n{no.rotulo.split('(')[0].strip()}"
        ax_grafo.text(
            no.x, no.y, rotulo_formatado,
            fontsize=9.0, fontweight='bold', color=cor_txt,
            ha='center', va='center', family='sans-serif'
        )

    for (u, v), arco in rede.arcos.items():
        p1 = pos[u]
        p2 = pos[v]
        ax_grafo.annotate(
            '', xy=p2, xytext=p1,
            arrowprops=dict(
                arrowstyle='-|>',
                color='#475569',
                lw=2.5,
                shrinkA=28,
                shrinkB=28,
                mutation_scale=18
            )
        )
        mx = (p1[0] + p2[0]) / 2.0
        my = (p1[1] + p2[1]) / 2.0
        ax_grafo.text(
            mx, my, f"c = {arco.capacidade} m³/h",
            fontsize=9.0, fontweight='bold', color='#0f172a',
            ha='center', va='center',
            bbox=dict(
                boxstyle='round,pad=0.25',
                facecolor='#ffffff',
                edgecolor='#94a3b8',
                linewidth=1.2,
                alpha=0.95
            ),
            zorder=5
        )

    ax_grafo.set_xlim(-0.2, 7.5)
    ax_grafo.set_ylim(0.0, 4.0)
    ax_grafo.axis('off')
    ax_grafo.set_title("Topologia da Rede de Abastecimento Hídrico (6 Vértices Estratégicos)", fontsize=15, fontweight='bold', color='#0f172a', pad=12)

    ax_regras = fig.add_axes([0.05, 0.04, 0.90, 0.20])
    ax_regras.set_facecolor('#f1f5f9')
    ax_regras.axis('off')

    texto_regras = (
        "LEIS FÍSICAS DE FLUXO EM REDES (CORMEN CAPÍTULO 26):\n\n"
        "1. Restrição de Capacidade: O fluxo f(u,v) em qualquer cano não pode exceder o diâmetro da tubulação: 0 ≤ f(u,v) ≤ c(u,v).\n"
        "2. Conservação de Vazão: Nas estações intermediárias (ETAs e Reservatórios), toda água que entra deve sair: ∑ f_ent = ∑ f_sai.\n"
        "3. Desafio da Engenharia Hídrica: Determinar a vazão máxima que a Represa (s) consegue enviar à Cidade (t) e identificar os gargalos."
    )

    ax_regras.text(
        0.5, 0.5, texto_regras,
        fontsize=9.5, fontweight='normal', color='#1e293b',
        ha='center', va='center',
        bbox=dict(
            boxstyle='round,pad=0.8',
            facecolor='#e2e8f0',
            edgecolor='#cbd5e1',
            linewidth=1.5
        )
    )

    plt.suptitle('Problema Prático: Otimização do Fornecimento de Água Urbana', fontsize=17, fontweight='bold', color='#0f172a', y=0.97)
    plt.savefig(caminho_saida, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()

def desenhar_passo_caminho_aumentador(rede, passo, algoritmo_nome, caminho_saida, total_passos):
    fig = plt.figure(figsize=(15, 8.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    ax_grafo = fig.add_axes([0.05, 0.28, 0.90, 0.62])
    ax_grafo.set_facecolor('#f8fafc')

    pos = {no.id: (no.x, no.y) for no in rede.nos.values()}
    g = nx.DiGraph()
    for no in rede.nos.values():
        g.add_node(no.id)

    caminho = passo['caminho']
    arestas_caminho = set()
    for i in range(len(caminho) - 1):
        arestas_caminho.add((caminho[i], caminho[i+1]))

    for no in rede.nos.values():
        cor_fundo, cor_borda, cor_txt = obter_estilo_no_didatico(no.id)
        if no.id in caminho:
            cor_borda = '#eab308'
            lw_borda = 4.0
        else:
            lw_borda = 2.5

        nx.draw_networkx_nodes(
            g, pos, nodelist=[no.id], ax=ax_grafo,
            node_size=3200, node_color=cor_fundo,
            edgecolors=cor_borda, linewidths=lw_borda
        )
        rotulo_formatado = f"{no.id}\n{no.rotulo.split('(')[0].strip()}"
        ax_grafo.text(
            no.x, no.y, rotulo_formatado,
            fontsize=9.0, fontweight='bold', color=cor_txt,
            ha='center', va='center', family='sans-serif'
        )

    fluxos = passo['fluxos']
    gargalo = passo['gargalo']

    for (u, v), arco in rede.arcos.items():
        p1 = pos[u]
        p2 = pos[v]
        flx = fluxos.get((u, v), 0)
        cap = arco.capacidade
        e_caminho = (u, v) in arestas_caminho

        if e_caminho:
            cor_aresta = '#eab308'
            largura = 4.5
        elif flx == cap and cap > 0:
            cor_aresta = '#dc2626'
            largura = 3.0
        elif flx > 0:
            cor_aresta = '#0284c7'
            largura = 2.0 + (flx / cap * 2.0)
        else:
            cor_aresta = '#94a3b8'
            largura = 1.4

        ax_grafo.annotate(
            '', xy=p2, xytext=p1,
            arrowprops=dict(
                arrowstyle='-|>',
                color=cor_aresta,
                lw=largura,
                shrinkA=28,
                shrinkB=28,
                mutation_scale=18
            )
        )

        mx = (p1[0] + p2[0]) / 2.0
        my = (p1[1] + p2[1]) / 2.0

        if e_caminho:
            texto_tubo = f"{flx}/{cap} (NOVO +{gargalo})"
            cor_fundo_box = '#fef08a'
            cor_borda_box = '#ca8a04'
        elif flx == cap and cap > 0:
            texto_tubo = f"{flx}/{cap} (SATURADO)"
            cor_fundo_box = '#fee2e2'
            cor_borda_box = '#dc2626'
        else:
            texto_tubo = f"{flx}/{cap}"
            cor_fundo_box = '#ffffff'
            cor_borda_box = '#cbd5e1'

        ax_grafo.text(
            mx, my, texto_tubo,
            fontsize=8.5, fontweight='bold', color='#0f172a',
            ha='center', va='center',
            bbox=dict(
                boxstyle='round,pad=0.22',
                facecolor=cor_fundo_box,
                edgecolor=cor_borda_box,
                linewidth=1.2,
                alpha=0.95
            ),
            zorder=5
        )

    ax_grafo.set_xlim(-0.2, 7.5)
    ax_grafo.set_ylim(0.0, 4.0)
    ax_grafo.axis('off')

    rota_texto = " → ".join(caminho)
    ax_grafo.set_title(f"Passo {passo['passo']} de {total_passos}: Caminho Aumentador [{rota_texto}]", fontsize=14, fontweight='bold', color='#0f172a', pad=12)

    ax_info = fig.add_axes([0.05, 0.04, 0.90, 0.20])
    ax_info.set_facecolor('#f8fafc')
    ax_info.axis('off')

    explicacao_passo = (
        f"ANÁLISE DIDÁTICA DO PASSO {passo['passo']} - {algoritmo_nome}:\n\n"
        f"• Rota Localizada: {rota_texto}\n"
        f"• Capacidade Gargalo (Tubo mais estreito da rota): {gargalo} m³/h injetados.\n"
        f"• Vazão Total Acumulada Entregue à Cidade: {passo['fluxo_total']} de 21 m³/h ({passo['fluxo_total']/21*100:.1f}% da capacidade máxima).\n"
        f"• Efeito Residual: Cada aresta percorrida tem sua capacidade residual direta reduzida em {gargalo} e cria/expande capacidade reversa para correções."
    )

    ax_info.text(
        0.5, 0.5, explicacao_passo,
        fontsize=9.5, fontweight='normal', color='#1e293b',
        ha='center', va='center',
        bbox=dict(
            boxstyle='round,pad=0.8',
            facecolor='#f1f5f9',
            edgecolor='#cbd5e1',
            linewidth=1.4
        )
    )

    plt.suptitle(f"Execução Passo a Passo: {algoritmo_nome}", fontsize=17, fontweight='bold', color='#0f172a', y=0.97)
    plt.savefig(caminho_saida, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()

def desenhar_push_relabel_didatico(rede, resultado, caminho_saida):
    fig = plt.figure(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    ax_alturas = fig.add_axes([0.06, 0.38, 0.42, 0.52])
    ax_alturas.set_facecolor('#f8fafc')

    alturas = resultado['alturas_finais']
    ids_nos = ['s', 'A', 'B', 'C', 'D', 't']
    nomes_nos = [rede.nos[i].rotulo for i in ids_nos]
    alturas_vals = [alturas.get(i, 0) for i in ids_nos]
    cores = ['#059669', '#0284c7', '#0284c7', '#2563eb', '#2563eb', '#dc2626']

    barras = ax_alturas.bar(nomes_nos, alturas_vals, color=cores, edgecolor='#0f172a', width=0.55, linewidth=1.5)
    for barra in barras:
        h = barra.get_height()
        ax_alturas.text(barra.get_x() + barra.get_width()/2, h + 0.15, f"h = {int(h)}", ha='center', fontsize=9.0, fontweight='bold', color='#1e293b')

    ax_alturas.set_ylabel('Cota Manométrica / Altura h(u)', fontsize=10.5, fontweight='bold', color='#1e293b')
    ax_alturas.set_title('Perfil de Alturas h(u) ao Final da Execução', fontsize=12, fontweight='bold', color='#0f172a')
    ax_alturas.set_ylim(0, 7.5)
    ax_alturas.grid(axis='y', linestyle='--', alpha=0.5)

    ax_fluxo = fig.add_axes([0.53, 0.38, 0.42, 0.52])
    ax_fluxo.set_facecolor('#f8fafc')

    pos = {no.id: (no.x, no.y) for no in rede.nos.values()}
    g = nx.DiGraph()
    for no in rede.nos.values():
        g.add_node(no.id)

    for no in rede.nos.values():
        cor_fundo, cor_borda, cor_txt = obter_estilo_no_didatico(no.id)
        nx.draw_networkx_nodes(
            g, pos, nodelist=[no.id], ax=ax_fluxo,
            node_size=2400, node_color=cor_fundo,
            edgecolors=cor_borda, linewidths=2.2
        )
        ax_fluxo.text(
            no.x, no.y, f"{no.id}\n(h={alturas.get(no.id, 0)})",
            fontsize=8.0, fontweight='bold', color=cor_txt,
            ha='center', va='center'
        )

    fluxos = resultado['fluxos']
    for (u, v), arco in rede.arcos.items():
        p1 = pos[u]
        p2 = pos[v]
        flx = fluxos.get((u, v), 0)
        cap = arco.capacidade
        cor = '#dc2626' if flx == cap else ('#0284c7' if flx > 0 else '#94a3b8')
        largura = 3.0 if flx == cap else 1.8

        ax_fluxo.annotate(
            '', xy=p2, xytext=p1,
            arrowprops=dict(arrowstyle='-|>', color=cor, lw=largura, shrinkA=24, shrinkB=24, mutation_scale=15)
        )
        mx = (p1[0] + p2[0]) / 2.0
        my = (p1[1] + p2[1]) / 2.0
        ax_fluxo.text(
            mx, my, f"{flx}/{cap}",
            fontsize=7.5, fontweight='bold', color='#0f172a',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor=cor, lw=1.0)
        )

    ax_fluxo.set_xlim(-0.2, 7.5)
    ax_fluxo.set_ylim(0.0, 4.0)
    ax_fluxo.axis('off')
    ax_fluxo.set_title(f"Rede com Fluxo Máximo Final ({resultado['fluxo_maximo']} m³/h)", fontsize=12, fontweight='bold', color='#0f172a')

    ax_explicacao = fig.add_axes([0.06, 0.04, 0.89, 0.28])
    ax_explicacao.set_facecolor('#ffffff')
    ax_explicacao.axis('off')

    texto_pr = (
        "ANALOGIA FÍSICA DE PUSH-RELABEL (GOLDBERG-TARJAN):\n\n"
        "1. Sem Caminhos Globais: Ao invés de buscar rotas inteiras de s até t (como Ford-Fulkerson),\n"
        "   o algoritmo opera LOCALMENTE em cada estação usando cotas e reservatórios com excesso represado.\n\n"
        "2. Regra do Escoamento Gravitacional (PUSH):\n"
        "   A água só escorre morro abaixo! A válvula (u, v) só abre se a cota do emissor for superior: h(u) = h(v) + 1.\n\n"
        "3. Regra da Bomba Elevatória (RELABEL):\n"
        "   Se a estação tem água represada (excesso e(u) > 0) mas todos os canos vizinhos estão no mesmo nível ou mais altos,\n"
        "   a gravidade é insuficiente: aciona-se a bomba e eleva-se a cota: h(u) = 1 + min{h(v) : (u, v) residual}.\n\n"
        "4. Devolução de Excesso: O volume de água que não consegue chegar à cidade sobe de cota além de |V| e retorna para a Represa."
    )

    ax_explicacao.text(
        0.5, 0.5, texto_pr,
        fontsize=9.2, fontweight='normal', color='#1e293b',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#f1f5f9', edgecolor='#cbd5e1', lw=1.4)
    )

    plt.suptitle('Comportamento do Algoritmo Push-Relabel: Cotas Altimétricas e Bombas', fontsize=17, fontweight='bold', color='#0f172a', y=0.97)
    plt.savefig(caminho_saida, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()

def desenhar_relabel_to_front_didatico(rede, resultado, caminho_saida):
    fig = plt.figure(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    ax_diagrama = fig.add_axes([0.06, 0.40, 0.88, 0.50])
    ax_diagrama.set_facecolor('#f8fafc')

    pos = {no.id: (no.x, no.y) for no in rede.nos.values()}
    g = nx.DiGraph()
    for no in rede.nos.values():
        g.add_node(no.id)

    for no in rede.nos.values():
        cor_fundo, cor_borda, cor_txt = obter_estilo_no_didatico(no.id)
        nx.draw_networkx_nodes(
            g, pos, nodelist=[no.id], ax=ax_diagrama,
            node_size=2800, node_color=cor_fundo,
            edgecolors=cor_borda, linewidths=2.5
        )
        ax_diagrama.text(
            no.x, no.y, f"{no.id}\n{no.rotulo.split('(')[0].strip()}",
            fontsize=8.5, fontweight='bold', color=cor_txt,
            ha='center', va='center'
        )

    fluxos = resultado['fluxos']
    for (u, v), arco in rede.arcos.items():
        p1 = pos[u]
        p2 = pos[v]
        flx = fluxos.get((u, v), 0)
        cap = arco.capacidade
        cor = '#dc2626' if flx == cap else ('#0284c7' if flx > 0 else '#94a3b8')
        largura = 3.2 if flx == cap else 1.8

        ax_diagrama.annotate(
            '', xy=p2, xytext=p1,
            arrowprops=dict(arrowstyle='-|>', color=cor, lw=largura, shrinkA=26, shrinkB=26, mutation_scale=16)
        )
        mx = (p1[0] + p2[0]) / 2.0
        my = (p1[1] + p2[1]) / 2.0
        ax_diagrama.text(
            mx, my, f"{flx}/{cap}",
            fontsize=8.0, fontweight='bold', color='#0f172a',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor=cor, lw=1.0)
        )

    ax_diagrama.set_xlim(-0.2, 7.5)
    ax_diagrama.set_ylim(0.0, 4.0)
    ax_diagrama.axis('off')
    ax_diagrama.set_title(f"Rede Convergida por Relabel-to-Front (Vazão Máxima = {resultado['fluxo_maximo']} m³/h)", fontsize=13, fontweight='bold', color='#0f172a')

    ax_lista = fig.add_axes([0.06, 0.04, 0.88, 0.32])
    ax_lista.set_facecolor('#f1f5f9')
    ax_lista.axis('off')

    lista_final_str = " ⇄ ".join(resultado['lista_final'])
    texto_rtf = (
        "ORQUESTRAÇÃO DO ALGORITMO RELABEL-TO-FRONT (CORMEN SEÇÃO 26.5):\n\n"
        f"• Lista Encadeada L de Vértices: [ {lista_final_str} ]\n"
        "• Rotina DISCHARGE (Descarga Completa):\n"
        "  Ao selecionar um vértice da lista, o algoritmo não o abandona enquanto houver excesso represado (e(u) > 0).\n"
        "  Ele realiza sucessivos pushes e relabels locais até que todo o excesso seja esvaziado.\n\n"
        "• Movimento TO-FRONT (Mover para o Início da Lista):\n"
        "  Sempre que um nó u sofre uma operação de RELABEL (elevação de cota), ele é removido de sua posição atual\n"
        "  e inserido NO INÍCIO da lista L (head). O ponteiro recomeça do início.\n\n"
        "• Garantia de Complexidade Ótima: Essa ordem de visitação estruturada garante complexidade assintótica estrita O(V³)."
    )

    ax_lista.text(
        0.5, 0.5, texto_rtf,
        fontsize=9.2, fontweight='normal', color='#1e293b',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#e2e8f0', edgecolor='#cbd5e1', lw=1.5)
    )

    plt.suptitle('Comportamento de Relabel-to-Front: Descarga Metódica e Lista Encadeada', fontsize=17, fontweight='bold', color='#0f172a', y=0.97)
    plt.savefig(caminho_saida, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()

def desenhar_teorema_corte_minimo_didatico(rede, fluxos, caminho_saida):
    corte_s, corte_t, arestas_corte, cap_corte = rede.calcular_corte_minimo(fluxos)

    fig = plt.figure(figsize=(15, 8.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    ax_grafo = fig.add_axes([0.05, 0.28, 0.90, 0.62])
    ax_grafo.set_facecolor('#f8fafc')

    pos = {no.id: (no.x, no.y) for no in rede.nos.values()}
    g = nx.DiGraph()
    for no in rede.nos.values():
        g.add_node(no.id)

    ax_grafo.axvspan(-0.2, 5.7, color='#dcfce7', alpha=0.35, label='Partição S (Captação e Reservatórios)')
    ax_grafo.axvspan(5.9, 7.5, color='#fee2e2', alpha=0.35, label='Partição T (Consumidores Finais)')
    ax_grafo.axvline(x=5.8, color='#dc2626', linestyle='--', lw=3.0, label='Linha de Corte Mínimo (Max-Flow Min-Cut)')

    for no in rede.nos.values():
        cor_fundo, cor_borda, cor_txt = obter_estilo_no_didatico(no.id)
        nx.draw_networkx_nodes(
            g, pos, nodelist=[no.id], ax=ax_grafo,
            node_size=3200, node_color=cor_fundo,
            edgecolors=cor_borda, linewidths=2.8
        )
        pertence = "[S]" if no.id in corte_s else "[T]"
        ax_grafo.text(
            no.x, no.y, f"{no.id} {pertence}\n{no.rotulo.split('(')[0].strip()}",
            fontsize=8.5, fontweight='bold', color=cor_txt,
            ha='center', va='center'
        )

    arestas_corte_set = {(a['u'], a['v']) for a in arestas_corte}

    for (u, v), arco in rede.arcos.items():
        p1 = pos[u]
        p2 = pos[v]
        flx = fluxos.get((u, v), 0)
        cap = arco.capacidade
        e_corte = (u, v) in arestas_corte_set

        cor = '#dc2626' if e_corte else '#94a3b8'
        largura = 4.2 if e_corte else 1.6

        ax_grafo.annotate(
            '', xy=p2, xytext=p1,
            arrowprops=dict(arrowstyle='-|>', color=cor, lw=largura, shrinkA=28, shrinkB=28, mutation_scale=18)
        )
        mx = (p1[0] + p2[0]) / 2.0
        my = (p1[1] + p2[1]) / 2.0
        texto = f"{flx}/{cap} [GARGALO DO CORTE]" if e_corte else f"{flx}/{cap}"
        ax_grafo.text(
            mx, my, texto,
            fontsize=8.5, fontweight='bold', color='#dc2626' if e_corte else '#0f172a',
            ha='center', va='center',
            bbox=dict(
                boxstyle='round,pad=0.22',
                facecolor='#ffffff',
                edgecolor=cor,
                linewidth=1.2,
                alpha=0.95
            ),
            zorder=5
        )

    ax_grafo.set_xlim(-0.2, 7.5)
    ax_grafo.set_ylim(0.0, 4.0)
    ax_grafo.axis('off')
    ax_grafo.legend(loc='upper left', fontsize=9.5, frameon=True, facecolor='#ffffff')
    ax_grafo.set_title("Visualização do Teorema do Fluxo Máximo e Corte Mínimo", fontsize=14, fontweight='bold', color='#0f172a', pad=12)

    ax_info = fig.add_axes([0.05, 0.04, 0.90, 0.20])
    ax_info.set_facecolor('#ffffff')
    ax_info.axis('off')

    lista_tubos_corte = ", ".join([f"{a['u']}→{a['v']} (cap={a['capacidade']})" for a in arestas_corte])
    texto_teorema = (
        "TEOREMA DO FLUXO MÁXIMO E CORTE MÍNIMO (MAX-FLOW MIN-CUT THEOREM):\n\n"
        f"• Valor do Fluxo Máximo: 21 m³/h == Capacidade do Corte Mínimo: {cap_corte} m³/h.\n"
        f"• Tubulações Críticas que Formam a Fronteira do Corte: {lista_tubos_corte}.\n"
        "• Conclusão Prática de Engenharia para a Apresentação:\n"
        "  Se a concessionária de água investir milhões para triplicar o cano Represa→ETA Norte (s→A), o fluxo na Cidade AUMENTA?\n"
        "  RESPOSTA: ZERO! Aumentar canos fora do corte mínimo tem impacto nulo. O investimento deve ser EXCLUSIVO nas tubulações do corte!"
    )

    ax_info.text(
        0.5, 0.5, texto_teorema,
        fontsize=9.5, fontweight='normal', color='#1e293b',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#fef2f2', edgecolor='#fca5a5', lw=1.5)
    )

    plt.suptitle('Teorema do Corte Mínimo: Diagnóstico Físico dos Gargalos Urbanos', fontsize=17, fontweight='bold', color='#0f172a', y=0.97)
    plt.savefig(caminho_saida, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()

def desenhar_quadro_comparativo(caminho_saida):
    fig = plt.figure(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    ax = fig.add_axes([0.05, 0.08, 0.90, 0.82])
    ax.set_facecolor('#ffffff')
    ax.axis('off')

    colunas = ['Algoritmo', 'Estratégia Mental de Busca', 'Complexidade Teórica', 'Comportamento na Rede Hídrica', 'Vantagem Prática']
    dados = [
        [
            'Ford-Fulkerson\n(Cormen 26.2)',
            'Busca caminhos aumentadores\narbitrários usando DFS.',
            'O(E · |f*|)\nPseudopolinomial',
            'Pode escolher caminhos longos\nou oscilar no pior caso.',
            'Conceitualmente simples,\nbase de todos os métodos.'
        ],
        [
            'Edmonds-Karp\n(Cormen 26.2)',
            'Busca caminhos aumentadores\nmais curtos em arestas (BFS).',
            'O(V · E²)\nPolinomial estrito',
            'Sistemático: 4 passos limpos\ncom distâncias não-decrescentes.',
            'Robusto, previsível e\nindepende dos valores de cap.'
        ],
        [
            'Push-Relabel\n(Cormen 26.4)',
            'Atuação local com reservatórios,\ncotas altimétricas e gravidade.',
            'O(V² · E)\nPolinomial assíncrono',
            'Empurra água morro abaixo e\neleva cotas via bombas.',
            'Altamente paralelizável,\nperfeito para redes físicas.'
        ],
        [
            'Relabel-to-Front\n(Cormen 26.5)',
            'Orquestração por lista L,\ndescarga total e to-front.',
            'O(V³)\nÓtimo assintótico',
            'Visita sistematicamente cada\nestação até esgotar o excesso.',
            'Menor complexidade teórica\npara grafos densos.'
        ]
    ]

    tabela = ax.table(
        cellText=dados,
        colLabels=colunas,
        cellLoc='center',
        loc='center',
        colColours=['#0f172a', '#0f172a', '#0f172a', '#0f172a', '#0f172a']
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(9.5)
    tabela.scale(1.0, 3.2)

    for (row, col), cell in tabela.get_celld().items():
        if row == 0:
            cell.set_text_props(color='#ffffff', weight='bold')
            cell.set_facecolor('#0f172a')
        else:
            cell.set_edgecolor('#cbd5e1')
            if row % 2 == 1:
                cell.set_facecolor('#f8fafc')
            else:
                cell.set_facecolor('#f1f5f9')

    plt.suptitle('Quadro Comparativo: Comportamento dos 4 Algoritmos de Fluxo Máximo', fontsize=17, fontweight='bold', color='#0f172a', y=0.96)
    plt.savefig(caminho_saida, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()

def gerar_suite_didatica_completa(dir_saida='sistema_abastecimento/output'):
    os.makedirs(dir_saida, exist_ok=True)
    dir_ff = os.path.join(dir_saida, '02_ford_fulkerson')
    dir_ek = os.path.join(dir_saida, '03_edmonds_karp')
    os.makedirs(dir_ff, exist_ok=True)
    os.makedirs(dir_ek, exist_ok=True)

    from sistema_abastecimento.modelo_didatico import criar_rede_didatica_exemplo
    rede = criar_rede_didatica_exemplo()

    desenhar_slide_problema(rede, os.path.join(dir_saida, '01_problema_abastecimento.png'))

    res_ff = rede.executar_ford_fulkerson()
    total_ff = len(res_ff['passos'])
    for p in res_ff['passos']:
        caminho_img = os.path.join(dir_ff, f"passo_{p['passo']}_ford_fulkerson.png")
        desenhar_passo_caminho_aumentador(rede, p, 'Ford-Fulkerson (DFS)', caminho_img, total_ff)

    res_ek = rede.executar_edmonds_karp()
    total_ek = len(res_ek['passos'])
    for p in res_ek['passos']:
        caminho_img = os.path.join(dir_ek, f"passo_{p['passo']}_edmonds_karp.png")
        desenhar_passo_caminho_aumentador(rede, p, 'Edmonds-Karp (BFS)', caminho_img, total_ek)

    res_pr = rede.executar_push_relabel_didatico()
    desenhar_push_relabel_didatico(rede, res_pr, os.path.join(dir_saida, '04_push_relabel_cotas_e_bombas.png'))

    res_rtf = rede.executar_relabel_to_front_didatico()
    desenhar_relabel_to_front_didatico(rede, res_rtf, os.path.join(dir_saida, '05_relabel_to_front_lista.png'))

    desenhar_teorema_corte_minimo_didatico(rede, res_ek['fluxos'], os.path.join(dir_saida, '06_teorema_corte_minimo.png'))

    desenhar_quadro_comparativo(os.path.join(dir_saida, '07_quadro_comparativo_algoritmos.png'))
