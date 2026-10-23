#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include <stdexcept>

namespace fluxo{

struct Aresta{
    int de;
    int para;
    long long cap;
    long long cap_original;
    long long fluxo;
    int rev;
};

struct ResultadoAlgoritmo{
    std::string nome_algoritmo;
    long long fluxo_maximo = 0;
    double tempo_microssegundos = 0.0;
    double tempo_milissegundos = 0.0;
    long long iteracoes = 0;
    long long pushes = 0;
    long long relabels = 0;
    std::vector<int> corte_minimo_s;
};

class Grafo{
public:
    Grafo() = default;
    explicit Grafo(int num_vertices);

    int obter_ou_criar_vertice(const std::string& nome);
    int obter_id_vertice(const std::string& nome) const;
    std::string obter_nome_vertice(int id) const;

    void adicionar_aresta(int u, int v, long long capacidade);
    void adicionar_aresta(const std::string& u, const std::string& v, long long capacidade);

    void definir_fonte(int s);
    void definir_fonte(const std::string& s);
    void definir_sorvedouro(int t);
    void definir_sorvedouro(const std::string& t);

    int fonte() const{ return fonte_id_; }
    int sorvedouro() const{ return sorvedouro_id_; }
    size_t num_vertices() const{ return adj_.size(); }
    size_t num_arestas() const{ return total_arestas_; }

    const std::vector<Aresta>& arestas_de(int u) const{ return adj_.at(u); }
    std::vector<Aresta>& arestas_de(int u){ return adj_.at(u); }

    void resetar_fluxo();
    Grafo clonar() const;
    std::vector<int> calcular_corte_minimo_s() const;

private:
    std::vector<std::vector<Aresta>> adj_;
    std::unordered_map<std::string, int> nome_para_id_;
    std::vector<std::string> id_para_nome_;
    int fonte_id_ = -1;
    int sorvedouro_id_ = -1;
    size_t total_arestas_ = 0;
};

}
