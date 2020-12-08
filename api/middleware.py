# -*- coding: utf-8 -*-

import settings
from uuid import uuid4
import redis
import json
import time

########################################################################
# COMPLETO: 
# Se crea la conexion a redis y asignarla a la variable "db".

db = redis.Redis(port = settings.REDIS_PORT, host = settings.REDIS_HOST, db = settings.REDIS_DB_ID)
########################################################################


def model_predict(text_data):
    """
    Esta función recibe sentencias para analizar desde nuestra API,
    las encola en Redis y luego queda esperando hasta recibir los
    resultados, qué son entonces devueltos a la API.

    Attributes
    ----------
    text_data : str
        Sentencia para analizar.

    Returns
    -------
    prediction : str
        Sentimiento de la oración. Puede ser: "Positivo",
        "Neutral" o "Negativo".
    score : float
        Valor entre 0 y 1 que especifica el grado de positividad
        de la oración.
    """
    prediction = None
    score = None

    #################################################################
    # COMPLETO:
    # Una tarea esta definida como un diccionario con dos entradas:
    #     - "id": será un hash aleatorio generado con uuid4 o
    #       similar, deberá ser de tipo string.
    #     - "text": texto que se quiere procesar, deberá ser de tipo
    #       string.
    #################################################################
    # Creamos una tarea para enviar a procesar
    job_id = str(uuid4())
    
    # Definimos la tarea como un diccionario con dos entradas: id y text.
    job_data = {
        "id": job_id,
        "text": text_data
    }
    # utilizamos rpush de Redis para encolar la tarea.
    db.rpush('service_queue',json.dumps(job_data))
    
    
    #################################################################

    # Iterar hasta recibir el resultado
    # while True:
        #################################################################
        # COMPLETO: En cada iteración tenemos que:
        #     1. Intentar obtener resultados desde Redis utilizando
        #        como key nuestro "job_id".
        #     2. Si no obtuvimos respuesta, dormir el proceso algunos
        #        milisegundos.
        #     3. Si obtuvimos respuesta, extraiga la predicción y el
        #        score para ser devueltos como salida de esta función.
        #################################################################
    while True
        # Intentamos obtener resultados desde Redis utilizando
        # como key nuestro "job_id".
        output = db.get(job_id)
        if output is not None:
            output = json.loads(output.decode('utf-8'))
            prediction = output['prediction']
            score = output['score']

        # Si obtenemos respuesta, extraemos la predicción y el
        # score para ser devueltos como salida de esta función.
            print(json.dumps({
            'text': text_data,
            'prediction': prediction,
            'score': score
        }))

            db.delete(job_id)
            break
        # Si no obtenemos respuesta, dormimos el proceso algunos milisegundos.
        time.sleep(2)
        #################################################################
       
    return prediction, score
    
