#include "ExecutorBenchmark.hpp"
#include <iostream>
#include <vector>
#include <string>
#include <filesystem>
#include <algorithm>

namespace fs = std::filesystem;

void exibir_ajuda(const char* nome_programa){
    std::cout << "Uso: " << nome_programa << " [opcoes] [arquivo_entrada]\n\n"
              << "Opcoes:\n"
              << "  --suite <dir>        Executa benchmark em todos os arquivos suportados (.txt, .dat, .csv, .json) no diretorio especificado.\n"
              << "  --source <nome>      Define o vertice fonte.\n"
              << "  --sink <nome>        Define o vertice sorvedouro.\n"
              << "  --output <arquivo>   Caminho para o arquivo CSV de saida (padrao: output/results.csv).\n"
              << "  --help               Exibe esta mensagem de ajuda.\n\n"
              << "Exemplos:\n"
              << "  " << nome_programa << "\n"
              << "  " << nome_programa << " input/02_diamante_patologico.dat\n"
              << "  " << nome_programa << " personalizado.json --source s --sink t\n";
}

int main(int argc, char* argv[]){
    try{
        std::string arquivo_customizado = "";
        std::string dir_bateria = "";
        std::string fonte_substituta = "";
        std::string sorvedouro_substituto = "";
        std::string csv_saida = "output/results.csv";
        std::string csv_escala = "output/results_escala.csv";

        for(int i = 1; i < argc; ++i){
            std::string arg = argv[i];
            if(arg == "--help" || arg == "-h"){
                exibir_ajuda(argv[0]);
                return 0;
            }else if(arg == "--suite" && i + 1 < argc){
                dir_bateria = argv[++i];
            }else if(arg == "--source" && i + 1 < argc){
                fonte_substituta = argv[++i];
            }else if(arg == "--sink" && i + 1 < argc){
                sorvedouro_substituto = argv[++i];
            }else if(arg == "--output" && i + 1 < argc){
                csv_saida = argv[++i];
                fs::path p(csv_saida);
                csv_escala = (p.parent_path() / "results_escala.csv").string();
            }else if(arg.rfind("--", 0) != 0){
                arquivo_customizado = arg;
            }
        }

        fluxo::ExecutorBenchmark executor;

        if(!arquivo_customizado.empty()){
            executor.executar_arquivo_unico(arquivo_customizado, fonte_substituta, sorvedouro_substituto);
            executor.exportar_csv(csv_saida);
        }else{
            std::string dir_alvo = dir_bateria.empty() ? "input" : dir_bateria;
            if(!fs::exists(dir_alvo)){
                if(fs::exists("benchmark/" + dir_alvo)){
                    dir_alvo = "benchmark/" + dir_alvo;
                    if(csv_saida == "output/results.csv"){
                        csv_saida = "benchmark/output/results.csv";
                        csv_escala = "benchmark/output/results_escala.csv";
                    }
                }else{
                    std::cerr << "Erro: Diretorio de entradas nao encontrado: " << dir_alvo << "\n";
                    return 1;
                }
            }

            std::vector<std::string> arquivos_teste;
            for(const auto& item : fs::directory_iterator(dir_alvo)){
                if(item.is_regular_file()){
                    std::string ext = item.path().extension().string();
                    std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
                    if(ext == ".txt" || ext == ".dat" || ext == ".csv" || ext == ".json"){
                        arquivos_teste.push_back(item.path().string());
                    }
                }
            }

            std::sort(arquivos_teste.begin(), arquivos_teste.end());

            if(arquivos_teste.empty()){
                std::cerr << "Nenhum arquivo de teste encontrado em: " << dir_alvo << "\n";
                return 1;
            }

            executor.executar_bateria(arquivos_teste);
            executor.exportar_csv(csv_saida);
            executor.executar_teste_escala(csv_escala);
        }

        return 0;
    }catch(const std::exception& e){
        std::cerr << "Excecao: " << e.what() << "\n";
        return 1;
    }
}
