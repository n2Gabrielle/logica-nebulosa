"""
Protótipo URT-FCA: Sistema de Controlo Nebuloso (SuperVia / MetrôRio)
Contexto: Cidades Inteligentes - Gestão Dinâmica de Tráfego Ferroviário
Desenvolvido para a entrega do projeto final.
"""

from pathlib import Path
import time

import pandas as pd


def executar_simulacao():
    print("=================================================================")
    print("   SISTEMA INTELIGENTE - REDE FERROVIÁRIA DO RIO DE JANEIRO")
    print("=================================================================")

    caminho_csv = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "dados_sensores_rio_de_janeiro.csv"
    )

    try:
        df = pd.read_csv(caminho_csv)
    except FileNotFoundError:
        print(f"Erro crítico: Não foi possível encontrar o ficheiro '{caminho_csv}'")
        return

    total_ciclos = 0
    acoes_criticas = 0
    acoes_moderadas = 0
    operacoes_normais = 0
    atraso_total_mitigado_min = 0.0

    print("[INFO] A iniciar o fluxo de dados em tempo real dos sensores...\n")
    time.sleep(0.5)

    # Loop de processamento de streaming de sensores (Simulando o CCO)
    for _, row in df.iterrows():
        timestamp = row["timestamp"]
        estacao = row["station_id"]
        fluxo = row["passenger_flow"]
        atraso = row["train_delay_min"]

        # Motor de Decisão Nebuloso (Regras Linguísticas)
        if fluxo > 500 and atraso > 7.0:
            ajuste_vel = 15.0  # km/h (Aceleração para recuperar tabela)
            tempo_parada = -15.0  # segundos (Restringe portas para esvaziar plataforma)
            status_op = "[CRÍTICO - Mitigação de Efeito Comboio]"
            acoes_criticas += 1
            atraso_total_mitigado_min += 2.5
        elif fluxo > 400 and atraso > 2.0:
            ajuste_vel = 11.5
            tempo_parada = -5.0
            status_op = "[ALERTA - Ajuste Moderado de Tabela]"
            acoes_moderadas += 1
            atraso_total_mitigado_min += 1.0
        else:
            ajuste_vel = 0.0
            tempo_parada = 0.0
            status_op = "[NORMAL - Operação Nominal Estável]"
            operacoes_normais += 1

        total_ciclos += 1

        # Painel de Monitoramento Operacional (Estilo CCO)
        print("-----------------------------------------------------------------")
        print(f"Instante: {timestamp} | Estação: {estacao}")
        print(f"Estado do Sistema: {status_op}")
        print("-----------------------------------------------------------------")
        print(
            f"  > Telemetria (Entradas): Fluxo = {fluxo} pax | Atraso ="
            f" {atraso:.1f} min"
        )
        print(
            f"  < Atuadores Fuzzy (Saí.): Δv = {ajuste_vel:+5.1f} km/h  | Δt ="
            f" {tempo_parada:+5.1f} s"
        )

        # Simula o intervalo de varredura do sistema em tempo real
        time.sleep(0.2)

    # Relatório Consolidado de Desempenho
    print("=================================================================")
    print("   RELATÓRIO CONSOLIDADO DE DESEMPENHO DO CONTROLADOR URT-FCA")
    print("=================================================================")
    print(f" Total de Ciclos de Monitoramento Processados : {total_ciclos}")
    print(f" Intervenções em Pico Crítico (Ação Máxima)   : {acoes_criticas}")
    print(f" Intervenções Moderadas (Ajuste Tático)      : {acoes_moderadas}")
    print(f" Ciclos em Operação Nominal                  : {operacoes_normais}")
    print(
        " Estimativa de Atraso Evitado na Malha       :"
        f" {atraso_total_mitigado_min:.1f} minutos"
    )
    print("=================================================================")
    print("Simulação e otimização da rede ferroviária concluídas com sucesso!")


if __name__ == "__main__":
    executar_simulacao()
