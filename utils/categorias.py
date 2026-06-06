import pandas as pd
import json
import os

# ============================================================
# NOMBRES INTERNOS (desde el modelo entrenado — coinciden exactamente)
# ============================================================
DEPTOS_INTERNOS = [
    'Antioquia', 'Arauca',
    'ArchipiÃ©Lago De San AndrÃ©S, Providencia Y Santa Catalina',
    'AtlÃ¡Ntico', 'BogotÃ¡, D.C.', 'BolÃ­Var', 'BoyacÃ¡',
    'Caldas', 'CaquetÃ¡', 'Casanare', 'Cauca', 'Cesar',
    'ChocÃ³', 'Cundinamarca', 'CÃ³Rdoba', 'GuainÃ­A',
    'Guaviare', 'Huila', 'La Guajira', 'Magdalena', 'Meta',
    'NariÃ±O', 'Norte De Santander', 'Putumayo', 'QuindÃ­O',
    'Risaralda', 'Santander', 'Sucre', 'Tolima', 'Valle Del Cauca',
    'VaupÃ©S', 'Vichada'
]

CULTIVOS_INTERNOS = [
    'Acacia', 'Acelga', 'Achiote', 'Achira', 'Agraz', 'Aguacate', 'Ahuyama',
    'Aji', 'Ajo', 'Ajonjoli', 'Albahaca', 'Alcachofa', 'Alfalfa', 'AlgodÃ³N',
    'Aliso', 'Anturio', 'AnÃ³N', 'Apio', 'Apio De Monte', 'ArazÃ¡',
    'Arbol Del Pan', 'AromÃ¡Ticas', 'Arracacha', 'ArrayÃ¡N', 'Arroz',
    'Arveja', 'ArÃ¡Ndano', 'Asai', 'Aster', 'Avena', 'Avena Cayuse',
    'Badea', 'BalÃº', 'Bananito', 'Banano', 'Banco De Proteina Forrajero',
    'Batata', 'Berenjena', 'Bijao', 'Bijas', 'BorojÃ³', 'Boton De Oro',
    'BotÃ³N De Oro', 'Brevo', 'Brillantina', 'BrÃ³Coli', 'Cacao', 'Cacay',
    'Caducifolios', 'CafÃ©', 'CalabacÃ­N', 'Calabaza', 'Calas', 'CalÃ©Ndula',
    'Camu Camu', 'Cannabis', 'Carambolo', 'Cardamomo', 'Caucho', 'CaÃ±A',
    'CaÃ±A Azucarera', 'CaÃ±A Forrajera', 'CaÃ±A Panelera', 'CaÃ±Amo',
    'Cebada', 'Cebolla', 'Cebolla De Bulbo', 'Cebolla De Rama', 'Cebolla Puerro',
    'CebollÃ­N', 'Cedro', 'Cedro Nogal', 'Ceiba', 'Chirimoya', 'Chisgua',
    'Cholupa', 'Chontaduro', 'ChÃ­A', 'CidrÃ³N', 'Cilantro', 'Ciruela',
    'Clavel', 'Cocculus', 'Cocona', 'Coliflor', 'Copoazu', 'Crisantemo',
    'Cubios', 'Curuba', 'CÃ­Tricos', 'CÃºrcuma', 'Durazno', 'Epifitas',
    'Esparrago', 'Espinaca', 'Estevia', 'EstragÃ³N', 'Estropajo', 'Eucalipto',
    'Eucalipto Baby Blue', 'Feijoa', 'Fique', 'Flor De Jamaica', 'Flores',
    'Follajes', 'Forestales', 'Forestales Nativos', 'Frambuesa', 'Fresa',
    'Frijol', 'Frutales Varios', 'Girasol', 'Gmelina Arborea', 'Granada',
    'Granadilla', 'Guaba', 'Guadua', 'Guamo', 'Guandul', 'GuanÃ¡Bana',
    'Guatila', 'Guayaba', 'Guisantes', 'Gulupa', 'Haba', 'Habichuela',
    'Helecho', 'Hierbabuena', 'Higo', 'Higuerilla', 'HipÃ©Rico',
    'Hortalizas Varias', 'Hortensias', 'Iraca', 'Jatropha', 'Jengibre',
    'Kiwi', 'Laurel', 'Lechuga', 'Leucaena', 'Lima', 'Limonaria', 'LimÃ³N',
    'Lulo', 'Macadamia', 'Maderable', 'Malanga', 'Mandarina', 'Mango',
    'Mangostino', 'Manzana', 'ManÃ­', 'ManÃ­ Forrajero', 'MaracuyÃ¡',
    'MaraÃ±Ã³N', 'Matarraton', 'MaÃ­Z', 'MaÃ­Z Forrajero', 'MelÃ³N',
    'Mezcla De Pastos', 'Millo', 'Mora', 'Morera', 'Moringa', 'MortiÃ±O',
    'Mostaza', 'Nabo', 'Naranja', 'Neem', 'Nopal', 'NÃ­Spero', 'Olivo',
    'OrÃ©Gano', 'Pachira Quinata', 'Palma', 'Palma Amarga', 'Palma De Aceite',
    'Palma De Coco', 'Palma Robelina', 'Palmito', 'Pancojer', 'Papa',
    'Papa Criolla', 'Papa De AÃ±O', 'Papaya', 'Papayuela', 'Pasifloras',
    'Pasto', 'Pasto Angleton', 'Pasto Azul Orchoro', 'Pasto Brachiaria',
    'Pasto Brizantha', 'Pasto Buffel', 'Pasto Carimagua', 'Pasto Climacuna',
    'Pasto Colosuana', 'Pasto Cuba 22', 'Pasto Cynodon', 'Pasto Elefante',
    'Pasto Estrella', 'Pasto Falsa Poa', 'Pasto Guinea', 'Pasto Imperial',
    'Pasto Kikuyo', 'Pasto Kingrass', 'Pasto Llanero', 'Pasto Maralfalfa',
    'Pasto Mombaza', 'Pasto Mulato', 'Pasto ParÃ¡', 'Pasto Paspalum',
    'Pasto Puntero', 'Pasto Ryegrass', 'Pasto Toledo', 'Pastos', 'Patilla',
    'Paulownia', 'Pendiente', 'Pepino', 'Pera', 'PimentÃ³N', 'Pimienta',
    'Pino', 'Pitahaya', 'PiÃ±A', 'Plantas AromÃ¡Ticas',
    'Plantas AromÃ¡Ticas Y Medicinales', 'Plantas Medicinales',
    'Plantas Nativas', 'PlÃ¡Tano', 'Pomelo', 'PompÃ³N', 'Proteas',
    'Quinua', 'Rambutan', 'Remolacha', 'Repollo', 'Roble', 'Romero',
    'Rosa', 'Ruda', 'Ruscus', 'Sacha Inchi', 'Sagu', 'Saman',
    'Silvopastoril', 'SnapdragÃ³N', 'Solidago', 'Sorgo', 'Sorgo Forrajero',
    'Soya', 'Stevia', 'SÃ¡Bila', 'Tabaco', 'Tabaco Negro', 'Tamarindo',
    'Tangare', 'Tangelo', 'Teca', 'Tomate', 'Tomate De Arbol',
    'Tomate De ÃRbol', 'Tomillo', 'Toronjil', 'Totumo', 'Trebol',
    'Trigo', 'TrÃ©Bol', 'Uchuva', 'Uva', 'Uva Caimarona', 'Vainilla',
    'Veranera', 'Yopo', 'Yuca', 'Zamia', 'Zanahoria', 'Zapote', 'Ã‘Ame'
]

TOPOGRAFIAS_INTERNAS = [
    'Ligeramente Ondulado', 'Moderadamente Ondulado', 'Ondulado',
    'Ondulado Y Pendiente', 'Pendiente', 'Pendiente Fuerte',
    'Pendiente Leve', 'Pendiente Moderada', 'Plano',
    'Plano Y Ondulado', 'Plano Y Pendiente'
]

DRENAJES_INTERNOS = [
    'Mal Drenaje', 'Muy Buen Drenaje', 'Muy Mal Drenaje', 'Regular Drenaje'
]

RIEGOS_INTERNOS = [
    'AspersiÃ³N - Goteo', 'AspersiÃ³N - Manguera', 'CaÃ±On',
    'Fertirriego', 'Goteo', 'Goteo - Gravedad', 'Gravedad',
    'Manguera', 'No Tiene', 'Por InundaciÃ³N', 'Superficial',
    'Superficial - Goteo', 'Superficial - InundaciÃ³N',
    'Superficial-AspersiÃ³N'
]

# ============================================================
# NOMBRES DE VISUALIZACION (con tildes correctas para mostrar)
# ============================================================
DEPTOS = [
    'Antioquia', 'Arauca', 'San Andrés y Providencia',
    'Atlántico', 'Bogotá', 'Bolívar', 'Boyacá',
    'Caldas', 'Caquetá', 'Casanare', 'Cauca', 'Cesar',
    'Chocó', 'Cundinamarca', 'Córdoba', 'Guainía',
    'Guaviare', 'Huila', 'La Guajira', 'Magdalena', 'Meta',
    'Nariño', 'Norte de Santander', 'Putumayo', 'Quindío',
    'Risaralda', 'Santander', 'Sucre', 'Tolima', 'Valle del Cauca',
    'Vaupés', 'Vichada'
]

CULTIVOS = sorted([
    'Aguacate', 'Ajo', 'Algodón', 'Almendra', 'Arracacha', 'Arroz', 'Arveja',
    'Auyama', 'Batata', 'Borojo', 'Botón de Oro', 'Brevo', 'Cacao', 'Café',
    'Caña de Azúcar', 'Caña Panelera', 'Cebada', 'Cebolla', 'Cebolla Cabezona',
    'Cebolla Larga', 'Cilantro', 'Ciruela', 'Coco', 'Col', 'Coliflor',
    'Chile', 'Chontaduro', 'Curuba', 'Durazno', 'Espinaca', 'Feijoa', 'Fique',
    'Fresa', 'Frijol', 'Frutales', 'Granadilla', 'Guanábana', 'Guayaba',
    'Guineo', 'Habichuela', 'Higo', 'Hortalizas', 'Iraca', 'Lechuga',
    'Limón', 'Lulo', 'Macadamia', 'Maíz', 'Mandarina', 'Mango', 'Manzana',
    'Maracuyá', 'Millo', 'Mora', 'Mostaza', 'Naranja', 'Níspero',
    'Papa', 'Papa Criolla', 'Papaya', 'Pastos', 'Pera', 'Perejil',
    'Pimentón', 'Piña', 'Plátano', 'Policultivos', 'Remolacha', 'Repollo',
    'Rosas', 'Rye Grass', 'Sábila', 'Sacha Inchi', 'Sorgo', 'Soya',
    'Tabaco', 'Tangelo', 'Tomate', 'Tomate de Árbol', 'Trigo',
    'Uchuva', 'Uva', 'Yuca', 'Zanahoria', 'Zapallo'
])

TOPOGRAFIAS = ['Plano', 'Ondulado', 'Pendiente', 'Plano-Ondulado', 'Ondulado-Pendiente',
               'Plano-Inundable', 'Terrazas', 'Colinas', 'Montañoso', 'Valle', 'Escarpado']

DRENAJES = ['Buen Drenaje', 'Mal Drenaje', 'Muy Buen Drenaje', 'Muy Mal Drenaje', 'Regular Drenaje']

RIEGOS = ['Gravedad', 'Goteo', 'Aspersión', 'No Tiene', 'Riego por Surcos',
          'Riego por Inundación', 'Microaspersión', 'Riego por Goteo', 'Riego por Aspersión',
          'Riego Manual', 'Riego por Surcos y Gravedad', 'Riego por Inundación y Surcos',
          'Riego por Goteo y Aspersión', 'No Aplica']

# ============================================================
# MAPEO: display -> interno (para predicción con el modelo)
# ============================================================
# MAPEO EXPLICITO: display (con tildes) -> interno (del modelo)
# ============================================================
DISP_A_INTERNO_DEPTO = {
    'Antioquia': 'Antioquia',
    'Arauca': 'Arauca',
    'San Andrés y Providencia': 'ArchipiÃ©Lago De San AndrÃ©S, Providencia Y Santa Catalina',
    'Atlántico': 'AtlÃ¡Ntico',
    'Bogotá': 'BogotÃ¡, D.C.',
    'Bolívar': 'BolÃ­Var',
    'Boyacá': 'BoyacÃ¡',
    'Caldas': 'Caldas',
    'Caquetá': 'CaquetÃ¡',
    'Casanare': 'Casanare',
    'Cauca': 'Cauca',
    'Cesar': 'Cesar',
    'Chocó': 'ChocÃ³',
    'Cundinamarca': 'Cundinamarca',
    'Córdoba': 'CÃ³Rdoba',
    'Guainía': 'GuainÃ­A',
    'Guaviare': 'Guaviare',
    'Huila': 'Huila',
    'La Guajira': 'La Guajira',
    'Magdalena': 'Magdalena',
    'Meta': 'Meta',
    'Nariño': 'NariÃ±O',
    'Norte de Santander': 'Norte De Santander',
    'Putumayo': 'Putumayo',
    'Quindío': 'QuindÃ­O',
    'Risaralda': 'Risaralda',
    'Santander': 'Santander',
    'Sucre': 'Sucre',
    'Tolima': 'Tolima',
    'Valle del Cauca': 'Valle Del Cauca',
    'Vaupés': 'VaupÃ©S',
    'Vichada': 'Vichada'
}

DISP_A_INTERNO_CULTIVO = {
    'Aguacate': 'Aguacate', 'Ajo': 'Ajo', 'Algodón': 'AlgodÃ³N',
    'Almendra': 'Almendra', 'Arracacha': 'Arracacha', 'Arroz': 'Arroz',
    'Arveja': 'Arveja', 'Auyama': 'Ahuyama', 'Batata': 'Batata',
    'Borojo': 'BorojÃ³', 'Botón de Oro': 'BotÃ³N De Oro',
    'Brevo': 'Brevo', 'Cacao': 'Cacao', 'Café': 'CafÃ©',
    'Caña de Azúcar': 'CaÃ±A Azucarera', 'Caña Panelera': 'CaÃ±A Panelera',
    'Cebada': 'Cebada', 'Cebolla': 'Cebolla',
    'Cebolla Cabezona': 'Cebolla De Bulbo', 'Cebolla Larga': 'Cebolla De Rama',
    'Cilantro': 'Cilantro', 'Ciruela': 'Ciruela', 'Coco': 'Coco',
    'Col': 'Col', 'Coliflor': 'Coliflor',
    'Chile': 'Chile', 'Chontaduro': 'Chontaduro', 'Curuba': 'Curuba',
    'Durazno': 'Durazno', 'Espinaca': 'Espinaca', 'Feijoa': 'Feijoa',
    'Fique': 'Fique', 'Fresa': 'Fresa', 'Frijol': 'Frijol',
    'Frutales': 'Frutales Varios', 'Granadilla': 'Granadilla',
    'Guanábana': 'GuanÃ¡Bana', 'Guayaba': 'Guayaba', 'Guineo': 'Guineo',
    'Habichuela': 'Habichuela', 'Higo': 'Higo', 'Hortalizas': 'Hortalizas Varias',
    'Iraca': 'Iraca', 'Lechuga': 'Lechuga', 'Limón': 'LimÃ³N',
    'Lulo': 'Lulo', 'Macadamia': 'Macadamia', 'Maíz': 'MaÃ­Z',
    'Mandarina': 'Mandarina', 'Mango': 'Mango', 'Manzana': 'Manzana',
    'Maracuyá': 'MaracuyÃ¡', 'Millo': 'Millo', 'Mora': 'Mora',
    'Mostaza': 'Mostaza', 'Naranja': 'Naranja', 'Níspero': 'NÃ­Spero',
    'Papa': 'Papa', 'Papa Criolla': 'Papa Criolla', 'Papaya': 'Papaya',
    'Pastos': 'Pastos', 'Pera': 'Pera', 'Perejil': 'Perejil',
    'Pimentón': 'PimentÃ³N', 'Piña': 'PiÃ±A', 'Plátano': 'PlÃ¡Tano',
    'Policultivos': 'Policultivos', 'Remolacha': 'Remolacha',
    'Repollo': 'Repollo', 'Rosas': 'Rosa', 'Rye Grass': 'Pasto Ryegrass',
    'Sábila': 'SÃ¡Bila', 'Sacha Inchi': 'Sacha Inchi', 'Sorgo': 'Sorgo',
    'Soya': 'Soya', 'Tabaco': 'Tabaco', 'Tangelo': 'Tangelo',
    'Tomate': 'Tomate', 'Tomate de Árbol': 'Tomate De Ã�Rbol',
    'Trigo': 'Trigo', 'Uchuva': 'Uchuva', 'Uva': 'Uva',
    'Yuca': 'Yuca', 'Zanahoria': 'Zanahoria', 'Zapallo': 'Zapote'
}

DISP_A_INTERNO_TOPOGRAFIA = {
    'Plano': 'Plano',
    'Ondulado': 'Ondulado',
    'Pendiente': 'Pendiente',
    'Plano-Ondulado': 'Plano Y Ondulado',
    'Ondulado-Pendiente': 'Ondulado Y Pendiente',
    'Plano-Inundable': 'Plano',
    'Terrazas': 'Plano',
    'Colinas': 'Ligeramente Ondulado',
    'Montañoso': 'Pendiente Fuerte',
    'Valle': 'Plano',
    'Escarpado': 'Pendiente Fuerte'
}

DISP_A_INTERNO_DRENAJE = {
    'Buen Drenaje': 'Regular Drenaje',
    'Mal Drenaje': 'Mal Drenaje',
    'Muy Buen Drenaje': 'Muy Buen Drenaje',
    'Muy Mal Drenaje': 'Muy Mal Drenaje',
    'Regular Drenaje': 'Regular Drenaje'
}

DISP_A_INTERNO_RIEGO = {
    'Gravedad': 'Gravedad',
    'Goteo': 'Goteo',
    'Aspersión': 'AspersiÃ³N - Goteo',
    'No Tiene': 'No Tiene',
    'Riego por Surcos': 'Superficial',
    'Riego por Inundación': 'Por InundaciÃ³N',
    'Microaspersión': 'AspersiÃ³N - Goteo',
    'Riego por Goteo': 'Goteo',
    'Riego por Aspersión': 'AspersiÃ³N - Goteo',
    'Riego Manual': 'Manguera',
    'Riego por Surcos y Gravedad': 'Superficial - Goteo',
    'Riego por Inundación y Surcos': 'Superficial - InundaciÃ³N',
    'Riego por Goteo y Aspersión': 'AspersiÃ³N - Goteo',
    'No Aplica': 'No Tiene'
}

FEATURES_NUM = ['pH', 'MO', 'fosforo', 'azufre', 'calcio', 'magnesio', 'potasio', 'CIC', 'CE', 'anios_est']

LABELS_CALIDAD = ['Baja', 'Media', 'Buena', 'Excelente']

RANGOS_NUTRIENTES = {
    'pH': {'bajo': 5.5, 'alto': 7.0, 'unidad': '', 'nombre': 'pH del suelo'},
    'MO': {'bajo': 3.0, 'alto': 10.0, 'unidad': '%', 'nombre': 'Materia Orgánica'},
    'fosforo': {'bajo': 10.0, 'alto': 40.0, 'unidad': 'ppm', 'nombre': 'Fósforo (P)'},
    'azufre': {'bajo': 8.0, 'alto': 20.0, 'unidad': 'ppm', 'nombre': 'Azufre (S)'},
    'calcio': {'bajo': 2.0, 'alto': 8.0, 'unidad': 'cmol/kg', 'nombre': 'Calcio (Ca)'},
    'magnesio': {'bajo': 1.0, 'alto': 2.0, 'unidad': 'cmol/kg', 'nombre': 'Magnesio (Mg)'},
    'potasio': {'bajo': 0.15, 'alto': 0.5, 'unidad': 'cmol/kg', 'nombre': 'Potasio (K)'},
    'CIC': {'bajo': 5.0, 'alto': 15.0, 'unidad': 'cmol/kg', 'nombre': 'CIC'},
    'CE': {'bajo': 0.0, 'alto': 1.0, 'unidad': 'dS/m', 'nombre': 'CE'}
}

MUNICIPIOS_INTERNOS = {
    'Antioquia': ['Medellín', 'Rionegro', 'Apartadó', 'Turbo', 'Santa Fe de Antioquia', 'La Ceja', 'Jardín', 'Guarne', 'Envigado', 'Itagüí', 'Bello', 'San Pedro de los Milagros', 'Marinilla', 'El Carmen de Viboral'],
    'Arauca': ['Arauca', 'Saravena', 'Tame', 'Puerto Rondón', 'Fortul', 'Cravo Norte', 'Arauquita'],
    'San Andrés y Providencia': ['San Andrés', 'Providencia', 'Santa Catalina'],
    'Atlántico': ['Barranquilla', 'Soledad', 'Malambo', 'Puerto Colombia', 'Baranoa', 'Sabanalarga', 'Luruaco', 'Repelón', 'Juan de Acosta', 'Santo Tomás', 'Polonuevo'],
    'Bogotá': ['Bogotá'],
    'Bolívar': ['Cartagena', 'Magangué', 'El Carmen de Bolívar', 'Sincelejo', 'San Pablo', 'Santa Rosa del Sur', 'Montecristo', 'Tiquisio', 'Arenal del Sur'],
    'Boyacá': ['Tunja', 'Duitama', 'Sogamoso', 'Paipa', 'Chiquinquirá', 'Sáchica', 'Villa de Leyva', 'Sutamarchán', 'Ramiriquí', 'Miraflores', 'Soatá'],
    'Caldas': ['Manizales', 'Chinchiná', 'Riosucio', 'Anserma', 'Salamina', 'Aguadas', 'Palestina', 'Neira', 'Villamaría', 'Supía', 'La Dorada'],
    'Caquetá': ['Florencia', 'San Vicente del Caguán', 'Cartagena del Chairá', 'Puerto Rico', 'La Montañita', 'El Paujil', 'San José del Fragua', 'Albania', 'Curillo', 'Valparaíso'],
    'Casanare': ['Yopal', 'Aguazul', 'Tauramena', 'Villanueva', 'Paz de Ariporo', 'Monterrey', 'Maní', 'Orocué', 'Trinidad', 'San Luis de Palenque'],
    'Cauca': ['Popayán', 'Santander de Quilichao', 'Puerto Tejada', 'El Bordo', 'Caloto', 'Corinto', 'Miranda', 'Cajibío', 'Silvia', 'Páez', 'Timbío', 'Buenos Aires'],
    'Cesar': ['Valledupar', 'Aguachica', 'Codazzi', 'La Paz', 'San Diego', 'Bosconia', 'Chiriguaná', 'El Copey', 'Becerril', 'Río de Oro', 'Gamarra'],
    'Chocó': ['Quibdó', 'Istmina', 'Tadó', 'Condoto', 'San José del Palmar', 'Bahía Solano', 'Nuquí', 'Juradó', 'Riosucio', 'El Cantón de San Pablo'],
    'Córdoba': ['Montería', 'Cereté', 'Sahagún', 'Lorica', 'Tierralta', 'Planeta Rica', 'Ciénaga de Oro', 'San Pelayo', 'Montelíbano', 'Purísima', 'San Antero'],
    'Cundinamarca': ['Bogotá', 'Soacha', 'Facatativá', 'Zipaquirá', 'Chía', 'Cajicá', 'Madrid', 'Mosquera', 'Fusagasugá', 'Girardot', 'Ubaté', 'Villeta', 'La Mesa', 'Sibaté', 'Tabio', 'Tocancipá'],
    'Guainía': ['Inírida', 'Barranco Minas', 'Mapiripana', 'San Felipe', 'Cacahual', 'La Guadalupe'],
    'Guaviare': ['San José del Guaviare', 'El Retorno', 'Calamar', 'Miraflores'],
    'Huila': ['Neiva', 'Pitalito', 'La Plata', 'Garzón', 'Campoalegre', 'San Agustín', 'Isnos', 'Palestina', 'Gigante', 'Aipe', 'Villavieja', 'Tello', 'Santa María'],
    'La Guajira': ['Riohacha', 'Maicao', 'Uribia', 'San Juan del Cesar', 'Fonseca', 'Barrancas', 'Dibulla', 'Distracción', 'Albania', 'Hatonuevo'],
    'Magdalena': ['Santa Marta', 'Ciénaga', 'Fundación', 'El Banco', 'Plato', 'Aracataca', 'Algarrobo', 'Pivijay', 'Chivolo', 'Remolino', 'San Zenón'],
    'Meta': ['Villavicencio', 'Acacías', 'Granada', 'Puerto López', 'San Martín', 'Restrepo', 'Cumaral', 'La Macarena', 'Puerto Gaitán', 'Cabuyaro', 'Mapiripán', 'Vista Hermosa'],
    'Nariño': ['Pasto', 'Tumaco', 'Ipiales', 'Barbacoas', 'Túquerres', 'La Unión', 'Sandoná', 'El Charco', 'Olaya Herrera', 'Francisco Pizarro'],
    'Norte de Santander': ['Cúcuta', 'Ocaña', 'Pamplona', 'Los Patios', 'Villa del Rosario', 'Chinácota', 'Ábrego', 'El Zulia', 'Sardinata'],
    'Putumayo': ['Mocoa', 'Puerto Asís', 'Orito', 'Valle del Guamuez', 'San Miguel', 'Puerto Caicedo', 'Sibundoy', 'Colón', 'Santiago', 'Villagarzón'],
    'Quindío': ['Armenia', 'Calarcá', 'Montenegro', 'La Tebaida', 'Quimbaya', 'Salento', 'Filandia', 'Buenavista', 'Pijao', 'Córdoba', 'Circasia'],
    'Risaralda': ['Pereira', 'Dosquebradas', 'Santa Rosa de Cabal', 'La Virginia', 'Marsella', 'Quinchía', 'Belén de Umbría', 'Apía', 'Santuario', 'Pueblo Rico'],
    'Santander': ['Bucaramanga', 'Barrancabermeja', 'San Gil', 'Socorro', 'Piedecuesta', 'Floridablanca', 'Girón', 'Lebrija', 'Barbosa', 'Puente Nacional', 'Vélez', 'Oiba', 'Málaga'],
    'Sucre': ['Sincelejo', 'Corozal', 'Tolú', 'San Marcos', 'San Benito Abad', 'Sampués', 'Ovejas', 'Morroa', 'Coveñas', 'San Antonio de Palmito'],
    'Tolima': ['Ibagué', 'Espinal', 'Honda', 'Melgar', 'Mariquita', 'Chaparral', 'Líbano', 'Rovira', 'Saldaña', 'Purificación', 'Flandes', 'San Luis', 'Planadas'],
    'Valle del Cauca': ['Cali', 'Buenaventura', 'Palmira', 'Tuluá', 'Cartago', 'Buga', 'Yumbo', 'Jamundí', 'Roldanillo', 'Caicedonia', 'Sevilla', 'Zarzal', 'El Cerrito', 'Ansermanuevo', 'La Unión', 'Tororó'],
    'Vaupés': ['Mitú', 'Taraira', 'Papunahua', 'Carurú', 'Pacoa', 'Yavaraté'],
    'Vichada': ['Puerto Carreño', 'Cumaribo', 'La Primavera', 'Santa Rosalía']
}

COL_NAMES = ['id', 'fecha', 'depto', 'municipio', 'cultivo', 'estado',
             'tiempo_est', 'topografia', 'drenaje', 'riego', 'fertilizantes',
             'pH', 'MO', 'fosforo', 'azufre', 'acidez', 'aluminio',
             'calcio', 'magnesio', 'potasio', 'sodio', 'CIC', 'CE',
             'Fe_olsen', 'Cu', 'Mn_olsen', 'Zn_olsen', 'B',
             'Fe_doble', 'Cu_doble', 'Mn_doble', 'Zn_doble']


def display_a_interno(categoria, valor_display):
    mapa = {
        'depto': DISP_A_INTERNO_DEPTO,
        'cultivo': DISP_A_INTERNO_CULTIVO,
        'topografia': DISP_A_INTERNO_TOPOGRAFIA,
        'drenaje': DISP_A_INTERNO_DRENAJE,
        'riego': DISP_A_INTERNO_RIEGO
    }
    m = mapa.get(categoria, {})
    return m.get(valor_display, valor_display)


def cargar_municipios_por_depto(models_path=None):
    if models_path is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_path = os.path.join(base, 'models')
    json_path = os.path.join(models_path, 'depto_municipios.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        resultado = {}
        for k, v in data.items():
            k_clean = k.strip().title()
            for d in DEPTOS:
                if d.lower().replace('í', 'i').replace('é', 'e') in k_clean.lower() or k_clean.lower() in d.lower().replace('í', 'i').replace('é', 'e').replace('á', 'a').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n'):
                    resultado[d] = sorted(v)
                    break
            else:
                resultado[k_clean] = sorted(v)
        return resultado
    return MUNICIPIOS_INTERNOS


def obtener_municipios(depto, municipios_por_depto=None):
    if municipios_por_depto is None:
        municipios_por_depto = MUNICIPIOS_INTERNOS
    return municipios_por_depto.get(depto, [])


def obtener_categorias_originales():
    df = pd.read_csv(
        r'C:\Users\ivanq\Desktop\Talento tech\trabajo final\Resultados_de_Análisis_de_Laboratorio_Suelos_en_Colombia_20260526.csv',
        encoding='utf-8', nrows=0
    )
    return list(df.columns)
