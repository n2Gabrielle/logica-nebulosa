"""
Protótipo Sistema de Controle Nebuloso com scikit-fuzzy
Contexto: Cidades Inteligentes - Gestão Dinâmica de Tráfego Ferroviário (SuperVia / MetrôRio)
"""

from pathlib import Path
import time

import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def configurar_controlador_fuzzy():
    """Configura as variáveis linguísticas, funções de pertinência e regras fuzzy."""
    fluxo = ctrl.Antecedent(np.arange(0, 601, 1), "fluxo")
    atraso = ctrl.Antecedent(np.arange(0, 15.1, 0.1), "atraso")

    ajuste_vel = ctrl.Consequent(np.arange(0, 16, 0.5), "ajuste_vel")
    tempo_parada = ctrl.Consequent(np.arange(-15, 1, 0.5), "tempo_parada")

    fluxo["baixo"] = fuzz.trapmf(fluxo.universe, [0, 0, 150, 350])
    fluxo["medio"] = fuzz.trimf(fluxo.universe, [250, 400, 500])
    fluxo["alto"] = fuzz.trapmf(fluxo.universe, [400, 500, 600, 600])

    atraso["baixo"] = fuzz.trapmf(atraso.universe, [0, 0, 1.5, 3.5])
    atraso["medio"] = fuzz.trimf(atraso.universe, [2.5, 5.0, 7.5])
    atraso["alto"] = fuzz.trapmf(atraso.universe, [6.5, 8.5, 15.0, 15.0])

    ajuste_vel["zero"] = fuzz.trimf(ajuste_vel.universe, [0, 0, 2])
    ajuste_vel["moderado"] = fuzz.trimf(ajuste_vel.universe, [5, 11.5, 13])
    ajuste_vel["maximo"] = fuzz.trapmf(ajuste_vel.universe, [11, 14, 15, 15])

    tempo_parada["padrao"] = fuzz.trimf(tempo_parada.universe, [-2, 0, 0])
    tempo_parada["reduzido"] = fuzz.trimf(tempo_parada.universe, [-8, -5, -2])
    tempo_parada["severo"] = fuzz.trapmf(
        tempo_parada.universe, [-15, -15, -12, -10]
    )

    regras = [
        ctrl.Rule(
            fluxo["alto"] & atraso["alto"],
            (ajuste_vel["maximo"], tempo_parada["severo"]),
        ),
        ctrl.Rule(
            fluxo["alto"] & atraso["medio"],
            (ajuste_vel["moderado"], tempo_parada["reduzido"]),
        ),
        ctrl.Rule(
            fluxo["medio"] & atraso["alto"],
            (ajuste_vel["moderado"], tempo_parada["reduzido"]),
        ),
        ctrl.Rule(
            fluxo["medio"] & atraso["medio"],
            (ajuste_vel["moderado"], tempo_parada["reduzido"]),
        ),
        ctrl.Rule(
            fluxo["baixo"] | atraso["baixo"],
            (ajuste_vel["zero"], tempo_parada["padrao"]),
        ),
    ]

    sistema_ctrl = ctrl.ControlSystem(regras)
    return ctrl.ControlSystemSimulation(sistema_ctrl)


def executar_simulacao():
    print("=================================================================")
    print("   SISTEMA INTELIGENTE - REDE FERROVIÁRIA DO RIO DE JANEIRO")
    print("=================================================================")

    fuzzy_sim = configurar_controlador_fuzzy()
    caminho_csv = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "dados_sensores_rio_de_janeiro.csv"
    )

    try:
        df = pd.read_csv(caminho_csv)
    except FileNotFoundError:
        print(f"Erro: Ficheiro de dados não encontrado em '{caminho_csv}'")
        return

    colunas_necessarias = {
        "timestamp",
        "station_id",
        "passenger_flow",
        "train_delay_min",
    }
    colunas_em_falta = colunas_necessarias.difference(df.columns)
    if colunas_em_falta:
        raise ValueError(
            "Faltam colunas obrigatórias no CSV: "
            + ", ".join(sorted(colunas_em_falta))
        )

    total_ciclos = 0
    atraso_total_mitigado = 0.0

    print("[INFO] A processar streaming de sensores com motor de inferência...\n")
    time.sleep(0.5)

    for _, row in df.iterrows():
        timestamp = row["timestamp"]
        estacao = row["station_id"]
        fluxo_val = float(row["passenger_flow"])
        atraso_val = float(row["train_delay_min"])

        fuzzy_sim.input["fluxo"] = float(np.clip(fluxo_val, 0.0, 600.0))
        fuzzy_sim.input["atraso"] = float(np.clip(atraso_val, 0.0, 15.0))
        fuzzy_sim.compute()

        ajuste_vel = fuzzy_sim.output["ajuste_vel"]
        tempo_parada = fuzzy_sim.output["tempo_parada"]

        if fluxo_val > 500 and atraso_val > 7.0:
            status_op = "[CRÍTICO - Alta Ação Corretiva]"
            atraso_total_mitigado += 2.5
        elif fluxo_val > 400 and atraso_val > 2.0:
            status_op = "[ALERTA - Ajuste Tático Moderado]"
            atraso_total_mitigado += 1.0
        else:
            status_op = "[NORMAL - Operação Estável]"

        total_ciclos += 1

        print("-----------------------------------------------------------------")
        print(f"Instante: {timestamp} | Estação: {estacao}")
        print(f"Estado: {status_op}")
        print("-----------------------------------------------------------------")
        print(
            f"  > Sensores (Entradas): Fluxo = {fluxo_val:.0f} pax | Atraso ="
            f" {atraso_val:.1f} min"
        )
        print(
            f"  < Atuadores Fuzzy (Saída Defuzzificada): Δv = {ajuste_vel:+5.2f}"
            f" km/h | Δt = {tempo_parada:+5.2f} s"
        )

        time.sleep(0.2)

    print("===============================================================")
    print("   RELATÓRIO CONSOLIDADO DE DESEMPENHO (SCI-KIT FUZZY)")
    print("=================================================================")
    print(f" Total de Ciclos Avaliados : {total_ciclos}")
    print(f" Estimativa de Atraso Evitado: {atraso_total_mitigado:.1f} minutos")
    print("=================================================================")
    print("Simulação concluída com sucesso!")


if __name__ == "__main__":
    executar_simulacao()
