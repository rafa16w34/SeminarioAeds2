import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon
import os

# Configurações globais de renderização
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

os.makedirs("imagens", exist_ok=True)

# Paleta de Cores Acadêmica Elegante
c_blue = '#1E3A8A'      # Azul Escuro Principal
c_teal = '#0284C7'      # Azul Ciano
c_green = '#16A34A'     # Verde Sucesso / Término
c_amber = '#D97706'     # Âmbar Decisão
c_purple = '#6D28D9'    # Roxo Lista Topológica
c_red = '#DC2626'       # Vermelho Cancelamento
c_text = '#0F172A'      # Texto Escuro Principal
c_muted = '#64748B'     # Cinza Suave Subtítulos

# ==============================================================================
# 1. FLUXOGRAMA: CAMINHOS AUMENTADORES (FORD-FULKERSON & EDMONDS-KARP)
# ==============================================================================
def gerar_caminhos_aumentadores():
    fig, ax = plt.subplots(figsize=(12.5, 5.2), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    # TÍTULO DESTACADO
    ax.text(6.25, 4.82, 'Paradigma de Aumentação Global por Caminhos (Ford-Fulkerson e Edmonds-Karp)', 
            ha='center', va='center', fontsize=11.2, fontweight='bold', color=c_blue)
    ax.text(6.25, 4.45, 'Ciclo Iterativo de Busca na Rede Residual, Gargalo e Cancelamento de Fluxo', 
            ha='center', va='center', fontsize=8.2, fontstyle='italic', color=c_muted)

    def draw_box(x, y, w, h, title, lines, ec=c_blue, fc='#FFFFFF'):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle='round,pad=0.08,rounding_size=0.15',
                             ec=ec, fc=fc, lw=1.3, zorder=2)
        ax.add_patch(box)
        ax.text(x, y + h/2 - 0.22, title, ha='center', va='top', fontsize=7.8, fontweight='bold', color=ec, zorder=3)
        y_cur = y + h/2 - 0.52
        for l in lines:
            ax.text(x, y_cur, l, ha='center', va='top', fontsize=7.0, color=c_text, zorder=3)
            y_cur -= 0.30

    # 1. Início
    box1 = FancyBboxPatch((0.5, 2.2), 1.9, 1.2, boxstyle='round,pad=0.08,rounding_size=0.5',
                          ec=c_blue, fc='#FFFFFF', lw=1.3, zorder=2)
    ax.add_patch(box1)
    ax.text(1.45, 2.95, 'INÍCIO', ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_blue, zorder=3)
    ax.text(1.45, 2.55, r'$f(u, v) = 0, \ \forall (u, v)$', ha='center', va='center', fontsize=7.0, color=c_text, zorder=3)

    # 2. Rede Residual G_f
    draw_box(4.3, 2.8, 2.7, 1.5, '1. Rede Residual $G_f$', [
        r'$c_f(u,v) = c(u,v) - f(u,v)$',
        r'$c_f(v,u) = f(u,v)$'
    ], ec=c_teal)

    # 3. Losango Decisão
    d_x, d_y, d_w, d_h = 7.6, 2.8, 2.5, 1.6
    diamond = Polygon([
        (d_x, d_y + d_h/2), (d_x + d_w/2, d_y),
        (d_x, d_y - d_h/2), (d_x - d_w/2, d_y)
    ], closed=True, ec=c_amber, fc='#FFFFFF', lw=1.3, zorder=2)
    ax.add_patch(diamond)
    ax.text(d_x, d_y + 0.18, r'Existe caminho' + '\n' + r'$s \leadsto t$ em $G_f$?', 
            ha='center', va='center', fontsize=7.4, fontweight='bold', color='#B45309', zorder=3)
    ax.text(d_x, d_y - 0.44, '(DFS em FF / BFS em EK)', ha='center', va='center', fontsize=6.5, fontstyle='italic', color='#78350F', zorder=3)

    # 4. Fim (Ramo NÃO)
    box4 = FancyBboxPatch((9.9, 2.2), 2.1, 1.2, boxstyle='round,pad=0.08,rounding_size=0.5',
                          ec=c_green, fc='#FFFFFF', lw=1.3, zorder=2)
    ax.add_patch(box4)
    ax.text(10.95, 2.95, 'FIM: Fluxo Máximo', ha='center', va='center', fontsize=8.0, fontweight='bold', color=c_green, zorder=3)
    ax.text(10.95, 2.55, r'Corte Mínimo $c(S, T)$', ha='center', va='center', fontsize=6.8, color=c_text, zorder=3)

    # 5. Aumentação (Ramo SIM)
    draw_box(7.6, 0.8, 3.4, 1.3, '2. Aumentação em $p$', [
        r'$c_f(p) = \min_{(u,v) \in p} c_f(u,v)$',
        r'$f(u,v) \leftarrow f(u,v) \pm c_f(p)$'
    ], ec=c_blue)

    # Setas
    def arrow(x1, y1, x2, y2, color=c_text):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='-|>', lw=1.2, color=color, mutation_scale=10), zorder=4)

    arrow(2.4, 2.8, 2.95, 2.8)
    arrow(5.65, 2.8, 6.35, 2.8)
    arrow(8.85, 2.8, 9.9, 2.8)
    ax.text(9.38, 3.02, 'Não', ha='center', va='center', fontsize=7.2, fontweight='bold', color=c_green)

    # Seta para baixo (Sim) com distância generosa de respiro
    arrow(7.6, 2.0, 7.6, 1.48)
    ax.text(7.95, 1.75, 'Sim', ha='left', va='center', fontsize=7.5, fontweight='bold', color=c_blue)

    # Loop de Retorno para Rede Residual
    ax.plot([5.9, 4.3, 4.3], [0.8, 0.8, 2.05], color=c_teal, lw=1.2, linestyle='--', zorder=4)
    ax.annotate('', xy=(4.3, 2.05), xytext=(4.3, 1.95),
                arrowprops=dict(arrowstyle='-|>', lw=1.2, color=c_teal, mutation_scale=10), zorder=4)
    ax.text(5.1, 0.58, 'Atualiza resíduos', ha='center', va='center', fontsize=6.8, fontstyle='italic', color=c_teal)

    plt.tight_layout()
    plt.savefig('imagens/fluxograma_paradigma_caminhos_aumentadores.png', transparent=True, bbox_inches='tight')
    plt.close()
    print("1/3 Saved: fluxograma_paradigma_caminhos_aumentadores.png")


# ==============================================================================
# 2. FLUXOGRAMA: PRÉ-FLUXO LOCAL (PUSH-RELABEL & RELABEL-TO-FRONT) - CORRIGIDO!
# ==============================================================================
def gerar_prefluxo_local():
    fig, ax = plt.subplots(figsize=(15.5, 5.5), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_xlim(0, 16.0)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # TÍTULO DESTACADO
    ax.text(8.0, 5.2, 'Paradigma de Pré-fluxo e Operações Locais (Push-Relabel e Relabel-to-Front)', 
            ha='center', va='center', fontsize=11.5, fontweight='bold', color=c_blue)
    ax.text(8.0, 4.82, 'Ciclo Iterativo de Descarregamento (Discharge), Alturas e Ordenação Topológica', 
            ha='center', va='center', fontsize=8.5, fontstyle='italic', color=c_muted)

    def draw_box(x, y, w, h, title, lines, ec=c_blue, fc='#FFFFFF'):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle='round,pad=0.08,rounding_size=0.15',
                             ec=ec, fc=fc, lw=1.3, zorder=2)
        ax.add_patch(box)
        ax.text(x, y + h/2 - 0.22, title, ha='center', va='top', fontsize=7.8, fontweight='bold', color=ec, zorder=3)
        y_cur = y + h/2 - 0.52
        for l in lines:
            ax.text(x, y_cur, l, ha='center', va='top', fontsize=6.8, color=c_text, zorder=3)
            y_cur -= 0.28

    # 1. Initialize-Preflow
    draw_box(1.5, 2.8, 2.4, 1.8, '1. Initialize-Preflow', [
        r'$h(s) = |V|, \ h(t) = 0$',
        r'$h(u) = 0, \ \forall u \notin \{s,t\}$',
        r'$f(s,v) = c(s,v)$',
        r'$e(v) = c(s,v)$'
    ], ec=c_blue)

    # 2. Losango Vértice Ativo
    d1_x, d1_y, d1_w, d1_h = 4.4, 2.8, 2.2, 1.6
    dia1 = Polygon([
        (d1_x, d1_y + d1_h/2), (d1_x + d1_w/2, d1_y),
        (d1_x, d1_y - d1_h/2), (d1_x - d1_w/2, d1_y)
    ], closed=True, ec=c_amber, fc='#FFFFFF', lw=1.3, zorder=2)
    ax.add_patch(dia1)
    ax.text(d1_x, d1_y + 0.16, r'Existe nó ativo' + '\n' + r'$u$ com $e(u) > 0$?', 
            ha='center', va='center', fontsize=7.2, fontweight='bold', color='#B45309', zorder=3)
    ax.text(d1_x, d1_y - 0.42, r'($u \neq s, t$)', ha='center', va='center', fontsize=6.5, fontstyle='italic', color='#78350F', zorder=3)

    # FIM: Fluxo Máximo (Abaixo do losango 1, livre de qualquer colisão!)
    box_end = FancyBboxPatch((4.4 - 1.1, 0.8 - 0.5), 2.2, 1.0, boxstyle='round,pad=0.08,rounding_size=0.4',
                             ec=c_green, fc='#FFFFFF', lw=1.3, zorder=2)
    ax.add_patch(box_end)
    ax.text(4.4, 1.0, 'FIM: Fluxo Máximo', ha='center', va='center', fontsize=7.6, fontweight='bold', color=c_green, zorder=3)
    ax.text(4.4, 0.65, r'$e(u) = 0, \ \forall u \notin \{s,t\}$', ha='center', va='center', fontsize=6.5, color=c_text, zorder=3)

    # 3. Losango Discharge (Admissível?)
    d2_x, d2_y, d2_w, d2_h = 7.5, 2.8, 2.2, 1.6
    dia2 = Polygon([
        (d2_x, d2_y + d2_h/2), (d2_x + d2_w/2, d2_y),
        (d2_x, d2_y - d2_h/2), (d2_x - d2_w/2, d2_y)
    ], closed=True, ec='#4338CA', fc='#FFFFFF', lw=1.3, zorder=2)
    ax.add_patch(dia2)
    ax.text(d2_x, d2_y + 0.16, r'Aresta $(u, v)$' + '\n' + r'é admissível?', 
            ha='center', va='center', fontsize=7.2, fontweight='bold', color='#4338CA', zorder=3)
    ax.text(d2_x, d2_y - 0.42, r'$c_f > 0$ e $h(u)=h(v)+1$', ha='center', va='center', fontsize=6.2, fontstyle='italic', color='#312E81', zorder=3)

    # 4A. Push (Cima)
    draw_box(10.7, 3.6, 2.4, 1.25, 'Push(u, v)', [
        r'$\Delta = \min(e(u), c_f(u,v))$',
        r'$e(u) \leftarrow e(u) - \Delta$',
        r'$e(v) \leftarrow e(v) + \Delta$'
    ], ec=c_teal)

    # 4B. Relabel (Baixo)
    draw_box(10.7, 2.0, 2.4, 1.25, 'Relabel(u)', [
        r'$h(u) \leftarrow 1 + \min_{(u,v) \in E_f} h(v)$',
        r'$u.atual \leftarrow início(u.N)$'
    ], ec=c_amber)

    # 5. Lista L (Direita, com espaçamento total sem sobreposição!)
    draw_box(14.2, 2.8, 2.4, 1.8, '3. Lista L (RTF)', [
        'Se remarcou $u$:',
        '  move $u$ à frente de $L$;',
        '  reinicia varredura.',
        'Senão: avança $u$ em $L$.'
    ], ec=c_purple)

    # Setas
    def arrow(x1, y1, x2, y2, color=c_text):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='-|>', lw=1.2, color=color, mutation_scale=10), zorder=4)

    # 1 -> 2
    arrow(2.7, 2.8, 3.3, 2.8)

    # 2 -> Fim (Não)
    arrow(4.4, 2.0, 4.4, 1.3, color=c_green)
    ax.text(4.65, 1.65, 'Não', ha='left', va='center', fontsize=7.0, fontweight='bold', color=c_green)

    # 2 -> 3 (Sim)
    arrow(5.5, 2.8, 6.4, 2.8, color=c_blue)
    ax.text(5.95, 3.02, 'Sim', ha='center', va='center', fontsize=7.0, fontweight='bold', color=c_blue)

    # 3 -> Push (Sim)
    ax.plot([d2_x, d2_x, 9.5], [d2_y + d2_h/2, 3.6, 3.6], color=c_teal, lw=1.2, zorder=3)
    ax.annotate('', xy=(9.5, 3.6), xytext=(9.4, 3.6),
                arrowprops=dict(arrowstyle='-|>', lw=1.2, color=c_teal, mutation_scale=10), zorder=4)
    ax.text(7.68, 3.75, 'Sim', ha='center', va='center', fontsize=6.8, fontweight='bold', color=c_teal)

    # 3 -> Relabel (Não)
    ax.plot([d2_x, d2_x, 9.5], [d2_y - d2_h/2, 2.0, 2.0], color=c_amber, lw=1.2, zorder=3)
    ax.annotate('', xy=(9.5, 2.0), xytext=(9.4, 2.0),
                arrowprops=dict(arrowstyle='-|>', lw=1.2, color=c_amber, mutation_scale=10), zorder=4)
    ax.text(7.68, 1.85, 'Não', ha='center', va='center', fontsize=6.8, fontweight='bold', color=c_amber)

    # Push -> Lista L (Conexão limpa sem cruzar caixas)
    ax.plot([11.9, 12.4, 13.0], [3.6, 3.6, 3.1], color=c_purple, lw=1.2, zorder=3)
    ax.annotate('', xy=(13.0, 3.1), xytext=(12.9, 3.15),
                arrowprops=dict(arrowstyle='-|>', lw=1.2, color=c_purple, mutation_scale=10), zorder=4)

    # Relabel -> Lista L
    ax.plot([11.9, 12.4, 13.0], [2.0, 2.0, 2.5], color=c_purple, lw=1.2, zorder=3)
    ax.annotate('', xy=(13.0, 2.5), xytext=(12.9, 2.45),
                arrowprops=dict(arrowstyle='-|>', lw=1.2, color=c_purple, mutation_scale=10), zorder=4)

    # Loop Superior de Retorno (Passa livremente no topo em y = 4.4 sem cruzar nenhuma caixa!)
    ax.plot([14.2, 14.2, 4.4, 4.4], [3.7, 4.4, 4.4, 3.6], color=c_purple, lw=1.2, linestyle='--', zorder=3)
    ax.annotate('', xy=(4.4, 3.6), xytext=(4.4, 3.7),
                arrowprops=dict(arrowstyle='-|>', lw=1.2, color=c_purple, mutation_scale=10), zorder=4)
    ax.text(9.3, 4.58, 'Próxima iteração na lista L', ha='center', va='center', fontsize=6.8, fontstyle='italic', color=c_purple)

    plt.tight_layout()
    plt.savefig('imagens/fluxograma_paradigma_prefluxo_local.png', transparent=True, bbox_inches='tight')
    plt.close()
    print("2/3 Saved: fluxograma_paradigma_prefluxo_local.png")


# ==============================================================================
# 3. DIAGRAMA: ESTADO DE MEMÓRIA E CANCELAMENTO DE FLUXO
# ==============================================================================
def gerar_estado_memoria_cancelamento():
    fig, ax = plt.subplots(figsize=(13.5, 4.4), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 4.4)
    ax.axis('off')

    # TÍTULO DESTACADO
    ax.text(6.75, 4.15, 'Mecânica de Estado de Memória: Arestas Antiparalelas e Cancelamento', 
            ha='center', va='center', fontsize=11.2, fontweight='bold', color=c_blue)
    ax.text(6.75, 3.82, 'Representação Residual em Baixo Nível e Reversão de Decisões sem Backtracking', 
            ha='center', va='center', fontsize=8.2, fontstyle='italic', color=c_muted)

    def draw_node(x, y, label, color='#1E293B'):
        c = plt.Circle((x, y), 0.32, ec=color, fc='#FFFFFF', lw=1.4, zorder=3)
        ax.add_patch(c)
        ax.text(x, y, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color=color, zorder=4)

    # Painel 1: (a) Aresta Física Original
    box_p1 = FancyBboxPatch((0.4, 0.4), 3.8, 3.1, boxstyle='round,pad=0.08,rounding_size=0.15',
                            ec='#CBD5E1', fc='#FFFFFF', lw=1.2, zorder=1)
    ax.add_patch(box_p1)
    ax.text(2.3, 3.2, '(a) Aresta Original em $G$', ha='center', va='center', fontsize=8.2, fontweight='bold', color=c_blue)
    draw_node(1.15, 2.0, 'u')
    draw_node(3.45, 2.0, 'v')
    ax.annotate('', xy=(3.13, 2.0), xytext=(1.47, 2.0),
                arrowprops=dict(arrowstyle='-|>', lw=2.0, color=c_teal, mutation_scale=12), zorder=2)
    ax.text(2.3, 2.3, r'$f = 6 \ / \ c = 10$', ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_teal)
    ax.text(2.3, 0.95, 'Capacidade nominal $c = 10$\nFluxo corrente $f = 6$', ha='center', va='center', fontsize=6.8, color=c_muted)

    # Painel 2: (b) Rede Residual G_f
    box_p2 = FancyBboxPatch((4.7, 0.4), 4.1, 3.1, boxstyle='round,pad=0.08,rounding_size=0.15',
                            ec='#CBD5E1', fc='#FFFFFF', lw=1.2, zorder=1)
    ax.add_patch(box_p2)
    ax.text(6.75, 3.2, '(b) Rede Residual $G_f$', ha='center', va='center', fontsize=8.2, fontweight='bold', color=c_blue)
    draw_node(5.45, 2.0, 'u')
    draw_node(8.05, 2.0, 'v')
    # Direta
    ax.annotate('', xy=(7.73, 2.22), xytext=(5.77, 2.22),
                arrowprops=dict(arrowstyle='-|>', lw=1.4, color=c_teal, mutation_scale=10), zorder=2)
    ax.text(6.75, 2.52, r'$c_f(u,v) = 10 - 6 = 4$ (avanço)', ha='center', va='center', fontsize=6.8, fontweight='bold', color=c_teal)
    # Reversa
    ax.annotate('', xy=(5.77, 1.78), xytext=(7.73, 1.78),
                arrowprops=dict(arrowstyle='-|>', lw=1.4, color=c_red, linestyle='--', mutation_scale=10), zorder=2)
    ax.text(6.75, 1.48, r'$c_f(v,u) = f = 6$ (cancelamento)', ha='center', va='center', fontsize=6.8, fontweight='bold', color=c_red)
    ax.text(6.75, 0.85, 'Aresta reversa permite desfazer fluxo!', ha='center', va='center', fontsize=6.6, fontstyle='italic', color=c_muted)

    # Painel 3: (c) Cancelamento de Fluxo
    box_p3 = FancyBboxPatch((9.3, 0.4), 3.8, 3.1, boxstyle='round,pad=0.08,rounding_size=0.15',
                            ec='#CBD5E1', fc='#FFFFFF', lw=1.2, zorder=1)
    ax.add_patch(box_p3)
    ax.text(11.2, 3.2, '(c) Efeito do Cancelamento', ha='center', va='center', fontsize=8.2, fontweight='bold', color=c_blue)
    draw_node(10.05, 2.0, 'u')
    draw_node(12.35, 2.0, 'v')
    ax.annotate('', xy=(12.03, 2.0), xytext=(10.37, 2.0),
                arrowprops=dict(arrowstyle='-|>', lw=2.0, color=c_green, mutation_scale=12), zorder=2)
    ax.text(11.2, 2.3, r'Novo $f = 4 \ / \ c = 10$', ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_green)
    ax.text(11.2, 1.15, 'Caminho usou reversa ($\\Delta = 2$):\n$f(u,v) \\leftarrow 6 - 2 = 4$\n(Desfez 2 un. sem backtracking)', 
            ha='center', va='center', fontsize=6.6, color=c_text)

    plt.tight_layout()
    plt.savefig('imagens/diagrama_estado_memoria_cancelamento.png', transparent=True, bbox_inches='tight')
    plt.close()
    print("3/3 Saved: diagrama_estado_memoria_cancelamento.png")

gerar_caminhos_aumentadores()
gerar_prefluxo_local()
gerar_estado_memoria_cancelamento()
