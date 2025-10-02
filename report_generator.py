# from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import Optional  # Importar Optional para campos opcionales

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class ReportSection(BaseModel):
    Rating: str
    Comment: str

# Definir el modelo principal ReportModel con Nota_de_prueba_escrita como campo opcional
class ReportModel(BaseModel):
    Motivación_y_Participación: ReportSection
    Aprendizaje: ReportSection
    Comportamiento: ReportSection
    Nota_de_prueba_oral: str
    Nota_de_prueba_escrita: Optional[str] = None  # Make this field optional
    Deberes: str
    Evaluación_general: str


llm4o = ChatOpenAI(model="gpt-4o")
llm4o_mini = ChatOpenAI(model="gpt-4o-mini")

errores_comunes = '''
Informes sin completar a pesar de que la información estaba proporcionada.
Traducción incompleta o imprecisa en algunos textos (ejemplo: uso de términos como "camaradas", ‘’encomiable’’ o frases que no corresponden a los datos).
Información no correcta y sensible. (Ejemplo: no tiene amigos en clase).
No traduce todas las oraciones de ejemplo en inglés.
En el apartado de motivación y participación, no se incluía el juego o actividad favorita del alumno, a pesar de que esta información estaba disponible. Este es un ejemplo, pero sucedía en varios apartados.
En los informes a veces, destacaba una habilidad y después la criticaba. Por ejemplo “Sergio es un compañero excelente que siempre respeta a los demás” y poco más adelante ponía “A veces no respeta los turnos de palabra”, lo cual no tiene congruencia.
A veces utiliza un vocabulario o estructuras más grandilocuentes, como por ejemplo “El alumno es un pilar fundamental para el funcionamiento de la clase”, lo cual es un poco excesivo para niños pequeños.
Falta de concordancia de género hablando de ‘’el profesor’’ y ‘’la profesora’’ cuando no eran de ese género. (no dar pie a este error ya que no conoces el género)
usar siempre mismos sinónimos, por ejemplo: 'lo que evidencia'. no uses la palabra 'evidencia'.
    '''

def generar_reporte(student, anterior_trimestre):

    print(student.data.get('student_name', ''))

    # Convert all values to strings, handling None
    student_data = {
        k: str(v).split()[0] if k == 'Nombre alumno' and v is not None else str(v)
        for k, v in student.data.items()
        if k != 'Nombre grupo' and k != 'Profesora' and v is not None  # Exclude 'Nombre grupo' and None values
    }

    # Determine if the category includes written test
    courses_with_written_test = ['B&B', 'Ben&Brenda', 'Ben&brenda', 'Tweens', 'Teens']
    include_written_test = student.category in courses_with_written_test

    # Prepare data to pass to LLM
    datos_estudiante = {k: v for k, v in student_data.items() if v.strip()}


    dod = f'''
    curso: {student.category.lower()}

1. Personaliza el informe y refleja el carácter y estilo de aprendizaje del estudiante.
2. Cada sección debe tener al menos 300 caracteres, no más de 600.
3. Usa el nombre del estudiante al menos una vez en cada sección, NO uses los apellidos, tampoco digas 'la/el estudiante ...).
4. En el apartado de motivación incluye ejemplos de actividades que el estudiante disfruta si las hay y estructuras de inglés que ha aprendido en aprendizaje.
5. Las frases aprendidas en inglés deben aparecer en apartado 'learning' entre comillas y deben ir seguidas de las traducciones en español entre paréntesis, nunca al revés (Solo las frases aprendidas que estén en inglés deben ser traducidas a español entre paréntesis, o el nombre de las actividades si están en inglés, no otras cosas). Todo el texto aparte siempre en español.
6. Asegúrate de que el informe refleje con precisión el progreso, carácter y aptitudes del estudiante. No seas solo positivo, que se muestre también que puede mejorar.
7. Escribe en tercera persona, evitando declaraciones en primera persona.
8. Enfócate en información relevante para el rendimiento en clase, evitando comentarios demasiado personales.
9. Sé tacto al abordar problemas, siempre proponiendo soluciones.
10. Asegúrate de que la evaluación coincida con el contenido escrito. No hables de la nota concreta, solo justifícala.
11. Usa lenguaje positivo y propone soluciones al abordar problemas.
12. Para el informe final del año, incluye una evaluación general y recomendaciones de práctica para el verano.
13. Para las clases de Babies, enfócate en las reacciones e indicadores de comprensión.
14. Para las clases de T&T, aborda el comportamiento, hábitos de trabajo y rendimiento en todas las habilidades.
15. No menciones verano o otros tiempos del año ya que no sabes en que trimestre está el alumno, tampoco menciones que no lo sabes. Tampoco menciones notas concretas aunque sí justificalas.
16. Crucial que no te inventes ningún dato que no te he proporcionado. Como asumir el numero de alumnos o el género del profesor. Solo usa lo que sabes.
17. Decir entrar al aula en vez de ‘’ingresar al aula’’, no decir "exitosamente", no hablar del alumno como un "recurso" o usar ninguna expresión latina, solo usar español de España.
18. Solo una vez dar alguna pequeña oración de ánimo como: sigue así, bien hecho, well done!, awesome, excellent, way to go! o alguna del estilo.
{ "19. Si el curso es mousy o linda, no hablar de 'práctica gramatical avanzada' ya que son pequeños." if 'mousy' in student.category.lower() or 'linda' in student.category.lower() else "" }

-----
errores que debes evitar:
{errores_comunes}


'''

    descripcion_tarea = f"""
Escribe un informe detallado para el estudiante basado en sus datos de rendimiento, sin inventar datos.
Sigue estas pautas de la Definición de Hecho:
{dod}


**Formato de Salida:**
{{
    "Motivación_y_Participación": {{
        "Rating": "Excellent/Very good/Good/Satisfactory",
        "Comment": "<Detailed comment>"
    }},
    "Aprendizaje": {{
        "Rating": "Excellent/Very good/Good/Satisfactory",
        "Comment": "<Detailed comment>"
    }},
    "Comportamiento": {{
        "Rating": "Excellent/Very good/Good/Satisfactory",
        "Comment": "<Detailed comment>"
    }},
    "Nota_de_prueba_oral": "<(Aquí solo puedes responder una de estas 4 sin inventartelo, oración completa): Aceptable. Entiende la pregunta, pero es necesario darle el inicio de la palabra para que responda utilizando un término aislado.
Bueno. Entiende la pregunta y responde con una palabra, aunque en ocasiones es necesario ayudarle con el inicio de la misma.
Muy bueno. Entiende la pregunta y responde utilizando la palabra adecuada, casi sin ayuda.
Excelente. Responde adecuadamente a la pregunta realizada por el profesor, ya sea con una sola palabra o con la estructura completa, sin necesidad de que se le ayude.>",
    "Deberes": "<(hay que hacer el comentario sobre lo datos)>",

    {"\"Nota_de_prueba_escrita\": \"<Detailed comment>\"," if include_written_test else "Añade esto si en el trimestre anterior también hubo written test comment: \"Nota_de_prueba_escrita\": \"<Detailed comment>\","}
    "Evaluación_general": "<Detailed comment>"
}}


{anterior_trimestre}


**Ahora, utilizando los datos proporcionados a continuación para el estudiante, genera el informe siguiendo el estilo del anterior pero escribelo de manera más humana que el anterior y variando la estructura para evitar repeticiones. A parte de variar estructura, también usa sinónimos sin que sean palabras poco comunes, para no repetirte.**

**ESENCIAL QUE SOLO USES DATOS DE AQUÍ Y NO TE INVENTES NINGÚN DATO NO PRESENTE. Datos del estudiante: **

{datos_estudiante}

(No menciones los datos numéricos, solo es una representación del profesor.)
**Importante**:
- REDACTA LO MÁS HUMANO POSIBLE COMO UN BUEN PROFESOR/PROFESORA
- Asegúrate de que el informe final esté en formato JSON válido.    
- Utiliza comillas dobles para las claves y los valores.
- Si necesitas incluir comillas dentro de un valor, escápalas usando \\\".

"""

    respuesta = client.beta.chat.completions.parse(
        model="o4-mini",
        messages=[{"role": "user", "content": descripcion_tarea}],
        response_format=ReportModel,
        # reasoning_effort='high'
    )

    # Extraer el contenido del informe
    informe = respuesta.choices[0].message.content

    print("Generated Report 1:", informe)

    revision_tarea = f'''
    Informe generado:\n\n{informe} 
    
    ------
    Asegurate que cumpla con todos los requisitos:
    {dod}

    ------
    Asegurate de que no aparezcan ninguno de estos errores:
    {errores_comunes}

    Solo corrige lo que tengas que cambiar del comment si hay algo, el rating dejalo igual siempre. nada más.
'''
    # respuesta = client.beta.chat.completions.parse(
    #     model="o3-mini",
    #     messages=[{"role": "user", "content": revision_tarea}],
    #     response_format=ReportModel
    # )

    # informe = respuesta.choices[0].message.content

    # print("Generated Report 2:", informe)

    try:
        # Convertir la respuesta a formato JSON si es válida
        report = json.loads(informe)
    except json.JSONDecodeError:
        # Manejar el caso donde la respuesta no es JSON válido
        print("Error: La respuesta no es JSON válido.")
        report = {}

    return report





class ReportModelTweens(BaseModel):
    Comportamiento: ReportSection
    Trabajo: ReportSection
    Rendimiento: ReportSection
    My_Way: Optional[str]
    Nota_de_prueba_oral: str  # Solo se necesita el comentario
    Nota_de_prueba_escrita: str  # Incluida para "Tweens"
    Deberes: str  # Añadido Homework sin calificación
    Evaluación_general: str    # Solo se necesita el comentario
    Nota_Global: str  # Añadido Global Score sin calificación

'''bb lo detecta como'''

def generar_reporte_tweens(student, anterior_trimestre):

    print(student.data.get('student_name', ''))


    # print(student.student_name)
    # for attr, value in vars(student).items():
    #     setattr(student, attr, str(value) if value is not None else '')

    courses_with_written_test = ['B&B', 'Ben&Brenda', 'Tweens', 'Teens']

    student_data = {
        k: str(v).split()[0] if k == 'Nombre alumno' and v is not None else str(v)
        for k, v in student.data.items()
        if k != 'Nombre grupo' and k != 'Profesora' and v is not None  # Exclude 'Nombre grupo' and None values
    }

    # Determine if the category includes written test
    courses_with_written_test = ['B&B', 'Ben&Brenda', 'Tweens', 'Teens']
    include_written_test = student.category in courses_with_written_test

    # Prepare data to pass to LLM
    datos_estudiante = {k: v for k, v in student_data.items() if v.strip()}

    dod = f'''
    curso: {student.category.lower()}
1. Personaliza el informe y refleja el carácter y estilo de aprendizaje del estudiante.
2. Cada sección debe tener al menos 300 caracteres, menos la de oral y writing test. Máximo 500-600.
3. Usa el nombre del estudiante al menos una vez en cada sección, NO uses los apellidos, tampoco digas 'la/el estudiante ....
4. Incluye ejemplos de actividades que el estudiante disfruta y estructuras de inglés que ha aprendido.
5. No hace falta que las incluyas, pero si las hay, las frases aprendidas en inglés entre comillas y las traducciones seguidas en español entre paréntesis (Solo las frases aprendidas que estén en inglés deben ser traducidas a español entre paréntesis, o el nombre de las actividades si están en inglés, nada más debe ir entre paréntesis) Todo el texto aparte siempre en español.
6. Asegúrate de que el informe refleje con precisión el progreso, carácter y aptitudes del estudiante.
7. Escribe en tercera persona, evitando declaraciones en primera persona.
8. Enfócate en información relevante para el rendimiento en clase, evitando comentarios demasiado personales.
9. Sé tacto al abordar problemas, siempre proponiendo soluciones.
10. Asegúrate de que la evaluación coincida con el contenido escrito. No hables de la nota concreta, solo justifícala.
11. Usa lenguaje positivo y propone soluciones al abordar problemas.
12. Para el informe final del año, incluye una evaluación general y recomendaciones de práctica para el verano.
13. Para las clases de Babies, enfócate en las reacciones e indicadores de comprensión.
14. Para las clases de T&T, aborda el comportamiento, hábitos de trabajo y rendimiento en todas las habilidades.
15. No menciones verano o otros tiempos del año ya que no sabes en que trimestre está el alumno, tampoco menciones que no lo sabes. Tampoco menciones notas concretas aunque sí justificalas.
16. Crucial que no te inventes ningún dato que no te he proporcionado. Como asumir el numero de alumnos o el género del profesor. Solo usa lo que sabes.
17. Decir entrar al aula en vez de ‘’ingresar al aula’’, no decir "exitosamente", no hablar del alumno como un "recurso" o usar ninguna expresión latina, solo usar español de España.
18. Solo una vez dar alguna pequeña oración de ánimo como: sigue así, bien hecho, well done!, awesome, excellent, way to go!.


-----
errores que debes evitar:
{errores_comunes}
'''

    # Construir la parte inicial del prompt con las calificaciones
    descripcion_tarea = f"""
Escribe un informe detallado para el estudiante basado en sus datos de rendimiento, sin inventar datos.
Sigue estas pautas de la Definición de Hecho:
{dod}

"""

    # Formato de salida específico para "Tweens" incluyendo Homework y Global Score
    formato_salida = """
**Formato de Salida:**
{
    "Comportamiento": {
        "Rating": "Excellent/Very good/Good/Satisfactory/Poor",
        "Comment": "<Detailed comment>"
    },
    "Trabajo": {
        "Rating": "Excellent/Very good/Good/Satisfactory/Poor",
        "Comment": "<Detailed comment>"
    },
    "Rendimiento": {
        "Rating": "Excellent/Very good/Good/Satisfactory/Poor",
        "Comment": "<Detailed comment>"
    },
    "My_Way": "<¿Cuáles son sus habilidades más fuertes?  aqui resume el tiempo activo en "My Way". >"**NO PONGAS este apartado si no tienes ningún dato al respecto.** *Se trata de una app, los alumnos hacen ejercicios escritos principalmente, y algunos orales, en el comentario destaca principalmente su expresión oral.*,
     "Nota_de_prueba_oral": "<(Aquí solo puedes responder una de estas 4 sin inventartelo, oración completa): Aceptable. Entiende la pregunta, pero es necesario darle el inicio de la palabra para que responda utilizando un término aislado.
Bueno. Entiende la pregunta y responde con una palabra, aunque en ocasiones es necesario ayudarle con el inicio de la misma.
Muy bueno. Entiende la pregunta y responde utilizando la palabra adecuada, casi sin ayuda.
Excelente. Responde adecuadamente a la pregunta realizada por el profesor, ya sea con una sola palabra o con la estructura completa, sin necesidad de que se le ayude.>",
    "Nota_de_prueba_escrita": "<Detailed comment>",
    "Homework": "<Detailed comment>",
    "Evaluación_general": "<Detailed comment>",
    "Global_Score": "<Detailed comment>"
}
"""

    descripcion_tarea += formato_salida

    # Ejemplo de informe adaptado para "Tweens" incluyendo Homework y Global Score


    # Construir la sección de datos del estudiante, incluyendo Homework y Global Score
    descripcion_tarea += f"""
**
**
Estos son los datos del trimestre anterior, no tienes que mencionar nada de aquí ni de que estás comparando, simplemente sirve para que sepas de que alumno se trata:
{anterior_trimestre}
**

**Ahora, utilizando los datos proporcionados a continuación para el estudiante, genera el informe siguiendo el estilo del anterior pero escribelo de manera más humana que el anterior y variando la estructura para evitar repeticiones. A parte de variar estructura, también usa sinónimos sin que sean palabras poco comunes, para no repetirte.**

**ESENCIAL QUE SOLO USES DATOS DE AQUÍ Y NO TE INVENTES NINGÚN DATO NO PRESENTE. Datos del estudiante: **

{datos_estudiante}

(No menciones los datos numéricos, solo es una representación del profesor.)
**Importante**:
- REDACTA LO MÁS HUMANO POSIBLE COMO UN BUEN PROFESOR/PROFESORA
- Asegúrate de que el informe final esté en formato JSON válido.    
- Utiliza comillas dobles para las claves y los valores.
- Si necesitas incluir comillas dentro de un valor, escápalas usando \\\".
**
"""

    # Generar el informe utilizando el modelo
    respuesta = client.beta.chat.completions.parse(
        model="o4-mini",
        messages=[{"role": "user", "content": descripcion_tarea}],
        response_format=ReportModelTweens,
        # reasoning_effort='high'
    )


    # Extraer el contenido del informe
    informe = respuesta.choices[0].message.content

    print("Generated Report 1:", informe)

    revision_tarea = f'''
    Informe generado:\n\n{informe} 
    
    ------
    Asegurate que cumpla con todos los requisitos:
    {dod}

    ------
    Asegurate de que no aparezcan ninguno de estos errores:
    {errores_comunes}

    Solo corrige lo que tengas que cambiar del comment si hay algo, el rating dejalo igual siempre. nada más.
'''
    # respuesta = client.beta.chat.completions.parse(
    #     model="o3-mini",
    #     messages=[{"role": "user", "content": revision_tarea}],
    #     response_format=ReportModelTweens
    # )

    # informe = respuesta.choices[0].message.content

    # print("Generated Report 2:", informe)



    if informe.startswith('```'):
        # Remove markdown code block formatting if present
        informe = informe.split('```')[1]
        if informe.startswith('json'):
            informe = informe[4:]
        informe = informe.strip()
    with open('names.txt', 'a') as file:
        file.write(f"{student.data.get('student_name', '')},{student.category.lower()}\n")


    try:
        # Convertir la respuesta a formato JSON si es válida
        report = json.loads(informe)
    except json.JSONDecodeError:
        # Manejar el caso donde la respuesta no es JSON válido
        print("Error: La respuesta no es JSON válido.")
        report = {}
    return report