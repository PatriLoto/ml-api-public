# -*- coding: utf-8 -*-

import redis
import settings
import json
import time
from classifier import SentimentClassifier
########################################################################
# COMPLETO: 
########################################################################
#  Se crea conexión a redis y se la asigna a la variable "db"
db = redis.Redis(port=settings.REDIS_PORT, host=settings.REDIS_HOST, db=settings.REDIS_DB_ID)
########################################################################

########################################################################
# COMPLETO: 
# Use classifier.SentimentClassifier de la libreria
# spanish_sentiment_analysis ya instalada
########################################################################
# Se instancia el  modelo de análisis de sentimientos.
model = SentimentClassifier()
########################################################################

def sentiment_from_score(score):
    """
    Esta función recibe como entrada el score de positividad
    de nuestra sentencia y dependiendo su valor devuelve una
    de las siguientes clases:
        - "Positivo": Cuando el score es mayor a 0.55.
        - "Neutral": Cuando el score se encuentra entre 0.45 y 0.55.
        - "Negativo": Cuando el score es menor a 0.45.

    Attributes
    ----------
    score : float
        Porcentaje de positividad.

    Returns
    -------
    sentiment : str
        Una de las siguientes etiquetas: "Negativo", "Neutral" o "Positivo".
    """
    ####################################################################
    # COMPLETO
    ####################################################################
    sentiment = None
    # se agrega el if 
    if score < 0.45:
        sentiment = 'Negativo'
    elif score < 0.55
        sentiment = 'Neutral'
    else:
        sentiment= 'Positivo'    

    ####################################################################

    return sentiment


def predict(text):
    """
    Esta función recibe como entrada una oración y devuelve una
    predicción de su sentimiento acompañado del score de positividad.

    Attributes
    ----------
    text : str
        Sentencia para analizar

    Returns
    -------
    sentiment : str
        Una de las siguientes etiquetas: "Negativo", "Neutral" o "Positivo".
    score : float
        Porcentaje de positividad.
    """
    sentiment = None
    score = None

    ####################################################################
    # COMPLETO:
    ####################################################################
    # Utilizando el clasificador instanciado previamente
    # ("model") se obtiene el score de positividad.
    # Y utilizando la función "sentiment_from_score" de este módulo
    # se obtiene el sentimiento ("sentiment") a partir del score
    score = model.predict(text)
    sentiment = sentiment_from_score(score)

    ####################################################################

    return sentiment, score


def classify_process():
    """
    Obtiene trabajos encolados por el cliente desde Redis. Los procesa
    y devuelve resultados.
    Toda la comunicación se realiza a travez de Redis, por ello esta
    función no posee atributos de entrada ni salida.
    """
    # Iteramos intentando obtener trabajos para procesar
    while True:
        ##################################################################
        # COMPLETO: 
        ##################################################################
        
        # Obtenemos un batch de trabajos encolados, usando lrange de Redis.
        # Y se almacenan los trabajos en la variable "queue".
        queue = db.lrange('service_queue',0,9)
        ##################################################################

        # Iteramos por cada trabajo obtenido
        for q in queue:
            ##############################################################
            # COMPLETO #
            ##############################################################
            # Utilizamos la función "predict" para procesar la
            # sentencia enviada en el trabajo.
            q = json.loads(q.decode('utf-8'))
            job_id = q['id']
            sentiment, score = predict(q['text'])

            # Creamos un diccionario con dos entradas: "prediction" y
            # "score" donde almacenaremos los resultados obtenidos.
            output = {'prediction': sentiment, 'score': score}

            # Utilizamos la funcion "set" de Redis para enviar la respuesta.
            # usamos como "key" el "job_id".
            db.set(job_id, json.dumps(output))
            ##############################################################

        ##################################################################
        # COMPLETO: 
        ##################################################################
        # Usamos ltrim de Redis para borrar los trabajos ya procesados. 
        # Luego dormimos el proceso durante unos milisengundos antes de
        # pedir por mas trabajos.    

        db.ltrim('service_queue', len(queue), -1)
        time.sleep(2)
        ##################################################################


if __name__ == "__main__":
    print('Launching ML service...')
    classify_process()
