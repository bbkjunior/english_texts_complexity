import json
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .to_prod.calculate_level_new import get_level_from_raw_text

# @route   POST api/level/
# @access  Public
@api_view(['POST'])
def get_level(request):
    # Вытаскиваем из запроса текст в переменную text
    text = request.data['text']
    
    # Здесь с текстом должна совершаться магия
    level = get_level_from_raw_text(text)
    # Передамем уровень текста в переменную level
    #level = 'upper-intermediate_aaa'

    responseJson = {
        "level": level,
        "text": text
    }

    return JsonResponse(responseJson)
