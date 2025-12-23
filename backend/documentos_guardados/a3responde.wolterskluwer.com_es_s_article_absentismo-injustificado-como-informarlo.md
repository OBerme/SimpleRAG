##  
**Proceso para informar faltas de asistencia injustificadas**

Para informar a un trabajador un descuento por una ausencia injustificada,
accede al punto "**Cálculo/ Gestión de incidencias/ Mantenimiento de
incidencias** " e indica el código de la empresa, del trabajador y, en el campo
"**Fecha** ", informa el día o los días del mes que el trabajador ha causado
absentismo injustificado.  
  
A continuación, selecciona la incidencia “**8- Absentismo Injustificado** ” y
especifica los días de absentismo en, días naturales (Días N), días laborales
(Días L), horas laborales (Horas L) y/o minutos laborales (Minutos L), según el
caso.

  

Al informarlo de este modo, durante los días de absentismo cotizará por la base
mínima, tanto el trabajador como el empresario, y no se deberá realizar ninguna
comunicación a T.G.S.S. En esta situación, **no se tendrá que realizar ninguna
comunicación a Sistema RED**.

En la incidencia **8 – “Absentismo Injustificado** ”, también dispones del
indicador **“Se tramita como alta sin retribución en afiliación (inactividad
6)”** , a través del cual tendrás la posibilidad de cotizar los días que el
trabajador causa absentismo por la base mínima, solo por la cuota empresarial.

Por defecto, el indicador aparece desmarcado, al activarlo aparecerán activos
los campos “**Fecha Inicio absentismo** ” y “**Fecha fin absentismo** ”, a
través de los cuales podrás informar el periodo de absentismo en el mes.

Al informar la “**Fecha de inicio y fin”** , la aplicación calculará,
automáticamente, los días N de absentismo en el periodo informado.

Al marcar el indicador “**Se tramita como alta sin retribución en afiliación
(inactividad 6)** ” se activarán los botones Sistema RED, para poder preparar el
movimiento de afiliación, ya que estos casos, sí que hay que comunicarlos a
Seguridad Social.

  * **“MC – Cambio de Contrato (Tipo/coeficiente) - Inicio Absentismo”**
  * **“MC – Cambio de contrato (Tipo/coeficiente) - Fin Absentismo”**

  
En el campo “**Literal hoja de salario** ” puedes indicar el texto que se
visualizará posteriormente en la hoja de salario del trabajador.

Por último, pulsa “**Aceptar** ” y “**Cancelar** ” para grabar la incidencia.

####

### **¿Cómo se refleja el absentismo injustificado en la hoja de salario?**

En la hoja de salario se puede visualizar esta situación de dos formas,
dependiendo si está activado o no el indicador del centro de trabajo "**Cálculo
Automático Cpto. Absentismo** " (acceso botón "**Indicadores Cálculo** " del
apartado "**Cálculo** ").  

  * Indicador "**Cálculo Automático Cpto. Absentismo** " (DESMARCADO): Los conceptos de cobro de la nómina aparecerán disminuidos y, además, se visualizará en la hoja de salario el literal que se ha indicado en la incidencia 8 - Absentismo Injustificado. En nuestro ejemplo, “**Absent. Injust**.”  

  * Indicador "**Cálculo Automático Cpto. Absentismo** " (MARCADO): aparecerán todos los conceptos íntegros de cobro y podrás visualizar el importe de descuento por los días de absentismo en el concepto automático 790 - "**Descuento por Absentism** o". Además, se visualizará el literal indicado en la incidencia 8, en nuestro ejemplo, “**Absent. Injust.** ”.  

****  
Se descontara el absentismo injustificado de aquellos conceptos salariales
informados en la ficha del trabajador que tengan marcado el indicador "**Prorr.
Absen. Injustificado** ", en el caso de tener desmarcado el indicador ese
concepto que se cobrará integro en ese mes, y no se descontará esa parte
proporcional.  

### ******¿Cómo se refleja el absentismo en SILTRA?**

En el caso de no tener marcado el indicador “**Se tramita como alta sin
retribución en afiliación (inactividad 6)** ” en la incidencia 8, se comunicará
a Seguridad Social un único tramo de Alta en el mes, ya que cotiza tanto el
trabajador como el empresario por la base mínima.

  
En el caso de tener marcado el indicador **“Se tramita como alta sin retribución
en afiliación (inactividad 6)** ” en la incidencia 8, en el asistente de Siltra
de la aplicación podemos ver esa base mínima que cotizará sólo el empresario,
pero en el fichero XML que enviamos a Siltra no aparecerá esta información, ya
que Seguridad Social ya realiza este cálculo al conocer la situación de
afiliación.

### **Artículos relacionados:**

  * Errores R9632 y R9582 en fichero de respuesta de SILTRA con absentismo o suspensión de empleo y sueldo

