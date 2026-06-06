from utils.categorias import RANGOS_NUTRIENTES, LABELS_CALIDAD


RECOMENDACIONES = {
    'pH': {
        'bajo': 'Aplicar cal dolomita (2-4 ton/ha) para elevar el pH. Realizar encalado 60-90 días antes de la siembra.',
        'alto': 'Aplicar azufre elemental (500-1000 kg/ha) o materia orgánica ácida para reducir el pH.',
        'optimo': 'pH en rango óptimo. Mantener prácticas actuales de encalado.'
    },
    'MO': {
        'bajo': 'Incorporar compost, gallinaza o abonos verdes (5-10 ton/ha/año). Rotar con cultivos de cobertura.',
        'alto': 'Excelente nivel de materia orgánica. Mantener prácticas de conservación.',
        'optimo': 'Nivel adecuado. Continuar con aportes anuales de materia orgánica.'
    },
    'fosforo': {
        'bajo': 'Aplicar DAP (150-250 kg/ha) o roca fosfórica (300-500 kg/ha). Realizar aplicación localizada.',
        'alto': 'Nivel alto de fósforo. Evitar fertilización fosfórada temporalmente.',
        'optimo': 'Fósforo en nivel adecuado. Mantener fertilización de mantenimiento (50-80 kg/ha P2O5).'
    },
    'azufre': {
        'bajo': 'Aplicar sulfato de amonio (100-200 kg/ha) o yeso agrícola (200-400 kg/ha).',
        'alto': 'Nivel adecuado. No requiere aplicación adicional de azufre.',
        'optimo': 'Azufre en nivel óptimo.'
    },
    'calcio': {
        'bajo': 'Aplicar yeso agrícola (500-1000 kg/ha) o cal dolomita (2-3 ton/ha).',
        'alto': 'Nivel alto. Evitar aplicaciones cálcicas. Revisar relación Ca/Mg.',
        'optimo': 'Calcio en nivel adecuado.'
    },
    'magnesio': {
        'bajo': 'Aplicar sulfato de magnesio (100-200 kg/ha) o cal dolomita (1-2 ton/ha).',
        'alto': 'Nivel alto. Verificar relación Ca/Mg para evitar desbalances.',
        'optimo': 'Magnesio en nivel óptimo.'
    },
    'potasio': {
        'bajo': 'Aplicar KCl (150-300 kg/ha) o sulfato de potasio (200-350 kg/ha). Fraccionar en 2-3 aplicaciones.',
        'alto': 'Nivel alto. Reducir o eliminar fertilización potásica temporalmente.',
        'optimo': 'Potasio en nivel adecuado. Mantener fertilización de mantenimiento.'
    },
    'CIC': {
        'bajo': 'Incrementar materia orgánica (5-10 ton/ha/año). En suelos arenosos, aplicar arcilla o zeolitas.',
        'alto': 'Excelente capacidad de intercambio catiónico.',
        'optimo': 'CIC en buen nivel.'
    },
    'CE': {
        'bajo': 'Nivel de salinidad óptimo.',
        'alto': 'Riesgo de salinidad. Aplicar lavado de suelos con agua de baja salinidad. Usar materia orgánica.',
        'optimo': 'CE en rango óptimo para la mayoría de cultivos.'
    }
}


def generar_recomendaciones(inputs):
    recs = []
    for nutriente, rangos in RANGOS_NUTRIENTES.items():
        valor = inputs.get(nutriente)
        if valor is None or valor == 0:
            continue
        nombre = rangos['nombre']
        if valor < rangos['bajo']:
            estado = 'bajo'
        elif valor > rangos['alto'] and nutriente not in ['CE']:
            estado = 'alto'
        elif nutriente == 'CE' and valor > rangos['alto']:
            estado = 'alto'
        else:
            estado = 'optimo'

        if nutriente in RECOMENDACIONES:
            rec = RECOMENDACIONES[nutriente].get(estado, '')
            if rec:
                recs.append((nombre, valor, rangos['unidad'], estado, rec))
    return recs


def recomendar_cultivo(calidad):
    mapa = {
        'Excelente': 'Aguacate Hass, Café Especial, Cacao Fino, Frutales de Alto Valor',
        'Buena': 'Café, Cacao, Plátano, Cítricos, Aguacate, Tomate, Maíz',
        'Media': 'Maíz, Yuca, Sorgo, Fríjol, Pastos, Caña Panelera',
        'Baja': 'Pastos Mejorados, Yuca Industrial, Sorgo, Especies Forestales Resistentes'
    }
    return mapa.get(calidad, 'Cultivos adaptables según análisis complementario')
