import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sistema_abastecimento.desenhador_didatico import gerar_suite_didatica_completa

def executar():
    dir_saida = sys.argv[1] if len(sys.argv) > 1 else 'sistema_abastecimento/output'
    gerar_suite_didatica_completa(dir_saida)

if __name__ == '__main__':
    executar()
