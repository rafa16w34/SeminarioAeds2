#pragma once

#include "Grafo.hpp"
#include <string>
#include <vector>

namespace fluxo{

struct EntradaTeste{
    std::string nome_teste;
    std::string caminho_arquivo;
    std::string formato;
    size_t num_vertices = 0;
    size_t num_arestas = 0;
    std::string nome_fonte;
    std::string nome_sorvedouro;
    std::vector<ResultadoAlgoritmo> resultados;
};

class ExecutorBenchmark{
public:
    ExecutorBenchmark() = default;

    EntradaTeste executar_arquivo_unico(const std::string& caminho_arquivo, const std::string& fonte = "", const std::string& sorvedouro = "");
    void executar_bateria(const std::vector<std::string>& caminhos_arquivos);
    void executar_teste_escala(const std::string& caminho_csv_escala);
    void exportar_csv(const std::string& caminho_csv_saida) const;
    void imprimir_tabela_resumo() const;

    const std::vector<EntradaTeste>& obter_entradas() const{ return entradas_; }

private:
    std::vector<EntradaTeste> entradas_;
};

}
