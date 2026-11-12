# Protótipo Sistema Inteligente: Controle Nebuloso para a Rede Ferroviária do Rio de Janeiro

Protótipo desenvolvido para a aplicação de sistemas inteligentes em cidades inteligentes, utilizando lógica nebulosa baseada no algoritmo **URT-FCA (Urban Rail Transport Fuzzy Control Algorithm)** para mitigar atrasos em cascata e gerenciar picos de lotação em horários de pico na malha ferroviária urbana (SuperVia / MetrôRio).

## Estrutura do repositório

- `data/`: base de dados de telemetria simulada das estações (`dados_sensores_rio_de_janeiro.csv`).
- `src/`: script principal do controlador em Python (`tempo_real_rio.py`).
- `requirements.txt`: dependências necessárias para executar o projeto.

## Como executar

1. Certifique-se de ter o Python instalado.
2. Na raiz do repositório, instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute a simulação:

   ```bash
   python src/tempo_real_rio.py
   ```

O script localiza o CSV relativamente à sua própria pasta, portanto também pode ser executado a partir de `src/`.
