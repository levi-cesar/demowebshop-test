# Demo Web Shop — automação de testes

Projeto da disciplina Automação de Testes Ágeis, com Python, Selenium,
pytest e Page Objects. Os requisitos e os 15 casos originais estão em
[docs/casos-de-teste-demowebshop.html](docs/casos-de-teste-demowebshop.html).
Abra esse arquivo no navegador para expandir cada caso.

## Preparação no Linux

Pré-requisitos: Python 3.10 ou superior e Google Chrome instalado.

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt



## Executar


source .venv/bin/activate
python -m pytest                       # Chrome sem janela
python -m pytest --headed              # Chrome com janela
python -m pytest --collect-only        # lista testes sem abrir navegador


O relatório é gerado em `reports/report.html`.

## Organização

- `pages/`: seletores, navegação e ações das páginas.
- `tests/`: cenários e verificações dos resultados esperados.
- `tests/conftest.py`: configuração e navegador novo para cada teste.
- `docs/`: enunciado original.
