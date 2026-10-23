#include "Grafo.hpp"
#include <queue>
#include <algorithm>

namespace fluxo{

Grafo::Grafo(int num_vertices){
    adj_.resize(num_vertices);
    id_para_nome_.resize(num_vertices);
    for(int i = 0; i < num_vertices; ++i){
        id_para_nome_[i] = std::to_string(i);
        nome_para_id_[id_para_nome_[i]] = i;
    }
}

int Grafo::obter_ou_criar_vertice(const std::string& nome){
    auto it = nome_para_id_.find(nome);
    if(it != nome_para_id_.end()){
        return it->second;
    }
    int id = static_cast<int>(adj_.size());
    adj_.emplace_back();
    id_para_nome_.push_back(nome);
    nome_para_id_[nome] = id;
    return id;
}

int Grafo::obter_id_vertice(const std::string& nome) const{
    auto it = nome_para_id_.find(nome);
    if(it == nome_para_id_.end()){
        throw std::runtime_error("Vertice '" + nome + "' nao encontrado no grafo.");
    }
    return it->second;
}

std::string Grafo::obter_nome_vertice(int id) const{
    if(id < 0 || id >= static_cast<int>(id_para_nome_.size())){
        return std::to_string(id);
    }
    return id_para_nome_[id];
}

void Grafo::adicionar_aresta(int u, int v, long long capacidade){
    if(u < 0 || v < 0){
        throw std::runtime_error("Indice de vertice invalido em adicionar_aresta.");
    }
    int max_id = std::max(u, v);
    if(max_id >= static_cast<int>(adj_.size())){
        adj_.resize(max_id + 1);
        id_para_nome_.resize(max_id + 1);
        for(int i = 0; i <= max_id; ++i){
            if(id_para_nome_[i].empty()){
                id_para_nome_[i] = std::to_string(i);
                nome_para_id_[id_para_nome_[i]] = i;
            }
        }
    }

    int rev_u = static_cast<int>(adj_[v].size());
    int rev_v = static_cast<int>(adj_[u].size());

    adj_[u].push_back(Aresta{u, v, capacidade, capacidade, 0, rev_u});
    adj_[v].push_back(Aresta{v, u, 0, 0, 0, rev_v});

    total_arestas_++;
}

void Grafo::adicionar_aresta(const std::string& u, const std::string& v, long long capacidade){
    int uid = obter_ou_criar_vertice(u);
    int vid = obter_ou_criar_vertice(v);
    adicionar_aresta(uid, vid, capacidade);
}

void Grafo::definir_fonte(int s){
    fonte_id_ = s;
}

void Grafo::definir_fonte(const std::string& s){
    fonte_id_ = obter_ou_criar_vertice(s);
}

void Grafo::definir_sorvedouro(int t){
    sorvedouro_id_ = t;
}

void Grafo::definir_sorvedouro(const std::string& t){
    sorvedouro_id_ = obter_ou_criar_vertice(t);
}

void Grafo::resetar_fluxo(){
    for(auto& lista : adj_){
        for(auto& aresta : lista){
            aresta.cap = aresta.cap_original;
            aresta.fluxo = 0;
        }
    }
}

Grafo Grafo::clonar() const{
    Grafo g;
    g.adj_ = this->adj_;
    g.nome_para_id_ = this->nome_para_id_;
    g.id_para_nome_ = this->id_para_nome_;
    g.fonte_id_ = this->fonte_id_;
    g.sorvedouro_id_ = this->sorvedouro_id_;
    g.total_arestas_ = this->total_arestas_;
    return g;
}

std::vector<int> Grafo::calcular_corte_minimo_s() const{
    std::vector<int> corte_s;
    if(fonte_id_ < 0 || fonte_id_ >= static_cast<int>(adj_.size())){
        return corte_s;
    }

    std::vector<bool> visitado(adj_.size(), false);
    std::queue<int> fila;

    visitado[fonte_id_] = true;
    fila.push(fonte_id_);

    while(!fila.empty()){
        int u = fila.front();
        fila.pop();
        corte_s.push_back(u);

        for(const auto& aresta : adj_[u]){
            if(aresta.cap > 0 && !visitado[aresta.para]){
                visitado[aresta.para] = true;
                fila.push(aresta.para);
            }
        }
    }
    return corte_s;
}

}
