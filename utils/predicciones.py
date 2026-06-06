import numpy as np
import pandas as pd
from utils.categorias import (
    FEATURES_NUM,
    DEPTOS_INTERNOS, CULTIVOS_INTERNOS,
    TOPOGRAFIAS_INTERNAS, DRENAJES_INTERNOS, RIEGOS_INTERNOS,
    DISP_A_INTERNO_DEPTO, DISP_A_INTERNO_CULTIVO,
    DISP_A_INTERNO_TOPOGRAFIA, DISP_A_INTERNO_DRENAJE, DISP_A_INTERNO_RIEGO
)

_MAPAS = {
    'depto': DISP_A_INTERNO_DEPTO,
    'cultivo': DISP_A_INTERNO_CULTIVO,
    'topografia': DISP_A_INTERNO_TOPOGRAFIA,
    'drenaje': DISP_A_INTERNO_DRENAJE,
    'riego': DISP_A_INTERNO_RIEGO,
}


def construir_vector(inputs, feature_names):
    vals = [inputs.get(f, 0) for f in FEATURES_NUM]
    cats = {}
    for prefix, lista, key in [
        ('depto_', DEPTOS_INTERNOS, 'depto'),
        ('cultivo_', CULTIVOS_INTERNOS, 'cultivo'),
        ('topografia_', TOPOGRAFIAS_INTERNAS, 'topografia'),
        ('drenaje_', DRENAJES_INTERNOS, 'drenaje'),
        ('riego_', RIEGOS_INTERNOS, 'riego')
    ]:
        raw = inputs.get(key, '')
        mapa = _MAPAS.get(key, {})
        selected = mapa.get(raw, raw)
        for val in lista:
            col = f'{prefix}{val}'
            cats[col] = 1 if val == selected else 0

    cols_feat = FEATURES_NUM + list(cats.keys())
    vec = np.array([vals + [cats.get(c, 0) for c in cats.keys()]], dtype=float)

    expected = set(feature_names)
    full = {}
    for i, name in enumerate(cols_feat):
        if name in expected:
            full[name] = vec[0, i]

    df = pd.DataFrame([full], columns=feature_names).fillna(0)
    return df[feature_names].values


def predecir_ips(model, scaler, inputs, feature_names):
    X = construir_vector(inputs, feature_names)
    X_s = scaler.transform(X)
    pred = model.predict(X_s)[0]
    pred = np.clip(pred, 0, 100)
    if pred < 40:
        calidad = 'Baja'
    elif pred < 60:
        calidad = 'Media'
    elif pred < 80:
        calidad = 'Buena'
    else:
        calidad = 'Excelente'
    return round(pred, 1), calidad


def predecir_productividad(model, scaler, inputs, feature_names):
    X = construir_vector(inputs, feature_names)
    X_s = scaler.transform(X)
    proba = model.predict_proba(X_s)[0, 1]
    pred = model.predict(X_s)[0]
    return int(pred), round(float(proba) * 100, 1)


def predecir_calidad(model, le, scaler, inputs, feature_names):
    X = construir_vector(inputs, feature_names)
    X_s = scaler.transform(X)
    probas = model.predict_proba(X_s)[0]
    pred = model.predict(X_s)[0]
    clase = le.inverse_transform([pred])[0]
    probas_dict = {le.inverse_transform([i])[0]: round(float(probas[i]) * 100, 1) for i in range(len(probas))}
    return clase, probas_dict
