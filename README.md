\# FarmaKnow



Asistente inteligente de medicamentos de venta libre (OTC), herbolaria y suplementos en Mexico.

Proyecto del challenge \*\*Alura Agente\*\* del programa \*\*Oracle Next Education (ONE)\*\*.



\## Descripcion



FarmaKnow es un agente de IA basado en RAG (Retrieval-Augmented Generation) que orienta a las

personas sobre opciones de venta libre para sintomas comunes. El usuario describe su malestar

(por seleccion guiada o texto libre) y el agente responde \*\*unicamente\*\* con base en un catalogo

curado de 161 registros, citando producto, principio activo, presentacion y contraindicaciones.



Caracteristicas de seguridad:



\- Nunca sugiere medicamentos de receta ni dosis especificas

\- Deteccion de sintomas de alerta (advertencia\_seria): ante posibles emergencias

&#x20; (dolor de pecho, sangrados, dificultad respiratoria) prioriza recomendar atencion

&#x20; medica inmediata en lugar de productos

\- Siempre recomienda consultar a un profesional de la salud

\- Si la informacion no esta en el catalogo, lo dice explicitamente en vez de inventar



\## Arquitectura



&#x20;   Usuario (Streamlit UI)

&#x20;      |

&#x20;      v

&#x20;   Pregunta -> Embedding (Cohere embed-multilingual-v3.0)

&#x20;      |

&#x20;      v

&#x20;   Busqueda semantica (ChromaDB, 162 chunks: 161 catalogo + 1 politica de uso)

&#x20;      |

&#x20;      v

&#x20;   Top-4 chunks + metadatos -> Prompt con reglas de seguridad

&#x20;      |

&#x20;      v

&#x20;   Generacion de respuesta (Cohere command-r7b-12-2024)

&#x20;      |

&#x20;      v

&#x20;   Respuesta + bandera de alerta + fuentes citadas



\## Tecnologias



\- \*\*Python\*\* - logica del agente

\- \*\*Cohere\*\* - embeddings multilingues y generacion de texto

\- \*\*ChromaDB\*\* - base de datos vectorial local

\- \*\*Pandas\*\* - procesamiento del catalogo

\- \*\*Streamlit\*\* - interfaz web

\- \*\*AWS EC2\*\* - deploy en la nube



\## Fuentes del catalogo



COFEPRIS, PLM, Cuadro Basico y Catalogo de Medicamentos (CSG), NOM-086-SSA1,

Farmacopea Herbolaria de los Estados Unidos Mexicanos.



\## Instalacion y ejecucion local



1\. Clonar el repositorio:



git clone https://github.com/jgodinezaviles/farmaknow.git

&#x20;      cd farmaknow



2\. Instalar dependencias:



&#x20;      pip install -r requirements.txt



3\. Configurar la API key de Cohere (gratuita en dashboard.cohere.com):



&#x20;      setx COHERE\_API\_KEY "tu\_key"        (Windows)

&#x20;      export COHERE\_API\_KEY="tu\_key"      (Linux/Mac)



4\. (Opcional) Regenerar la base vectorial - ya viene incluida en el repo:



&#x20;      python src/indexar\_catalogo.py



5\. Ejecutar la aplicacion:



&#x20;      python -m streamlit run app.py



\## Ejemplos de preguntas y respuestas



\*\*Pregunta:\*\* "me arde el estomago despues de comer"

\*\*Respuesta:\*\* El agente sugiere antiacidos de venta libre del catalogo (ej. Melox,

Riopan) con sus principios activos y contraindicaciones, recordando seguir las

instrucciones del empaque y consultar a un profesional.



\*\*Pregunta:\*\* "tengo dolor de pecho"

\*\*Respuesta:\*\* El agente detecta el sintoma de alerta y recomienda buscar atencion

medica inmediata en lugar de sugerir productos.



\*\*Pregunta:\*\* "cual es la capital de Francia"

\*\*Respuesta:\*\* El agente indica que no encontro informacion sobre esto en el

catalogo disponible (no responde fuera de su dominio).



\## Deploy en OCI



\## Deploy



Desplegado en \*\*AWS EC2\*\* (instancia t3.micro, Amazon Linux 2023, capa gratuita).



URL publica: http://18.206.184.187:8501



Nota: el programa Oracle Next Education confirmo que OCI es una sugerencia y no

un requisito obligatorio, siempre que el proyecto quede accesible mediante una

URL publica. Se opto por AWS EC2 por mayor disponibilidad de recursos en la

capa gratuita al momento del despliegue.



Servicios utilizados:

\- Amazon EC2 (computo, instancia t3.micro)

\- Security Groups (firewall: SSH, HTTP, HTTPS, puerto 8501 para Streamlit)



!\[FarmaKnow en ejecucion](docs/captura\_deploy.png)



\## Politica de uso



Ver docs/politica\_uso\_alcance.md. FarmaKnow es un proyecto educativo; la informacion

es orientativa y no sustituye la valoracion de un profesional de la salud.

