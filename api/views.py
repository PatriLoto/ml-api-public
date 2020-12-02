# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
)

from middleware import model_predict


router = Blueprint('app_name',
                   __name__,
                   template_folder='templates')


@router.route('/', methods=['GET', 'POST'])
def index():
    """
    Esta función renderiza un frontend donde podemos ingresar
    sentencias y obtener una prediccion de su sentimiento.
    """
    context = {
        'text': None,
        'prediction': None,
        'score': None,
        'success': False
    }
    # Obtiene la sentencia ingresada por el usuario en el frontend
    text_data = request.form.get('text_data')

    if text_data:
        #################################################################
        # COMPLETO: 
        #################################################################
        # Se Envia el texto ingresado para ser procesado
        # por nuestra función middleware.model_predict.
        prediction, score = model_predict(text_data)
       
        # Con los resultados obtenidos completamos el diccionario "context"
        # para mostrar la predicción en el frontend.
        context = {
            'text': text_data,
            'prediction': prediction,
            'score': score,
            'success': True
        }
        
        #################################################################

    return render_template('index.html', context=context)


@router.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """
    [Práctico 2 - No completar]
    Esta función nos permitirá darle feedback a nuestra API
    para los casos en los que clasificamos una oración
    con un sentimiento erroneo.
    """
    context = {
        'text': None,
        'prediction': None,
        'score': None,
        'success': False
    }
    return render_template('index.html', context=context)


@router.route('/predict', methods=['POST'])
def predict():
    """
    Método POST que permite obtener predicciones de análisis de
    sentimiento a partir de oraciones.
    """
    # Respuesta inicial
    rpse = {
        'success': False,
        'prediction': None,
        'score': None
    }

    # Nos aseguramos que el método sea correcto y tengamos datos
    # para procesar
    if request.method == 'POST' and request.args.get('text'):
        #################################################################
        # COMPLETO: 
        #################################################################
        # Extraemos la sentencia a procesar y utilizamos la
        # función middleware.model_predict para obtener el sentimiento
        # de la misma.
        text_data = request.args.get('text')
        prediction, score = model_predict(text_data)

        # se completan los campos de "rpse" con los valores obtenidos.
        rpse = {
        'text': text_data,
        'prediction': prediction,
        'score': score, 
        'success': True
        }

        return jsonify(rpse)

    return jsonify(rpse), 400
