def calcAjustesResultantes(cant_categorias):
	""" Dada la cantidad de categorias registradas,
		retorna la cantidad de ajustes apropiada """
	return 0 if cant_categorias <= 1 else (cant_categorias * 2) - 1