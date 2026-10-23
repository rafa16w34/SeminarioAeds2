#pragma once

#include "Grafo.hpp"

namespace fluxo{

class AlgoritmosFluxoMaximo{
public:
    static ResultadoAlgoritmo ford_fulkerson_dfs(Grafo& g);
    static ResultadoAlgoritmo edmonds_karp_bfs(Grafo& g);
    static ResultadoAlgoritmo push_relabel_generico(Grafo& g);
    static ResultadoAlgoritmo relabel_to_front(Grafo& g);
};

}
