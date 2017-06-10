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
			texto += 'rule "ruleCategorizacion%s"\n' %str(prioridad_base)
			texto += '\t\tno-loop\n'
			texto += '\t\tsalience %s\n' %str(prioridad_base)
			texto += '\twhen\n'
			texto += '\t\tpersona : Persona()\n'
			texto += '\t\t\teval( persona.getPrecategoria().equals("%s") && persona.getAjuste().equals("%s") )\n' %(categ.descripcion, str(ajuste.valor))
			texto += '\tthen\n'
			texto += '\t\tpersona.setCategoria("%s");\n' %ajustarPC(categorias, ajustes, categ, ajuste)
			texto += 'end\n\n'
			prioridad_base -= 1
	return texto


def ajustarPC(categorias, ajustes, precategorizacion, ajuste):
	""" aplica el ajuste a la precategorización y retorna la categorización final """
	pos_precat = categorias.filter(prioridad__lt=precategorizacion.prioridad).count()
	pos_result = pos_precat - ajuste.valor
	if pos_result <= 0:
		categorizacion = categorias.first()
	elif pos_result >= categorias.count():
		categorizacion = categorias.last()
	else:
		categorizacion = categorias[pos_result]
	return categorizacion.descripcion