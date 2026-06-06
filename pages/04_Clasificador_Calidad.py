import streamlit as st
import pandas as pd
import numpy as np
import os, sys, joblib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from utils.predicciones import predecir_calidad
from utils.categorias import DEPTOS, CULTIVOS, TOPOGRAFIAS, DRENAJES, RIEGOS, LABELS_CALIDAD
from utils.visualizaciones import barras_probabilidad

st.set_page_config(page_title='Clasificador Calidad - AgroPredict', page_icon='🌳', layout='wide')
models_path = os.path.join(BASE, 'models')
rf = joblib.load(os.path.join(models_path, 'random_forest.pkl'))
scaler = joblib.load(os.path.join(models_path, 'scaler_rf.pkl'))
le = joblib.load(os.path.join(models_path, 'label_encoder.pkl'))
with open(os.path.join(models_path, 'features_logistic.txt'), 'r', encoding='utf-8', errors='ignore') as f:
    feature_names = [line.strip() for line in f]

if 'pred_hecho_04' not in st.session_state:
    st.session_state.pred_hecho_04 = False
if 'resultados_04' not in st.session_state:
    st.session_state.resultados_04 = None

st.markdown('<h1>\U0001F333 Clasificador de Calidad del Suelo</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#AAAAAA;">Clasifique la calidad del suelo en **Baja**, **Media**, **Buena** o **Excelente** usando Random Forest con 4 categorías de calidad.</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    with st.container(border=True):
        st.markdown('### \U0001F4CA Variables del Suelo')
        r1, r2, r3 = st.columns(3)
        with r1:
            pH = st.slider('pH', 3.0, 9.0, 5.5, 0.1, key='rf_ph')
            MO = st.slider('MO (%)', 0.0, 30.0, 4.0, 0.1, key='rf_mo')
            fosforo = st.number_input('Fósforo (ppm)', 0.0, 500.0, 15.0, 1.0, key='rf_p')
        with r2:
            azufre = st.number_input('Azufre (ppm)', 0.0, 200.0, 10.0, 1.0, key='rf_s')
            calcio = st.number_input('Calcio (cmol/kg)', 0.0, 30.0, 4.0, 0.1, key='rf_ca')
            magnesio = st.number_input('Magnesio (cmol/kg)', 0.0, 10.0, 1.0, 0.1, key='rf_mg')
        with r3:
            potasio = st.number_input('Potasio (cmol/kg)', 0.0, 5.0, 0.3, 0.01, key='rf_k')
            CIC = st.number_input('CIC (cmol/kg)', 0.0, 40.0, 10.0, 0.5, key='rf_cic')
            CE = st.number_input('CE (dS/m)', 0.0, 10.0, 0.5, 0.1, key='rf_ce')
        anios_est = st.selectbox('Años establecimiento', [0.5, 3.0, 7.5, 15.0],
                                 format_func=lambda x: {0.5:'0-1 año', 3.0:'1-5 años', 7.5:'5-10 años', 15.0:'Más de 10 años'}[x],
                                 key='rf_anios')

    with st.container(border=True):
        st.markdown('### \U0001F4CD Categóricas')
        c1, c2 = st.columns(2)
        with c1:
            depto = st.selectbox('Departamento', sorted(DEPTOS), key='rf_depto')
            cultivo = st.selectbox('Cultivo', sorted(CULTIVOS), key='rf_cult')
        with c2:
            topografia = st.selectbox('Topografía', TOPOGRAFIAS, key='rf_topo')
            drenaje = st.selectbox('Drenaje', DRENAJES, key='rf_dren')
            riego = st.selectbox('Riego', RIEGOS, key='rf_riego')

with col2:
    st.markdown('### \U0001F4CA Rangos de Calidad')
    colores = {'Baja': '#F44336', 'Media': '#FF9800', 'Buena': '#4CAF50', 'Excelente': '#2E7D32'}
    for cat in LABELS_CALIDAD:
        st.markdown(f'<span class="badge" style="background:{colores[cat]};color:white;">{cat}</span> ', unsafe_allow_html=True)

b_col1, b_col2 = st.columns([3, 1])
with b_col1:
    btn_pred = st.button('\U0001F333 Clasificar Calidad', type='primary', use_container_width=True)
with b_col2:
    btn_reset = st.button('\U0001F504 Restablecer', type='secondary', use_container_width=True)

if btn_reset:
    for key in ['rf_ph', 'rf_mo', 'rf_p', 'rf_s', 'rf_ca', 'rf_mg', 'rf_k', 'rf_cic', 'rf_ce', 'rf_anios',
                'rf_depto', 'rf_cult', 'rf_topo', 'rf_dren', 'rf_riego']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.pred_hecho_04 = False
    st.session_state.resultados_04 = None
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
        clase, probas = predecir_calidad(rf, le, scaler, inputs, feature_names)
        st.session_state.pred_hecho_04 = True
        st.session_state.resultados_04 = {'clase': clase, 'probas': probas}

if st.session_state.pred_hecho_04 and st.session_state.resultados_04:
    res = st.session_state.resultados_04
    clase, probas = res['clase'], res['probas']

    res_container = st.container(border=True)
    with res_container:
        st.markdown('### Resultado de Clasificación')
        color_badge = {'Baja': '#F44336', 'Media': '#FF9800', 'Buena': '#4CAF50', 'Excelente': '#2E7D32'}
        st.markdown(f'<span class="badge" style="background:{color_badge[clase]};color:white;">\U0001F3C6 {clase}</span>', unsafe_allow_html=True)

    st.plotly_chart(barras_probabilidad(probas), use_container_width=True)

    st.markdown("### \U0001F4A1 Recomendación por Calidad")
    rec_map = {
        'Excelente': 'Suelo óptimo para cultivos de alto valor como Café Especial, Aguacate Hass o Cacao Fino. Mantenga prácticas de conservación.',
        'Buena': 'Suelo adecuado para la mayoría de cultivos comerciales. Aplique fertilización de mantenimiento según requerimientos del cultivo.',
        'Media': 'Suelo con limitaciones moderadas. Requiere enmiendas específicas (encalado, materia orgánica, fertilización dirigida).',
        'Baja': 'Suelo con limitaciones significativas. Priorice la corrección de pH, incremento de MO y fertilización balanceada antes de sembrar.'
    }
    st.info(rec_map.get(clase, ''))
