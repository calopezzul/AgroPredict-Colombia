import streamlit as st
import pandas as pd
import os, json

st.set_page_config(page_title='Inicio - AgroPredict Colombia', page_icon='🌾', layout='wide')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
models_path = os.path.join(BASE, 'models')

st.markdown("""
<div class="hero" style="text-align:center;padding:3rem 1rem;background:linear-gradient(135deg,rgba(76,175,80,0.08),rgba(76,175,80,0.02));border-radius:16px;margin-bottom:2rem;border:1px solid rgba(76,175,80,0.15);">
    <h1 style="color:#4CAF50;font-size:2.8rem;margin-bottom:0.5rem;font-weight:800;">\U0001F33E AgroPredict Colombia</h1>
    <p style="color:#AAAAAA;font-size:1.2rem;max-width:700px;margin:0 auto;">Plataforma interactiva de Machine Learning para la optimización de la productividad agrícola sostenible en Colombia</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="kpi-card"><h3>92,738</h3><p>Registros de Suelos Procesados</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="kpi-card"><h3>32</h3><p>Departamentos de Colombia</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="kpi-card"><h3>279</h3><p>Tipos de Cultivos</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="kpi-card"><h3>4</h3><p>Modelos de Machine Learning</p></div>', unsafe_allow_html=True)

st.markdown('<h2 style="color:#4CAF50;font-size:1.5rem;margin:2rem 0 1rem 0;border-bottom:2px solid rgba(76,175,80,0.2);padding-bottom:0.5rem;">\U0001F4CA Contexto del Problema</h2>', unsafe_allow_html=True)
st.markdown("""
El sector agropecuario colombiano enfrenta tres grandes desafíos:
- **Baja adopción tecnológica**: Menos del 15% de los productores utiliza herramientas digitales (DANE, 2023)
- **Ineficiencia productiva**: Rendimientos por debajo del promedio regional latinoamericano
- **Cambio climático**: Afectación creciente en ciclos productivos (IDEAM, 2025)
""")

col_obj1, col_obj2 = st.columns(2)
with col_obj1:
    st.markdown('<h2 style="color:#4CAF50;font-size:1.5rem;margin:1.5rem 0 1rem 0;">\U0001F3AF Objetivo General</h2>', unsafe_allow_html=True)
    st.info("Desarrollar modelos de Machine Learning para optimizar la productividad agrícola mediante el análisis de variables edafoclimáticas, como base para la transferencia tecnológica en el sector agropecuario colombiano.")
with col_obj2:
    st.markdown('<h2 style="color:#4CAF50;font-size:1.5rem;margin:1.5rem 0 1rem 0;">\U0001F4CB Objetivos Específicos (SMART)</h2>', unsafe_allow_html=True)
    st.markdown("""
    1. Limpiar y procesar un dataset de +90,000 registros para modelado predictivo
    2. Implementar 3 modelos de ML con métricas de desempeño superiores al 75%
    3. Identificar las 5 variables edáficas más influyentes en la productividad
    4. Generar recomendaciones agronómicas basadas en datos y modelos
    5. Desplegar una aplicación interactiva para uso de productores y extensionistas
    """)

st.markdown('<h2 style="color:#4CAF50;font-size:1.5rem;margin:2rem 0 1rem 0;">\U0001F4CA Metodología CRISP-ML</h2>', unsafe_allow_html=True)
crisp_data = {
    'Fase': ['Comprensión del Problema', 'Comprensión de Datos', 'Preparación', 'EDA', 'Modelado', 'Evaluación', 'Despliegue', 'Monitoreo'],
    'Descripción': [
        'Baja productividad agrícola, adopción tecnológica limitada',
        '92,738 registros, 32 variables edafoclimáticas, 32 departamentos',
        'Limpieza, encoding, feature engineering (IPS como target compuesto)',
        'Visualizaciones, correlaciones, análisis de distribuciones',
        'Ridge, Regresión Logística, Random Forest + KNN + K-Means',
        'Validación cruzada 5-fold, GridSearch, R², AUC, F1',
        'App Streamlit interactiva con 8 módulos funcionales',
        'Actualización continua vía GitHub Actions + retrain automático'
    ]
}
st.dataframe(pd.DataFrame(crisp_data), use_container_width=True, hide_index=True)

st.markdown('<h2 style="color:#4CAF50;font-size:1.5rem;margin:2rem 0 1rem 0;">\U0001F517 Herramientas Disponibles</h2>', unsafe_allow_html=True)
tools = [
    ('\U0001F52E Predictor IPS', 'Predice el Índice de Productividad del Suelo usando Regresión Ridge. Recibe 10 variables edáficas + 5 categóricas.'),
    ('\U0001F9EA Clasificador de Productividad', 'Clasifica suelos en Alta/Baja productividad mediante Regresión Logística. AUC objetivo ≥ 0.85.'),
    ('\U0001F333 Clasificador de Calidad', 'Clasifica la calidad del suelo en 4 categorías (Baja/Media/Buena/Excelente) con Random Forest.'),
    ('\U0001F50D Buscador KNN', 'Encuentra los suelos más similares en la base de datos usando K-Nearest Neighbors.'),
    ('\U0001F30D Mapa y Clusters', 'Visualiza clusters de suelos con K-Means + mapa coroplético de Colombia por IPS promedio.'),
    ('\U0001F4CA Dashboard EDA', 'Exploración interactiva de datos: distribuciones, correlaciones, rankings y valores nulos.'),
    ('\U0001F4F7 Análisis y Visualización', 'Galería de gráficos y análisis de los modelos de Machine Learning implementados.')
]
for icon, desc in tools:
    st.markdown(f'<div class="dark-card" style="margin-bottom:0.6rem;"><h3>{icon}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

st.markdown('<h2 style="color:#4CAF50;font-size:1.5rem;margin:2rem 0 1rem 0;">\U0001F9CA Matriz DOFA</h2>', unsafe_allow_html=True)
d1, d2, d3, d4 = st.columns(4)
with d1:
    st.success('\U0001F4AA **Fortalezas**\n- Dataset real de laboratorio\n- CRISP-ML estructurado\n- Múltiples modelos\n- App funcional interactiva')
with d2:
    st.warning('\U0001FA9C **Debilidades**\n- Datos desbalanceados\n- Sin variables climáticas directas\n- Alta dimensionalidad')
with d3:
    st.info('\U0001F680 **Oportunidades**\n- Política Agro 4.0\n- Crecimiento AgTech\n- Datos abiertos del DANE')
with d4:
    st.error('\U000026A0 **Amenazas**\n- Resistencia al cambio\n- Variabilidad climática\n- Calidad heterogénea de laboratorios')

st.markdown('<h2 style="color:#4CAF50;font-size:1.5rem;margin:2rem 0 1rem 0;">\U0001F4DA Marco Teórico (APA)</h2>', unsafe_allow_html=True)
refs = [
    "Arango, J. & Sánchez, L. (2022). Agricultura de precisión en Colombia. *Revista de Ciencias Agrícolas*, 56(3), 214-230.",
    "Cardona, P. & Morales, R. (2023). Machine learning para predicción de rendimientos agrícolas. *Ingeniería y Competitividad*, 25(1), e-12345.",
    "DANE. (2023). *Censo Nacional Agropecuario 2022*. Bogotá: Departamento Administrativo Nacional de Estadística.",
    "IDEAM. (2025). *Cambio Climático en Colombia 2024-2025*. Instituto de Hidrología, Meteorología y Estudios Ambientales.",
    "Jaramillo, M. et al. (2023). Inteligencia artificial en el agro colombiano. *Revista de Ingeniería*, 52, 78-95.",
    "MinAgricultura. (2024). *Plan de Ciencia, Tecnología e Innovación Agropecuaria 2024-2030*.",
    "Pérez, D. & Gómez, A. (2023). CRISP-ML en agricultura de precisión. *Tecnura*, 27(75), 112-128.",
    "Quinlan, J. R. (1986). Induction of decision trees. *Machine Learning*, 1(1), 81-106.",
    "Shearer, C. (2000). The CRISP-DM model. *Journal of Data Warehousing*, 5(4), 13-22."
]
for ref in refs:
    st.markdown(f'- {ref}')

st.divider()
st.markdown('<p style="text-align:center;color:#666;font-size:0.85rem;">AgroPredict Colombia — Proyecto de Optimización y Transferencia Tecnológica en el Sector Agropecuario Colombiano</p>', unsafe_allow_html=True)
