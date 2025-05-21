import pandas as pd

def calcular_interes_compuesto(capital_inicial, tasa_interes, anios, frecuencia, aportes):
    frecuencia_map = {
        "Anualmente": 1,
        "Mensualmente": 12
    }

    n = frecuencia_map[frecuencia]
    tasa_decimal = tasa_interes / 100
    registros = []
    
    monto = capital_inicial
    aportes_acumulados = 0
    interes_acumulado = 0

    for i in range(1, anios + 1):
        interes_anual = 0
        aporte_total_anual = aportes * n
        for _ in range(n):
            interes = monto * (tasa_decimal / n)
            interes_anual += interes
            monto += interes + aportes

        aportes_acumulados += aporte_total_anual
        interes_acumulado += interes_anual

        registros.append({
            "Año": i,
            "Depósito Inicial": capital_inicial,
            "Aportes acumulados": aportes_acumulados,
            "Interés acumulado": interes_acumulado,
            "Total acumulado": monto
        })

    df = pd.DataFrame(registros)
    return df, aportes_acumulados, interes_acumulado, monto
