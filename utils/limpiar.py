import pandas as pd
import numpy as np
import os

_MOJIBAKE_CHARS = 'Ã¡Ã©Ã­Ã³ÃºÃ±ÃÃ‰ÃÃ“ÃšÃ‘Ã¼Ãœ'


def tiene_mojibake(texto):
    if not isinstance(texto, str):
        return False
    return any(ch in texto for ch in _MOJIBAKE_CHARS)


def limpiar_mojibake(texto):
    if not isinstance(texto, str):
        return texto
    if not tiene_mojibake(texto):
        return texto
    try:
        corregido = texto.encode('latin1').decode('utf-8')
        return corregido
    except Exception:
        return texto


def limpiar_serie(serie):
    if serie.dtype != 'object':
        return serie
    return serie.astype(str).apply(limpiar_mojibake)


def limpiar_dataframe(df, columnas_texto=None):
    if columnas_texto is None:
        columnas_texto = df.select_dtypes(include='object').columns.tolist()
    for col in columnas_texto:
        if col in df.columns:
            df[col] = limpiar_serie(df[col])
    return df


def detectar_encoding(ruta):
    if not os.path.exists(ruta):
        return 'utf-8'
    with open(ruta, 'rb') as f:
        raw = f.read(10000)
    if raw.startswith(b'\xef\xbb\xbf'):
        return 'utf-8-sig'
    try:
        raw.decode('utf-8')
        return 'utf-8'
    except UnicodeDecodeError:
        try:
            raw.decode('latin1')
            return 'latin1'
        except Exception:
            return 'utf-8'


def leer_csv_seguro(ruta, **kwargs):
    if not os.path.exists(ruta):
        ruta_gz = ruta + '.gz'
        if os.path.exists(ruta_gz):
            ruta = ruta_gz
            kwargs.setdefault('compression', 'gzip')
    enc = kwargs.pop('encoding', detectar_encoding(ruta))
    df = pd.read_csv(ruta, encoding=enc, **kwargs)
    for col in df.select_dtypes(include='object').columns:
        df[col] = limpiar_serie(df[col])
    return df


def reportar_calidad(df, nombre='DataFrame'):
    total = len(df)
    nulos = df.isnull().sum()
    nulos_pct = (nulos / total * 100).round(1)
    duplicados = df.duplicated().sum()
    reporte = {
        'nombre': nombre,
        'total_filas': total,
        'columnas': len(df.columns),
        'filas_duplicadas': duplicados,
        'pct_duplicados': round(duplicados / total * 100, 1) if total > 0 else 0,
    }
    cols_con_nulos = nulos[nulos > 0]
    if len(cols_con_nulos) > 0:
        reporte['nulos'] = {c: {'cantidad': int(nulos[c]), 'porcentaje': float(nulos_pct[c])}
                           for c in cols_con_nulos.index}
    else:
        reporte['nulos'] = {}
    return reporte


def mostrar_reporte_calidad(st, reporte):
    st.markdown(f'**Calidad de datos: {reporte["nombre"]}**')
    c1, c2, c3 = st.columns(3)
    c1.metric('Filas', f"{reporte['total_filas']:,}")
    c2.metric('Columnas', reporte['columnas'])
    c3.metric('Duplicados', f"{reporte['filas_duplicadas']} ({reporte['pct_duplicados']}%)")
    if reporte['nulos']:
        with st.expander(f'Valores nulos ({len(reporte["nulos"])} columnas)'):
            for col, info in sorted(reporte['nulos'].items(), key=lambda x: -x[1]['porcentaje']):
                st.markdown(f'`{col}`: {info["cantidad"]:,} ({info["porcentaje"]}%)')


def limpiar_texto_colombia(texto):
    m = {
        'Archipiã\x89Lago De San Andrã\x89S, Providencia Y Santa Catalina': 'San Andrés y Providencia',
        'Atlã\x81Ntico': 'Atlántico',
        'Bogotã\x81, D.C.': 'Bogotá',
        'Bolã\x8dVar': 'Bolívar',
        'Boyacã\x81': 'Boyacá',
        'Caquetã\x81': 'Caquetá',
        'Chocã\x93': 'Chocó',
        'Cã\x93Rdoba': 'Córdoba',
        'Guainã\x8dA': 'Guainía',
        'Nariã\x91O': 'Nariño',
        'Quindã\x8dO': 'Quindío',
        'Vaupã\x89S': 'Vaupés',
        'Cã\x93Rdoba': 'Córdoba',
    }
    return m.get(texto, limpiar_mojibake(texto))
