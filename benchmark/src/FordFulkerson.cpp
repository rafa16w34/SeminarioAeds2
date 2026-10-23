#include "AlgoritmosFluxoMaximo.hpp"
#include <vector>
#include <algorithm>
#include <chrono>

namespace fluxo{
namespace{

long long dfs_buscar_caminho(Grafo& g, int u, int t, long long fluxo_atual, std::vector<bool>& visitado, std::vector<std::pair<int, int>>& caminho, size_t deslocamento_inicial = 0){
    if(u == t){
        return fluxo_atual;
    }
    visitado[u] = true;

    auto& arestas = g.arestas_de(u);
    size_t total = arestas.size();

    for(size_t offset = 0; offset < total; ++offset){
        size_t i = (offset + deslocamento_inicial) % total;
        auto& aresta = arestas[i];
        if(!visitado[aresta.para] && aresta.cap > 0){
            caminho.push_back({u, static_cast<int>(i)});
            long long empurrado = dfs_buscar_caminho(g, aresta.para, t, std::min(fluxo_atual, aresta.cap), visitado, caminho, 0);
            if(empurrado > 0){
                return empurrado;
            }
            caminho.pop_back();
        }
    }
    return 0;
}

}

ResultadoAlgoritmo AlgoritmosFluxoMaximo::ford_fulkerson_dfs(Grafo& g){
    ResultadoAlgoritmo resultado;
    resultado.nome_algoritmo = "Ford-Fulkerson (DFS)";

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

    while(true){
        std::vector<bool> visitado(n, false);
        std::vector<std::pair<int, int>> caminho;
        size_t deslocamento = g.arestas_de(s).empty() ? 0 : (caminhos_aumentadores % g.arestas_de(s).size());
        long long gargalo = dfs_buscar_caminho(g, s, t, 1e18, visitado, caminho, deslocamento);

        if(gargalo == 0){
            break;
        }

        for(const auto& passo : caminho){
            int u = passo.first;
            int idx = passo.second;
            auto& fwd = g.arestas_de(u)[idx];
            auto& rev = g.arestas_de(fwd.para)[fwd.rev];

            fwd.cap -= gargalo;
            rev.cap += gargalo;
            fwd.fluxo += gargalo;
            rev.fluxo -= gargalo;
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
