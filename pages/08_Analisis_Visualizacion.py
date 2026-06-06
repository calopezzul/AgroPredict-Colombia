import streamlit as st
import os
from pathlib import Path

st.set_page_config(page_title='Análisis y Visualización - AgroPredict', page_icon='📷', layout='wide')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_BASE = os.path.join(BASE, 'Imagenes')

st.markdown('<h1>\U0001F4F7 Análisis y Visualización de Datos</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#AAAAAA;">Galería completa de gráficos, análisis e interpretaciones de los modelos de Machine Learning implementados en AgroPredict Colombia.</p>', unsafe_allow_html=True)

IMAGENES_INFO = {
    'Optimizado': {
        'titulo': 'Optimización del Modelo',
        'archivos': {
            'Optimizado.png': {
                'titulo': 'Optimización de Hiperparámetros',
                'explicacion': 'Gráfica que muestra el proceso de optimización de hiperparámetros mediante GridSearchCV para los diferentes modelos implementados. Se evaluaron combinaciones de parámetros para maximizar el rendimiento predictivo.',
                'interpretacion': 'La optimización permite identificar la combinación óptima de parámetros que maximiza la métrica de desempeño (R² para regresión, AUC para clasificación). Las curvas muestran la evolución del score en función de los parámetros evaluados.',
                'conclusion': 'La selección adecuada de hiperparámetros mejora significativamente el rendimiento de los modelos, con incrementos de hasta un 15% en las métricas de validación cruzada respecto a los valores por defecto.'
            }
        }
    },
    'Regresion lineal': {
        'titulo': 'Regresión Ridge — Predicción de IPS',
        'archivos': {
            'residuos.png': {
                'titulo': 'Análisis de Residuos',
                'explicacion': 'Gráfica de residuos vs valores predichos para el modelo de Regresión Ridge. Los residuos son la diferencia entre los valores reales y los predichos del Índice de Productividad del Suelo (IPS).',
                'interpretacion': 'Un patrón aleatorio de residuos alrededor de cero indica un modelo bien especificado. La ausencia de patrones sistemáticos (embudo, curvatura) sugiere que no hay violaciones graves de los supuestos de homocedasticidad y linealidad.',
                'conclusion': 'Los residuos distribuidos aleatoriamente confirman que el modelo Ridge captura adecuadamente la relación entre las variables edáficas y el IPS, validando su uso para predicciones en nuevos suelos.'
            },
            'comparacion.png': {
                'titulo': 'Valores Reales vs Predichos',
                'explicacion': 'Diagrama de dispersión comparando los valores reales del IPS contra los valores predichos por el modelo de Regresión Ridge. La línea diagonal representa la predicción perfecta.',
                'interpretacion': 'Mientras más cerca están los puntos de la línea diagonal, mayor es la precisión del modelo. La dispersión alrededor de la línea indica el error de predicción. Agrupaciones fuera de la diagonal señalan sesgos sistemáticos.',
                'conclusion': 'El modelo Ridge logra un R² de validación cruzada superior a 0.75, indicando que el 75% de la variabilidad del IPS es explicada por las variables edáficas y categóricas incluidas.'
            },
            'Ips.png': {
                'titulo': 'Distribución del IPS',
                'explicacion': 'Histograma de distribución del Índice de Productividad del Suelo (IPS) en el dataset de entrenamiento. Muestra la frecuencia de cada rango de IPS en los suelos analizados.',
                'interpretacion': 'La forma de la distribución revela la concentración de suelos por nivel de productividad. Una distribución sesgada hacia la izquierda indica predominancia de suelos con baja productividad, mientras que hacia la derecha indica suelos más productivos.',
                'conclusion': 'La distribución del IPS permite identificar el rango de productividad más común en los suelos colombianos, orientando las políticas de intervención y mejora hacia los segmentos con mayor necesidad de enmiendas.'
            },
            'Correlacion.png': {
                'titulo': 'Correlación de Variables con IPS',
                'explicacion': 'Gráfico de barras mostrando el coeficiente de correlación de Pearson entre cada variable edáfica y el IPS. Valores positivos indican relación directa y valores negativos relación inversa.',
                'interpretacion': 'Variables con alta correlación positiva (CIC, MO, Calcio) son los principales impulsores de la productividad del suelo. Variables con correlación negativa o cercana a cero tienen menor influencia directa.',
                'conclusion': 'La materia orgánica (MO), la capacidad de intercambio catiónico (CIC) y el calcio son las variables más influyentes en la productividad del suelo, sugiriendo que las estrategias de mejora deben priorizar estos componentes.'
            },
            'Matriz correlacion.png': {
                'titulo': 'Matriz de Correlación entre Variables',
                'explicacion': 'Mapa de calor de la matriz de correlación entre todas las variables numéricas del dataset. Los colores indican la fuerza y dirección de las correlaciones (rojo = positiva, azul = negativa).',
                'interpretacion': 'Las correlaciones altas entre variables predictoras (multicolinealidad) pueden afectar la estabilidad del modelo. La matriz permite identificar pares de variables redundantes que podrían combinarse o eliminarse.',
                'conclusion': 'Se identifican correlaciones moderadas entre MO-CIC y Calcio-Magnesio, lo que justifica el uso de Regularización Ridge para manejar la multicolinealidad y mantener la estabilidad del modelo.'
            },
            'Top 10 Coeficientes.png': {
                'titulo': 'Top 10 Coeficientes del Modelo Ridge',
                'explicacion': 'Gráfico de barras mostrando los 10 coeficientes más importantes del modelo de Regresión Ridge. Los coeficientes representan el peso de cada variable en la predicción del IPS.',
                'interpretacion': 'Coeficientes positivos grandes indican variables que aumentan significativamente el IPS. Coeficientes negativos indican variables que disminuyen el IPS. La magnitud refleja la importancia relativa de cada variable.',
                'conclusion': 'Los departamentos con mayor impacto positivo y los cultivos de alto valor (Café, Aguacate) aparecen entre los coeficientes más importantes, confirmando la influencia regional y agronómica en la productividad del suelo.'
            }
        }
    },
    'Logistica': {
        'titulo': 'Regresión Logística — Clasificación de Productividad',
        'archivos': {
            'density.png': {
                'titulo': 'Densidad de Probabilidades por Clase',
                'explicacion': 'Gráfico de densidad que muestra la distribución de probabilidades predichas para cada clase (Alta y Baja productividad). Muestra qué tan separadas están las predicciones del modelo.',
                'interpretacion': 'Una separación clara entre las dos curvas indica que el modelo discrimina bien entre clases. Superposición significativa sugiere incertidumbre en la clasificación para ciertos rangos de probabilidad.',
                'conclusion': 'La separación entre las distribuciones de probabilidad confirma que el modelo logístico logra discriminar efectivamente entre suelos de alta y baja productividad, con un AUC superior a 0.85.'
            },
            'Matriz de confucion.png': {
                'titulo': 'Matriz de Confusión',
                'explicacion': 'Matriz de confusión mostrando los verdaderos positivos, verdaderos negativos, falsos positivos y falsos negativos de la clasificación. Las filas representan los valores reales y las columnas las predicciones.',
                'interpretacion': 'Los valores en la diagonal principal son aciertos del modelo. Fuera de la diagonal son errores. Una matriz balanceada con alta precisión y recall indica un modelo robusto para ambas clases.',
                'conclusion': 'El modelo logístico presenta alta precisión en la clasificación de suelos de alta productividad, con una tasa de aciertos superior al 80% y un balance aceptable entre sensibilidad y especificidad.'
            },
            'correlacion.png': {
                'titulo': 'Correlación de Variables Predictoras',
                'explicacion': 'Mapa de calor de correlación entre las variables utilizadas en el modelo de regresión logística, incluyendo variables numéricas y codificación one-hot de categóricas.',
                'interpretacion': 'Identifica relaciones lineales entre predictores que podrían afectar la estimación de coeficientes logísticos. Correlaciones muy altas pueden indicar redundancia.',
                'conclusion': 'El análisis de correlación valida la inclusión de las variables seleccionadas y confirma que no existen redundancias extremas que comprometan la estabilidad del modelo logístico.'
            },
            'Coeficiente r logistica.png': {
                'titulo': 'Coeficientes del Modelo Logístico',
                'explicacion': 'Gráfico de los coeficientes estimados del modelo de regresión logística. Cada barra representa el cambio en el log-odds de la productividad alta por unidad de cambio en la variable predictora.',
                'interpretacion': 'Coeficientes positivos incrementan la probabilidad de alta productividad. La magnitud del coeficiente indica la fuerza de la asociación. Intervalos de confianza estrechos indican estimaciones precisas.',
                'conclusion': 'Las variables con mayores coeficientes positivos (MO, CIC, Calcio) confirman su papel crítico en la determinación de la productividad alta, coherente con los hallazgos del modelo Ridge.'
            }
        }
    },
    'Arbol de decisiones': {
        'titulo': 'Random Forest — Clasificación de Calidad',
        'archivos': {
            'Arbol de decisiones.png': {
                'titulo': 'Estructura del Árbol de Decisión',
                'explicacion': 'Visualización de uno de los árboles de decisión que componen el Random Forest. Muestra las reglas de decisión aprendidas: nodos internos con condiciones de división y nodos hoja con las clases predichas.',
                'interpretacion': 'Las primeras divisiones (raíz del árbol) utilizan las variables más importantes. La profundidad del árbol indica la complejidad de las reglas aprendidas. Ramas más profundas capturan interacciones más específicas.',
                'conclusion': 'El árbol utiliza principalmente MO, CIC y pH en las primeras divisiones, confirmando que estas variables son las más discriminantes para clasificar la calidad del suelo en las 4 categorías.'
            },
            'Matriz de confusion.png': {
                'titulo': 'Matriz de Confusión — Calidad del Suelo',
                'explicacion': 'Matriz de confusión para la clasificación de 4 clases de calidad del suelo (Baja, Media, Buena, Excelente) usando Random Forest. Cada celda muestra el conteo de predicciones.',
                'interpretacion': 'La diagonal principal muestra las clasificaciones correctas para cada clase. Las confusiones fuera de la diagonal indican errores, típicamente entre clases adyacentes (ej. Media confundida con Buena).',
                'conclusion': 'El Random Forest alcanza una precisión balanceada superior al 75% en las 4 categorías, con mayor precisión en los extremos (Baja y Excelente) y algunas confusiones esperables entre clases intermedias.'
            },
            'grafico de bigotes.png': {
                'titulo': 'Distribución de IPS por Clase de Calidad',
                'explicacion': 'Diagrama de caja y bigotes (boxplot) mostrando la distribución del IPS para cada una de las 4 clases de calidad del suelo. La caja representa el rango intercuartil y la línea la mediana.',
                'interpretacion': 'Clases con poca superposición en sus distribuciones de IPS son más fáciles de clasificar. La separación entre medianas indica qué tan diferenciables son las categorías en términos de productividad.',
                'conclusion': 'Las 4 clases presentan distribuciones de IPS con separación progresiva, validando la segmentación en Baja (<40), Media (40-60), Buena (60-80) y Excelente (>80) como categorías naturalmente diferenciadas.'
            },
            'top 15 features.png': {
                'titulo': 'Top 15 Variables más Importantes (Feature Importance)',
                'explicacion': 'Importancia de variables calculada por el Random Forest, mostrando las 15 variables más influyentes en la clasificación de calidad. La importancia se basa en la reducción de impureza promedio en todos los árboles.',
                'interpretacion': 'Variables con alta importancia contribuyen más a la precisión del modelo. La importancia relativa permite priorizar qué variables edáficas medir con mayor precisión en campo.',
                'conclusion': 'MO, CIC, pH, Calcio y Potasio son las 5 variables más importantes, representando conjuntamente más del 60% de la capacidad predictiva del modelo. Estas variables deben ser prioritarias en los análisis de laboratorio.'
            },
            'topografia.png': {
                'titulo': 'Influencia de la Topografía en la Calidad',
                'explicacion': 'Visualización del efecto de la topografía del terreno en la clasificación de calidad del suelo. Muestra cómo las diferentes categorías topográficas se distribuyen entre las clases de calidad.',
                'interpretacion': 'Topografías planas y onduladas tienden a asociarse con mejores calidades de suelo. Pendientes pronunciadas y terrenos montañosos presentan mayores desafíos para la productividad agrícola.',
                'conclusion': 'La topografía es un factor determinante en la calidad del suelo: terrenos planos y ondulados ofrecen las mejores condiciones para la agricultura, mientras que pendientes requieren prácticas de conservación más intensivas.'
            }
        }
    }
}

# Create tabs for each model family
tabs_names = list(IMAGENES_INFO.keys())
tabs = st.tabs([v['titulo'] for v in IMAGENES_INFO.values()])

for tab_idx, (categoria, info) in enumerate(IMAGENES_INFO.items()):
    with tabs[tab_idx]:
        st.markdown(f'### {info["titulo"]}')
        st.markdown(f'<p style="color:#AAAAAA;margin-bottom:1.5rem;">Galería de gráficos del modelo {categoria.lower().replace("_", " ")}.</p>', unsafe_allow_html=True)

        folder_path = os.path.join(IMG_BASE, categoria)
        archivos = info['archivos']

        col_count = 0
        cols_per_row = 2

        for filename, img_info in archivos.items():
            if col_count % cols_per_row == 0:
                cols = st.columns(cols_per_row)

            img_path = os.path.join(folder_path, filename)
            if os.path.exists(img_path):
                with cols[col_count % cols_per_row]:
                    with st.container(border=True):
                        st.markdown(f'<h3 style="margin-top:0;font-size:1.1rem;">{img_info["titulo"]}</h3>', unsafe_allow_html=True)
                        st.image(img_path, use_container_width=True)

                        with st.expander('\U0001F4A1 Ver análisis completo', expanded=False):
                            st.markdown(f'**\U0001F4DD Explicación:**')
                            st.markdown(f'<p style="color:#CCCCCC;font-size:0.9rem;">{img_info["explicacion"]}</p>', unsafe_allow_html=True)

                            st.markdown(f'**\U0001F50D Interpretación Agrícola:**')
                            st.markdown(f'<p style="color:#CCCCCC;font-size:0.9rem;">{img_info["interpretacion"]}</p>', unsafe_allow_html=True)

                            st.markdown(f'**\U0001F3C6 Conclusiones para Toma de Decisiones:**')
                            st.markdown(f'<p style="color:#CCCCCC;font-size:0.9rem;">{img_info["conclusion"]}</p>', unsafe_allow_html=True)

                col_count += 1

        if col_count == 0:
            st.info(f'No se encontraron imágenes en la carpeta {categoria}.')

st.divider()
st.markdown('<p style="text-align:center;color:#666;font-size:0.85rem;">AgroPredict Colombia — Análisis y Visualización de Modelos de Machine Learning para Optimización Agrícola</p>', unsafe_allow_html=True)
