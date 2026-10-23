#pragma once

#include "Grafo.hpp"
#include <string>

namespace fluxo{

class LeitorGrafo{
public:
    static Grafo carregar_de_arquivo(const std::string& caminho_arquivo, const std::string& fonte_substituta = "", const std::string& sorvedouro_substituto = "");
    static Grafo carregar_txt_ou_dat(const std::string& caminho_arquivo);
    static Grafo carregar_csv(const std::string& caminho_arquivo);
    static Grafo carregar_json(const std::string& caminho_arquivo);
};

}
