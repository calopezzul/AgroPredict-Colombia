# AgroPredict Colombia 🌾

Plataforma interactiva de **Machine Learning** para la optimización y transferencia tecnológica en el sector agropecuario colombiano.

## 📋 Descripción

AgroPredict Colombia es una aplicación Streamlit que integra 4 modelos de Machine Learning (Ridge, Regresión Logística, Random Forest, K-Means, KNN) para predecir y clasificar la productividad del suelo basado en 15 variables edáficas y categóricas.

**Dataset:** 92,738 registros de análisis de laboratorio de suelos en Colombia, 32 departamentos, 279 cultivos.

## 🚀 Características

| Módulo | Descripción | Modelo |
|--------|-------------|--------|
| **Predictor IPS** | Predice el Índice de Productividad del Suelo (0-100) | Ridge Regression |
| **Clasificador Productividad** | Clasifica suelos en Alta/Baja productividad | Regresión Logística |
| **Clasificador Calidad** | Clasifica en Baja/Media/Buena/Excelente | Random Forest |
| **Buscador KNN** | Encuentra suelos similares en la base de datos | K-Nearest Neighbors |
| **Mapa y Clusters** | Mapa coroplético de Colombia + K-Means clustering | K-Means + PCA |
| **EDA Dashboard** | Exploración interactiva de datos | Visualizaciones Plotly |

## 🛠️ Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/agropredict-colombia.git
cd agropredict-colombia

# Instalar dependencias
pip install -r requirements.txt

# Entrenar modelos
python models/entrenar_modelos.py

# Ejecutar la app
streamlit run app.py
```

## 📁 Estructura del Proyecto

```
├── app.py                       # Entry point de la app
├── pages/                       # 7 páginas de la aplicación
│   ├── 01_Inicio.py             # Landing page
│   ├── 02_Predictor_IPS.py      # Regresión Ridge
│   ├── 03_Clasificador_Prod.py  # Regresión Logística
│   ├── 04_Clasificador_Calidad.py # Random Forest
│   ├── 05_KNN_Similaridad.py    # KNN
│   ├── 06_KMeans_Clusters.py    # K-Means + Mapa
│   └── 07_EDA_Dashboard.py      # EDA interactivo
├── models/                      # Modelos entrenados + script de entrenamiento
│   ├── entrenar_modelos.py      # Pipeline de entrenamiento
│   ├── ridge.pkl / logistic.pkl / random_forest.pkl
│   ├── scaler_*.pkl / label_encoder.pkl
│   ├── kmeans.pkl / pca.pkl
│   └── depto_ips.json / knn_sample.parquet
├── utils/                       # Funciones auxiliares
│   ├── categorias.py            # Listas de categorías y rangos
│   ├── predicciones.py          # Funciones de predicción
│   ├── recomendaciones.py       # Recomendaciones agronómicas
│   └── visualizaciones.py       # Gráficos (gauge, radar, mapa, etc.)
├── assets/
│   └── colombia.geojson         # Mapa departamental de Colombia
├── requirements.txt
├── README.md
└── .streamlit/config.toml       # Tema de la app
```

## 📊 Modelos de Machine Learning

| Modelo | Tipo | Variable Objetivo | Métrica Esperada |
|--------|------|-------------------|------------------|
| Ridge | Regresión | IPS (continuo 0-100) | R² ≥ 0.70 |
| Regresión Logística | Clasificación binaria | prod_alta (0/1) | AUC ≥ 0.85 |
| Random Forest | Clasificación multiclase | calidad (4 clases) | F1-weighted ≥ 0.75 |
| K-Means | Clustering no supervisado | 4 clusters | Silhouette Score |

## 🔄 Actualización Automática

El proyecto incluye un workflow de GitHub Actions que entrena los modelos automáticamente el primer día de cada mes. Ver `.github/workflows/retrain.yml`.

## 👨‍🌾 Uso

1. Navegue a la **Landing Page** para contexto del proyecto
2. Use el **Predictor IPS** ingresando las variables del suelo
3. Consulte el **Clasificador de Calidad** para recomendaciones de cultivo
4. Explore el **Mapa de Colombia** para ver distribución espacial del IPS
5. Use el **EDA Dashboard** para análisis exploratorio interactivo

## 📚 Marco Teórico

- Arango, J. & Sánchez, L. (2022). Agricultura de precisión en Colombia. *Rev. Cs. Agrícolas*, 56(3), 214-230.
- Cardona, P. & Morales, R. (2023). ML para rendimientos agrícolas. *Ing. y Competitividad*, 25(1).
- DANE (2023). *Censo Nacional Agropecuario 2022*.
- Jaramillo, M. et al. (2023). IA en el agro colombiano. *Rev. Ingeniería*, 52, 78-95.
- Quinlan, J. R. (1986). Induction of decision trees. *Machine Learning*, 1(1), 81-106.

## 📄 Licencia

MIT
