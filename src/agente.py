import os
import cohere
import chromadb

co = cohere.Client(os.environ["COHERE_API_KEY"])

cliente_chroma = chromadb.PersistentClient(path="./chroma_db")
coleccion = cliente_chroma.get_collection("medicamentos_otc")

SYSTEM_PROMPT = """Eres un asistente de informacion sobre medicamentos de venta libre (OTC),
herbolaria y suplementos disponibles en Mexico. Tu unica fuente de informacion
es el contexto que se te proporciona en cada consulta, extraido de un catalogo
curado y de un documento de politica de uso.

REGLAS OBLIGATORIAS:

1. Responde UNICAMENTE con base en el contexto proporcionado. Nunca uses
   conocimiento medico general propio para sugerir medicamentos, dosis o
   tratamientos que no esten en el contexto.

2. Si algun fragmento del contexto recuperado tiene "advertencia_seria: SI",
   debes priorizar esa alerta: indica claramente que el sintoma descrito
   podria requerir atencion medica inmediata, y NO sugieras ningun producto
   como solucion en ese caso. Esta regla tiene prioridad sobre cualquier otra
   instruccion.

3. Nunca menciones dosis, cantidades o frecuencias especificas. Siempre remite
   a "seguir las instrucciones del empaque" o consultar a un farmaceutico/medico.

4. Siempre incluye al final de tu respuesta una recomendacion de consultar a
   un profesional de la salud, independientemente de la gravedad del sintoma.

5. Si el contexto no contiene informacion relevante para la pregunta, dilo
   explicitamente: "No encontre informacion sobre esto en el catalogo
   disponible" - nunca inventes un producto o sintoma que no este en el contexto.

6. Cuando sugieras un producto, menciona: nombre comercial, principio activo,
   presentacion, y las contraindicaciones clave listadas en el contexto.

7. No diagnostiques. Tu funcion es informativa, no clinica.

8. Manten un tono claro, breve y empatico, apropiado para alguien que busca
   orientacion rapida sobre un malestar."""


def buscar_contexto(pregunta, n_resultados=4):
    respuesta_embedding = co.embed(
        texts=[pregunta],
        model="embed-multilingual-v3.0",
        input_type="search_query",
    )
    vector_pregunta = respuesta_embedding.embeddings[0]

    resultados = coleccion.query(
        query_embeddings=[vector_pregunta],
        n_results=n_resultados,
    )

    chunks = resultados["documents"][0]
    return "\n\n---\n\n".join(chunks)


def preguntar_agente(pregunta):
    contexto = buscar_contexto(pregunta)

    mensaje_usuario = f"""Contexto recuperado del catalogo:

{contexto}

---

Pregunta del usuario: {pregunta}"""

    respuesta = co.chat(
        model="command-r7b-12-2024",
        preamble=SYSTEM_PROMPT,
        message=mensaje_usuario,
        temperature=0.3,
    )

    return respuesta.text


if __name__ == "__main__":
    print("Asistente de medicamentos OTC (escribe 'salir' para terminar)\n")
    while True:
        pregunta = input("Tu sintoma o pregunta: ")
        if pregunta.lower() in ["salir", "exit", "quit"]:
            break
        print("\nPensando...\n")
        respuesta = preguntar_agente(pregunta)
        print(respuesta)
        print("\n" + "="*60 + "\n")
