import requests #Librería para realizar peticiones HTTP
from bs4 import BeautifulSoup #Librería para extraer información del contenido HTML

def obtener_noticias_cespe():
    """
    Obtener el contenido HTML de la página de noticias de la CESPE
    y extrae el texto de las noticias.
    """
    url = "http://www.cespe.gob.mx/public/Noticias" #URL de las noticias de CESPE
    
    respuesta = requests.get(url) #Envío de la petición GET a la página web
    soup = BeautifulSoup(respuesta.text, 'html.parser') #Creación del objeto BeautifulSoup
    
    noticias_texto = [] #Lista vacía para almacenar las noticias finales
    textos_vistos = set() #Conjunto para rastrear los textos ya procesados
    
    articulos = soup.find_all(['h2', 'h3', 'p']) #Extraer los encabezados y párrafos del documento
    
    for elementos in articulos: #Recorrido de los elementos HTML encontrados
        texto = elementos.get_text(strip=True) #Obtener el texto y limpieza de espacios en blanco al inicio y final
        
        if len(texto) > 30 and texto not in textos_vistos: #Filtro para validar longitud y verificar que no esté duplicado
            textos_vistos.add(texto) #Registro del nuevo texto en el conjunto para evitar repeticiones
            noticias_texto.append(texto) #Meter el texto limpio en la lista final
            
    return noticias_texto #Lista con todos los textos de noticias procesados

def procesar_y_evaluar_dias(texto):
    """
    Analizar el texto de una noticia, detectar los días de la semana seguidos de un número
    y validar que dicho número esté en el rango de 1 a 31.
    """
    dias_semana = ["domingo", "lunes", "martes", "miercoles", "miércoles", "jueves", "viernes", "sabado", "sábado"] # Lista de días
    
    palabras = texto.split() #Cadena de texto a lista de palabras
    diccionario_dias = {} #Creación del diccionario que servirá de almacenamiento
    
    texto_size = len(palabras) #Cálculo del total de palabras
    
    for i in range(texto_size): #Búsqueda por posición en la lista de palabras
        palabra_actual = palabras[i].lower().strip(",.:;") #Convertir a minúsculas y limpieza de signos de puntuación
        
        if palabra_actual in dias_semana: #Evaluación si la palabra coincide con un día de la semana
            if i + 1 < texto_size: #Validación de existencia de un elemento después/siguiente en la lista
                siguiente_palabra = palabras[i + 1].strip(",.:;") #Limpieza de caracteres en la siguiente palabra
                
                if siguiente_palabra.isdigit(): #Evaluación si la palabra siguiente es un número entero
                    numero_dia = int(siguiente_palabra) #Conversión del string a entero
                    
                    if 1 <= numero_dia <= 31: #Evaluación del rango válido (1 al 31)
                        #Normalización de días para eliminar acentos en las llaves del diccionario
                        dia_limpio = "miercoles" if palabra_actual in ["miercoles", "miércoles"] else palabra_actual
                        dia_limpio = "sabado" if dia_limpio in ["sabado", "sábado"] else dia_limpio
                        
                        diccionario_dias[dia_limpio] = numero_dia #Guardado en el diccionario
                    else:
                        print(f"Día descartado fuera de rango (1-31): {palabra_actual} {numero_dia}") # Descartados
                        
    return diccionario_dias #Mostrar el diccionario
