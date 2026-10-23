#include "AlgoritmosFluxoMaximo.hpp"
#include <vector>
#include <list>
#include <algorithm>
#include <chrono>

namespace fluxo{

ResultadoAlgoritmo AlgoritmosFluxoMaximo::relabel_to_front(Grafo& g){
    ResultadoAlgoritmo resultado;
    resultado.nome_algoritmo = "Relabel-to-Front";

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
    std::vector<size_t> aresta_atual(n, 0);

    long long total_pushes = 0;
    long long total_relabels = 0;
    long long total_discharges = 0;

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
        }
    }

    std::list<int> L;
    for(int i = 0; i < n; ++i){
        if(i != s && i != t){
            L.push_back(i);
        }
    }

    auto descarregar = [&](int u){
        auto& arestas = g.arestas_de(u);
        while(excesso[u] > 0){
            if(aresta_atual[u] >= arestas.size()){
                int menor_altura = 2 * n;
                for(const auto& aresta : arestas){
                    if(aresta.cap > 0){
                        menor_altura = std::min(menor_altura, altura[aresta.para]);
                    }
                }
                if(menor_altura < 2 * n){
                    altura[u] = 1 + menor_altura;
                    total_relabels++;
                }
                aresta_atual[u] = 0;
            }else{
                auto& aresta = arestas[aresta_atual[u]];
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
                }else{
                    aresta_atual[u]++;
                }
            }
        }
    };

    auto it = L.begin();
    while(it != L.end()){
        int u = *it;
        int altura_anterior = altura[u];

        descarregar(u);
        total_discharges++;

        if(altura[u] > altura_anterior){
            L.erase(it);
            L.push_front(u);
            it = std::next(L.begin());
        }else{
            ++it;
        }
    }

    auto fim = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::micro> duracao_us = fim - inicio;

    resultado.fluxo_maximo = excesso[t];
    resultado.tempo_microssegundos = duracao_us.count();
    resultado.tempo_milissegundos = duracao_us.count() / 1000.0;
    resultado.pushes = total_pushes;
    resultado.relabels = total_relabels;
    resultado.iteracoes = total_discharges;
    resultado.corte_minimo_s = g.calcular_corte_minimo_s();

    return resultado;
}

}
