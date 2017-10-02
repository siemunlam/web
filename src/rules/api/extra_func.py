# -*- coding: utf-8 -*-
def parseData(data, factor):
    tempResults = dict()
    newData = {'count': 0, 'results': list()}
    for piece in data:
        if not piece[factor] in tempResults:
            tempResults[piece[factor]] = [ piece['descripcion'], ]
        else:
            tempResults[piece[factor]].append(piece['descripcion'])
    for key in sorted(list(tempResults.keys()), key=str.lower):
        newData['results'].append({ key: tempResults[key]})
    newData['count'] = len(newData['results'])
    return newData