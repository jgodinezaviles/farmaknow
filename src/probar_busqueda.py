import os
import cohere
import chromadb

co = cohere.Client(os.environ["COHERE_API_KEY"])
cliente_chroma = chromadb.PersistentClient(path="./chroma_db")
coleccion = cliente_chroma.get_collection("medicamentos_otc")

pregunta = "me duele mucho la cabeza y tengo fiebre"

# Generar embedding de la pregunta (ojo: input_type distinto al de indexacion)
respuesta_embedding = co.embed(
    texts=[pregunta],
    model="embed-multilingual-v3.0",
    input_type="search_query",
)
vector_pregunta = respuesta_embedding.embeddings[0]

# Buscar los 3 chunks mas cercanos
resultados = coleccion.query(
    query_embeddings=[vector_pregunta],
    n_results=3,
)

print(f"Pregunta: {pregunta}\n")
for i, doc in enumerate(resultados["documents"][0]):
    print(f"--- Resultado {i+1} ---")
    print(doc)
    print(f"Metadata: {resultados['metadatas'][0][i]}")
    print()
