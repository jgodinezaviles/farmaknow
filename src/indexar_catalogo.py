import os
import pandas as pd
import cohere
import chromadb

# 1. Conectar a Cohere usando la variable de entorno
co = cohere.Client(os.environ["COHERE_API_KEY"])

# 2. Leer el catalogo unificado
df = pd.read_csv("docs/catalogo_unificado.csv")

# 3. Convertir cada fila en un texto narrativo (esto es lo que se convierte en embedding)
def fila_a_texto(row):
    return (
        f"Sintoma: {row['sintoma']}. "
        f"Categoria: {row['categoria']}. "
        f"Medicamento sugerido: {row['nombre_comercial']} "
        f"(principio activo: {row['principio_activo']}), "
        f"presentacion: {row['presentacion']}. "
        f"Clasificacion de venta: {row['clasificacion_venta']}. "
        f"Contraindicaciones: {row['contraindicaciones_clave']}. "
        f"Nivel de alerta (advertencia_seria): {row['advertencia_seria']}. "
        f"Fuente: {row['fuente']}."
    )

textos = df.apply(fila_a_texto, axis=1).tolist()

# 4. Leer el documento de politica y agregarlo como un chunk mas
with open("docs/politica_uso_alcance.md", "r", encoding="utf-8") as f:
    politica_texto = f.read()

textos.append(politica_texto)

# 5. Preparar metadatos (uno por cada texto, en el mismo orden)
metadatos = []
for _, row in df.iterrows():
    metadatos.append({
        "tipo": "medicamento",
        "grupo": row["grupo"],
        "categoria_normalizada": row["categoria_normalizada"],
        "advertencia_seria": row["advertencia_seria"],
        "nombre_comercial": row["nombre_comercial"],
    })

metadatos.append({
    "tipo": "politica",
    "grupo": "politica_uso",
    "categoria_normalizada": "politica",
    "advertencia_seria": "NO",
    "nombre_comercial": "N/A",
})

ids = [f"chunk_{i}" for i in range(len(textos))]

print(f"Total de chunks a indexar: {len(textos)}")

# 6. Generar embeddings con Cohere (multilingue, funciona bien en espanol)
print("Generando embeddings con Cohere...")
response = co.embed(
    texts=textos,
    model="embed-multilingual-v3.0",
    input_type="search_document",
)
embeddings = response.embeddings

# 7. Guardar todo en Chroma (base de datos vectorial local)
cliente_chroma = chromadb.PersistentClient(path="./chroma_db")

# Si la coleccion ya existe de una corrida anterior, la borramos para empezar limpio
try:
    cliente_chroma.delete_collection("medicamentos_otc")
except Exception:
    pass

coleccion = cliente_chroma.create_collection("medicamentos_otc")

coleccion.add(
    ids=ids,
    embeddings=embeddings,
    documents=textos,
    metadatas=metadatos,
)

print("Indexacion completa. Base guardada en ./chroma_db")
print(f"Total de documentos en la coleccion: {coleccion.count()}")
