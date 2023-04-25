# Cómo funciona esta cosa

Primero, instalar ``pip install flask`` para que el servidor local funcione.

Luego, los pasos son los siguientes: 
* Ejecutar el servidor apropiado para la task a realizar ``api_taskN.py`` donde N es la task, ojo que este servidor simula al mismo tiempo la taskNa y taskNb, y no avanzará de ronda mientras no se le entreguen predicciones para ambas subtasks (si solo se quiere analizar una subtask se puede entregar el mismo pipeline para cada subtask simplemente e ignorar los resultados de la subtask que no interesa).
*  Correr el notebook SERVER REQUEST LOOP cambiando en las últimas celdas la task, subtasks y los pipelines apropiados. Por ahora la lematización se dejó fuera de los pipelines para mayor rapidez.
* Correr el notebook anterior debería generar un archivo json dependiendo de la task que se corrió.
* Luego se pueden correr los notebooks de evaluación, cambiando en las primeras celdas la task a analizar.

OJO que si el servidor local termina de enviar todas las rondas entonces debe reiniciarse, ya que de lo contrario no enviará nada útil.



