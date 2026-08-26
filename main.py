#Importación de funciones
from funciones.cespe_scraping import obtener_noticias_cespe, procesar_y_evaluar_dias

def main():
    print("Iniciando scraping en la página de CESPE\n")
    
    #1. Obtención de las noticias publicadas
    noticias = obtener_noticias_cespe() # Llamada a la función de extracción
    print(f"Se encontraron {len(noticias)} noticias.\n")
      
    #2. Evaluación de cada noticia
    for noticia in noticias: # Recorrido de las noticias
        diccionario_dias = procesar_y_evaluar_dias(noticia) #Evaluación de los días
        
        if diccionario_dias: #Verificación si se identificaron días válidos
            print(f"--- Noticia ---")
            print(f"Texto: {noticia[:400]}...") #Muestra los primeros 400 caracteres del texto
            print(f"Días: {diccionario_dias}\n") #Muestra el diccionario de los días

if __name__ == "__main__": #Bloque de inicio
    main()  #Llamada a la función principal
