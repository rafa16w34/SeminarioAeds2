#include "ExecutorBenchmark.hpp"
#include "LeitorGrafo.hpp"
#include "AlgoritmosFluxoMaximo.hpp"
#include <iostream>
#include <fstream>
#include <iomanip>
#include <filesystem>

namespace fluxo{
namespace{

std::string obter_nome_base(const std::string& caminho){
    std::filesystem::path p(caminho);
    return p.stem().string();
}

std::string obter_extensao(const std::string& caminho){
    std::filesystem::path p(caminho);
    return p.extension().string();
}

}

EntradaTeste ExecutorBenchmark::executar_arquivo_unico(const std::string& caminho_arquivo, const std::string& fonte, const std::string& sorvedouro){
    EntradaTeste entrada;
    entrada.caminho_arquivo = caminho_arquivo;
    entrada.nome_teste = obter_nome_base(caminho_arquivo);
    entrada.formato = obter_extensao(caminho_arquivo);

    Grafo grafo_base = LeitorGrafo::carregar_de_arquivo(caminho_arquivo, fonte, sorvedouro);
    entrada.num_vertices = grafo_base.num_vertices();
    entrada.num_arestas = grafo_base.num_arestas();
    entrada.nome_fonte = grafo_base.obter_nome_vertice(grafo_base.fonte());
    entrada.nome_sorvedouro = grafo_base.obter_nome_vertice(grafo_base.sorvedouro());

    {
        Grafo g = grafo_base.clonar();
        entrada.resultados.push_back(AlgoritmosFluxoMaximo::ford_fulkerson_dfs(g));
    }

    {
        Grafo g = grafo_base.clonar();
        entrada.resultados.push_back(AlgoritmosFluxoMaximo::edmonds_karp_bfs(g));
    }

    {
        Grafo g = grafo_base.clonar();
        entrada.resultados.push_back(AlgoritmosFluxoMaximo::push_relabel_generico(g));
    }

    {
        Grafo g = grafo_base.clonar();
        entrada.resultados.push_back(AlgoritmosFluxoMaximo::relabel_to_front(g));
    }

    entradas_.push_back(entrada);
    return entrada;
}

void ExecutorBenchmark::executar_bateria(const std::vector<std::string>& caminhos_arquivos){
    entradas_.clear();
    for(const auto& caminho : caminhos_arquivos){
        try{
            executar_arquivo_unico(caminho);
        }catch(const std::exception& ex){
        }
    }
}

void ExecutorBenchmark::imprimir_tabela_resumo() const{
}

void ExecutorBenchmark::exportar_csv(const std::string& caminho_csv_saida) const{
    std::filesystem::path p(caminho_csv_saida);
    if(p.has_parent_path()){
        std::filesystem::create_directories(p.parent_path());
    }

    std::ofstream out(caminho_csv_saida);
    if(!out.is_open()){
        throw std::runtime_error("Nao foi possivel abrir o caminho CSV de saida: " + caminho_csv_saida);
    }

    out << "cenario_teste,formato,vertices,arestas,fonte,sorvedouro,algoritmo,fluxo_maximo,"
        << "tempo_microssegundos,tempo_milissegundos,iteracoes_ou_discharges,pushes,relabels\n";

    for(const auto& entrada : entradas_){
        for(const auto& res : entrada.resultados){
            out << entrada.nome_teste << ","
                << entrada.formato << ","
                << entrada.num_vertices << ","
                << entrada.num_arestas << ","
                << entrada.nome_fonte << ","
                << entrada.nome_sorvedouro << ","
                << "\"" << res.nome_algoritmo << "\","
                << res.fluxo_maximo << ","
                << std::fixed << std::setprecision(2) << res.tempo_microssegundos << ","
                << std::fixed << std::setprecision(5) << res.tempo_milissegundos << ","
                << res.iteracoes << ","
                << res.pushes << ","
                << res.relabels << "\n";
        }
    }
}

void ExecutorBenchmark::executar_teste_escala(const std::string& caminho_csv_escala){
    std::filesystem::path p(caminho_csv_escala);
    if(p.has_parent_path()){
        std::filesystem::create_directories(p.parent_path());
    }

    std::ofstream out(caminho_csv_escala);
    if(!out.is_open()){
        throw std::runtime_error("Nao foi possivel abrir o caminho CSV de escala: " + caminho_csv_escala);
    }

    out << "capacidade_m,algoritmo,fluxo_maximo,tempo_microssegundos,tempo_milissegundos,iteracoes,pushes,relabels\n";

    std::vector<long long> valores_m = {10, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000};

    for(long long m : valores_m){
        Grafo g;
        g.adicionar_aresta("s", "u", m);
        g.adicionar_aresta("s", "v", m);
        g.adicionar_aresta("u", "v", 1);
        g.adicionar_aresta("u", "t", m);
        g.adicionar_aresta("v", "t", m);
        g.definir_fonte("s");
        g.definir_sorvedouro("t");

        std::vector<ResultadoAlgoritmo> res;
        {
            Grafo c = g.clonar();
            res.push_back(AlgoritmosFluxoMaximo::ford_fulkerson_dfs(c));
        }
        {
            Grafo c = g.clonar();
            res.push_back(AlgoritmosFluxoMaximo::edmonds_karp_bfs(c));
        }
        {
            Grafo c = g.clonar();
            res.push_back(AlgoritmosFluxoMaximo::push_relabel_generico(c));
        }
        {
            Grafo c = g.clonar();
            res.push_back(AlgoritmosFluxoMaximo::relabel_to_front(c));
        }

        for(const auto& r : res){
            out << m << ",\""
                << r.nome_algoritmo << "\","
                << r.fluxo_maximo << ","
                << std::fixed << std::setprecision(2) << r.tempo_microssegundos << ","
                << std::fixed << std::setprecision(5) << r.tempo_milissegundos << ","
                << r.iteracoes << ","
                << r.pushes << ","
                << r.relabels << "\n";
        }
    }
}

}
