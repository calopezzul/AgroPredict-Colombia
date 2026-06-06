import streamlit as st
import pandas as pd
import numpy as np
import os, sys, joblib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from utils.categorias import DEPTOS, CULTIVOS, TOPOGRAFIAS, DRENAJES, RIEGOS, FEATURES_NUM
from utils.visualizaciones import comparar_suelos
from utils.limpiar import leer_csv_seguro
from sklearn.neighbors import NearestNeighbors

st.set_page_config(page_title='KNN Similaridad - AgroPredict', page_icon='🔍', layout='wide')
models_path = os.path.join(BASE, 'models')
knn_sample = leer_csv_seguro(os.path.join(models_path, 'knn_sample.csv'))

FEATS_KNN = ['pH', 'MO', 'fosforo', 'azufre', 'calcio', 'magnesio', 'potasio', 'CIC', 'CE']
X_knn = knn_sample[FEATS_KNN].values

nn = NearestNeighbors(n_neighbors=10, metric='euclidean')
nn.fit(X_knn)

if 'pred_hecho' not in st.session_state:
    st.session_state.pred_hecho = False
if 'resultados' not in st.session_state:
    st.session_state.resultados = None

st.markdown('<h1>\U0001F50D Buscador de Suelos Similares (KNN)</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#AAAAAA;">Encuentre los suelos más similares en la base de datos del laboratorio según sus características edáficas usando K-Nearest Neighbors.</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    with st.container(border=True):
        st.markdown('### \U0001F4CA Características del Suelo')
        r1, r2 = st.columns(2)
        with r1:
            pH = st.slider('pH', 3.0, 9.0, 5.5, 0.1, key='knn_ph')
            MO = st.slider('MO (%)', 0.0, 30.0, 4.0, 0.1, key='knn_mo')
            fosforo = st.number_input('Fósforo (ppm)', 0.0, 500.0, 15.0, 1.0, key='knn_p')
            azufre = st.number_input('Azufre (ppm)', 0.0, 200.0, 10.0, 1.0, key='knn_s')
        with r2:
            calcio = st.number_input('Calcio (cmol/kg)', 0.0, 30.0, 4.0, 0.1, key='knn_ca')
            magnesio = st.number_input('Magnesio (cmol/kg)', 0.0, 10.0, 1.0, 0.1, key='knn_mg')
            potasio = st.number_input('Potasio (cmol/kg)', 0.0, 5.0, 0.3, 0.01, key='knn_k')
            CIC = st.number_input('CIC (cmol/kg)', 0.0, 40.0, 10.0, 0.5, key='knn_cic')
            CE = st.number_input('CE (dS/m)', 0.0, 10.0, 0.5, 0.1, key='knn_ce')

with col2:
    k = st.slider('Número de vecinos', 1, 10, 5, key='knn_vecinos')
    st.markdown('### \U0001F4CA Cómo funciona')
    st.markdown("""
    El algoritmo **K-Nearest Neighbors (KNN)** calcula la distancia euclidiana entre el suelo ingresado y todos los suelos en la base de datos.

    Los resultados muestran los **suelos más similares** con sus valores de IPS, permitiendo:
    - Identificar suelos comparables
    - Estimar productividad potencial
    - Referenciar casos exitosos similares
    """)

b_col1, b_col2 = st.columns([3, 1])
with b_col1:
    btn_pred = st.button('\U0001F50D Buscar Suelos Similares', type='primary', use_container_width=True)
with b_col2:
    btn_reset = st.button('\U0001F504 Restablecer', type='secondary', use_container_width=True)

if btn_reset:
    for key in ['knn_ph', 'knn_mo', 'knn_p', 'knn_s', 'knn_ca', 'knn_mg', 'knn_k', 'knn_cic', 'knn_ce', 'knn_vecinos']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.pred_hecho = False
    st.session_state.resultados = None
    st.rerun()

if btn_pred:
    with st.spinner('Buscando suelos similares...'):
        query = np.array([[pH, MO, fosforo, azufre, calcio, magnesio, potasio, CIC, CE]])
        distances, indices = nn.kneighbors(query, n_neighbors=k)
        similares = knn_sample.iloc[indices[0]].copy()
        similares['distancia'] = distances[0].round(3)
        ips_mean = similares['IPS'].mean()
        ips_std = similares['IPS'].std()
        st.session_state.pred_hecho = True
        st.session_state.resultados = {
            'similares': similares,
            'ips_mean': ips_mean,
            'ips_std': ips_std,
            'k': k
        }

if st.session_state.pred_hecho and st.session_state.resultados:
    res = st.session_state.resultados
    similares = res['similares']
    ips_mean = res['ips_mean']
    ips_std = res['ips_std']
    k = res['k']

    st.markdown(f'### \U0001F4CB {k} Suelos Más Similares Encontrados')
    cols_show = FEATS_KNN + ['IPS', 'distancia']
    st.dataframe(similares[cols_show].round(2), use_container_width=True, hide_index=True)

    st.markdown('### \U0001F4CA Comparación Visual')
    st.plotly_chart(comparar_suelos(similares), use_container_width=True)

    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        st.metric('IPS Promedio Vecinos', f'{ips_mean:.1f}')
    with col_i2:
        st.metric('Desviación Estándar', f'{ips_std:.1f}')
    with col_i3:
        st.metric('IPS Mín - Máx', f'{similares["IPS"].min():.0f} - {similares["IPS"].max():.0f}')

    st.markdown("### \U0001F4A1 Recomendación")
    if ips_mean >= 60:
        st.success(f'Los suelos similares tienen un IPS promedio de {ips_mean:.1f} (Alta productividad). Considere prácticas de manejo exitosas aplicadas en estos casos.')
    else:
        st.warning(f'Los suelos similares tienen un IPS promedio de {ips_mean:.1f} (Baja-Media productividad). Revise las recomendaciones agronómicas para mejorar las condiciones del suelo.')
