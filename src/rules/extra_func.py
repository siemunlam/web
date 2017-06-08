MAX_REGLAS_CAT = 1000

def calcAjustesResultantes(cant_categorias):
	""" Dada la cantidad de categorias registradas,
		retorna la cantidad de ajustes apropiada """
	return 0 if cant_categorias <= 1 else (cant_categorias * 2) - 1


def escribirReglasDeCategorizacion(categorias, ajustes):
	""" retorna el texto de las reglas de
	categorización para Drools """
	texto = ''
	prioridad_base = -1
	for categ in categorias:
		for ajuste in ajustes:
			texto += escribirRDC(prioridad_base, categ.descripcion, str(ajuste.valor), ajustarPC(categorias, ajustes, categ, ajuste))
			prioridad_base = prioridad_base - 1
	return texto


def escribirRDC(basePriority, precategorizacion, ajuste, categorizacion):
	texto = ''
	texto += 'rule "ruleCategorizacion%s"\n' %str(-basePriority)
	texto += '\t\tno-loop\n'
	texto += '\t\tsalience %s\n' %str(basePriority)
	texto += '\twhen\n'
	texto += '\t\tpersona : Persona()\n'
	texto += '\t\t\teval( persona.getPrecategoria().equals("%s") && persona.getAjuste().equals("%s") )\n' %(precategorizacion, ajuste)
	texto += '\tthen\n'
	texto += '\t\tpersona.setCategoria("%s")\n' %categorizacion
	texto += 'end\n\n'
	return texto

def ajustarPC(categorias, ajustes, precategorizacion, ajuste):
	pos = categorias.filter(prioridad__lt = precategorizacion.prioridad).count()
	pos_result = pos - ajuste.valor
	if pos_result <= 0:
		categorizacion = categorias.first()
	elif pos_result >= categorias.count():
		categorizacion = categorias.last()
	else:
		categorizacion = categorias[pos_result]
	return categorizacion.descripcion