#include "AlgoritmosFluxoMaximo.hpp"
#include <vector>
#include <queue>
#include <algorithm>
#include <chrono>

namespace fluxo{

ResultadoAlgoritmo AlgoritmosFluxoMaximo::push_relabel_generico(Grafo& g){
    ResultadoAlgoritmo resultado;
    resultado.nome_algoritmo = "Push-Relabel (Genérico)";

    int s = g.fonte();
    int t = g.sorvedouro();
    int n = static_cast<int>(g.num_vertices());

    if(s < 0 || t < 0 || s >= n || t >= n || s == t){
        return resultado;
    }

    g.resetar_fluxo();

    auto inicio = std::chrono::high_resolution_clock::now();

    std::vector<long long> excesso(n, 0);
    std::vector<int> altura(n, 0);
    std::vector<bool> na_fila(n, false);
    std::queue<int> fila_ativos;

    long long total_pushes = 0;
    long long total_relabels = 0;

    altura[s] = n;
    altura[t] = 0;

    for(auto& aresta : g.arestas_de(s)){
        if(aresta.cap > 0){
            long long delta = aresta.cap;
            auto& rev = g.arestas_de(aresta.para)[aresta.rev];

            aresta.cap -= delta;
            rev.cap += delta;
            aresta.fluxo += delta;
            rev.fluxo -= delta;

            excesso[s] -= delta;
            excesso[aresta.para] += delta;
            total_pushes++;

            if(aresta.para != s && aresta.para != t && !na_fila[aresta.para]){
                fila_ativos.push(aresta.para);
                na_fila[aresta.para] = true;
            }
        }
    }

    while(!fila_ativos.empty()){
        int u = fila_ativos.front();
        fila_ativos.pop();
        na_fila[u] = false;

        auto& arestas = g.arestas_de(u);

        for(auto& aresta : arestas){
            if(excesso[u] == 0){
                break;
            }

            if(aresta.cap > 0 && altura[u] == altura[aresta.para] + 1){
                long long delta = std::min(excesso[u], aresta.cap);
                auto& rev = g.arestas_de(aresta.para)[aresta.rev];

                aresta.cap -= delta;
                rev.cap += delta;
                aresta.fluxo += delta;
                rev.fluxo -= delta;

                excesso[u] -= delta;
                excesso[aresta.para] += delta;
                total_pushes++;

                if(aresta.para != s && aresta.para != t && !na_fila[aresta.para]){
                    fila_ativos.push(aresta.para);
                    na_fila[aresta.para] = true;
                }
            }
        }

        if(excesso[u] > 0){
            int menor_altura_vizinho = 2 * n;
            for(const auto& aresta : arestas){
                if(aresta.cap > 0){
                    menor_altura_vizinho = std::min(menor_altura_vizinho, altura[aresta.para]);
                }
            }

            if(menor_altura_vizinho < 2 * n){
                altura[u] = 1 + menor_altura_vizinho;
                total_relabels++;
            }

            fila_ativos.push(u);
            na_fila[u] = true;
        }
    }

    auto fim = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::micro> duracao_us = fim - inicio;

    resultado.fluxo_maximo = excesso[t];
    resultado.tempo_microssegundos = duracao_us.count();
    resultado.tempo_milissegundos = duracao_us.count() / 1000.0;
    resultado.pushes = total_pushes;
    resultado.relabels = total_relabels;
    resultado.iteracoes = total_pushes + total_relabels;
    resultado.corte_minimo_s = g.calcular_corte_minimo_s();

    return resultado;
}

}
