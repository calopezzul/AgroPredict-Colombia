import streamlit as st
import pandas as pd
import numpy as np
import os, sys, joblib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from utils.predicciones import predecir_productividad
from utils.categorias import DEPTOS, CULTIVOS, TOPOGRAFIAS, DRENAJES, RIEGOS
st.set_page_config(page_title='Clasificador Productividad - AgroPredict', page_icon='🧪', layout='wide')

models_path = os.path.join(BASE, 'models')
logistic = joblib.load(os.path.join(models_path, 'logistic.pkl'))
scaler = joblib.load(os.path.join(models_path, 'scaler_logistic.pkl'))
with open(os.path.join(models_path, 'features_logistic.txt'), 'r', encoding='utf-8', errors='ignore') as f:
    feature_names = [line.strip() for line in f]

if 'pred_hecho_03' not in st.session_state:
    st.session_state.pred_hecho_03 = False
if 'resultados_03' not in st.session_state:
    st.session_state.resultados_03 = None

st.markdown('<h1>\U0001F9EA Clasificador de Productividad del Suelo</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#AAAAAA;">Determine si un suelo tiene **Alta** o **Baja** productividad potencial basado en sus características edáficas mediante Regresión Logística.</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    with st.container(border=True):
        st.markdown('### \U0001F4CA Variables del Suelo')
        r1, r2, r3 = st.columns(3)
        with r1:
            pH = st.slider('pH', 3.0, 9.0, 5.5, 0.1, key='log_ph')
            MO = st.slider('MO (%)', 0.0, 30.0, 4.0, 0.1, key='log_mo')
            fosforo = st.number_input('Fósforo (ppm)', 0.0, 500.0, 15.0, 1.0, key='log_p')
        with r2:
            azufre = st.number_input('Azufre (ppm)', 0.0, 200.0, 10.0, 1.0, key='log_s')
            calcio = st.number_input('Calcio (cmol/kg)', 0.0, 30.0, 4.0, 0.1, key='log_ca')
            magnesio = st.number_input('Magnesio (cmol/kg)', 0.0, 10.0, 1.0, 0.1, key='log_mg')
        with r3:
            potasio = st.number_input('Potasio (cmol/kg)', 0.0, 5.0, 0.3, 0.01, key='log_k')
            CIC = st.number_input('CIC (cmol/kg)', 0.0, 40.0, 10.0, 0.5, key='log_cic')
            CE = st.number_input('CE (dS/m)', 0.0, 10.0, 0.5, 0.1, key='log_ce')
        anios_est = st.selectbox('Años establecimiento', [0.5, 3.0, 7.5, 15.0],
                                 format_func=lambda x: {0.5:'0-1 año', 3.0:'1-5 años', 7.5:'5-10 años', 15.0:'Más de 10 años'}[x],
                                 key='log_anios')

    with st.container(border=True):
        st.markdown('### \U0001F4CD Categóricas')
        c1, c2 = st.columns(2)
        with c1:
            depto = st.selectbox('Departamento', sorted(DEPTOS), key='log_depto')
            cultivo = st.selectbox('Cultivo', sorted(CULTIVOS), key='log_cult')
        with c2:
            topografia = st.selectbox('Topografía', TOPOGRAFIAS, key='log_topo')
            drenaje = st.selectbox('Drenaje', DRENAJES, key='log_dren')
            riego = st.selectbox('Riego', RIEGOS, key='log_riego')

with col2:
    st.markdown('### \U0001F4CA Interpretación')
    st.markdown("""
    **Productividad Alta (1):** IPS >= 60  
    **Productividad Baja (0):** IPS < 60  

    El modelo usa Regresión Logística optimizada con AUC objetivo ≥ 0.85.
    """)

b_col1, b_col2 = st.columns([3, 1])
with b_col1:
    btn_pred = st.button('\U0001F9EA Clasificar Productividad', type='primary', use_container_width=True)
with b_col2:
    btn_reset = st.button('\U0001F504 Restablecer', type='secondary', use_container_width=True)

if btn_reset:
    for key in ['log_ph', 'log_mo', 'log_p', 'log_s', 'log_ca', 'log_mg', 'log_k', 'log_cic', 'log_ce', 'log_anios',
                'log_depto', 'log_cult', 'log_topo', 'log_dren', 'log_riego']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.pred_hecho_03 = False
    st.session_state.resultados_03 = None
    st.rerun()

if btn_pred:
    with st.spinner('Clasificando...'):
        inputs = {
            'pH': pH, 'MO': MO, 'fosforo': fosforo, 'azufre': azufre,
            'calcio': calcio, 'magnesio': magnesio, 'potasio': potasio,
            'CIC': CIC, 'CE': CE, 'anios_est': anios_est,
            'depto': depto,
            'cultivo': cultivo,
            'topografia': topografia,
            'drenaje': drenaje,
            'riego': riego
        }
        pred, proba = predecir_productividad(logistic, scaler, inputs, feature_names)
        st.session_state.pred_hecho_03 = True
        st.session_state.resultados_03 = {'pred': pred, 'proba': proba}

if st.session_state.pred_hecho_03 and st.session_state.resultados_03:
    res = st.session_state.resultados_03
    pred, proba = res['pred'], res['proba']

    res_container = st.container(border=True)
    with res_container:
        st.markdown('### Resultado de Clasificación')
        if pred == 1:
            st.markdown(f'<span class="badge" style="background:#2E7D32;color:white;">\U00002705 Productividad ALTA</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="badge" style="background:#F44336;color:white;">\U0000274C Productividad BAJA</span>', unsafe_allow_html=True)

        st.markdown(f'**Probabilidad de Alta Productividad:** {proba:.1f}%')
        prob_color = '#4CAF50' if proba >= 50 else '#F44336'
        st.markdown(f'<div style="height:30px;border-radius:15px;margin:0.5rem 0;background:#333;overflow:hidden;"><div style="height:100%;width:{proba}%;background:{prob_color};border-radius:15px;transition:width 0.5s;"></div></div>', unsafe_allow_html=True)

        confianza = 'Alta' if (proba > 80 or proba < 20) else ('Media' if (proba > 60 or proba < 40) else 'Baja')
        st.markdown(f'**Nivel de confianza:** {confianza}')

        st.markdown("### \U0001F4A1 Recomendación")
        if pred == 1:
            st.success('Este suelo tiene condiciones favorables para cultivos de alto valor. Consulte el Predictor IPS para recomendaciones específicas de manejo.')
        else:
            st.warning('Este suelo requiere mejoras. Consulte las recomendaciones agronómicas en el Predictor IPS para identificar las limitaciones principales.')
