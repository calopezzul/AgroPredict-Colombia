import streamlit as st
import pandas as pd
import numpy as np
import os, sys, joblib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from utils.predicciones import predecir_ips
from utils.recomendaciones import generar_recomendaciones, recomendar_cultivo
from utils.categorias import DEPTOS, CULTIVOS, TOPOGRAFIAS, DRENAJES, RIEGOS, FEATURES_NUM, RANGOS_NUTRIENTES
from utils.visualizaciones import gauge_ips, radar_nutrientes

st.set_page_config(page_title='Predictor IPS - AgroPredict', page_icon='🔮', layout='wide')
models_path = os.path.join(BASE, 'models')
ridge = joblib.load(os.path.join(models_path, 'ridge.pkl'))
scaler = joblib.load(os.path.join(models_path, 'scaler_ridge.pkl'))
with open(os.path.join(models_path, 'features_ridge.txt'), 'r', encoding='utf-8', errors='ignore') as f:
    feature_names = [line.strip() for line in f]

if 'pred_hecho_02' not in st.session_state:
    st.session_state.pred_hecho_02 = False
if 'resultados_02' not in st.session_state:
    st.session_state.resultados_02 = None

st.markdown('<h1>\U0001F52E Predictor del Índice de Productividad del Suelo (IPS)</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#AAAAAA;">Ingrese las variables edáficas y características del terreno para predecir el IPS del suelo mediante Regresión Ridge.</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    with st.container(border=True):
        st.markdown('### \U0001F4CA Variables Numéricas')
        r1, r2, r3, r4, r5 = st.columns(5)
        with r1:
            pH = st.slider('pH', 3.0, 9.0, 5.5, 0.1, key='ips_ph')
            MO = st.slider('MO (%)', 0.0, 30.0, 4.0, 0.1, key='ips_mo')
        with r2:
            fosforo = st.number_input('Fósforo (ppm)', 0.0, 500.0, 15.0, 1.0, key='ips_p')
            azufre = st.number_input('Azufre (ppm)', 0.0, 200.0, 10.0, 1.0, key='ips_s')
        with r3:
            calcio = st.number_input('Calcio (cmol/kg)', 0.0, 30.0, 4.0, 0.1, key='ips_ca')
            magnesio = st.number_input('Magnesio (cmol/kg)', 0.0, 10.0, 1.0, 0.1, key='ips_mg')
        with r4:
            potasio = st.number_input('Potasio (cmol/kg)', 0.0, 5.0, 0.3, 0.01, key='ips_k')
            CIC = st.number_input('CIC (cmol/kg)', 0.0, 40.0, 10.0, 0.5, key='ips_cic')
        with r5:
            CE = st.number_input('CE (dS/m)', 0.0, 10.0, 0.5, 0.1, key='ips_ce')
            anios_est = st.selectbox('Años establecimiento', [0.5, 3.0, 7.5, 15.0],
                                     format_func=lambda x: {0.5:'0-1 año', 3.0:'1-5 años', 7.5:'5-10 años', 15.0:'Más de 10 años'}[x],
                                     key='ips_anios')

    with st.container(border=True):
        st.markdown('### \U0001F4CD Variables Categóricas')
        c1, c2 = st.columns(2)
        with c1:
            depto = st.selectbox('Departamento', sorted(DEPTOS), key='ips_depto')
            cultivo = st.selectbox('Cultivo', sorted(CULTIVOS), key='ips_cult')
        with c2:
            topografia = st.selectbox('Topografía', TOPOGRAFIAS, key='ips_topo')
            drenaje = st.selectbox('Drenaje', DRENAJES, key='ips_dren')
            riego = st.selectbox('Riego', RIEGOS, key='ips_riego')

with col2:
    st.markdown('### \U0001F4CC Referencia de Rangos')
    st.markdown('<div style="font-size:0.85rem;color:#AAAAAA;">', unsafe_allow_html=True)
    for k, v in RANGOS_NUTRIENTES.items():
        st.markdown(f'**{v["nombre"]}**: {v["bajo"]}–{v["alto"]} {v["unidad"]}')
    st.markdown('</div>', unsafe_allow_html=True)

b_col1, b_col2 = st.columns([3, 1])
with b_col1:
    predecir_btn = st.button('\U0001F52E Predecir IPS', type='primary', use_container_width=True)
with b_col2:
    reset_btn = st.button('\U0001F504 Restablecer', type='secondary', use_container_width=True)

if reset_btn:
    for key in ['ips_ph', 'ips_mo', 'ips_p', 'ips_s', 'ips_ca', 'ips_mg', 'ips_k', 'ips_cic', 'ips_ce', 'ips_anios',
                'ips_depto', 'ips_cult', 'ips_topo', 'ips_dren', 'ips_riego']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.pred_hecho_02 = False
    st.session_state.resultados_02 = None
    st.rerun()

if predecir_btn:
    with st.spinner('Calculando IPS...'):
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
        ips, calidad = predecir_ips(ridge, scaler, inputs, feature_names)
        recs = generar_recomendaciones(inputs)
        cult_sug = recomendar_cultivo(calidad)
        st.session_state.pred_hecho_02 = True
        st.session_state.resultados_02 = {'ips': ips, 'calidad': calidad, 'inputs': inputs, 'recs': recs, 'cult_sug': cult_sug}

if st.session_state.pred_hecho_02 and st.session_state.resultados_02:
    res = st.session_state.resultados_02
    ips = res['ips']
    calidad = res['calidad']
    inputs = res['inputs']
    recs = res['recs']
    cult_sug = res['cult_sug']

    r1, r2 = st.columns([1, 1])
    with r1:
        st.plotly_chart(gauge_ips(ips), use_container_width=True)
    with r2:
        color_badge = {'Baja': '#F44336', 'Media': '#FF9800', 'Buena': '#4CAF50', 'Excelente': '#2E7D32'}
        st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f'### \U0001F3AF IPS: **{ips}**')
        st.markdown(f'<span class="badge" style="background:{color_badge[calidad]};color:white;">{calidad}</span>', unsafe_allow_html=True)
        st.markdown(f'**Cultivos recomendados:** {cult_sug}')
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander('\U0001F4A1 Ver recomendaciones agronómicas detalladas', expanded=True):
        if recs:
            for nombre, valor, unidad, estado, rec in recs:
                icono = {'bajo': '\U0001F4E9', 'alto': '\U0001F4E9', 'optimo': '\U00002705'}
                st.markdown(f'<div class="rec-card">{icono.get(estado,"")} <strong>{nombre}</strong>: {valor} {unidad} — {rec}</div>', unsafe_allow_html=True)
        else:
            st.info('No se generaron recomendaciones específicas.')

    st.plotly_chart(radar_nutrientes(inputs), use_container_width=True)
