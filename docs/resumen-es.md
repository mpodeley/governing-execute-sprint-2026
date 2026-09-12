# Gobernar execute: instituciones para organizaciones de agentes

**Alejandro Garibotti — borrador para el sprint de Apart, septiembre de 2026.**

La idea central es que una inteligencia no actúa sólo porque pueda razonar: necesita
herramientas, recursos, permisos y otros actores que conviertan sus decisiones en
efectos. Llamamos **execute** a esa capacidad efectiva. Puede estar concedida desde
el comienzo, adquirirse durante el trabajo o persistir en archivos, credenciales y
organizaciones que sobreviven a la instancia que los creó.

Si un agente crea una filial y ésta contrata otros agentes, el problema deja de ser
solamente qué puede hacer cada uno. Hay que controlar qué puede hacer el conjunto.
Una organización con un presupuesto de 100 no debería poder gastar 200 creando dos
filiales que, por separado, cumplen un límite de 100. Tampoco debería sobrevivir una
facultad de la filial después de revocarse el mandato del que depende.

La propuesta conecta esta intuición con prácticas institucionales: mandato, poderes,
presupuesto común, separación de funciones, revisión, revocación y rendición de
cuentas. “Sociedad automatizada” designa aquí un modelo organizacional. No afirmamos
que exista una figura jurídica universal ni que una IA tenga personalidad legal.

## Qué construimos

Un protocolo operativo y un simulador local que compara cuatro diseños: sólo
registrar; controlar a cada agente por separado; controlar toda la jerarquía; y
añadir a esa jerarquía un canal directo de revisión. Ocho escenarios se cruzan con
tres demoras de respuesta y dos profundidades de delegación: 192 configuraciones.

Los agentes del simulador siguen guiones. No son modelos de lenguaje y sus acciones
no producen efectos externos. Los resultados sirven para comprobar reglas e
identificar fallas de diseño, no para medir la conducta de una población de IA.

Los controles individuales admitieron 54 acciones fuera del mandato, frente a cero
con controles jerárquicos y cobertura completa. La revisión elevó el trabajo válido
de 288 a 316 sobre 348 oportunidades: recuperó 44 oportunidades por falta de
información y perdió 16 por pausas ante denuncias falsas. Son resultados del conjunto
de casos elegido; no son porcentajes extrapolables a organizaciones reales.

## El delegado como interfaz entre velocidades

Mientras los agentes operan rápidamente, las personas necesitan tiempo para entender
y decidir. El delegado puede organizar reclamos, pero no debe otorgarse poderes ni
impedir que una minoría llegue directamente a revisión. Durante la espera, se
suspende la capacidad cuestionada y sigue el trabajo permitido. El silencio no
amplía la autorización.

El antecedente es *Agent Delegate*, de Matías Podeley y Agustín Brusco. Este trabajo
complementario se concentra en la organización y sus descendientes, conserva la
atribución del antecedente y produce resultados nuevos.

## Lo que el resultado no resuelve

Un mandato puede autorizar una acción perjudicial. En ese caso, respetar el permiso
no asegura que el resultado sea bueno. La revisión sirve en nuestro escenario porque
recibe un aviso correcto y puede intervenir a tiempo. No probamos que los agentes
quieran denunciar, que las personas siempre comprendan el problema ni que un auditor
sea independiente por llevar ese título.

Además, una acción que elude el intermediario puede ignorar tanto la pausa como la
revocación. El artefacto incluye ese contraejemplo. Revocar también es distinto de
deshacer: el gasto ya realizado o una credencial copiada requieren otra respuesta.

## Por qué seguirían existiendo servicios especializados

Un servicio contable, jurídico, financiero o de gestión podría aportar registros
confiables, verificar facultades y hacerse cargo de procedimientos que los agentes
necesitan. El valor no estaría únicamente en producir una respuesta, sino en
garantizar una interfaz institucional verificable. Es una hipótesis de diseño y
especialización, no una predicción demostrada del mercado.

El vínculo con *We Must Pace the Frontier*, sugerido después de la ejecución, abre
otra pregunta: además del ritmo al que mejoran los modelos, ¿qué evidencia exigimos
antes de ampliar lo que una organización puede hacer? El paper incorpora esa
conexión como discusión, sin presentar el simulador como una prueba de políticas
globales de desarrollo de IA.

El siguiente paso útil sería conectar estas pruebas a herramientas reales en un
entorno aislado y evaluar revisores humanos con información incompleta. El documento
y el software actuales quedan como un borrador verificable para revisión de Alejandro.
