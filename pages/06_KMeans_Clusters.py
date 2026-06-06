import streamlit as st
import pandas as pd
import numpy as np
import os, sys, json, joblib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from utils.categorias import FEATURES_NUM, DEPTOS
from utils.visualizaciones import mapa_colombia
from utils.limpiar import limpiar_texto_colombia
from sklearn.decomposition import PCA
st.set_page_config(page_title='Mapa y Clusters - AgroPredict', page_icon='🌍', layout='wide')
models_path = os.path.join(BASE, 'models')
kmeans = joblib.load(os.path.join(models_path, 'kmeans.pkl'))
pca_model = joblib.load(os.path.join(models_path, 'pca.pkl'))
scaler_k = joblib.load(os.path.join(models_path, 'scaler_kmeans.pkl'))
geo_path = os.path.join(BASE, 'assets', 'colombia.geojson')

with open(os.path.join(models_path, 'depto_ips.json'), 'r', encoding='utf-8') as f:
    depto_ips_raw = json.load(f)
depto_ips = {}
for k, v in depto_ips_raw.items():
    k_clean = limpiar_texto_colombia(k)
    k_norm = k_clean.lower().replace('í','i').replace('é','e').replace('á','a').replace('ó','o').replace('ú','u').replace('ñ','n')
    matched = False
    for d in DEPTOS:
        d_norm = d.lower().replace('í','i').replace('é','e').replace('á','a').replace('ó','o').replace('ú','u').replace('ñ','n')
        if d_norm == k_norm:
            k_clean = d
            matched = True
            break
    depto_ips[k_clean] = v

st.markdown('<h1>\U0001F30D Mapa de Colombia y Clustering de Suelos</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(['\U0001F5FA Mapa de Colombia por IPS', '\U0001F300 Clustering K-Means'])

with tab1:
    st.markdown('### Mapa Coroplético de Colombia — IPS Promedio por Departamento')
    st.markdown('<p style="color:#AAAAAA;">Los departamentos se muestran coloreados según el IPS promedio (rojo = bajo, amarillo = medio, verde = alto).</p>', unsafe_allow_html=True)

    m = mapa_colombia(geo_path, depto_ips)
    from streamlit_folium import st_folium
    st_folium(m, width=900, height=600)

    st.markdown('### \U0001F4CA Departamentos con Mayor y Menor IPS')
    sorted_d = sorted(depto_ips.items(), key=lambda x: x[1] if x[1] else 0, reverse=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('**Top 5 — Mayor IPS**')
        for depto, ips in sorted_d[:5]:
            st.markdown(f'- **{depto}**: {ips:.1f}')
    with c2:
        st.markdown('**Bottom 5 — Menor IPS**')
        for depto, ips in sorted_d[-5:]:
            st.markdown(f'- **{depto}**: {ips:.1f}')

with tab2:
    st.markdown('### \U0001F300 Clustering de Suelos con K-Means (k=4)')
    st.markdown('<p style="color:#AAAAAA;">Visualización de los 4 clusters de suelos proyectados en 2 componentes principales (PCA).</p>', unsafe_allow_html=True)

    rng = np.random.default_rng(42)
    X_sim = rng.normal(0, 1, (5000, 10))
    df_pca = pd.DataFrame(pca_model.transform(scaler_k.transform(X_sim)),
                          columns=['PC1', 'PC2'])
    df_pca['cluster'] = kmeans.predict(X_sim)

    import plotly.express as px

    fig = px.scatter(df_pca, x='PC1', y='PC2', color=df_pca['cluster'].astype(str),
                     color_discrete_sequence=['#F44336', '#FF9800', '#4CAF50', '#2E7D32'],
                     title='Proyección PCA de los 4 Clusters de Suelos',
                     labels={'cluster': 'Cluster'})
    fig.update_traces(marker=dict(size=4, opacity=0.6))
    fig.update_layout(
        paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
        font=dict(color='#E0E0E0'),
        xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
        yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
        legend=dict(font=dict(color='#BBBBBB'))
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('### \U0001F4CA Perfil de los Clusters')
    centroids = scaler_k.inverse_transform(kmeans.cluster_centers_)
    df_cent = pd.DataFrame(centroids, columns=FEATURES_NUM)
    df_cent.index = [f'Cluster {i}' for i in range(4)]

    colors = ['#F44336', '#FF9800', '#4CAF50', '#2E7D32']
    for i in range(4):
        st.markdown(f'<div style="background:{colors[i]};border-radius:12px;padding:1rem;margin:0.5rem 0;color:white;">'
                    f'<strong>Cluster {i}</strong> — '
                    f'pH: {df_cent.loc[f"Cluster {i}","pH"]:.1f} | '
                    f'MO: {df_cent.loc[f"Cluster {i}","MO"]:.1f}% | '
                    f'Fósforo: {df_cent.loc[f"Cluster {i}","fosforo"]:.0f} ppm | '
                    f'CIC: {df_cent.loc[f"Cluster {i}","CIC"]:.1f} | '
                    f'IPS estimado: {df_cent.loc[f"Cluster {i}"].mean():.0f}'
                    f'</div>', unsafe_allow_html=True)

    st.dataframe(df_cent.round(2), use_container_width=True)
