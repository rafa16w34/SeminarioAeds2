CXX = g++
CXXFLAGS = -std=c++20 -O3 -Wall -Wextra -Ibenchmark/include
PYTHON = python3

BENCHMARK_DIR = benchmark
SRC_DIR = $(BENCHMARK_DIR)/src
INC_DIR = $(BENCHMARK_DIR)/include
INPUT_DIR = $(BENCHMARK_DIR)/input
OUTPUT_DIR = $(BENCHMARK_DIR)/output
SCRIPTS_DIR = $(BENCHMARK_DIR)/scripts
BUILD_DIR = $(BENCHMARK_DIR)/build
BIN_DIR = $(BENCHMARK_DIR)/bin

SRCS = $(SRC_DIR)/Grafo.cpp \
       $(SRC_DIR)/FordFulkerson.cpp \
       $(SRC_DIR)/EdmondsKarp.cpp \
       $(SRC_DIR)/PushRelabel.cpp \
       $(SRC_DIR)/RelabelToFront.cpp \
       $(SRC_DIR)/LeitorGrafo.cpp \
       $(SRC_DIR)/ExecutorBenchmark.cpp \
       $(SRC_DIR)/main.cpp

OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.o, $(SRCS))
TARGET = $(BIN_DIR)/benchmark_runner

.PHONY: all benchmark run run-benchmark plot test clean simulacao-abastecimento help

all: benchmark

benchmark: $(TARGET)

$(TARGET): $(OBJS) | $(BIN_DIR)
	@$(CXX) $(CXXFLAGS) -o $@ $^

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(BUILD_DIR)
	@$(CXX) $(CXXFLAGS) -c $< -o $@

$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

$(OUTPUT_DIR):
	@mkdir -p $(OUTPUT_DIR)

run-benchmark: $(TARGET) | $(OUTPUT_DIR)
	@./$(TARGET) --suite $(INPUT_DIR) --output $(OUTPUT_DIR)/results.csv

plot:
	@$(PYTHON) $(SCRIPTS_DIR)/generate_plots.py $(OUTPUT_DIR)/results.csv

run: benchmark run-benchmark plot

test: run

simulacao-abastecimento:
	@if [ -f sistema_abastecimento/main.py ]; then \
		$(PYTHON) sistema_abastecimento/main.py; \
	fi

clean:
	@rm -rf $(BUILD_DIR) $(BIN_DIR)

help:
	@echo "Alvos disponiveis no Makefile:"
	@echo "  make                        - Compila todo o projeto C++"
	@echo "  make run                    - Compila, executa os testes e gera todos os graficos PNG de uma vez"
	@echo "  make run-benchmark          - Executa apenas o benchmark C++"
	@echo "  make plot                   - Gera apenas os graficos PNG"
	@echo "  make simulacao-abastecimento - Executa o projeto Python da Frente 2"
	@echo "  make clean                  - Remove arquivos binarios e objetos compilados"
