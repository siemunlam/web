# -*- coding: utf-8 -*-
def parseData(data, factor):
    newData = {'count': 0, 'results': dict()}
    for piece in data:
        if not piece[factor] in newData['results']:
            newData['results'][piece[factor]] = [ piece['descripcion'], ]
        else:
            newData['results'][piece[factor]].append(piece['descripcion'])
    newData['count'] = len(newData['results'])
    return newData

def removeEmptyEntries(dictionary):
    for key in list(dictionary['results'].keys()):
        if not dictionary['results'][key]:
            del dictionary['results'][key]
    return dictionary