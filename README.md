# Seminário de Algoritmos e Estruturas de Dados II: Fluxo Máximo em Redes

<p align="center">
  <img src="https://img.shields.io/badge/C%2B%2B-20-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++20" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Makefile-GNU-047857?style=for-the-badge&logo=gnu&logoColor=white" alt="GNU Make" />
  <img src="https://img.shields.io/badge/Algoritmos-AEDs%20II-ea580c?style=for-the-badge" alt="AEDs II" />
  <img src="https://img.shields.io/badge/Referência-Cormen%20Cap.%2026-7c3aed?style=for-the-badge" alt="Cormen Cap. 26" />
  <img src="https://img.shields.io/badge/Visualizações-PNG%20300DPI-0284c7?style=for-the-badge" alt="PNG 300DPI" />
</p>

---

## Sumário
- [Visão Geral](#visão-geral)
- [Algoritmos Abordados](#algoritmos-abordados)
- [Frente 1: Benchmark Modular e Análise de Escalabilidade](#frente-1-benchmark-modular-e-análise-de-escalabilidade)
  - [Cenários de Teste](#cenários-de-teste)
  - [Métricas e Visualizações Geradas](#métricas-e-visualizações-geradas)
- [Frente 2: Estudo de Caso Prático Didático (Abastecimento Hídrico)](#frente-2-estudo-de-caso-prático-didático-abastecimento-hídrico)
  - [A Analogia Física da Rede Hidráulica](#a-analogia-física-da-rede-hidráulica)
  - [Lâminas Visuais do Storyboard Didático](#lâminas-visuais-do-storyboard-didático)
- [Requisitos e Dependências](#requisitos-e-dependências)
- [Instruções de Compilação e Execução](#instruções-de-compilação-e-execução)

---

## Visão Geral

Este projeto foi desenvolvido como base prática e teórica para o Seminário de **Algoritmos e Estruturas de Dados II (AEDs II)**, fundamentado no **Capítulo 26 (*Maximum Flow*)** do livro clássico *Algoritmos: Teoria e Prática* (Cormen, Leiserson, Rivest e Stein — CLRS).

O projeto é dividido em duas frentes complementares:
1. **Frente 1 (Benchmark Experimental em C++20)**: Implementação modular e medição de desempenho assintótico dos algoritmos em cenários extremos e sob variação de escala de capacidade ($M \in [10^2, 10^7]$).
2. **Frente 2 (Estudo de Caso Prático Didático em Python)**: Storyboard sequencial em PNG demonstrando intuitivamente como o problema de transporte de água funciona e como cada algoritmo se comporta ao buscar a solução ótima.

---

## Algoritmos Abordados

| Algoritmo | Seção Cormen | Paradigma / Mecanismo | Complexidade Assintótica |
| :--- | :---: | :--- | :---: |
| **Ford-Fulkerson** | 26.2 | Método de caminhos aumentadores arbitrários via DFS | $\mathcal{O}(E \cdot \|f^*\|)$ |
| **Edmonds-Karp** | 26.2 | Busca do caminho aumentador mais curto em arestas via BFS | $\mathcal{O}(V \cdot E^2)$ |
| **Push-Relabel** | 26.4 | Operações locais assíncronas com pré-fluxo, cotas $h(u)$ e excessos $e(u)$ | $\mathcal{O}(V^2 \cdot E)$ |
| **Relabel-to-Front** | 26.5 | Orquestração por lista encadeada $L$, rotina de descarga (`discharge`) e movimento para a frente | $\mathcal{O}(V^3)$ |
| **Corte Mínimo** | 26.2 | Teorema do Fluxo Máximo e Corte Mínimo ($\text{Fluxo Máx} = \text{Capacidade Mín}$) | $\mathcal{O}(V + E)$ sobre o residual |

---

## Frente 1: Benchmark Modular e Análise de Escalabilidade

Implementada em **C++20** com compilação otimizada (`-O3`) e medições de alta precisão via `std::chrono::high_resolution_clock`.

### Cenários de Teste

A suíte analisa topologias de naturezas distintas, lidas em múltiplos formatos:

1. **`01_exemplo_cormen.txt`**: Topologia com 6 vértices do livro do Cormen (Figura 26.1), com arestas antiparalelas ($v_1 \rightleftarrows v_2$).
2. **`02_diamante_patologico.dat`**: Grafo em diamante com aresta central unitária ($c=1$), induzindo o pior caso de Ford-Fulkerson com $20.000$ iterações.
3. **`03_emparelhamento_bipartido.csv`**: Problema de atribuição ótima de candidatos a temas com capacidades unitárias ($c=1$).
4. **`04_rede_densa.json`**: Grafo direcionado acíclico (DAG) multicamadas denso, com alto número de arestas transversais.
5. **`05_abastecimento_urbano.txt`**: Malha municipal de distribuição de água contendo represa, ETAs, reservatórios e setores industriais/residenciais.

### Métricas e Visualizações Geradas

A execução do benchmark produz arquivos em `benchmark/output/`:
- **`grafico_barras_tempo.png`**: Comparativo de tempo de execução em milissegundos (escala logarítmica).
- **`grafico_barras_operacoes.png`**: Contagem de iterações, aumentações, pushes e relabels internos.
- **`grafico_linhas_escalabilidade.png`**: Escalabilidade do tempo e das operações em função de $M \in [10^2, 10^7]$ no diamante patológico.
- **Diagramas das Topologias**:
  - `grafo_01_exemplo_cormen.png`
  - `grafo_02_diamante_patologico.png`
  - `grafo_03_emparelhamento_bipartido.png`
  - `grafo_04_rede_densa.png`
  - `grafo_05_abastecimento_urbano.png`
  - `grafos_todos_benchmarks.png` (mosaico consolidado com resumo teórico).

---

## Frente 2: Estudo de Caso Prático Didático (Abastecimento Hídrico)

A Frente 2 utiliza uma rede de abastecimento hídrico de 6 nós para ilustrar o comportamento de cada algoritmo sem abstrações excessivas.

### A Analogia Física da Rede Hidráulica

- **Represa ($s$)**: Fonte de captação de água bruta no topo da serra.
- **Estações de Tratamento ($A$ e $B$)**: ETAs Norte e Sul que dosam a vazão.
- **Reservatórios ($C$ e $D$)**: Caixas d'água elevadas de distribuição intermediária.
- **Cidade ($t$)**: Sorvedouro e centros de consumo habitacionais.
- **Canos**: Arestas direcionadas com capacidade máxima nominal em $\text{m}^3/\text{h}$.

#### Paralelo com os Algoritmos:
- **Ford-Fulkerson & Edmonds-Karp**: Abertura de rotas completas de adutoras da represa até a cidade. O diâmetro do cano mais estreito dita o volume daquele passo (gargalo). Arestas residuais reversas representam a capacidade de remanejar água despachada anteriormente.
- **Push-Relabel (Goldberg-Tarjan)**:
  - Cota altimétrica $h(u)$: Altura da água ou pressão piezométrica. A represa fica em $h(s)=6$ e a cidade em $h(t)=0$.
  - Excesso $e(u)$: Volume represado no reservatório à espera de vazão.
  - Operação PUSH: Abertura de comportas; a água escorre morro abaixo por gravidade ($h(u) = h(v) + 1$).
  - Operação RELABEL: Acionamento de bombas elevatórias; quando a água está represada mas não há saída em cota inferior, a estação eleva sua própria cota.
- **Relabel-to-Front**: Orquestração metódica onde cada estação é descarregada totalmente (`discharge`) e movida para o início da fila de prioridade (`to-front`) ao ser pressurizada.
- **Corte Mínimo**: Particiona a cidade entre zona de captação saturada ($S$) e zona de consumo ($T$). As tubulações que cruzam o corte indicam os gargalos exatos da infraestrutura onde a prefeitura deve investir para aumentar o abastecimento.

### Lâminas Visuais do Storyboard Didático

Geradas em `sistema_abastecimento/output/`:
1. **`01_problema_abastecimento.png`**: Formulação do problema real e restrições físicas.
2. **`02_ford_fulkerson/passo_[1..4]_ford_fulkerson.png`**: Demonstração passo a passo da busca por DFS, destacando o caminho, o gargalo e o residual.
3. **`03_edmonds_karp/passo_[1..4]_edmonds_karp.png`**: Passo a passo com BFS, evidenciando o caminho com menor número de tubulações e distâncias não-decrescentes.
4. **`04_push_relabel_cotas_e_bombas.png`**: Gráfico de barras de cotas altimétricas $h(u)$ e mapa do escoamento gravitacional.
5. **`05_relabel_to_front_lista.png`**: Visualização da lista encadeada $L$, rotina de descarga e garantia de complexidade $\mathcal{O}(V^3)$.
6. **`06_teorema_corte_minimo.png`**: Linha de corte $(S, T)$ e comprovação de que $\text{Fluxo Máximo} = \text{Capacidade do Corte} = 21\text{ m}^3/\text{h}$.
7. **`07_quadro_comparativo_algoritmos.png`**: Tabela comparativa dos 4 algoritmos sintetizando estratégias, complexidades e comportamentos.

---

## Requisitos e Dependências

- **Compilador C++**: `g++` ou `clang++` com suporte completo a C++20.
- **Python**: Versão 3.10 ou superior.
- **Bibliotecas Python**:
  ```bash
  pip install matplotlib networkx plotly kaleido pandas
  ```

---

## Instruções de Compilação e Execução

O `Makefile` unifica todas as tarefas do projeto de forma limpa e silenciosa:

```bash
# Compilar todo o projeto C++ (Frente 1)
make

# Executar benchmark completo, testes de escala e gerar todos os gráficos PNG
make run

# Gerar apenas os diagramas visuais dos grafos de benchmark
make visual-grafos

# Gerar todas as lâminas didáticas da simulação de abastecimento (Frente 2)
make simulacao-abastecimento

# Limpar binários e objetos compilados
make clean

# Exibir manual de comandos disponíveis
make help
```
