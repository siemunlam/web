from .serializers import AuxilioSerializer
from ..models import Asignacion, Auxilio, EstadoAuxilio
from medicos.models import Medico
import json
from math import sin,cos,sqrt,asin,pi


def generarAsignacion(self):
	# 1. Buscar auxilio pendiente o en_curso màs prioritario que posea una asignacion vacia
	## Si no encuentro ninguno, salir.
	auxilio_a_asignar = getAuxilioAAsignar()
	if auxilio_a_asignar is None:
		return False
	# 2.1 Buscar médico disponible que no esté en ninguna asignacion 'en camino', 'en el lugar' o 'en traslado' o también
	# buscar médico disponible con asignacion 'en camino' y con categorizacion y prioridad del auxilio menor a la del auxilio a asignar. Filtro por cercanìa. Me quedo solamente con uno.
	## Si no encuentro ninguno, salir.
	medicos_libres = getMedicoAAsignar()
	if not medicos_libres.exists():
		return False
	# 3.0 Seleccionar el médico màs cercano al auxilio
	medico_a_asignar = filtrar_por_cercania(medicos_libres, auxilio_a_asignar.solicitud.ubicacion_coordenadas)
	# 3.1 Asignar el médico al auxilio
	nueva_asignacion = Asignacion.objects.create(medico=medico_a_asignar, estado=Asignacion.EN_CAMINO)
	auxilio_a_asignar.asignaciones.add(nueva_asignacion)
	# 3.2 Actualizar el estado del auxilio
	actualizarEstado(auxilio_a_asignar)
	# 3.3 Enviar notificacion al médico
	notificarMedico(medico_a_asignar, auxilio_a_asignar)
	# 3.4.1 Si el médico que encontré estaba vinculado a otro auxilio, lo desvinculo y llamo otra vez a generarAsignacion()
	# 3.4.2 Si el médico que encontré era el ùnico "asignado" a ese auxilio, pongo ese auxilio en 'pendiente'
	desvincularMedico(medico_a_asignar, auxilio_a_asignar)


def filtrarAuxiliosPorEstado(estados=None):
	if not estados is None:
		if len(estados) > 1:
			estados = ', '.join(estados)
		query = '''	SELECT *
					FROM auxilios_auxilio
					WHERE EXISTS (SELECT 1
					FROM auxilios_auxilio_estados
					INNER JOIN auxilios_estadoauxilio
						ON auxilios_estadoauxilio.id = auxilios_auxilio_estados.estadoauxilio_id
					GROUP BY auxilios_auxilio_estados.auxilio_id
					HAVING auxilios_estadoauxilio.fecha = (SELECT MAX(auxilios_estadoauxilio.fecha)
					FROM auxilios_estadoauxilio
					WHERE auxilios_estadoauxilio.id = auxilios_auxilio_estados.estadoauxilio_id
					AND auxilios_auxilio.id = auxilios_auxilio_estados.auxilio_id)
					AND (auxilios_estadoauxilio.estado in (%s)))'''%estados			
		object_list = list(Auxilio.objects.raw(query))
	else:
		object_list = Auxilio.objects.all()
	return object_list


def getAuxilioAAsignar():
	# Busca el auxilio en estado PENDIENTE o EN CURSO màs prioritario que posea una asignacion sin atender
	# Es decir, que posea menos asignaciones que no tengas estado CANCELADA que moviles_requeridos
	## 1- Busco los auxilios en estado PENDIENTE o EN CURSO
	auxilios = filtrarAuxiliosPorEstado([EstadoAuxilio.PENDIENTE, EstadoAuxilio.EN_CURSO])
	## 2- Ya que los auxilios estan ordenados por categoria, prioridad y orden de llegada,
	## devuelvo el primero que encuentre que posee asignaciones sin atender.
	for auxilio in auxilios:
		if auxilio.solicitud.cantidad_moviles > obtenerAsignacionesAtendidas(auxilio.asignaciones):
			return auxilio
	return None


def obtenerAsignacionesAtendidas(asignaciones):
	asignaciones_atendidas = 0
	if asignaciones.count() > 0:
		for asignacion in asignaciones:
			if asignacion.estado in [Asignacion.EN_CAMINO, Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO, Asignacion.FINALIZADA]:
				asignaciones_atendidas += 1
	return asignaciones_atendidas


def getMedicoAAsignar():
	# Busca los médicos en estado DISPONIBLE
	medicos_disponibles = Medico.objects.filter(estado=Medico.DISPONIBLE)
	# Busca a los médicos que estén atendiendo algùn auxilio.
	medicos_asignados = Medico.objects.filter(asignacion__estado__in=[Asignacion.EN_CAMINO, Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO])
	# Hace la diferencia limpiando los campos de ordenamiento de las queries
	# porque a Django no le gusta   -.-'
	medicos_disponibles.query.clear_ordering(force_empty=True)
	medicos_asignados.query.clear_ordering(force_empty=True)
	medicos_sin_asignar = medicos_disponibles.difference(medicos_asignados)
	medicos_sin_asignar.query.clear_ordering(force_empty=True) #éste es por las dudas
	return medicos_sin_asignar


def filtrar_por_cercania(medicos, coordenadas):
	medico_mas_cercano = None
	menor_distancia = None
	for medico in medicos:
		if not medico_mas_cercano or calcular_distancia(medico.ubicacion_gps, coordenadas) < menor_distancia:
			medico_mas_cercano = medico
			menor_distancia = medico.ubicacion_gps
	return medico_mas_cercano


def calcular_distancia(coordenadas_1, coordenadas_2):
	json1 = json.loads(coordenadas_1)
	json2 = json.loads(coordenadas_2)
	lat1 = json1['lat']
	long1 = json1['long']
	lat2 = json2['lat']
	long2 = json2['long']
	
	r = 6371000 #radio terrestre medio, en metros
	c = pi/180 #constante para transformar grados en radianes
	
	#Fórmula de Haversine
	distanciaHaversine = 2*r*asin(sqrt(sin(c*(lat2-lat1)/2)**2 + cos(c*lat1)*cos(c*lat2)*sin(c*(long2-long1)/2)**2))
	return distanciaHaversine


def actualizarEstado(auxilio):
	estadoActual = auxilio.estados.first()
	if estadoActual.estado != EstadoAuxilio.EN_CURSO:
		nuevo_estado = EstadoAuxilio.objects.create(estado = EstadoAuxilio.EN_CURSO)
		auxilio_a_asignar.estados.add(nuevo_estado)


def notificarMedico(medico, auxilio):
	url = 'https://firebase.google.com/docs/cloud-messaging/blabalbal/%s' %medico.fcm_code
	serializer = AuxilioSerializer(auxilio)
	json_data = serializer.data
	try:
		response = requests.post(url, data=json_data, timeout=10)
		if response.status_code == requests.codes.ok:
			return True
		else:
			response.raise_for_status()
	except Exception as e:
		messages.error(self.request, u'No fue posible comunicarse con el médico DNI: %s. Error: %s' %(medico.dni, e), extra_tags='danger')
		return HttpResponseRedirect(reverse_lazy('home'))


def desvincularMedico(medico, auxilio=None, estado=Asignacion.DESVIADA):
	asignacion = Asignacion.objects.get(medico=medico, estado__in=[Asignacion.EN_CAMINO, Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO])
	asignacion.estado = estado
	asignacion.save()
	if auxilio:
		nueva_asignacion = Asignacion.objects.create(medico=medico)
		auxilio.asignaciones.add(nueva_asignacion)