# -*- coding: utf-8 -*-
from rules.models import ReglaDeAjuste, ReglaDePreCategorizacion

def parseData(data, factor):
    """
    Formatea los factores y valores, filtrando ajuste o precategorización con el string 'factor'.
    Filtra los valores que no tienen una regla asociada y los factores sin valores con reglas asociadas.
    Retorna un diccionario que contiene una entrada de arrays por cada factor.
    """
    newData = {'count': 0, 'results': dict()}
    for piece in data:
        if (factor == 'factorDeAjuste_descripcion' and ReglaDeAjuste.objects.prefetch_related('FactorDeAjuste', 'ValorDeFactorDeAjuste').filter(condicion__descripcion=piece['descripcion'], condicion__factorDeAjuste__descripcion=piece[factor]).exists()) or (factor == 'factorDePreCategorizacion_descripcion' and ReglaDePreCategorizacion.objects.prefetch_related('FactorDePreCategorizacion', 'ValorDeFactorDePreCategorizacion').filter(condicion__descripcion=piece['descripcion'], condicion__factorDePreCategorizacion__descripcion=piece[factor]).exists()):
            if not piece[factor] in newData['results']:
                newData['results'][piece[factor]] = [ piece['descripcion'], ]
            else:
                newData['results'][piece[factor]].append(piece['descripcion'])
    newData['count'] = len(newData['results'])
    return newData