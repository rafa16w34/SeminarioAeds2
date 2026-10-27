import copy
from collections import deque

class No:
    def __init__(self, id_no, rotulo, x, y):
        self.id = id_no
        self.rotulo = rotulo
        self.x = x
        self.y = y

class Arco:
    def __init__(self, u, v, capacidade):
        self.u = u
        self.v = v
        self.capacidade = capacidade

class RedeDidatica:
    def __init__(self):
        self.nos = {}
        self.arcos = {}
        self.adjacencia = {}
        self.fonte = 's'
        self.sorvedouro = 't'

    def adicionar_no(self, id_no, rotulo, x, y):
        self.nos[id_no] = No(id_no, rotulo, x, y)
        if id_no not in self.adjacencia:
            self.adjacencia[id_no] = []

    def adicionar_arco(self, u, v, capacidade):
        self.arcos[(u, v)] = Arco(u, v, capacidade)
        if u not in self.adjacencia:
            self.adjacencia[u] = []
        if v not in self.adjacencia:
            self.adjacencia[v] = []
        if v not in self.adjacencia[u]:
            self.adjacencia[u].append(v)
        if u not in self.adjacencia[v]:
            self.adjacencia[v].append(u)

    def obter_capacidade(self, u, v):
        if (u, v) in self.arcos:
            return self.arcos[(u, v)].capacidade
        return 0

    def executar_ford_fulkerson(self):
        fluxo = {(u, v): 0 for u, v in self.arcos}
        for u, v in self.arcos:
            if (v, u) not in fluxo:
                fluxo[(v, u)] = 0

        passos = []
        fluxo_total = 0
        passo_num = 1

        while True:
            pai = {}
            visitados = {self.fonte}
            pilha = [self.fonte]

            while pilha:
                atual = pilha.pop()
                if atual == self.sorvedouro:
                    break

                for vizinho in sorted(self.adjacencia.get(atual, [])):
                    residual = self.obter_capacidade(atual, vizinho) - fluxo.get((atual, vizinho), 0)
                    if residual > 0 and vizinho not in visitados:
                        visitados.add(vizinho)
                        pai[vizinho] = atual
                        pilha.append(vizinho)

            if self.sorvedouro not in pai:
                break

            gargalo = float('inf')
            curr = self.sorvedouro
            caminho = []
            while curr != self.fonte:
                caminho.append(curr)
                p = pai[curr]
                res = self.obter_capacidade(p, curr) - fluxo.get((p, curr), 0)
                if res < gargalo:
                    gargalo = res
                curr = p
            caminho.append(self.fonte)
            caminho.reverse()

            for i in range(len(caminho) - 1):
                u = caminho[i]
                v = caminho[i + 1]
                fluxo[(u, v)] = fluxo.get((u, v), 0) + gargalo
                fluxo[(v, u)] = fluxo.get((v, u), 0) - gargalo

            fluxo_total += gargalo
            passos.append({
                'passo': passo_num,
                'caminho': caminho,
                'gargalo': gargalo,
                'fluxo_total': fluxo_total,
                'fluxos': copy.deepcopy(fluxo)
            })
            passo_num += 1

        return {
            'algoritmo': 'Ford-Fulkerson (DFS)',
            'fluxo_maximo': fluxo_total,
            'passos': passos,
            'fluxos': fluxo
        }

    def executar_edmonds_karp(self):
        fluxo = {(u, v): 0 for u, v in self.arcos}
        for u, v in self.arcos:
            if (v, u) not in fluxo:
                fluxo[(v, u)] = 0

        passos = []
        fluxo_total = 0
        passo_num = 1

        while True:
            pai = {}
            visitados = {self.fonte}
            fila = deque([self.fonte])

            while fila:
                atual = fila.popleft()
                if atual == self.sorvedouro:
                    break

                for vizinho in sorted(self.adjacencia.get(atual, [])):
                    residual = self.obter_capacidade(atual, vizinho) - fluxo.get((atual, vizinho), 0)
                    if residual > 0 and vizinho not in visitados:
                        visitados.add(vizinho)
                        pai[vizinho] = atual
                        fila.append(vizinho)

            if self.sorvedouro not in pai:
                break

            gargalo = float('inf')
            curr = self.sorvedouro
            caminho = []
            while curr != self.fonte:
                caminho.append(curr)
                p = pai[curr]
                res = self.obter_capacidade(p, curr) - fluxo.get((p, curr), 0)
                if res < gargalo:
                    gargalo = res
                curr = p
            caminho.append(self.fonte)
            caminho.reverse()

            for i in range(len(caminho) - 1):
                u = caminho[i]
                v = caminho[i + 1]
                fluxo[(u, v)] = fluxo.get((u, v), 0) + gargalo
                fluxo[(v, u)] = fluxo.get((v, u), 0) - gargalo

            fluxo_total += gargalo
            passos.append({
                'passo': passo_num,
                'caminho': caminho,
                'gargalo': gargalo,
                'fluxo_total': fluxo_total,
                'fluxos': copy.deepcopy(fluxo)
            })
            passo_num += 1

        return {
            'algoritmo': 'Edmonds-Karp (BFS)',
            'fluxo_maximo': fluxo_total,
            'passos': passos,
            'fluxos': fluxo
        }

    def executar_push_relabel_didatico(self):
        n = len(self.nos)
        alturas = {u: 0 for u in self.nos}
        excessos = {u: 0 for u in self.nos}
        fluxo = {(u, v): 0 for u, v in self.arcos}
        for u, v in self.arcos:
            if (v, u) not in fluxo:
                fluxo[(v, u)] = 0

        alturas[self.fonte] = n
        etapas = []

        for v in sorted(self.adjacencia.get(self.fonte, [])):
            cap = self.obter_capacidade(self.fonte, v)
            if cap > 0:
                fluxo[(self.fonte, v)] = cap
                fluxo[(v, self.fonte)] = -cap
                excessos[v] = cap
                excessos[self.fonte] -= cap

        etapas.append({
            'etapa': 1,
            'titulo': 'Inicialização do Pré-Fluxo Saturante',
            'descricao': f"A Represa (cota h={n}) enche as tubulações s->A e s->B com capacidade máxima por gravidade.",
            'alturas': copy.deepcopy(alturas),
            'excessos': copy.deepcopy(excessos),
            'fluxos': copy.deepcopy(fluxo),
            'operacao': 'SATURACAO_FONTE'
        })

        iteracao = 2
        while True:
            candidatos = [u for u in self.nos if u != self.fonte and u != self.sorvedouro and excessos[u] > 0]
            if not candidatos:
                break

            u = candidatos[0]
            vizinho_descida = None
            for v in sorted(self.adjacencia.get(u, [])):
                residual = self.obter_capacidade(u, v) - fluxo.get((u, v), 0)
                if residual > 0 and alturas[u] == alturas[v] + 1:
                    vizinho_descida = v
                    break

            if vizinho_descida is not None:
                v = vizinho_descida
                residual = self.obter_capacidade(u, v) - fluxo.get((u, v), 0)
                delta = min(excessos[u], residual)
                fluxo[(u, v)] += delta
                fluxo[(v, u)] -= delta
                excessos[u] -= delta
                excessos[v] += delta
                etapas.append({
                    'etapa': iteracao,
                    'titulo': f"Operação PUSH: {u} → {v}",
                    'descricao': f"Água escorre morro abaixo de {u} (h={alturas[u]}) para {v} (h={alturas[v]}). Vazão: {delta} m³/h.",
                    'alturas': copy.deepcopy(alturas),
                    'excessos': copy.deepcopy(excessos),
                    'fluxos': copy.deepcopy(fluxo),
                    'operacao': 'PUSH',
                    'u': u,
                    'v': v,
                    'delta': delta
                })
            else:
                menor_altura_vizinho = float('inf')
                for v in sorted(self.adjacencia.get(u, [])):
                    residual = self.obter_capacidade(u, v) - fluxo.get((u, v), 0)
                    if residual > 0 and alturas[v] < menor_altura_vizinho:
                        menor_altura_vizinho = alturas[v]

                if menor_altura_vizinho < float('inf'):
                    antiga = alturas[u]
                    alturas[u] = 1 + menor_altura_vizinho
                    etapas.append({
                        'etapa': iteracao,
                        'titulo': f"Operação RELABEL: Elevação em {u}",
                        'descricao': f"Estação {u} tem água represada mas não há saída morro abaixo. Aciona bomba e eleva cota de {antiga} para {alturas[u]}.",
                        'alturas': copy.deepcopy(alturas),
                        'excessos': copy.deepcopy(excessos),
                        'fluxos': copy.deepcopy(fluxo),
                        'operacao': 'RELABEL',
                        'u': u,
                        'altura_antiga': antiga,
                        'nova_altura': alturas[u]
                    })
            iteracao += 1
            if iteracao > 100:
                break

        fluxo_final = sum(fluxo.get((u, self.sorvedouro), 0) for u in self.adjacencia.get(self.sorvedouro, []))

        return {
            'algoritmo': 'Push-Relabel (Goldberg-Tarjan)',
            'fluxo_maximo': fluxo_final,
            'etapas': etapas,
            'alturas_finais': alturas,
            'excessos_finais': excessos,
            'fluxos': fluxo
        }

    def executar_relabel_to_front_didatico(self):
        n = len(self.nos)
        alturas = {u: 0 for u in self.nos}
        excessos = {u: 0 for u in self.nos}
        fluxo = {(u, v): 0 for u, v in self.arcos}
        for u, v in self.arcos:
            if (v, u) not in fluxo:
                fluxo[(v, u)] = 0

        alturas[self.fonte] = n
        for v in sorted(self.adjacencia.get(self.fonte, [])):
            cap = self.obter_capacidade(self.fonte, v)
            if cap > 0:
                fluxo[(self.fonte, v)] = cap
                fluxo[(v, self.fonte)] = -cap
                excessos[v] = cap
                excessos[self.fonte] -= cap

        lista_l = [u for u in sorted(self.nos.keys()) if u != self.fonte and u != self.sorvedouro]
        etapas_l = []

        etapas_l.append({
            'etapa': 1,
            'titulo': 'Inicialização da Lista L',
            'descricao': f"Vértices intermediários organizados em lista encadeada L: {lista_l}.",
            'lista_l': list(lista_l),
            'no_foco': lista_l[0],
            'alturas': copy.deepcopy(alturas),
            'excessos': copy.deepcopy(excessos)
        })

        idx = 0
        contador = 2
        while idx < len(lista_l):
            u = lista_l[idx]
            altura_anterior = alturas[u]

            while excessos[u] > 0:
                empurrou = False
                for v in sorted(self.adjacencia.get(u, [])):
                    res = self.obter_capacidade(u, v) - fluxo.get((u, v), 0)
                    if res > 0 and alturas[u] == alturas[v] + 1:
                        delta = min(excessos[u], res)
                        fluxo[(u, v)] += delta
                        fluxo[(v, u)] -= delta
                        excessos[u] -= delta
                        excessos[v] += delta
                        empurrou = True
                        if excessos[u] == 0:
                            break

                if not empurrou:
                    min_h = float('inf')
                    for v in sorted(self.adjacencia.get(u, [])):
                        res = self.obter_capacidade(u, v) - fluxo.get((u, v), 0)
                        if res > 0 and alturas[v] < min_h:
                            min_h = alturas[v]
                    if min_h < float('inf'):
                        alturas[u] = 1 + min_h

            if alturas[u] > altura_anterior:
                no_movido = lista_l.pop(idx)
                lista_l.insert(0, no_movido)
                etapas_l.append({
                    'etapa': contador,
                    'titulo': f"Descarga e Movimento to-front ({u})",
                    'descricao': f"Nó {u} foi elevado para cota {alturas[u]} e movido para a frente da lista L.",
                    'lista_l': list(lista_l),
                    'no_foco': u,
                    'alturas': copy.deepcopy(alturas),
                    'excessos': copy.deepcopy(excessos)
                })
                idx = 0
            else:
                idx += 1

            contador += 1
            if contador > 50:
                break

        fluxo_final = sum(fluxo.get((u, self.sorvedouro), 0) for u in self.adjacencia.get(self.sorvedouro, []))

        return {
            'algoritmo': 'Relabel-to-Front',
            'fluxo_maximo': fluxo_final,
            'etapas': etapas_l,
            'lista_final': lista_l,
            'fluxos': fluxo
        }

    def calcular_corte_minimo(self, fluxos):
        visitados = set()
        fila = deque([self.fonte])
        visitados.add(self.fonte)

        while fila:
            atual = fila.popleft()
            for vizinho in self.adjacencia.get(atual, []):
                residual = self.obter_capacidade(atual, vizinho) - fluxos.get((atual, vizinho), 0)
                if residual > 0 and vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)

        corte_s = visitados
        corte_t = set(self.nos.keys()) - corte_s

        arestas_corte = []
        capacidade_total = 0
        for (u, v), arco in self.arcos.items():
            if u in corte_s and v in corte_t:
                arestas_corte.append({
                    'u': u,
                    'v': v,
                    'capacidade': arco.capacidade,
                    'fluxo': fluxos.get((u, v), 0)
                })
                capacidade_total += arco.capacidade

        return corte_s, corte_t, arestas_corte, capacidade_total

def criar_rede_didatica_exemplo():
    rede = RedeDidatica()
    rede.adicionar_no('s', 'Represa (s)', 0.5, 2.0)
    rede.adicionar_no('A', 'ETA Norte (A)', 2.5, 3.2)
    rede.adicionar_no('B', 'ETA Sul (B)', 2.5, 0.8)
    rede.adicionar_no('C', 'Res. Central (C)', 4.8, 3.2)
    rede.adicionar_no('D', 'Res. Leste (D)', 4.8, 0.8)
    rede.adicionar_no('t', 'Cidade (t)', 6.8, 2.0)

    rede.adicionar_arco('s', 'A', 12)
    rede.adicionar_arco('s', 'B', 10)
    rede.adicionar_arco('A', 'C', 9)
    rede.adicionar_arco('A', 'D', 5)
    rede.adicionar_arco('B', 'C', 4)
    rede.adicionar_arco('B', 'D', 8)
    rede.adicionar_arco('C', 't', 11)
    rede.adicionar_arco('D', 't', 10)

    return rede
