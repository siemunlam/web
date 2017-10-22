function saveMotivosSolicitud(solicitud, motivo_solicitudes_map) {
    if (solicitud !== null) {
        var motivos_solicitud = solicitud.motivo;
        motivos_solicitud = motivos_solicitud.replace(/{|}|"/g, '');
        motivos_solicitud = motivos_solicitud.replace(/:/g, ' es ');
        var motivos = new Array();
        motivos = motivos_solicitud.split(',');
        
        for (motivo in motivos) {
            // console.log("value: " + );
            if (motivo_solicitudes_map[motivos[motivo]] === undefined) {
                var origen = {
                    descripcion: motivos[motivo],
                    cantidad: 1
                };
                motivo_solicitudes_map[motivos[motivo]] = origen;                    
            } else {
                motivo_solicitudes_map[motivos[motivo]].cantidad++;
            }
        }
    }
}

function saveClasificacionAuxilio(categoria_auxilio, clasificacion_auxilios_map) {
  if (categoria_auxilio !== null) {       
      if (clasificacion_auxilios_map[categoria_auxilio.descripcion] === undefined) {
          var cat = {
              descripcion: categoria_auxilio.descripcion,
              prioridad: categoria_auxilio.prioridad,
              color: categoria_auxilio.color,
              cantidad: 1
          };
          clasificacion_auxilios_map[categoria_auxilio.descripcion] = cat;                   
      } else {
        clasificacion_auxilios_map[categoria_auxilio.descripcion].cantidad++;
      }
  }
}

function saveCategorizacionAuxilio(asignaciones, auxilios_map) {
    if (!jQuery.isEmptyObject(asignaciones)) {
        var fecha_auxilio = null;
        for (var asignacion in asignaciones) {
            if (!jQuery.isEmptyObject(asignaciones[asignacion].formulariofinalizacion)) {
                var categorizacion = "";
                if (asignaciones[asignacion].formulariofinalizacion.asistencia_realizada) {
                    categorizacion = asignaciones[asignacion].formulariofinalizacion.categorizacion;
                } else {
                    categorizacion = asignaciones[asignacion].formulariofinalizacion.motivo_inasistencia;
                }

                if (auxilios_map[categorizacion] === undefined) {
                    var categorizacion_auxilio = {
                        descripcion: categorizacion,
                        cantidad: 1
                    };
                    auxilios_map[categorizacion] = categorizacion_auxilio;                    
                } else {
                    auxilios_map[categorizacion].cantidad++;
                }
            }
        }
    }
}


function saveOrigenSolicitud(solicitud, origen_solicitudes_map) {
  if (solicitud !== null) {            
      if (origen_solicitudes_map[solicitud.origen] === undefined) {
          var origen = {
              descripcion: solicitud.origen,
              color: solicitud.origen == 'Web' ? '#ff9f40' : solicitud.origen == 'Agente virtual' ? '#99ff99' : '#9966ff',
              cantidad: 1
          };
          origen_solicitudes_map[solicitud.origen] = origen;                    
      } else {
          origen_solicitudes_map[solicitud.origen].cantidad++;
      }
  }
}

function saveFechaSolicitud(solicitud, fecha_solicitudes_map) {
  if (solicitud !== null) {        
      var fecha_solicitud = moment(solicitud.fecha).format('DD/MM/YY');
      if (fecha_solicitudes_map[fecha_solicitud] === undefined) {
          var fecha = {
              descripcion: fecha_solicitud,
              cantidad: 1
          };
          fecha_solicitudes_map[fecha_solicitud] = fecha;                    
      } else {
          fecha_solicitudes_map[fecha_solicitud].cantidad++;
      }
  }
}

function saveAuxiliosCancelados(auxilio, auxilios_map) {
    var estados = auxilio.estados;
    if (!jQuery.isEmptyObject(estados)) {
        var fecha_auxilio = null;
        for (var estado in estados) {
            if (estados[estado].estado === "Cancelado") {
                var fecha_solicitud = moment(estados[estado].fecha).format('DD/MM/YY');
                if (auxilios_map[fecha_solicitud] === undefined) {
                    var fecha = {
                        descripcion: fecha_solicitud,
                        cantidad: 1
                    };
                    auxilios_map[fecha_solicitud] = fecha;                    
                } else {
                    auxilios_map[fecha_solicitud].cantidad++;
                }
            }
        }
    }
}
  
function saveAuxiliosPorEstado(auxilio, auxilios_map, estado_auxilio) {
  var estados = auxilio.estados;
  if (!jQuery.isEmptyObject(estados)) {
      var fecha_pendiente = null;
      var fecha_auxilio = null;
      for (var estado in estados) {
          fecha = moment(estados[estado].fecha);
          if (estados[estado].estado === "Pendiente") {
              fecha_pendiente = fecha;
          } else if (estados[estado].estado === estado_auxilio) {
              fecha_auxilio = fecha;
          }
      } 
      if (fecha_pendiente !== null && fecha_auxilio !== null) {
          var dif_minutos = fecha_auxilio.diff(fecha_pendiente, 'minutes');
          if (auxilios_map[auxilio.categoria.descripcion] === undefined) {
              var est = {
                  descripcion: auxilio.categoria.descripcion,
                  color: auxilio.categoria.color,
                  tiempo_total_minutos: dif_minutos,
                  cantidad: 1
              };
              auxilios_map[auxilio.categoria.descripcion] = est;     
          } else {
              auxilios_map[auxilio.categoria.descripcion].cantidad++;
              auxilios_map[auxilio.categoria.descripcion].tiempo_total_minutos += dif_minutos;
          }
      }
  }
}

async function loadAuxilios(api_url) {
    var motivo_solicitudes = {};
    var origen_solicitudes = {}; 
    var fecha_solicitudes = {};
    var clasificacion_auxilios = {};  
    var categorizacion_auxilios = {};
    var fecha_cancelados = {};
    var auxilios_en_curso = {};
    var auxilios_finalizados = {};
    await fetch(api_url, getAuthorizedFetchOption()).then(response => {
        return checkStatus(response);
    }).then(response => {
        return response.json();
    }).then(jsonData => {
        jsonData.map((auxilio) => {
        saveMotivosSolicitud(auxilio.solicitud, motivo_solicitudes); 
        saveClasificacionAuxilio(auxilio.categoria, clasificacion_auxilios);
        saveCategorizacionAuxilio(auxilio.asignaciones, categorizacion_auxilios);
        saveOrigenSolicitud(auxilio.solicitud, origen_solicitudes);
        saveFechaSolicitud(auxilio.solicitud, fecha_solicitudes);
        saveAuxiliosCancelados(auxilio, fecha_cancelados);
        saveAuxiliosPorEstado(auxilio, auxilios_en_curso, "En curso");
        saveAuxiliosPorEstado(auxilio, auxilios_finalizados, "Finalizado");
    });
    }).catch(error => {
    console.log(`Error al realizar fetch a ${api_url}: ${error.message}`);
    });
    marcarMotivosSolicitudesGrafico(motivo_solicitudes, "grafico1");
    marcarOrigenSolicitudesGrafico(origen_solicitudes, "grafico2");
    marcarFechaEnElTiempoGrafico(fecha_solicitudes, "grafico3");
    marcarClasificacionAuxiliosGrafico(clasificacion_auxilios, "grafico4");
    marcarCategorizacionAuxiliosGrafico(categorizacion_auxilios, "grafico5");
    marcarFechaEnElTiempoGrafico(fecha_cancelados, "grafico6");
    marcarTiempoEnColaGrafico(auxilios_en_curso, "grafico7");
    marcarTiempoEnColaGrafico(auxilios_finalizados  , "grafico8");
}

function mostrarMensajeGraficoSinInformacion(elemento) {
    var canvas = document.getElementById(elemento);
    var ctx = canvas.getContext("2d");
    ctx.font = "14px Arial";
    ctx.textAlign = "center";
    ctx.fillText("No hay información para mostrar", canvas.width/2, canvas.height/2); 
}

// TODO: Ver si hay alguna forma mejor dentro de las opciones de Chart porque esto no asegura unicidad de colores.
var getColorDinamico = function() {
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return "rgb(" + r + "," + g + "," + b + ")"
}

function setChart(ctx, type, labels, data, color, options, label) {
    var grafico = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: color,
                borderColor: color,
                borderWidth: 1
            }]
        },
        options: options
    });
}


function marcarClasificacionAuxiliosGrafico(categorias, elemento) {
    if (!jQuery.isEmptyObject(categorias)) {
        var data = [];
        var label = [];
        var color = [];
        for (var key in categorias) {
            label.push(categorias[key].descripcion);
            data.push(categorias[key].cantidad);
            color.push(categorias[key].color);
        }
        setChart(document.getElementById(elemento), 'doughnut', label, data, color, null, "Total");
    } else {
        mostrarMensajeGraficoSinInformacion(elemento);
    }
}

function marcarCategorizacionAuxiliosGrafico(categorizacion, elemento) {
    if (!jQuery.isEmptyObject(categorizacion)) {
        var data = [];
        var label = [];
        var color = [];
        for (var key in categorizacion) {
            label.push(categorizacion[key].descripcion);
            var color_categorizacion =  categorizacion[key].descripcion == 'Ubicación incorrecta' ? '#ff9f40' : 
                                        categorizacion[key].descripcion == 'No responde' ? '#99ff99' :
                                        categorizacion[key].descripcion == 'Apropiadamente categorizado' ? '#9966ff' :
                                        categorizacion[key].descripcion == 'Sobre-categorizado' ? '#66ffee' :
                                        categorizacion[key].descripcion == 'Sub-categorizado' ? '#55ab54' :
                                        '#000000';
            data.push(categorizacion[key].cantidad);
            color.push(color_categorizacion);
        }
        setChart(document.getElementById(elemento), 'doughnut', label, data, color, null, "Total");
    } else {
        mostrarMensajeGraficoSinInformacion(elemento);
    }
}

function marcarMotivosSolicitudesGrafico(motivo_solicitudes, elemento) {
    if (!jQuery.isEmptyObject(motivo_solicitudes)) {
        var data = [];
        var label = [];
        var color = [];
        for (var key in motivo_solicitudes) {
            label.push(motivo_solicitudes[key].descripcion);
            data.push(motivo_solicitudes[key].cantidad);
            color.push(getColorDinamico());
        }
        setChart(document.getElementById(elemento), 'doughnut', label, data, color, null, "Total");
    } else {
        mostrarMensajeGraficoSinInformacion(elemento);
    }
}

function marcarOrigenSolicitudesGrafico(origen_solicitudes, elemento) {
    if (!jQuery.isEmptyObject(origen_solicitudes)) {
        var data = [];
        var label = [];
        var color = [];
        for (var key in origen_solicitudes) {
            label.push(origen_solicitudes[key].descripcion);
            data.push(origen_solicitudes[key].cantidad);
            color.push(origen_solicitudes[key].color);
        }

        var options = {
            legend: {
            "display": false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        };
            
        setChart(document.getElementById(elemento), 'bar', label, data, color, options, "Total");
    } else {
        mostrarMensajeGraficoSinInformacion(elemento);
    }
}

function marcarFechaEnElTiempoGrafico(fecha_solicitudes, elemento) {
    if (!jQuery.isEmptyObject(fecha_solicitudes)) {
        var data = [];
        var label = [];
        var color = [];
        for (var key in fecha_solicitudes) {
            label.push(fecha_solicitudes[key].descripcion);
            data.push(fecha_solicitudes[key].cantidad);
        }

        var options = {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        };
        setChart(document.getElementById(elemento), 'line', label, data, '#4bc0c0', options, "Total");   
    } else {
        mostrarMensajeGraficoSinInformacion(elemento);
    }
}

function marcarTiempoEnColaGrafico(categorias, elemento) {
    if (!jQuery.isEmptyObject(categorias)) {
        var data = [];
        var label = [];
        var color = [];
        for (var key in categorias) {
            label.push(categorias[key].descripcion);
            data.push(Math.round(categorias[key].tiempo_total_minutos / categorias[key].cantidad));
            color.push(categorias[key].color);
        }

        var options = {
            legend: {
            "display": false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }],
                xAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        };
        setChart(document.getElementById(elemento), 'horizontalBar', label, data, color, options, "Minutos");
    } else {
        mostrarMensajeGraficoSinInformacion(elemento);
    }
}