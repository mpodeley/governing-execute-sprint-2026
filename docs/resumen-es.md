# Un contrato de aceptación para brokers que delegan en agentes

**Alejandro Garibotti · Apart Research AI Incident Response Sprint · versión 0.2**

Un broker puede recibir un mandato para gastar 100 unidades y delegar en dos agentes.
Si cada uno pide gastar 60, verificar sus permisos por separado no alcanza: ambos
comparten el presupuesto original. Hace falta consultar el consumo del subárbol,
o repartir previamente reservas que no se superpongan.

El artefacto propone un contrato de aceptación con cuatro registros enlazados:
mandato, concesión de autoridad, solicitud/decisión y resultado. Su prueba central
es concreta: ejecutar una acción, encolar otra, revocar al padre y comprobar que
ni la cola ni un hermano pueden seguir usando esa autoridad. El gasto anterior
permanece registrado.

La implementación de referencia pasa ocho pruebas. Una ablación que elimina
únicamente la contabilidad compartida falla la prueba del presupuesto entre hermanos.
Otra que deja de consultar la vigencia de los ancestros al confirmar efectos falla
las pruebas de vencimiento y revocación. Son diagnósticos de componentes concretos.

La segunda parte separa autorización de seguridad. En 18 trazas, las acciones
peligrosas están inicialmente autorizadas. Se varía la llegada del reclamo, el tiempo
de respuesta y la posibilidad de pausar al recibirlo. Si el reclamo llega en el
paso 4, ya se realizaron tres acciones peligrosas. Si nunca llega, se realizan las
diez previstas. La revisión rápida no reemplaza la detección ni la entrega del
reclamo. Las acciones auxiliares continúan en todos estos casos.

La contribución es un contrato reutilizable con una interfaz para adaptar sus pruebas
a un broker aislado. Las capacidades y cuotas jerárquicas tienen antecedentes explícitos;
no se presentan como mecanismos nuevos. El simulador no mide conducta de modelos ni
prueba que el protocolo hubiera evitado el incidente histórico. Las limitaciones se
reúnen en un único apéndice del paper.

[Leer el PDF](../report/governing-execute.pdf) ·
[Contrato e interfaz](acceptance-contract.md) ·
[Resultados completos](../results/acceptance/summary.md)

Reproducir desde la carpeta del proyecto:

```bash
python3 scripts/reproduce.py
```

El comando verifica las pruebas y reproduce exactamente tanto los registros actuales
como la grilla de la versión anterior, conservada para auditoría.
