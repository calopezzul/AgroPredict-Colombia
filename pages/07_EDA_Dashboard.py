import streamlit as st
import pandas as pd
import numpy as np
import os, sys
import plotly.express as px
import plotly.graph_objects as go
from copy import deepcopy

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from utils.categorias import FEATURES_NUM, DEPTOS
from utils.limpiar import leer_csv_seguro, limpiar_dataframe, reportar_calidad, mostrar_reporte_calidad

def _grafico_ranking(df, titulo, color_scale='RdYlGn'):
    fig = px.bar(df, x='valor', y='nombre', orientation='h',
                 color='valor', color_continuous_scale=color_scale,
                 title=titulo, text_auto='.1f')
    fig.update_traces(textfont=dict(color='#FFFFFF', size=11))
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=40, b=20),
                      paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
                      font=dict(color='#E0E0E0'),
                      xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
                      yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
                      coloraxis_colorbar=dict(tickfont=dict(color='#BBBBBB')))
    return fig

def _grafico_serie_temporal(df, x_col, y_col, titulo):
    fig = px.line(df, x=x_col, y=y_col, markers=True, title=titulo)
    fig.update_traces(line=dict(color='#4CAF50', width=3), marker=dict(size=8, color='#4CAF50'))
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=40, b=20),
                      paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
                      font=dict(color='#E0E0E0'),
                      xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
                      yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')))
    return fig
st.set_page_config(page_title='Dashboard - AgroPredict', page_icon='📊', layout='wide')
st.markdown('<h1>\U0001F4CA Dashboard de Análisis y Métricas</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#AAAAAA;">Panel integral con indicadores clave, visualizaciones e inteligencia de negocio sobre el dataset de suelos colombianos.</p>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    BASE_L = os.path.join(BASE, 'Dataset')
    ruta = os.path.join(BASE_L, 'Resultados_de_Analisis_de_Laboratorio_Suelos_en_Colombia_20260526.csv')
    df = leer_csv_seguro(ruta)
    cols = {0:'id',1:'fecha',2:'depto',3:'municipio',4:'cultivo',5:'estado',6:'tiempo_est',7:'topografia',8:'drenaje',9:'riego',10:'fertilizantes',11:'pH',12:'MO',13:'fosforo',14:'azufre',15:'acidez',16:'aluminio',17:'calcio',18:'magnesio',19:'potasio',20:'sodio',21:'CIC',22:'CE',23:'Fe_olsen',24:'Cu',25:'Mn_olsen',26:'Zn_olsen',27:'B',28:'Fe_doble',29:'Cu_doble',30:'Mn_doble',31:'Zn_doble'}
    df.columns = [cols[i] for i in range(len(df.columns))]
    nulos = ['ND','Nd','nd','No indica','No Indica','NO','Ninguno','Ninguna','N','no','nan','NaN','']
    for c in df.columns:
        df[c] = df[c].replace(nulos, np.nan).astype(str).str.strip()
    nums = ['pH','MO','fosforo','azufre','acidez','aluminio','calcio','magnesio','potasio','sodio','CIC','CE','Fe_olsen','Cu','Mn_olsen','Zn_olsen','B','Fe_doble','Cu_doble','Mn_doble','Zn_doble']
    for c in nums:
        lt = df[c].str.match(r'^<', na=False)
        df.loc[lt, c] = df.loc[lt, c].str.replace('<','',regex=False).str.strip()
        df[c] = df[c].str.replace(',', '.', regex=False)
        df[c] = pd.to_numeric(df[c], errors='coerce')
        df.loc[lt, c] = df.loc[lt, c] / 2
    def parse_anios(v):
        if pd.isna(v): return np.nan
        s = str(v).lower().strip()
        if '0 a 1' in s: return 0.5
        if '1 a 5' in s: return 3
        if '5 a 10' in s: return 7.5
        if 'mas de 10' in s: return 15
        return np.nan
    df['anios_est'] = df['tiempo_est'].apply(parse_anios)
    def calc_ips(row):
        s = 0
        if pd.notna(row.get('pH')):
            ph = row['pH']
            if 5.5 <= ph <= 7.0: s += 20
            elif 5.0 <= ph < 5.5 or 7.0 < ph <= 7.5: s += 15
            elif 4.5 <= ph < 5.0 or 7.5 < ph <= 8.0: s += 10
            else: s += 5
        if pd.notna(row.get('MO')):
            mo = row['MO']
            if mo > 10: s += 15
            elif mo > 5: s += 12
            elif mo > 3: s += 8
            else: s += 4
        if pd.notna(row.get('CIC')):
            cic = row['CIC']
            if cic > 15: s += 15
            elif cic > 10: s += 12
            elif cic > 5: s += 8
            else: s += 4
        if pd.notna(row.get('fosforo')):
            p = row['fosforo']
            if p > 40: s += 10
            elif p > 20: s += 8
            elif p > 10: s += 5
            else: s += 2
        if pd.notna(row.get('potasio')):
            k = row['potasio']
            if k > 0.5: s += 10
            elif k > 0.3: s += 8
            elif k > 0.15: s += 5
            else: s += 2
        if pd.notna(row.get('CE')):
            ce = row['CE']
            if ce < 0.5: s += 10
            elif ce < 1.0: s += 8
            elif ce < 2.0: s += 5
            else: s += 2
        if pd.notna(row.get('calcio')):
            ca = row['calcio']
            if ca > 8: s += 10
            elif ca > 4: s += 8
            elif ca > 2: s += 5
            else: s += 2
        if pd.notna(row.get('magnesio')):
            mg = row['magnesio']
            if mg > 2: s += 10
            elif mg > 1: s += 7
            else: s += 3
        return s
    df['IPS'] = df.apply(calc_ips, axis=1)
    df['calidad'] = pd.cut(df['IPS'], bins=[0,40,60,80,100], labels=['Baja','Media','Buena','Excelente'])
    df['prod_alta'] = (df['IPS'] >= 60).astype(int)
    antes = len(df)
    df = df.drop_duplicates()
    despues = len(df)
    if antes != despues:
        st.cache_data.clear()
    return df

with st.spinner('Cargando dataset completo para dashboard...'):
    df = load_data()

with st.expander('\U0001F4CB Calidad de Datos — Auditoría automática'):
    reporte = reportar_calidad(df, 'Suelos Colombia')
    mostrar_reporte_calidad(st, reporte)
    if reporte.get('nulos'):
        st.caption('Las columnas con alta nulidad pueden afectar visualizaciones. Los rankings y correlaciones excluyen nulos automáticamente.')

# FILTROS GLOBALES
with st.container(border=True):
    st.markdown('### \U0001F3AF Filtros Globales')
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        deptos_opts = ['Todos'] + sorted(df['depto'].dropna().unique())
        depto_sel = st.selectbox('Departamento', deptos_opts)
    with f2:
        cultivos_opts = ['Todos'] + sorted(df['cultivo'].dropna().unique())
        cultivo_sel = st.selectbox('Cultivo', cultivos_opts)
    with f3:
        ips_range = st.slider('Rango IPS', 0, 100, (0, 100))
    with f4:
        cal_opts = ['Todas'] + ['Baja', 'Media', 'Buena', 'Excelente']
        cal_sel = st.selectbox('Calidad', cal_opts)

mask = pd.Series(True, index=df.index)
if depto_sel != 'Todos':
    mask &= (df['depto'] == depto_sel)
if cultivo_sel != 'Todos':
    mask &= (df['cultivo'] == cultivo_sel)
if cal_sel != 'Todas':
    mask &= (df['calidad'] == cal_sel)
mask &= (df['IPS'] >= ips_range[0]) & (df['IPS'] <= ips_range[1])
df_f = df[mask].copy()

# =============================================
# SECCION 1: KPI PRINCIPALES
# =============================================
st.markdown('<h2 style="margin-top:1.5rem;">\U0001F4C8 Indicadores Principales</h2>', unsafe_allow_html=True)

total_registros = len(df_f)
total_deptos = df_f['depto'].nunique()
total_municipios = df_f['municipio'].nunique()
total_cultivos = df_f['cultivo'].nunique()
prod_total = df_f['IPS'].sum()
rend_promedio = df_f['IPS'].mean()

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.metric('Total Registros', f'{total_registros:,}')
with k2:
    st.metric('Departamentos', f'{total_deptos}')
with k3:
    st.metric('Municipios', f'{total_municipios}', help='Municipios con registros en la muestra')
with k4:
    st.metric('Cultivos', f'{total_cultivos}')
with k5:
    st.metric('Producción Total', f'{prod_total:,.0f}')
with k6:
    st.metric('Rend. Promedio', f'{rend_promedio:.1f}')

# =============================================
# SECCION 2: VISUALIZACIONES PRINCIPALES
# =============================================
tab_dist, tab_corr, tab_rank, tab_ts = st.tabs([
    '\U0001F4CA Distribuciones', '\U0001F4A1 Correlaciones', '\U0001F3C6 Rankings', '\U0001F4C8 Tendencia Temporal'
])

with tab_dist:
    st.markdown('### Distribución de Variables Numéricas')
    var_sel = st.selectbox('Seleccione variable', FEATURES_NUM + ['IPS'], key='dist_var')
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig = px.histogram(df_f, x=var_sel, nbins=40, color_discrete_sequence=['#4CAF50'],
                           title=f'Histograma de {var_sel}', marginal='box')
        fig.update_layout(
            paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
            font=dict(color='#E0E0E0'),
            xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
            yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB'))
        )
        st.plotly_chart(fig, use_container_width=True)
    with col_g2:
        fig2 = px.box(df_f, y=var_sel, color_discrete_sequence=['#4CAF50'],
                      title=f'Boxplot de {var_sel}')
        fig2.update_layout(
            paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
            font=dict(color='#E0E0E0'),
            yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB'))
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('### Distribución de Calidad del Suelo')
    cal_counts = df_f['calidad'].value_counts().reindex(['Baja','Media','Buena','Excelente'], fill_value=0)
    colores_cal = {'Baja':'#F44336','Media':'#FF9800','Buena':'#4CAF50','Excelente':'#2E7D32'}
    fig3 = px.bar(x=cal_counts.index, y=cal_counts.values,
                  color=cal_counts.index, color_discrete_map=colores_cal,
                  title='Distribución de Calidad del Suelo', text_auto=True)
    fig3.update_traces(textfont=dict(color='#FFFFFF'))
    fig3.update_layout(
        paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
        font=dict(color='#E0E0E0'),
        xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
        yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB'))
    )
    st.plotly_chart(fig3, use_container_width=True)

    # =============================================
    # SECCION 4: INSIGHTS AUTOMATICOS - INTELIGENCIA DE NEGOCIO
    # =============================================
    st.markdown('<h2 style="margin-top:1.5rem;">\U0001F4A1 Insights Automáticos — Inteligencia de Negocio</h2>', unsafe_allow_html=True)

    with st.container(border=True):
        insights = []

        # Depto lider
        dept_rank = df_f.groupby('depto')['IPS'].mean().dropna().sort_values(ascending=False)
        if len(dept_rank) > 0:
            lider_depto = dept_rank.index[0]
            lider_ips = dept_rank.values[0]
            insights.append(('\U0001F3C6 Departamento Líder', f'**{lider_depto}** lidera con un IPS promedio de **{lider_ips:.1f}**, indicando las mejores condiciones de suelo para productividad agrícola.'))

        # Cultivo dominante
        cult_count = df_f['cultivo'].value_counts()
        if len(cult_count) > 0:
            cult_dom = cult_count.index[0]
            cult_dom_pct = cult_count.values[0] / total_registros * 100
            insights.append(('\U0001F33E Cultivo Dominante', f'**{cult_dom}** es el cultivo más frecuente con **{cult_count.values[0]:,}** registros ({cult_dom_pct:.1f}% del total filtrado).'))

        # Cultivo con mejor IPS
        cult_ips = df_f.groupby('cultivo')['IPS'].mean().dropna().sort_values(ascending=False)
        if len(cult_ips) > 0:
            best_cult = cult_ips.index[0]
            best_ips = cult_ips.values[0]
            insights.append(('\U00002B50 Mejor Rendimiento por Cultivo', f'**{best_cult}** presenta el IPS promedio más alto ({best_ips:.1f}), siendo el cultivo con mejor potencial productivo en los suelos analizados.'))

        # Departamento con mas registros
        dept_count = df_f['depto'].value_counts()
        if len(dept_count) > 0:
            top_dept = dept_count.index[0]
            top_dept_pct = dept_count.values[0] / total_registros * 100
            insights.append(('\U0001F4CB Mayor Cobertura', f'**{top_dept}** concentra la mayor cantidad de análisis con **{dept_count.values[0]:,}** registros ({top_dept_pct:.1f}% del total).'))

        # Calidad predominante
        cal_dist = df_f['calidad'].value_counts()
        if len(cal_dist) > 0:
            cal_pred = cal_dist.index[0]
            cal_pred_pct = cal_dist.values[0] / total_registros * 100
            insights.append(('\U0001F504 Calidad Predominante', f'La calidad **{cal_pred}** es la más común con **{cal_dist.values[0]:,}** registros ({cal_pred_pct:.1f}% del total).'))

        # Promedio general
        insights.append(('\U0001F4CA IPS Promedio General', f'El IPS promedio general es **{rend_promedio:.1f}** sobre un máximo de 100, indicando el nivel base de productividad del suelo en la región seleccionada.'))

        # Topografia mas comun
        topo_count = df_f['topografia'].value_counts()
        if len(topo_count) > 0:
            topo_top = topo_count.index[0]
            insights.append(('\U0001F3D4 Topografía Más Común', f'**{topo_top}** es la topografía predominante con **{topo_count.values[0]:,}** registros.'))

        cols_insights = st.columns(2)
        for i, (icon_title, desc) in enumerate(insights):
            with cols_insights[i % 2]:
                st.markdown(f'<div class="insight-card"><strong>{icon_title}</strong><br>{desc}</div>', unsafe_allow_html=True)

    # =============================================
    # SECCION 5: COMPARATIVOS REGIONALES
    # =============================================
    st.markdown('<h2 style="margin-top:1.5rem;">\U0001F30D Comparativos Regionales</h2>', unsafe_allow_html=True)

    if depto_sel == 'Todos':
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown('### Top 10 Departamentos por IPS Promedio')
            dept_rank_full = df.groupby('depto')['IPS'].mean().dropna().sort_values(ascending=False).head(10)
            dept_df_full = pd.DataFrame({'nombre': dept_rank_full.index, 'valor': dept_rank_full.values})
            st.plotly_chart(_grafico_ranking(dept_df_full, ''), use_container_width=True)

        with col_r2:
            st.markdown('### Distribución Geográfica de Calidad')
            dept_cal = df.groupby('depto')['calidad'].value_counts(normalize=True).mul(100).reset_index(name='porcentaje')
            dept_cal = dept_cal[dept_cal['calidad'] == 'Excelente'].sort_values('porcentaje', ascending=False).head(10)
            if len(dept_cal) > 0:
                fig_dc = px.bar(dept_cal, x='porcentaje', y='depto', orientation='h',
                               color='porcentaje', color_continuous_scale='Greens',
                               title='% de Suelos con Calidad Excelente por Departamento', text_auto='.1f')
                fig_dc.update_traces(textfont=dict(color='#FFFFFF'))
                fig_dc.update_layout(
                    paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
                    font=dict(color='#E0E0E0'),
                    xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
                    yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB'))
                )
                st.plotly_chart(fig_dc, use_container_width=True)
            else:
                st.info('No hay suficientes datos para el comparativo regional.')

with tab_corr:
    st.markdown('### Matriz de Correlación (triángulo inferior)')
    nums_show = [c for c in FEATURES_NUM if c in df_f.columns and c != 'anios_est'] + ['IPS']
    df_corr = df_f[nums_show].dropna()
    if len(df_corr) > 5:
        corr = df_corr.corr()
        corr_tri = corr.where(np.tril(np.ones(corr.shape), k=-1).astype(bool))
        corr_tri = corr_tri.dropna(how='all', axis=0).dropna(how='all', axis=1)
        if corr_tri.size > 0:
            fig = px.imshow(corr_tri, text_auto='.2f', color_continuous_scale='RdYlGn',
                            title='Correlación entre Variables (triángulo inferior)', aspect='auto')
            fig.update_traces(zmin=-1, zmax=1)
            fig.update_layout(
                paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
                font=dict(color='#E0E0E0'),
                coloraxis_colorbar=dict(tickfont=dict(color='#BBBBBB'))
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('### Correlación con IPS')
        ips_corr = corr['IPS'].drop('IPS', errors='ignore').sort_values(ascending=False)
        fig2 = px.bar(x=ips_corr.index, y=ips_corr.values,
                      color=ips_corr.values, color_continuous_scale='RdYlGn',
                      title='Correlación de cada Variable con IPS')
        fig2.update_traces(texttemplate='%{y:.2f}', textposition='outside')
        fig2.update_layout(
            paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
            font=dict(color='#E0E0E0'),
            xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
            yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
            yaxis_range=[-1, 1]
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info('Datos insuficientes para calcular correlaciones significativas.')

    # =============================================
    # SECCION 3: VALORES NULOS
    # =============================================
    st.markdown('<h2 style="margin-top:1.5rem;">\U0000274C Análisis de Calidad de Datos</h2>', unsafe_allow_html=True)
    null_pct = (df_f.isnull().sum() / len(df_f) * 100).sort_values(ascending=False)
    null_pct = null_pct[null_pct > 0]
    if len(null_pct) > 0:
        fig_nulos = px.bar(x=null_pct.index, y=null_pct.values,
                           color=null_pct.values, color_continuous_scale='Reds',
                           title='Porcentaje de Valores Nulos por Columna',
                           text_auto='.1f')
        fig_nulos.update_traces(textfont=dict(color='#FFFFFF'))
        fig_nulos.update_layout(
            paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
            font=dict(color='#E0E0E0'),
            xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
            yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB'), title='% Nulos')
        )
        st.plotly_chart(fig_nulos, use_container_width=True)

        with st.expander('Ver resumen de nulos en tabla'):
            null_df = pd.DataFrame({
                'Variable': null_pct.index,
                '% Nulos': null_pct.values.round(1),
                'Registros Nulos': df_f.isnull().sum()[null_pct.index].values
            })
            st.dataframe(null_df, use_container_width=True, hide_index=True)
    else:
        st.success('No hay valores nulos en los datos filtrados.')

with tab_rank:
    st.markdown('### Top Departamentos por IPS Promedio')
    df_rank_dept = df_f.groupby('depto')['IPS'].mean().dropna().reset_index()
    df_rank_dept.columns = ['nombre', 'valor']
    df_rank_dept = df_rank_dept.sort_values('valor', ascending=False).head(15).reset_index(drop=True)
    st.plotly_chart(_grafico_ranking(df_rank_dept, 'Top 15 Departamentos — IPS Promedio'), use_container_width=True)

    st.markdown('### Top Cultivos por IPS Promedio')
    df_rank_cult = df_f.groupby('cultivo')['IPS'].mean().dropna().reset_index()
    df_rank_cult.columns = ['nombre', 'valor']
    df_rank_cult = df_rank_cult.sort_values('valor', ascending=False).head(15).reset_index(drop=True)
    st.plotly_chart(_grafico_ranking(df_rank_cult, 'Top 15 Cultivos — IPS Promedio'), use_container_width=True)

    st.markdown('### Distribución por Cultivo (Cantidad de Registros)')
    cult_count = df_f['cultivo'].value_counts().reset_index()
    cult_count.columns = ['nombre', 'valor']
    cult_count = cult_count.head(15)
    fig_cc = px.bar(cult_count, x='valor', y='nombre', orientation='h',
                    color='valor', color_continuous_scale='Viridis',
                    title='Top 15 Cultivos — Número de Registros', text_auto=True)
    fig_cc.update_traces(textfont=dict(color='#FFFFFF'))
    fig_cc.update_layout(
        height=400,
        paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
        font=dict(color='#E0E0E0'),
        xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
        yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB'))
    )
    st.plotly_chart(fig_cc, use_container_width=True)

with tab_ts:
    st.markdown('### Tendencia Temporal de IPS')
    if 'fecha' in df_f.columns and df_f['fecha'].notna().any():
        df_ts = df_f[df_f['fecha'].notna()].copy()
        df_ts['fecha'] = pd.to_datetime(df_ts['fecha'], errors='coerce')
        df_ts = df_ts.dropna(subset=['fecha']).drop_duplicates(subset=['id', 'fecha'] if 'id' in df_ts.columns else None)
        if len(df_ts) > 0:
            df_ts['año'] = df_ts['fecha'].dt.year.astype(int)
            trend = df_ts.groupby('año', as_index=False)['IPS'].agg(IPS_promedio='mean', registros='count', desviacion='std')
            trend = trend.drop_duplicates(subset=['año'])
            st.plotly_chart(_grafico_serie_temporal(trend, 'año', 'IPS_promedio',
                            'Evolución del IPS Promedio por Año'), use_container_width=True)

            st.markdown('### Distribución Temporal por Calidad')
            ts_cal = df_ts.groupby(['año', 'calidad'], as_index=False).size()
            ts_cal = ts_cal.drop_duplicates(subset=['año', 'calidad'])
            fig_ts = px.area(ts_cal, x='año', y='size', color='calidad',
                             color_discrete_map=colores_cal,
                             title='Evolución de Calidad del Suelo por Año',
                             line_group='calidad')
            fig_ts.update_layout(
                paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
                font=dict(color='#E0E0E0'),
                xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
                yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
                legend=dict(font=dict(color='#BBBBBB'))
            )
            st.plotly_chart(fig_ts, use_container_width=True)

            st.markdown('### Volumen de Registros por Año')
            fig_vol = px.bar(trend, x='año', y='registros',
                            color='registros', color_continuous_scale='Greens',
                            title='Cantidad de Análisis de Suelos por Año', text_auto=True)
            fig_vol.update_traces(textfont=dict(color='#FFFFFF'))
            fig_vol.update_layout(
                paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
                font=dict(color='#E0E0E0'),
                xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
                yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB'))
            )
            st.plotly_chart(fig_vol, use_container_width=True)
        else:
            st.info('No hay datos de fecha disponibles para análisis temporal.')
    else:
        st.info('No hay datos de fecha disponibles para análisis temporal.')
st.markdown(f'<p style="text-align:center;color:#666;font-size:0.8rem;margin-top:2rem;">Registros analizados: {total_registros:,} | Datos de {total_deptos} departamentos y {total_cultivos} cultivos</p>', unsafe_allow_html=True)
