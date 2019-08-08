import random
import string
import pandas as pd
import uuid
import os
import git
import urllib.request
import json
from faker import Faker


fake = Faker('es_MX')

# nombres y apellidos
hombres = pd.read_csv('./corpus/hombres.csv')
hombres = hombres.values
mujeres = pd.read_csv('./corpus/mujeres.csv')
mujeres = mujeres.values
apellidos = pd.read_csv('./corpus/apellidos-20.csv')
apellidos = apellidos.values

# descarga los catálogos
#if not os.path.isdir('./catalogos'):
#    print('Descargando repositorio de catálogos...')
#    git.Git('.').clone('https://github.com/PDNMX/catalogos.git')
#    print('Listo!')

# (https://www.inegi.org.mx/app/ageeml/)
#if not os.path.isfile('./catun_localidad.xlsx'):
#    print('Descargando catálogo de localidades...')
#    urllib.request.urlretrieve('https://www.inegi.org.mx/contenidos/app/ageeml/catuni/loc_mincona/catun_localidad.xlsx',
#                               './catun_localidad.xlsx')
#    print('Listo!')

catun = pd.read_excel('./catun_localidad.xlsx', header=3)

# Marco Geoestadístico (https://www.inegi.org.mx/app/ageeml/)


def get_id():
    return str(uuid.uuid1())


def rand_bool():
    return random.choice([True, False])


def get_name():
    gender = random.choice(['F', 'M'])

    name = random.choice(hombres) if gender is 'M' else\
        random.choice(mujeres)
    name = str(name[0])
    return name


def get_last_name():
    apellido = random.choice(apellidos)
    apellido = str(apellido[0])
    return apellido


def get_email(domain):
    length = 12
    letters = string.ascii_lowercase
    user = ''.join(random.choice(letters) for i in range(length))
    return "{0}@{1}".format(user, domain)


def get_telephone(type):
    prefix = '+52' + ('1' if type == 'celular' else '')
    return prefix + str(random.randint(5500000000, 7779999999))


def get_bith_date():
    dia = (random.randint(1, 28))
    mes = (random.randint(1, 12))
    anio = (random.randint(1950, 1999))

    dia = "0{0}".format(dia) if dia < 10 else "{0}".format(dia)
    mes = "0{0}".format(mes) if mes < 10 else "{0}".format(mes)
    return "{0}-{1}-{2}".format(anio, mes, dia)


def get_college():

    colleges = [
        'Instituto Politécnico Nacional',
        'Instituto Tecnológico Autónomo de México',
        'Universidad Nacional Autónoma de México',
        'Universidad Iberoamericana',
        'Universidad de Guadalajara'
    ]

    return random.choice(colleges)


def get_amount(a, b):
    return round(random.uniform(a, b), 2)


def get_degree():
    degrees = [
        'Ingeniería en Sistemas Computacionales',
        'Licenciatura en Matemáticas Aplicadas',
        'Ingeniería en Computación',
        'Ingeniería en Comunicaciones y Electrónica',
        'Licenciatura en Derecho',
        'Licenciatura en Ciencias Políticas',
        'Licenciatura en Física',
        'Ingeniería Industrial',
        'Ingeniería Civil',
        "Licenciatura en Historia",
        "Licenciatura en Ciencias de la Comunicación",
        "Ingeniería Mecánica",
        "Ingeniería Petrolera",
        "Ingeniería en Telecomunicaciones",
        "Ingeniería Química"
    ]
    return random.choice(degrees)


def get_position():
    positions = [
        'Enlace de Alto Nivel de Responsabilidad',
        'Jefe de Departamento',
        'Subdirector de Area',
        'Director de Area',
        'Director General Adjunto',
        'Director General',
        'Titular de Unidad'
    ]
    return random.choice(positions)


def lorem_ipsum():
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."


def get_address():

    rows = len(catun)
    index = random.randint(0, rows - 1)
    loc = catun.iloc[index]

    return {
        "pais": {
            "valor": "MEXICO",
            "codigo": "MX"
        },
        "entidad_federativa": {
            "nom_agee":  loc['nom_ent'],
            "cve_agee":  str(loc['cve_ent'])
        },
        "municipio": {
            "nom_agem": loc['nom_mun'],
            "cve_agem": str(loc['cve_mun'])
        },
        "cp": "55018",
        "localidad": {
            "nom_loc": loc['nom_loc'],
            "cve_loc": str(loc['cve_loc'])
        },
        "asentamiento": {
            "cve_asen": 1,
            "nom_asen": "AGUA CLARA",
            "cve_tipo_asen": 16
        },
        "vialidad": {
            "tipo_vial": "CALLE",
            "nom_vial": fake.street_name()
        },
        "numExt": "24",
        "numInt": "48"
    }


def citizenship():
    countries = [
        {
            "valor": "Mexico",
            "codigo": "MX"
        },
        {
            "valor": "Australia",
            "codigo": "AU"
        },
        {
            "valor": "Bolivia",
            "codigo": "BO"
        },
        {
            "valor": "Brazil",
            "codigo": "BR"
        },
        {
            "valor": "Canada",
            "codigo": "CA"
        },
        {
            "valor": "Chile",
            "codigo": "CL"
        },
        {
            "valor": "China",
            "codigo": "CN"
        },
        {
            "valor": "Colombia",
            "codigo": "CO"
        },
        {
            "valor": "Cuba",
            "codigo": "CU"
        },
        {
            "valor": "Findland",
            "codigo": "FI"
        },
        {
            "valor":"Venezuela",
            "codigo":"VE"
        }
    ]

    c1 = random.choice(countries)
    c2 = random.choice(countries)

    return [c1, c2] if c1.get("codigo") != c2.get("codigo") else [c1]

institutions = [
    "ADMINISTRACION DEL PATRIMONIO DE LA BENEFICENCIA PUBLICA",
    "ADMINISTRACION FEDERAL DE SERVICIOS EDUCATIVOS EN EL DISTRITO FEDERAL",
    "ADMINISTRACION PORTUARIA INTEGRAL DE ALTAMIRA S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE COATZACOALCOS S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE DOS BOCAS S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE ENSENADA S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE GUAYMAS S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE LAZARO CARDENAS S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE MANZANILLO S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE MAZATLAN S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE PROGRESO S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE PUERTO MADERO, S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE PUERTO VALLARTA S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE SALINA CRUZ S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE TAMPICO S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE TOPOLOBAMPO S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE TUXPAN S.A. DE C.V.",
    "ADMINISTRACION PORTUARIA INTEGRAL DE VERACRUZ S.A. DE C.V.",
    "AEROPUERTO INTERNACIONAL DE LA CIUDAD DE MEXICO S.A. DE C.V.",
    "AEROPUERTOS Y SERVICIOS AUXILIARES",
    "AGENCIA ESPACIAL MEXICANA",
    "AGENCIA MEXICANA DE COOPERACIÓN INTERNACIONAL PARA EL DESARROLLO",
    "AGENCIA NACIONAL DE SEGURIDAD INDUSTRIAL Y DE PROTECCIÓN AL MEDIO AMBIENTE DEL SECTOR HIDROCARBUROS",
    "AGROASEMEX S.A.",
    "APOYOS Y SERVICIOS A LA COMERCIALIZACION AGROPECUARIA",
    "ARCHIVO GENERAL DE LA NACION",
    "AUTORIDAD FEDERAL PARA EL DESARROLLO DE LAS ZONAS ECONÓMICAS ESPECIALES",
    "BANCO DEL AHORRO NACIONAL Y SERVICIOS FINANCIEROS S N C",
    "BANCO NACIONAL DE COMERCIO EXTERIOR S.N.C.",
    "BANCO NACIONAL DE CREDITO RURAL S.N.C.",
    "BANCO NACIONAL DE OBRAS Y SERVICIOS PUBLICOS S.N.C.",
    "BANCO NACIONAL DEL EJERCITO FUERZA AEREA Y ARMADA S.N.C.",
    "CAMINOS Y PUENTES FEDERALES DE INGRESOS Y SERVICIOS CONEXOS",
    "CASA DE MONEDA DE MEXICO",
    "CENTRO DE CAPACITACION CINEMATOGRAFICA A.C.",
    "CENTRO DE ENSEÑANZA TECNICA INDUSTRIAL.",
    "CENTRO DE ESTUDIOS SUPERIORES EN TURISMO",
    "CENTRO DE EVALUACION Y DESARROLLO HUMANO",
    "CENTRO DE INGENIERIA Y DESARROLLO INDUSTRIAL",
    "CENTRO DE INVESTIGACION CIENTIFICA DE YUCATAN A.C.",
    "CENTRO DE INVESTIGACION CIENTIFICA Y DE EDUCACION SUPERIOR DE ENSENADA B.C.",
    "CENTRO DE INVESTIGACION EN ALIMENTACION Y DESARROLLO A.C.",
    "CENTRO DE INVESTIGACION EN GEOGRAFIA Y GEOMATICA ING. JORGE L. TAMAYO A.C.",
    "CENTRO DE INVESTIGACION EN MATEMATICAS A.C.",
    "CENTRO DE INVESTIGACION EN MATERIALES AVANZADOS S.C.",
    "CENTRO DE INVESTIGACION EN QUIMICA APLICADA",
    "CENTRO DE INVESTIGACION Y ASISTENCIA EN TECNOLOGIA Y DISEÑO DEL ESTADO DE JALISCO A.C.",
    "CENTRO DE INVESTIGACION Y DE ESTUDIOS AVANZADOS DEL INSTITUTO POLITECNICO NACIONAL",
    "CENTRO DE INVESTIGACION Y DESARROLLO TECNOLOGICO EN ELECTROQUIMICA S.C.",
    "CENTRO DE INVESTIGACION Y DOCENCIA ECONOMICAS A.C.",
    "CENTRO DE INVESTIGACION Y SEGURIDAD NACIONAL",
    "CENTRO DE INVESTIGACIONES BIOLOGICAS DEL NOROESTE S.C.",
    "CENTRO DE INVESTIGACIONES EN OPTICA A.C.",
    "CENTRO DE INVESTIGACIONES Y ESTUDIOS SUPERIORES EN ANTROPOLOGIA SOCIAL",
    "CENTRO DE PRODUCCION DE PROGRAMAS INFORMATIVOS Y ESPECIALES",
    "CENTRO NACIONAL DE CONTROL DE ENERGÍA",
    "CENTRO NACIONAL DE CONTROL DE GAS NATURAL",
    "CENTRO NACIONAL DE EQUIDAD DE GENERO Y SALUD REPRODUCTIVA",
    "CENTRO NACIONAL DE EXCELENCIA TECNOLOGICA EN SALUD",
    "CENTRO NACIONAL DE LA TRANSFUSION SANGUINEA",
    "CENTRO NACIONAL DE METROLOGIA",
    "CENTRO NACIONAL DE PLANEACION, ANALISIS E INFORMACION PARA EL COMBATE A LA DELINCUENCIA",
    "CENTRO NACIONAL DE PREVENCION DE DESASTRES",
    "CENTRO NACIONAL DE TRASPLANTES",
    "CENTRO NACIONAL DE VIGILANCIA EPIDEMIOLOGICA Y CONTRTOL DE ENFERMEDADES",
    "CENTRO NACIONAL PARA LA PREVENCION Y CONTROL DEL VIH/SIDA",
    "CENTRO NACIONAL PARA LA PREVENCIÓN Y EL CONTROL DE LAS ADICCIONES",
    "CENTRO NACIONAL PARA LA SALUD DE LA INFANCIA Y ADOLESCENCIA",
    "CENTRO REGIONAL DE ALTA ESPECIALIDAD EN CHIAPAS",
    "CENTROS DE INTEGRACION JUVENIL A.C.",
    "CFE CORPORATIVO",
    "CFE DISTRIBUCIÓN",
    "CFE GENERACIÓN I",
    "CFE GENERACIÓN II",
    "CFE GENERACIÓN III",
    "CFE GENERACIÓN IV",
    "CFE GENERACIÓN V",
    "CFE GENERACIÓN VI",
    "CFE SUMINISTRADOR DE SERVICIOS BÁSICOS",
    "CFE TRANSMISIÓN",
    "CIATEC, A.C. CENTRO DE INNOVACION APLICADA EN TECNOLOGIAS COMPETITIVAS",
    "CIATEQ, A.C. CENTRO DE TECNOLOGIA AVANZADA",
    "COLEGIO DE BACHILLERES",
    "COLEGIO DE POSTGRADUADOS",
    "COLEGIO NACIONAL DE EDUCACION PROFESIONAL TECNICA",
    "COLEGIO SUPERIOR AGROPECUARIO DEL ESTADO DE GUERRERO",
    "COMISION DE APELACION Y ARBITRAJE DEL DEPORTE",
    "COMISION DE OPERACION Y FOMENTO DE ACTIVIDADES ACADEMICAS DEL INSTITUTO POLITECNICO NACIONAL",
    "COMISIÓN EJECUTIVA DE ATENCIÓN A VÍCTIMAS",
    "COMISION FEDERAL DE ELECTRICIDAD",
    "COMISION FEDERAL DE MEJORA REGULATORIA",
    "COMISION FEDERAL DE TELECOMUNICACIONES",
    "COMISION FEDERAL PARA LA PROTECCION CONTRA RIESGOS SANITARIOS",
    "COMISION NACIONAL BANCARIA Y DE VALORES",
    "COMISION NACIONAL DE ACUACULTURA Y PESCA",
    "COMISION NACIONAL DE ARBITRAJE MEDICO",
    "COMISION NACIONAL DE AREAS NATURALES PROTEGIDAS",
    "COMISION NACIONAL DE BIOETICA",
    "COMISION NACIONAL DE CULTURA FISICA Y DEPORTE",
    "COMISIÓN NACIONAL DE HIDROCARBUROS",
    "COMISION NACIONAL DE LAS ZONAS ARIDAS",
    "COMISION NACIONAL DE LIBROS DE TEXTO GRATUITOS",
    "COMISION NACIONAL DE LOS SALARIOS MINIMOS",
    "COMISION NACIONAL DE PROTECCION SOCIAL EN SALUD",
    "COMISION NACIONAL DE SEGURIDAD NUCLEAR Y SALVAGUARDIAS",
    "COMISION NACIONAL DE SEGUROS Y FIANZAS",
    "COMISION NACIONAL DE VIVIENDA",
    "COMISION NACIONAL DEL AGUA",
    "COMISION NACIONAL DEL SISTEMA DE AHORRO PARA EL RETIRO",
    "COMISION NACIONAL FORESTAL",
    "COMISION NACIONAL PARA EL DESARROLLO DE LOS PUEBLOS INDIGENAS",
    "COMISION NACIONAL PARA EL USO EFICIENTE DE LA ENERGIA",
    "COMISION NAL. PARA LA PROTECCION Y DEFENSA DE LOS USUARIOS DE SERVICIOS FINANCIEROS",
    "COMISION PARA LA REGULARIZACION DE LA TENENCIA DE LA TIERRA",
    "COMISION PARA PREVENIR Y ERRADICAR LA VIOLENCIA CONTRA LAS MUJERES",
    "COMISION REGULADORA DE ENERGIA",
    "COMITE NACIONAL MIXTO DE PROTECCION AL SALARIO",
    "COMITÉ NACIONAL PARA EL DESARROLLO SUSTENTABLE DE LA CAÑA DE AZÚCAR",
    "COMPAÑIA MEXICANA DE EXPLORACIONES S.A. DE C.V.",
    "COMPAÑIA OPERADORA DEL CENTRO CULTURAL Y TURISTICO DE TIJUANA S.A. DE C.V.",
    "CONSEJERIA JURIDICA DEL EJECUTIVO FEDERAL",
    "CONSEJO DE MENORES",
    "CONSEJO DE PROMOCION TURISTICA DE MEXICO S.A. DE C.V.",
    "CONSEJO NACIONAL DE CIENCIA Y TECNOLOGIA",
    "CONSEJO NACIONAL DE EVALUACION DE LA POLITICA DE DESARROLLO SOCIAL",
    "CONSEJO NACIONAL DE FOMENTO EDUCATIVO",
    "CONSEJO NACIONAL DE NORMALIZACION Y CERTIFICACION DE COMPETENCIA LABORALES",
    "CONSEJO NACIONAL PARA EL DESARROLLO Y LA INCLUSIÓN DE LAS PERSONAS CON DISCAPACIDAD",
    "CONSEJO NACIONAL PARA LA CULTURA Y LAS ARTES",
    "CONSEJO NACIONAL PARA PREVENIR LA DISCRIMINACION",
    "COORDINACION GENERAL DE LA COMISION MEXICANA DE AYUDA A REFUGIADOS",
    "COORDINACION NACIONAL DEL PROGRAMA DE DESARROLLO HUMANO OPORTUNIDADES",
    "CORPORACIÓN ÁNGELES VERDES",
    "CORPORACION MEXICANA DE INVESTIGACION EN MATERIALES S.A. DE C.V.",
    "DICONSA S.A. DE C.V.",
    "EDUCAL S.A. DE C.V.",
    "EL COLEGIO DE LA FRONTERA NORTE A.C.",
    "EL COLEGIO DE LA FRONTERA SUR",
    "EL COLEGIO DE MEXICO, A.C.",
    "EL COLEGIO DE MICHOACAN A.C.",
    "EL COLEGIO DE SAN LUIS A.C",
    "ESTUDIOS CHURUBUSCO AZTECA S.A.",
    "EXPORTADORA DE SAL S.A.DE C.V.",
    "FERROCARRIL DEL ISTMO DE TEHUANTEPEC S.A. DE C.V.",
    "FERROCARRILES NACIONALES DE MEXICO",
    "FIDEICOMISO DE FOMENTO MINERO",
    "FIDEICOMISO DE FORMACION Y CAPACITACION PARA EL PERSONAL DE LA MARINA MERCANTE NACIONAL",
    "FIDEICOMISO DE RIESGO COMPARTIDO",
    "FIDEICOMISO FONDO DE CAPITALIZACION E INVERSION DEL SECTOR RURAL",
    "FIDEICOMISO FONDO NACIONAL DE FOMENTO EJIDAL",
    "FIDEICOMISO FONDO NACIONAL DE HABITACIONES POPULARES",
    "FIDEICOMISO PARA LA CINETECA NACIONAL",
    "FIDEICOMISO PROMEXICO",
    "FINANCIERA RURAL",
    "FONATUR CONSTRUCTORA, S.A. DE C.V.",
    "FONATUR MANTENIMIENTO TURISTICO, S.A. DE C.V.",
    "FONATUR OPERADORA PORTUARIA, S.A. DE C.V.",
    "FONATUR PRESTADORA DE SERVICIOS, S.A. DE C.V.",
    "FONDO DE CULTURA ECONOMICA",
    "FONDO DE EMPRESAS EXPROPIADAS DEL SECTOR AZUCARERO",
    "FONDO DE GARANTIA Y FOMENTO PARA LA AGRICULTURA, GANADERIA Y AVICULTURA",
    "FONDO DE GARANTIA Y FOMENTO PARA LAS ACTIVIDADES PESQUERAS",
    "FONDO DE INFORMACION Y DOCUMENTACION PARA LA INDUSTRIA",
    "FONDO DE LA VIVIENDA DEL ISSSTE",
    "FONDO DE OPERACION Y FINANCIAMIENTO BANCARIO A LA VIVIENDA",
    "FONDO ESPECIAL DE ASISTENCIA TECNICA Y GARANTIA PARA LOS CREDITOS AGROPECUARIOS",
    "FONDO ESPECIAL PARA FINANCIAMIENTOS AGROPECUARIOS",
    "FONDO NACIONAL DE FOMENTO AL TURISMO",
    "FONDO NACIONAL PARA EL FOMENTO DE LAS ARTESANIAS",
    "FONDO PARA EL DESARROLLO DE LOS RECURSOS HUMANOS",
    "GRUPO AEROPORTUARIO DE LA CIUDAD DE MEXICO S.A. DE C.V.",
    "HOSPITAL GENERAL DE MEXICO",
    "HOSPITAL GENERAL DR. MANUEL GEA GONZALEZ",
    "HOSPITAL INFANTIL DE MEXICO FEDERICO GOMEZ",
    "HOSPITAL JUAREZ DE MEXICO",
    "HOSPITAL REGIONAL DE ALTA ESPECIALIDAD DE CIUDAD VICTORIA BICENTENARIO 2010",
    "HOSPITAL REGIONAL DE ALTA ESPECIALIDAD DE IXTAPALUCA",
    "HOSPITAL REGIONAL DE ALTA ESPECIALIDAD DE LA PENINSULA DE YUCATAN",
    "HOSPITAL REGIONAL DE ALTA ESPECIALIDAD DE OAXACA",
    "HOSPITAL REGIONAL DE ALTA ESPECIALIDAD DEL BAJIO",
    "I.I.I. SERVICIOS S.A. DE C.V.",
    "IMPRESORA Y ENCUADERNADORA PROGRESO S.A. DE C.V.",
    "INSTALACIONES INMOBILIARIAS PARA INDUSTRIAS, S.A. DE C.V.",
    "INSTITUTO DE ADMINISTRACION Y AVALUOS DE BIENES NACIONALES",
    "INSTITUTO DE CAPACITACION Y PROFESIONALIZACION EN PROCURACION DE JUSTICIA FEDERAL",
    "INSTITUTO DE ECOLOGIA A.C. (INV)",
    "INSTITUTO DE INVESTIGACIONES DR. JOSE MARIA LUIS MORA",
    "INSTITUTO DE INVESTIGACIONES ELECTRICAS",
    "INSTITUTO DE LOS MEXICANOS EN EL EXTERIOR",
    "INSTITUTO DE SEGURIDAD SOCIAL PARA LAS FUERZAS ARMADAS MEXICANAS",
    "INSTITUTO DE SEGURIDAD Y SERVICIOS SOCIALES DE LOS TRABAJADORES DEL ESTADO",
    "INSTITUTO DEL FONDO NACIONAL PARA EL CONSUMO DE LOS TRABAJADORES",
    "INSTITUTO FEDERAL DE ACCESO A LA INFORMACION PUBLICA",
    "INSTITUTO FEDERAL DE TELECOMUNICACIONES",
    "INSTITUTO MATIAS ROMERO DE ESTUDIOS DIPLOMATICOS",
    "INSTITUTO MEXICANO DE CINEMATOGRAFIA",
    "INSTITUTO MEXICANO DE LA JUVENTUD",
    "INSTITUTO MEXICANO DE LA PROPIEDAD INDUSTRIAL",
    "INSTITUTO MEXICANO DE LA RADIO",
    "INSTITUTO MEXICANO DE TECNOLOGIA DEL AGUA",
    "INSTITUTO MEXICANO DEL PETROLEO",
    "INSTITUTO MEXICANO DEL SEGURO SOCIAL",
    "INSTITUTO MEXICANO DEL TRANSPORTE",
    "INSTITUTO NACIONAL DE ANTROPOLOGIA E HISTORIA",
    "INSTITUTO NACIONAL DE ASTROFISICA OPTICA Y ELECTRONICA",
    "INSTITUTO NACIONAL DE BELLAS ARTES Y LITERATURA",
    "INSTITUTO NACIONAL DE CANCEROLOGIA",
    "INSTITUTO NACIONAL DE CARDIOLOGIA IGNACIO CHAVEZ",
    "INSTITUTO NACIONAL DE CIENCIAS MEDICAS Y NUTRICION SALVADOR ZUBIRAN (INV)",
    "INSTITUTO NACIONAL DE CIENCIAS PENALES",
    "INSTITUTO NACIONAL DE DESARROLLO SOCIAL",
    "INSTITUTO NACIONAL DE ECOLOGIA",
    "INSTITUTO NACIONAL DE ECOLOGÍA Y CAMBIO CLIMÁTICO",
    "INSTITUTO NACIONAL DE ENFERMEDADES RESPIRATORIAS",
    "INSTITUTO NACIONAL DE ESTUDIOS HISTORICOS DE LAS REVOLUCIONES DE MEXICO",
    "INSTITUTO NACIONAL DE GERIATRÍA",
    "INSTITUTO NACIONAL DE INFRAESTRUCTURA FÍSICA EDUCATIVA",
    "INSTITUTO NACIONAL DE INVESTIGACIONES FORESTALES AGRICOLAS Y PECUARIAS",
    "INSTITUTO NACIONAL DE INVESTIGACIONES NUCLEARES",
    "INSTITUTO NACIONAL DE LA ECONOMÍA SOCIAL",
    "INSTITUTO NACIONAL DE LA PESCA",
    "INSTITUTO NACIONAL DE LAS MUJERES",
    "INSTITUTO NACIONAL DE LAS PERSONAS ADULTAS MAYORES",
    "INSTITUTO NACIONAL DE LENGUAS INDIGENAS",
    "INSTITUTO NACIONAL DE MEDICINA GENOMICA",
    "INSTITUTO NACIONAL DE MIGRACION",
    "INSTITUTO NACIONAL DE NEUROLOGIA Y NEUROCIRUGIA DR. MANUEL VELASCO SUAREZ",
    "INSTITUTO NACIONAL DE PEDIATRIA",
    "INSTITUTO NACIONAL DE PERINATOLOGIA ISIDRO ESPINOSA DE LOS REYES",
    "INSTITUTO NACIONAL DE PSIQUIATRIA RAMON DE LA FUENTE MUÑIZ",
    "INSTITUTO NACIONAL DE REHABILITACION",
    "INSTITUTO NACIONAL DE SALUD PUBLICA",
    "INSTITUTO NACIONAL DEL DERECHO DE AUTOR",
    "INSTITUTO NACIONAL PARA EL DESARROLLO DE CAPACIDADES DEL SECTOR RURAL A.C.",
    "INSTITUTO NACIONAL PARA EL FEDERALISMO Y EL DESARROLLO MUNICIPAL",
    "INSTITUTO NACIONAL PARA LA EDUCACION DE LOS ADULTOS",
    "INSTITUTO NACIONAL PARA LA EVALUACION DE LA EDUCACION",
    "INSTITUTO PARA EL DESARROLLO TECNICO DE LAS HACIENDAS PUBLICAS",
    "INSTITUTO PARA LA PROTECCION AL AHORRO BANCARIO",
    "INSTITUTO POLITECNICO NACIONAL",
    "INSTITUTO POTOSINO DE INVESTIGACION CIENTIFICA Y TECNOLOGICA, A.C.",
    "LABORATORIOS DE BIOLOGICOS Y REACTIVOS DE MEXICO S.A. DE C.V.",
    "LICONSA S.A. DE C.V.",
    "LOTERIA NACIONAL PARA LA ASISTENCIA PUBLICA",
    "NACIONAL FINANCIERA S.N.C.",
    "NOTIMEX, AGENCIA DE NOTICIAS DEL ESTADO MEXICANO",
    "NOTIMEX S.A. DE C.V.",
    "PATRONATO DE OBRAS E INSTALACIONES DEL INSTITUTO POLITECNICO NACIONAL",
    "PEMEX-EXPLORACION Y PRODUCCION",
    "PEMEX-GAS Y PETROQUIMICA BASICA",
    "PEMEX-PETROQUIMICA",
    "PEMEX-REFINACION",
    "PETROLEOS MEXICANOS",
    "P.M.I. COMERCIO INTERNACIONAL S.A. DE C.V.",
    "POLICIA FEDERAL",
    "PRESIDENCIA DE LA REPUBLICA",
    "PREVENCION Y READAPTACION SOCIAL",
    "PROCURADURIA AGRARIA",
    "PROCURADURIA DE LA DEFENSA DEL CONTRIBUYENTE",
    "PROCURADURIA FEDERAL DE LA DEFENSA DEL TRABAJO",
    "PROCURADURIA FEDERAL DE PROTECCION AL AMBIENTE",
    "PROCURADURIA FEDERAL DEL CONSUMIDOR",
    "PROCURADURIA GENERAL DE LA REPUBLICA",
    "PRODUCTORA NACIONAL DE BIOLOGICOS VETERINARIOS",
    "PRONOSTICOS PARA LA ASISTENCIA PUBLICA",
    "RADIO EDUCACION",
    "REGISTRO AGRARIO NACIONAL",
    "SECCION MEXICANA DE LA COMISION INTERNACIONAL DE LIMITES Y AGUAS MEXICO-ESTADOS UNIDOS DE AMERICA",
    "SECCION MEXICANA DE LA COMISION INTERNACIONAL DE LIMITES Y AGUAS MEXICO-GUATEMALA-BELICE",
    "SECRETARIA DE AGRICULTURA GANADERIA DESARROLLO RURAL PESCA Y ALIMENTACION",
    "SECRETARIA DE COMUNICACIONES Y TRANSPORTES",
    "SECRETARÍA DE CULTURA",
    "SECRETARIA DE DESARROLLO AGRARIO, TERRITORIAL Y URBANO",
    "SECRETARIA DE DESARROLLO SOCIAL",
    "SECRETARIA DE ECONOMIA",
    "SECRETARIA DE EDUCACION PUBLICA",
    "SECRETARIA DE ENERGIA",
    "SECRETARIA DE GOBERNACION",
    "SECRETARIA DE HACIENDA Y CREDITO PUBLICO",
    "SECRETARIA DE LA DEFENSA NACIONAL",
    "SECRETARIA DE LA FUNCION PUBLICA",
    "SECRETARIA DE MARINA",
    "SECRETARIA DE MEDIO AMBIENTE Y RECURSOS NATURALES",
    "SECRETARIA DE RELACIONES EXTERIORES",
    "SECRETARIA DE SALUD",
    "SECRETARIA DE TURISMO",
    "SECRETARIA DEL TRABAJO Y PREVISION SOCIAL",
    "SECRETARÍA EJECUTIVA DEL SISTEMA NACIONAL ANTICORRUPCIÓN",
    "SECRETARIA GENERAL DEL CONSEJO NACIONAL DE POBLACION",
    "SECRETARIA TECNICA DE LA COMISION CALIFICADORA DE PUBLICACIONES Y REVISTAS ILUSTRADAS",
    "SECRETARIADO EJECUTIVO DEL SISTEMA NACIONAL ANTICORRUPCIÓN",
    "SECRETARIADO EJECUTIVO DEL SISTEMA NACIONAL DE SEGURIDAD PUBLICA",
    "SERVICIO DE ADMINISTRACION TRIBUTARIA",
    "SERVICIO DE ADMINISTRACION Y ENAJENACION DE BIENES",
    "SERVICIO DE INFORMACION AGROALIMENTARIA Y PESQUERA",
    "SERVICIO DE PROTECCIÓN FEDERAL",
    "SERVICIO GEOLOGICO MEXICANO",
    "SERVICIO NACIONAL DE INSPECCION Y CERTIFICACION DE SEMILLAS",
    "SERVICIO NACIONAL DE SANIDAD INOCUIDAD Y CALIDAD AGROALIMENTARIA",
    "SERVICIO POSTAL MEXICANO",
    "SERVICIOS A LA NAVEGACION EN EL ESPACIO AEREO MEXICANO",
    "SERVICIOS AEROPORTUARIOS DE LA CIUDAD DE MEXICO S.A. DE C.V.",
    "SERVICIOS DE ALMACENAMIENTO DEL NORTE S.A.",
    "SERVICIOS DE ATENCION PSIQUIATRICA",
    "SISTEMA NACIONAL PARA EL DESARROLLO INTEGRAL DE LA FAMILIA",
    "SISTEMA PÚBLICO DE RADIODIFUSIÓN DEL ESTADO MEXICANO",
    "SOCIEDAD HIPOTECARIA FEDERAL S.N.C.",
    "TALLERES GRAFICOS DE MEXICO",
    "TECNOLOGICO NACIONAL DE MEXICO",
    "TELECOMUNICACIONES DE MEXICO",
    "TELEVISION METROPOLITANA S.A. DE C.V.",
    "TRANSPORTADORA DE SAL S.A. DE C.V.",
    "TRIBUNAL FEDERAL DE CONCILIACION Y ARBITRAJE",
    "TRIBUNAL FEDERAL DE JUSTICIA FISCAL Y ADMINISTRATIVA CON SEDE EN EL DISTRITO FEDERAL",
    "TRIBUNAL SUPERIOR AGRARIO.",
    "TRIBUNALES UNITARIOS AGRARIOS",
    "UNIVERSIDAD ABIERTA Y A DISTANCIA DE MÉXICO",
    "UNIVERSIDAD AUTONOMA AGRARIA ANTONIO NARRO",
    "UNIVERSIDAD AUTONOMA DE CHAPINGO",
    "UNIVERSIDAD AUTONOMA METROPOLITANA",
    "UNIVERSIDAD PEDAGOGICA NACIONAL",
    "XE-IPN CANAL 11"
]

def get_institution():
    return random.choice(institutions)



with open("./catalogs/catRelacionPersona.json") as relacion_persona:
    cat_relacion_persona = json.load(relacion_persona)


with open("./catalogs/catTipoApoyo.json") as tipo_apoyo:
    cat_tipo_apoyo = json.load(tipo_apoyo)

def dependiente():

    return {
        "nombre_personal": {
            "nombres": get_name(),
            "primer_apellido": get_last_name(),
            "segundo_apellido": get_last_name()
        },
        "tipo_relacion": random.choice(cat_relacion_persona),
        "nacionalidades": citizenship(),
        "curp": fake.curp(),
        "rfc": fake.rfc(),
        "fecha_nacimiento": get_bith_date(),
        "numero_identificacion_nacional": "ABCD1234",
        "habita_domicilio_declarante": rand_bool(),
        "domicilio": get_address(),
        "medio_contacto": get_email('coldmailcom'),
        "ingresos_propios": True,
        "ocupacion_profesion": "Administrador de empresas",
        "sector_industria": {
            "codigo": "SFS",
            "valor": "Servicios de salud y asistencia social"
        },
        "proveedor_contratista_gobierno": True,
        "tiene_intereses_mismo_sector_declarante": True,
        "desarrolla_cabildeo_sector_declarante": {
            "respuesta": True,
            "observaciones": lorem_ipsum()
        },
        "beneficiario_programa_publico": [{
            "nombre_programa": "Prospera",
            "institucion_otorga_apoyo": get_institution(),
            "tipo_apoyo": random.choice(cat_tipo_apoyo),
            "valor_apoyo": random.randint(10000, 100000)
        }],
        "observaciones": lorem_ipsum()
    }



def bien_mueble_registrable():
    return {
        "id": 123,
        "tipo_operacion": {
            "codigo": "INCP",
            "valor": "Incorporacion"
        },
        "tipo_bien_mueble": {
            "codigo": "VEH",
            "valor": "Vehiculo"
        },
        "marca": random.choice (["BMW", "MASERATI","NISSAN", "KIA", "FERRARI", "JAGUAR", "FORD", "JEEP"]),
        "submarca": "RS-122234",
        "modelo": 2018,
        "numero_serie": "6545243-4334",
        "lugar_registro": {
            "pais": {
                "valor": "MEXICO",
                "codigo": "MX"
            },
            "entidad": {
                "nom_agee": "MEXICO",
                "cve_agee": "15"
            }
        },
        "titular_bien": {
            "codigo": "DECL",
            "valor": "Declarante"
        },
        "porcentaje_propiedad": 70,
        "nombres_copropietarios": [
            get_name()+" "+get_last_name()+" "+get_last_name()
        ],
        "numero_registro_vehicular": 455000,
        "forma_adquisicion": {
            "codigo": "CES",
            "valor": "Cesion"
        },
        "nombre_denominacion_adquirio": get_name()+" "+get_last_name()+" "+get_last_name(),
        "rfc_quien_adquirio": fake.rfc(),
        "relacion_persona_quien_adquirio": random.choice(cat_relacion_persona),
        "sector_industria": {
            "codigo": "SFS",
            "valor": "Servicios de salud y asistencia social"
        },
        "fecha_adquisicion": get_bith_date(),
        "precio_adquisicion": {
            "valor": 4000,
            "moneda": {
                "codigo": "MXN",
                "moneda": "MXN"
            }
        },
        "observaciones": lorem_ipsum()
    }


with open('./catalogs/catTipoBienInmueble.json') as inmuebles:
    cat_bien_inmueble = json.load(inmuebles)
    #cat_bien_inmueble

with open('./catalogs/catFormaAdquisicion.json') as forma_adquisicion:
    cat_forma_adquisicion = json.load(forma_adquisicion)

def bien_inmueble():

    inmueble = {
        "id": 123,
        "tipo_operacion": {
            "codigo": "INCP",
            "valor": "Incorporacion"
        },
        "tipo_bien": random.choice(cat_bien_inmueble),
        "superficie_terreno": random.randint(300, 600),
        "superficie_construccion": random.randint(70, 150),
        "titular": {
            "codigo": "DECL",
            "valor": "Declarante"
        },
        "porcentaje_propiedad": random.randint(10,70),
        "nombre_copropietario": {
            "nombres": get_name(),
            "primer_apellido": get_last_name(),
            "segundo_apellido": get_last_name()
        },
        "identificacion_bien": {
            "numero_escritura_publica": random.randint(100000,99999999),
            "numero_registro_publico": random.randint(100000,99999999),
            "folio_real": "AAC"+ str(random.randint(10000, 100000)),
            "fecha_contrato": "2010-07-26" ###
        },
        "domicilio_bien": get_address(),
        "forma_adquisicion": random.choice(cat_forma_adquisicion),
        "nombre_denominacion_quien_adquirio": get_name() + " " + get_last_name() + " " + get_last_name(),
        "rfc_quien_adquirio": fake.rfc(),
        "curp_quien_adquirio": fake.curp(),
        "relacion_persona_adquirio": random.choice(cat_relacion_persona),
        "sector_industria": {
            "codigo": "SFS",
            "valor": "Servicios de salud y asistencia social"
        },
        "fecha_adquisicion": get_bith_date(),
        "precio_adquisicion": {
            "valor": random.randint(100000, 20000000),
            "moneda": {
                "codigo": "MXN",
                "moneda": "MXN"
            }
        },
        "valor_catastral": random.randint(100000, 20000000),
        "observaciones": lorem_ipsum()
    }

    return inmueble

def nivel_gobierno():
    niveles = [
        {
            "codigo": "EST",
            "valor": "Estatal"
        },
        {
            "codigo": "FED",
            "valor": "Federal"
        },
        {
            "codigo": "MUN",
            "valor": "Municipal"
        }
    ]

    return random.choice(niveles)

def grados_academicos():
    grados = [
      {
        "codigo": "PREE",
        "valor": "Preescolar"
      },
      {
        "codigo": "PRIM",
        "valor": "Primaria"
      },
      {
        "codigo": "SECU",
        "valor": "Secundaria"
      },
      {
        "codigo": "BACH",
        "valor": "Bachillerato"
      },
      {
        "codigo": "LICE",
        "valor": "Licenciatura"
      },
      {
        "codigo": "MAES",
        "valor": "Maestría"
      },
      {
        "codigo": "DOCT",
        "valor": "Doctorado"
      }
    ]

    return random.choice(grados)