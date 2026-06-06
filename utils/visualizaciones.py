import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

DARK_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor='#1A1C23',
        plot_bgcolor='#1A1C23',
        font=dict(color='#E0E0E0', size=12),
        title=dict(font=dict(color='#FFFFFF', size=16)),
        xaxis=dict(
            gridcolor='#333333',
            tickfont=dict(color='#BBBBBB'),
            title=dict(font=dict(color='#CCCCCC'))
        ),
        yaxis=dict(
            gridcolor='#333333',
            tickfont=dict(color='#BBBBBB'),
            title=dict(font=dict(color='#CCCCCC'))
        ),
        legend=dict(
            font=dict(color='#CCCCCC'),
            bgcolor='rgba(0,0,0,0)'
        ),
        hoverlabel=dict(bgcolor='#262730', font=dict(color='#FFFFFF')),
        colorway=['#4CAF50', '#66BB6A', '#FF9800', '#F44336', '#2196F3', '#AB47BC', '#26A69A', '#FFA726']
    )
)


def gauge_ips(valor):
    color = '#4CAF50' if valor >= 60 else ('#FF9800' if valor >= 40 else '#F44336')
    fig = go.Figure(go.Indicator(
        mode='gauge+number+delta',
        value=valor,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': 'IPS', 'font': {'size': 24, 'color': '#FFFFFF'}},
        delta={'reference': 60, 'position': 'top', 'font': {'color': '#CCCCCC'}},
        number={'font': {'color': '#FFFFFF', 'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#666', 'tickfont': {'color': '#BBBBBB'}},
            'bar': {'color': color},
            'bgcolor': '#262730',
            'borderwidth': 2,
            'bordercolor': '#444',
            'steps': [
                {'range': [0, 40], 'color': '#4A2020'},
                {'range': [40, 60], 'color': '#4A3A20'},
                {'range': [60, 80], 'color': '#1A3A20'},
                {'range': [80, 100], 'color': '#1A4A20'}
            ],
            'threshold': {
                'line': {'color': '#FFFFFF', 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20),
                      paper_bgcolor='#1A1C23', font=dict(color='#E0E0E0'))
    return fig


def barras_probabilidad(probas_dict):
    colores = {'Baja': '#F44336', 'Media': '#FF9800', 'Buena': '#4CAF50', 'Excelente': '#2E7D32'}
    df = pd.DataFrame({
        'Clase': list(probas_dict.keys()),
        'Probabilidad': list(probas_dict.values())
    })
    df['Color'] = df['Clase'].map(colores)
    fig = px.bar(df, x='Clase', y='Probabilidad', color='Clase',
                 color_discrete_map=colores, text='Probabilidad',
                 labels={'Probabilidad': 'Probabilidad (%)'})
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside',
                      textfont=dict(color='#FFFFFF'))
    fig.update_layout(yaxis_range=[0, 100], height=350, showlegend=False,
                      margin=dict(l=20, r=20, t=30, b=20),
                      paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
                      font=dict(color='#E0E0E0'),
                      xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
                      yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')))
    return fig


def radar_nutrientes(inputs):
    categorias = ['pH', 'MO', 'Fósforo', 'Calcio', 'Magnesio', 'Potasio', 'CIC']
    valores = [
        min(inputs.get('pH', 0) / 7.0 * 100, 100),
        min(inputs.get('MO', 0) / 10.0 * 100, 100),
        min(inputs.get('fosforo', 0) / 40.0 * 100, 100),
        min(inputs.get('calcio', 0) / 8.0 * 100, 100),
        min(inputs.get('magnesio', 0) / 2.0 * 100, 100),
        min(inputs.get('potasio', 0) / 0.5 * 100, 100),
        min(inputs.get('CIC', 0) / 15.0 * 100, 100)
    ]
    fig = go.Figure(data=go.Scatterpolar(
        r=valores + [valores[0]],
        theta=categorias + [categorias[0]],
        fill='toself',
        fillcolor='rgba(76, 175, 80, 0.3)',
        line=dict(color='#4CAF50', width=2),
        marker=dict(size=8, color='#4CAF50')
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color='#BBBBBB'),
            bgcolor='rgba(38, 39, 48, 0.8)',
            angularaxis=dict(color='#BBBBBB', gridcolor='#444')
        ),
        height=350, margin=dict(l=40, r=40, t=20, b=20),
        showlegend=False,
        paper_bgcolor='#1A1C23', font=dict(color='#E0E0E0')
    )
    return fig


def comparar_suelos(df_similares):
    fig = go.Figure()
    cols_num = ['pH', 'MO', 'fosforo', 'azufre', 'calcio', 'magnesio', 'potasio', 'CIC', 'CE']
    colores = px.colors.qualitative.Set2
    for i, (_, row) in enumerate(df_similares.iterrows()):
        fig.add_trace(go.Scatterpolar(
            r=[row[c] for c in cols_num] + [row[cols_num[0]]],
            theta=cols_num + [cols_num[0]],
            mode='lines+markers',
            name=f'Vecino {i+1} (dist={row.get("distancia",0):.2f})',
            line=dict(width=1, color=colores[i % len(colores)])
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, color='#BBBBBB'),
            bgcolor='rgba(38, 39, 48, 0.8)',
            angularaxis=dict(color='#BBBBBB', gridcolor='#444')
        ),
        height=400, margin=dict(l=40, r=40, t=30, b=20),
        paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
        font=dict(color='#E0E0E0'),
        legend=dict(font=dict(color='#CCCCCC'), bgcolor='rgba(0,0,0,0)')
    )
    return fig


def _normalizar_depto(nombre):
    if not isinstance(nombre, str):
        return ''
    m = {
        'san andres': 'san andrés y providencia',
        'bogota': 'bogotá',
        'norte de santander': 'norte de santander',
        'valle del cauca': 'valle del cauca',
    }
    n = nombre.lower().strip()
    n = n.replace(' d.c.', '').replace(', d.c.', '')
    return m.get(n, n)


def mapa_colombia(geo_path, df_deptos):
    import folium
    from streamlit_folium import st_folium
    import json
    from branca.colormap import linear

    m = folium.Map(location=[4.5, -74], zoom_start=5.5, tiles='CartoDB dark_matter')

    with open(geo_path, 'r', encoding='utf-8') as f:
        geo_data = json.load(f)

    ips_min = 0
    ips_max = 10
    colormap = linear.RdYlGn_11.scale(ips_min, ips_max)
    colormap.caption = 'IPS Promedio por Departamento'

    for feature in geo_data['features']:
        geo_name = feature['properties'].get('NOMBRE_DPT', feature['properties'].get('dpto', ''))
        geo_norm = _normalizar_depto(geo_name)

        ips_valor = None
        for k, v in df_deptos.items():
            if _normalizar_depto(k) == geo_norm:
                ips_valor = v
                break

        if ips_valor is not None:
            ips_text = f'{ips_valor:.1f}'
            color = colormap(ips_valor)
        else:
            ips_text = 'Sin datos'
            color = '#444444'

        feature['properties']['IPS_valor'] = ips_valor if ips_valor is not None else ''
        feature['properties']['IPS_texto'] = ips_text
        feature['properties']['color'] = color

    folium.GeoJson(
        geo_data,
        name='IPS por Departamento',
        style_function=lambda x: {
            'fillColor': x['properties'].get('color', '#444444'),
            'fillOpacity': 0.8,
            'color': '#FFFFFF',
            'weight': 1.5
        },
        highlight_function=lambda x: {
            'fillOpacity': 0.95,
            'weight': 2.5,
            'color': '#FFD700'
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=['NOMBRE_DPT', 'IPS_texto'],
            aliases=['Departamento:', 'IPS Promedio:'],
            localize=True,
            style='background-color: #1A1C23; color: #E0E0E0; border: 1px solid #444; font-size: 13px;'
        )
    ).add_to(m)

    colormap.add_to(m)

    return m


def crear_kpi_card(titulo, valor, icono='', delta=None, color='#4CAF50'):
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode='number+delta' if delta is not None else 'number',
        value=float(valor) if isinstance(valor, (int, float)) else 0,
        number={'font': {'color': '#FFFFFF', 'size': 36}, 'suffix': '' if isinstance(valor, str) else ''},
        delta={'reference': delta, 'font': {'color': '#66BB6A'}} if delta is not None else None,
        title={'text': f'{icono} {titulo}', 'font': {'color': '#AAAAAA', 'size': 14}}
    ))
    fig.update_layout(
        height=130,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor='#1A1C23',
        font=dict(color='#E0E0E0')
    )
    return fig


def grafico_ranking(df, titulo, color_scale='RdYlGn'):
    fig = px.bar(
        df, x='valor', y='nombre', orientation='h',
        color='valor', color_continuous_scale=color_scale,
        title=titulo, text_auto='.1f'
    )
    fig.update_traces(textfont=dict(color='#FFFFFF', size=11))
    fig.update_layout(
        height=400, margin=dict(l=10, r=10, t=40, b=20),
        paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
        font=dict(color='#E0E0E0'),
        xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
        yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
        coloraxis_colorbar=dict(tickfont=dict(color='#BBBBBB'))
    )
    return fig


def grafico_serie_temporal(df, x_col, y_col, titulo):
    fig = px.line(
        df, x=x_col, y=y_col,
        markers=True, line_shape='spline',
        title=titulo
    )
    fig.update_traces(
        line=dict(color='#4CAF50', width=3),
        marker=dict(color='#4CAF50', size=8),
        fill='tozeroy', fillcolor='rgba(76, 175, 80, 0.1)'
    )
    fig.update_layout(
        height=400, margin=dict(l=10, r=10, t=40, b=20),
        paper_bgcolor='#1A1C23', plot_bgcolor='#1A1C23',
        font=dict(color='#E0E0E0'),
        xaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
        yaxis=dict(gridcolor='#333', tickfont=dict(color='#BBBBBB')),
        hovermode='x unified'
    )
    return fig
