#include "AlgoritmosFluxoMaximo.hpp"
#include <vector>
#include <queue>
#include <algorithm>
#include <chrono>

namespace fluxo{

ResultadoAlgoritmo AlgoritmosFluxoMaximo::edmonds_karp_bfs(Grafo& g){
    ResultadoAlgoritmo resultado;
    resultado.nome_algoritmo = "Edmonds-Karp (BFS)";

    int s = g.fonte();
    int t = g.sorvedouro();
    int n = static_cast<int>(g.num_vertices());

    if(s < 0 || t < 0 || s >= n || t >= n || s == t){
        return resultado;
    }

    g.resetar_fluxo();

    auto inicio = std::chrono::high_resolution_clock::now();

    long long fluxo_total = 0;
    long long caminhos_aumentadores = 0;

    struct ArestaPai{
        int u = -1;
        int idx = -1;
    };

    while(true){
        std::vector<ArestaPai> pai(n);
        std::vector<bool> visitado(n, false);
        std::queue<int> fila;

        visitado[s] = true;
        fila.push(s);

        bool alcancou_sorvedouro = false;

        while(!fila.empty()){
            int u = fila.front();
            fila.pop();

            if(u == t){
                alcancou_sorvedouro = true;
                break;
            }

            const auto& arestas = g.arestas_de(u);
            for(size_t i = 0; i < arestas.size(); ++i){
                const auto& aresta = arestas[i];
                if(!visitado[aresta.para] && aresta.cap > 0){
                    visitado[aresta.para] = true;
                    pai[aresta.para] = {u, static_cast<int>(i)};
                    fila.push(aresta.para);
                }
            }
        }

        if(!alcancou_sorvedouro){
            break;
        }

        long long gargalo = 1e18;
        int atual = t;
        while(atual != s){
            int u = pai[atual].u;
            int idx = pai[atual].idx;
            const auto& aresta = g.arestas_de(u)[idx];
            gargalo = std::min(gargalo, aresta.cap);
            atual = u;
        }

        atual = t;
        while(atual != s){
            int u = pai[atual].u;
            int idx = pai[atual].idx;
            auto& fwd = g.arestas_de(u)[idx];
            auto& rev = g.arestas_de(atual)[fwd.rev];

            fwd.cap -= gargalo;
            rev.cap += gargalo;
            fwd.fluxo += gargalo;
            rev.fluxo -= gargalo;

            atual = u;
        }

        fluxo_total += gargalo;
        caminhos_aumentadores++;
    }

    auto fim = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::micro> duracao_us = fim - inicio;

    resultado.fluxo_maximo = fluxo_total;
    resultado.tempo_microssegundos = duracao_us.count();
    resultado.tempo_milissegundos = duracao_us.count() / 1000.0;
    resultado.iteracoes = caminhos_aumentadores;
    resultado.corte_minimo_s = g.calcular_corte_minimo_s();

    return resultado;
}

}
