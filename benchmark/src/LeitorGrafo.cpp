#include "LeitorGrafo.hpp"
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <cctype>

namespace fluxo{
namespace{

std::string aparar(const std::string& texto){
    size_t primeiro = texto.find_first_not_of(" \t\r\n");
    if(primeiro == std::string::npos) return "";
    size_t ultimo = texto.find_last_not_of(" \t\r\n");
    return texto.substr(primeiro, (ultimo - primeiro + 1));
}

std::string para_minusculas(std::string texto){
    std::transform(texto.begin(), texto.end(), texto.begin(), [](unsigned char c){ return std::tolower(c); });
    return texto;
}

std::string extrair_extensao(const std::string& caminho){
    size_t ponto = caminho.find_last_of('.');
    if(ponto == std::string::npos) return "";
    return para_minusculas(caminho.substr(ponto));
}

std::vector<std::string> dividir(const std::string& texto, char delimitador){
    std::vector<std::string> partes;
    std::string parte;
    std::istringstream stream(texto);
    while(std::getline(stream, parte, delimitador)){
        partes.push_back(aparar(parte));
    }
    return partes;
}

}

Grafo LeitorGrafo::carregar_txt_ou_dat(const std::string& caminho_arquivo){
    std::ifstream arquivo(caminho_arquivo);
    if(!arquivo.is_open()){
        throw std::runtime_error("Nao foi possivel abrir o arquivo: " + caminho_arquivo);
    }

    Grafo g;
    std::string linha;
    std::string fonte = "";
    std::string sorvedouro = "";
    bool fonte_sorvedouro_definidos = false;

    while(std::getline(arquivo, linha)){
        linha = aparar(linha);
        if(linha.empty() || linha[0] == '#' || (linha.size() >= 2 && linha[0] == '/' && linha[1] == '/')){
            std::string minuscula = para_minusculas(linha);
            if(minuscula.find("source:") != std::string::npos || minuscula.find("fonte:") != std::string::npos){
                size_t pos_f = minuscula.find("source:");
                if(pos_f == std::string::npos) pos_f = minuscula.find("fonte:");
                size_t tam_tag_f = (minuscula.find("source:") != std::string::npos) ? 7 : 6;
                size_t pos_s = minuscula.find("sink:");
                if(pos_s == std::string::npos) pos_s = minuscula.find("sorvedouro:");
                size_t tam_tag_s = (minuscula.find("sink:") != std::string::npos) ? 5 : 11;
                size_t pos_virgula = minuscula.find(",", pos_f);

                if(pos_f != std::string::npos && pos_s != std::string::npos){
                    fonte = aparar(linha.substr(pos_f + tam_tag_f, (pos_virgula != std::string::npos ? pos_virgula - (pos_f + tam_tag_f) : pos_s - (pos_f + tam_tag_f))));
                    sorvedouro = aparar(linha.substr(pos_s + tam_tag_s));
                    fonte_sorvedouro_definidos = true;
                }
            }
            continue;
        }

        std::istringstream iss(linha);
        std::vector<std::string> palavras;
        std::string p;
        while(iss >> p){
            palavras.push_back(p);
        }

        if(palavras.size() == 2 && !fonte_sorvedouro_definidos){
            fonte = palavras[0];
            sorvedouro = palavras[1];
            fonte_sorvedouro_definidos = true;
        }else if(palavras.size() >= 3){
            std::string u = palavras[0];
            std::string v = palavras[1];
            long long cap = std::stoll(palavras[2]);
            g.adicionar_aresta(u, v, cap);
        }
    }

    if(!fonte.empty()) g.definir_fonte(fonte);
    if(!sorvedouro.empty()) g.definir_sorvedouro(sorvedouro);

    return g;
}

Grafo LeitorGrafo::carregar_csv(const std::string& caminho_arquivo){
    std::ifstream arquivo(caminho_arquivo);
    if(!arquivo.is_open()){
        throw std::runtime_error("Nao foi possivel abrir o arquivo: " + caminho_arquivo);
    }

    Grafo g;
    std::string linha;
    std::string fonte = "";
    std::string sorvedouro = "";
    bool primeira_linha = true;

    while(std::getline(arquivo, linha)){
        linha = aparar(linha);
        if(linha.empty() || linha[0] == '#'){
            std::string minuscula = para_minusculas(linha);
            if(minuscula.find("source:") != std::string::npos || minuscula.find("fonte:") != std::string::npos){
                size_t pos_f = minuscula.find("source:");
                if(pos_f == std::string::npos) pos_f = minuscula.find("fonte:");
                size_t tam_tag_f = (minuscula.find("source:") != std::string::npos) ? 7 : 6;
                size_t pos_s = minuscula.find("sink:");
                if(pos_s == std::string::npos) pos_s = minuscula.find("sorvedouro:");
                size_t tam_tag_s = (minuscula.find("sink:") != std::string::npos) ? 5 : 11;
                size_t pos_virgula = minuscula.find(",", pos_f);

                if(pos_f != std::string::npos && pos_s != std::string::npos){
                    fonte = aparar(linha.substr(pos_f + tam_tag_f, (pos_virgula != std::string::npos ? pos_virgula - (pos_f + tam_tag_f) : pos_s - (pos_f + tam_tag_f))));
                    sorvedouro = aparar(linha.substr(pos_s + tam_tag_s));
                }
            }
            continue;
        }

        std::vector<std::string> colunas = dividir(linha, ',');
        if(colunas.size() < 3) continue;

        std::string cabecalho0 = para_minusculas(colunas[0]);
        if(primeira_linha && (cabecalho0 == "source" || cabecalho0 == "from" || cabecalho0 == "origem" || cabecalho0 == "u" || cabecalho0 == "de")){
            primeira_linha = false;
            continue;
        }
        primeira_linha = false;

        std::string u = colunas[0];
        std::string v = colunas[1];
        long long cap = std::stoll(colunas[2]);
        g.adicionar_aresta(u, v, cap);
    }

    if(!fonte.empty()) g.definir_fonte(fonte);
    if(!sorvedouro.empty()) g.definir_sorvedouro(sorvedouro);

    return g;
}

Grafo LeitorGrafo::carregar_json(const std::string& caminho_arquivo){
    std::ifstream arquivo(caminho_arquivo);
    if(!arquivo.is_open()){
        throw std::runtime_error("Nao foi possivel abrir o arquivo: " + caminho_arquivo);
    }

    std::stringstream buffer;
    buffer << arquivo.rdbuf();
    std::string conteudo = buffer.str();

    Grafo g;
    std::string fonte = "";
    std::string sorvedouro = "";

    auto buscar_chave = [&](const std::string& chave) -> std::string{
        size_t pos = conteudo.find("\"" + chave + "\"");
        if(pos != std::string::npos){
            size_t dois_pontos = conteudo.find(':', pos);
            size_t aspa1 = conteudo.find('"', dois_pontos);
            size_t aspa2 = conteudo.find('"', aspa1 + 1);
            if(aspa1 != std::string::npos && aspa2 != std::string::npos){
                return conteudo.substr(aspa1 + 1, aspa2 - aspa1 - 1);
            }
        }
        return "";
    };

    fonte = buscar_chave("source");
    if(fonte.empty()) fonte = buscar_chave("fonte");

    sorvedouro = buscar_chave("sink");
    if(sorvedouro.empty()) sorvedouro = buscar_chave("sorvedouro");

    size_t idx = 0;
    while((idx = conteudo.find('{', idx)) != std::string::npos){
        size_t fecha = conteudo.find('}', idx);
        if(fecha == std::string::npos) break;

        std::string obj = conteudo.substr(idx, fecha - idx + 1);
        idx = fecha + 1;

        if((obj.find("\"from\"") != std::string::npos || obj.find("\"de\"") != std::string::npos || obj.find("\"origem\"") != std::string::npos) &&
            (obj.find("\"to\"") != std::string::npos || obj.find("\"para\"") != std::string::npos || obj.find("\"destino\"") != std::string::npos)){
            
            auto extrair_string = [&](const std::string& chave) -> std::string{
                size_t k_pos = obj.find("\"" + chave + "\"");
                if(k_pos == std::string::npos) return "";
                size_t dois_pontos = obj.find(':', k_pos);
                size_t q1 = obj.find('"', dois_pontos);
                size_t q2 = obj.find('"', q1 + 1);
                if(q1 != std::string::npos && q2 != std::string::npos){
                    return obj.substr(q1 + 1, q2 - q1 - 1);
                }
                return "";
            };

            auto extrair_numero = [&](const std::string& chave) -> long long{
                size_t k_pos = obj.find("\"" + chave + "\"");
                if(k_pos == std::string::npos) return 0;
                size_t dois_pontos = obj.find(':', k_pos);
                size_t num_inicio = obj.find_first_of("-0123456789", dois_pontos);
                size_t num_fim = obj.find_first_not_of("0123456789", num_inicio);
                if(num_inicio != std::string::npos){
                    std::string num_str = obj.substr(num_inicio, num_fim - num_inicio);
                    return std::stoll(num_str);
                }
                return 0;
            };

            std::string u = extrair_string("from");
            if(u.empty()) u = extrair_string("de");
            if(u.empty()) u = extrair_string("origem");

            std::string v = extrair_string("to");
            if(v.empty()) v = extrair_string("para");
            if(v.empty()) v = extrair_string("destino");

            long long cap = extrair_numero("capacity");
            if(cap == 0) cap = extrair_numero("capacidade");
            if(cap == 0) cap = extrair_numero("cap");

            if(!u.empty() && !v.empty() && cap > 0){
                g.adicionar_aresta(u, v, cap);
            }
        }
    }

    if(!fonte.empty()) g.definir_fonte(fonte);
    if(!sorvedouro.empty()) g.definir_sorvedouro(sorvedouro);

    return g;
}

Grafo LeitorGrafo::carregar_de_arquivo(const std::string& caminho_arquivo, const std::string& fonte_substituta, const std::string& sorvedouro_substituto){
    std::string ext = extrair_extensao(caminho_arquivo);
    Grafo g;

    if(ext == ".json"){
        g = carregar_json(caminho_arquivo);
    }else if(ext == ".csv"){
        g = carregar_csv(caminho_arquivo);
    }else{
        g = carregar_txt_ou_dat(caminho_arquivo);
    }

    if(!fonte_substituta.empty()){
        g.definir_fonte(fonte_substituta);
    }
    if(!sorvedouro_substituto.empty()){
        g.definir_sorvedouro(sorvedouro_substituto);
    }

    if(g.fonte() == -1 || g.sorvedouro() == -1){
        if(g.num_vertices() >= 2){
            if(g.fonte() == -1) g.definir_fonte(0);
            if(g.sorvedouro() == -1) g.definir_sorvedouro(static_cast<int>(g.num_vertices()) - 1);
        }else{
            throw std::runtime_error("O grafo em '" + caminho_arquivo + "' precisa definir fonte e sorvedouro.");
        }
    }

    return g;
}

}
