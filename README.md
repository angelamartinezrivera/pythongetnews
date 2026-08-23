## Nombre: Angela Guadalupe Martínez Rivera

# Documentación del Trabajo de Scraping de la página de noticias de CESPE

## 1. Configuración del entorno de desarrollo

Para el desarrollo de este proyecto se utilizó **Python 3.14.3**

La ejecución de Python se realizó desde la terminal de Visual Studio Code. Esto permitió crear y administrar entornos virtuales, instalar dependencias y ejecutar los scripts del trabajo.

Utilicé el programa **Visual Studio Code**, ya que es la herramienta con la que tengo más familiaridad. Además, facilita la edición de código, la administración de proyectos en Python y la ejecución de scripts desde una terminal integrada.

---

## 2. Revisión de trabajos previos

Antes de comenzar el desarrollo del trabajo, realicé una revisión de los trabajos elaborados anteriormente en la materia **Programación para la Extracción de Datos**.

Estos trabajos me sirvieron de referencia para comprender nuevamente conceptos relacionados con:

- Web Scraping.
- Uso de librerías para extracción de datos.
- Procesamiento de información obtenida desde páginas web.
- Organización modular de proyectos en Python.

Además de servir como guía para la elaboración del Scraping de la página de **CESPE**, esta revisión me ayudó a reforzar conocimientos adquiridos durante el curso y recordar procedimientos.

### Ejemplos de trabajos utilizados como referencia

<img width="280" height="276" alt="image" src="https://github.com/user-attachments/assets/e5230e04-bc8c-4988-b76c-f19d8682f52b" />

<img width="626" height="347" alt="image" src="https://github.com/user-attachments/assets/ccce0d77-2891-41e2-a2b5-4843a3c1da60" />

<img width="570" height="359" alt="image" src="https://github.com/user-attachments/assets/c4cc0ca6-bb83-4fed-890f-af0c4806fca6" />

<img width="620" height="338" alt="image" src="https://github.com/user-attachments/assets/3e305ad7-0cfd-40a8-9882-708f5925f367" />

---

## 3. Creación de la estructura del proyecto

Posteriormente se creó una carpeta destinada exclusivamente al desarrollo del proyecto dentro de la carpeta **Documentos** llamada **pythongetnews**.

Esta carpeta funcionó como directorio principal para almacenar todos los archivos relacionados con el scraping, incluyendo código fuente, módulos y entorno virtual.

<img width="341" height="140" alt="image" src="https://github.com/user-attachments/assets/71ae3562-6da4-4f45-8a85-66728e32faa5" />

Una vez creada la carpeta, se abrió **Visual Studio Code** y se accedió al directorio del proyecto para comenzar la configuración del entorno de trabajo.

---

## 4. Creación y activación del entorno virtual

Con el objetivo de mantener aisladas las dependencias del proyecto, se creó un entorno virtual mediante el siguiente comando:

```bash
python -m venv venv
```

Después de crear el entorno virtual, se procedió a activarlo utilizando el siguiente comando:

```bash
venv\Scripts\activate
```

Una vez activado el entorno virtual, instalé las librerías necesarias para el trabajo, usando el siguiente comando.

```bash
pip install beautifulsoup4 requests mysql-connector-python
```

---

## 5. Creación de la carpeta de módulos

Dentro de la carpeta principal del proyecto se creó una carpeta llamada **modulos**,  para almacenar las funciones encargadas del Scraping.

---

## 6. Desarrollo del módulo `cespe_scraping.py`

El archivo `cespe_scraping.py` contiene las funciones para realizar el Scraping y procesar la información obtenida desde el portal de noticias de CESPE.

### Código del módulo

```python
# Módulo para extraer noticias de la CESPE y procesar fechas válidas
import requests # Librería para realizar peticiones HTTP
from bs4 import BeautifulSoup # Librería para extraer información del contenido HTML

def obtener_noticias_cespe():
    """
    Obtener el contenido HTML de la página de noticias de la CESPE
    y extrae el texto de las noticias.
    """
    url = "http://www.cespe.gob.mx/public/Noticias" # URL de las noticias de CESPE
    
    respuesta = requests.get(url) # Envío de la petición GET a la página web
    soup = BeautifulSoup(respuesta.text, 'html.parser') # Creación del objeto BeautifulSoup
    
    noticias_texto = [] # Lista vacía para almacenar las noticias finales
    textos_vistos = set() # Conjunto auxiliar para rastrear los textos ya procesados
    
    articulos = soup.find_all(['h2', 'h3', 'p']) # Extraer los encabezados y párrafos del documento
    
    for elem in articulos: # Recorrido de los elementos HTML encontrados
        texto = elem.get_text(strip=True) # Limpieza de espacios en blanco al inicio y final
        
        if len(texto) > 30 and texto not in textos_vistos: # Filtro para validar longitud y verificar que no esté duplicado
            textos_vistos.add(texto) # Registro del nuevo texto en el conjunto para evitar futuras repeticiones
            noticias_texto.append(texto) # Meter el texto limpio en la lista final
            
    return noticias_texto # Retorno de la lista con todos los textos de noticias procesados

def procesar_y_evaluar_dias(texto):
    """
    Analizar el texto de una noticia, detectar los días de la semana seguidos de un número
    y validar que dicho número esté en el rango de 1 a 31.
    """
    dias_semana = ["domingo", "lunes", "martes", "miercoles", "miércoles", "jueves", "viernes", "sabado", "sábado"] # Lista de días
    
    palabras = texto.split() # Cadena de texto a lista de palabras
    diccionario_dias = {} # Creación del diccionario que servirá de almacenamiento
    
    texto_size = len(palabras)  # Cálculo del total de palabras
    
    for i in range(texto_size): # Búsqueda por posición en la lista de palabras
        palabra_actual = palabras[i].lower().strip(",.:;") # Convertir a minúsculas y limpieza de signos
        
        if palabra_actual in dias_semana: # Evaluación si la palabra coincide con un día de la semana
            if i + 1 < texto_size: # Validación de existencia de un elemento después/siguiente en la lista
                siguiente_palabra = palabras[i + 1].strip(",.:;") # Limpieza de caracteres en la siguiente palabra
                
                if siguiente_palabra.isdigit(): # Evaluación si la palabra siguiente es un número entero
                    numero_dia = int(siguiente_palabra) # Conversión del string a entero
                    
                    if 1 <= numero_dia <= 31: # Evaluación del rango válido (1 al 31)
                        # Normalización de días para eliminar acentos en las llaves del diccionario
                        dia_limpio = "miercoles" if palabra_actual in ["miercoles", "miércoles"] else palabra_actual
                        dia_limpio = "sabado" if dia_limpio in ["sabado", "sábado"] else dia_limpio
                        
                        diccionario_dias[dia_limpio] = numero_dia # Guardado en el diccionario
                    else:
                        print(f"Día descartado fuera de rango (1-31): {palabra_actual} {numero_dia}") # Descartados
                        
    return diccionario_dias # Retorno del diccionario
```

### Funcionalidad del módulo

Estas funciones permiten:

- Conectarse al portal de noticias de CESPE
- Obtener el contenido HTML de la página
- Extraer párrafos de información
- Analizar el contenido de cada noticia
- Detectar días de la semana acompañados de fechas
- Generar diccionarios con el día y número

---

## 7. Desarrollo del archivo principal `main.py`

Después de crear el módulo con las funciones necesarias, se desarrolló el archivo principal `main.py`, encargado de coordinar todo el proceso del Scraping.

### Código del archivo principal

```python
# Archivo ejecutable principal
from modulos.cespe_scraping import obtener_noticias_cespe, procesar_y_evaluar_dias # Importación de funciones

def main():
    print("Iniciando scraping en la página de CESPE\n")
    
    # 1. Obtención de las noticias publicadas
    noticias = obtener_noticias_cespe() # Llamada a la función de extracción
    print(f"Se encontraron {len(noticias)} noticias.\n")
    
    # Lista global para guardar los diccionarios de cada noticia procesada
    resultados_totales = []
    
    # 2. Evaluación de cada noticia
    for noticia in noticias: # Recorrido de las noticias
        diccionario_evaluado = procesar_y_evaluar_dias(noticia) # Evaluación de los días
        
        if diccionario_evaluado: # Verificación si se identificaron días válidos
            print(f"--- Noticia ---")
            print(f"Texto: {noticia[:400]}...") # Muestra los primeros 400 caracteres del texto
            print(f"Diccionario obtenido: {diccionario_evaluado}\n") # Muestra del diccionario obtenido
            
            resultados_totales.append(diccionario_evaluado) # Agregar a la lista de resultados generales
            
    print("Procesamiento completado.")

if __name__ == "__main__": # Bloque de inicio
    main()  # Llamada a la función principal
```

### Funcionalidad del archivo principal

El archivo principal realiza lo siguiente:

1. Importa las funciones del módulo
2. Inicia el proceso de Scraping
3. Obtiene las noticias de CESPE
4. Procesa cada noticia individualmente
5. Evalúa los días de la semana
6. Almacena los resultados en una lista
7. Muestra los resultados obtenidos en la terminal

---

## 8. Ejecución del programa

Con todos los archivos creados y el entorno virtual activado, el programa se ejecutó desde la terminal de Visual Studio Code utilizando el siguiente comando:

```bash
python main.py
```

Durante la ejecución, el sistema accede al portal de noticias de CESPE, obtiene la información disponible, procesa cada publicación y genera diccionarios con los días y fechas válidas detectadas.

---

## 9. Resultados obtenidos

<img width="690" height="424" alt="image" src="https://github.com/user-attachments/assets/eae3c943-58bc-4a6d-b7d1-2bdd13c62040" />

Muestra que se encontraron 41 noticias, pero solo 4 noticias sí cumplen con el filtro. Por lo tanto, 37 noticias son comunicados generales que no tienen una fecha en formato "día + número del 1 al 31" (como "martes 4" o "domingo 9"), la función procesar_y_evaluar_dias() devuelve {} para ellas.
