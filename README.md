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

\*\*Respuesta:\*\* Entiendo que tienes ardor estomacal después de comer. En este caso, te sugiero que consideres usar Riopan. Este medicamento contiene magaldrato y dimeticona, y está disponible en gel oral en sobres. Sin embargo, es importante que sigas las instrucciones del empaque y que consultes a un profesional de la salud si los síntomas persisten o empeoran.



Recuerda que es fundamental no automedicarse y buscar siempre la orientación de un médico o farmacéutico cuando se trata de la salud.



\*\*Pregunta:\*\* "tengo dolor de pecho"

\*\*Respuesta:\*\* El dolor de pecho puede ser un síntoma preocupante y, en algunos casos, puede indicar una condición médica grave. Es importante no automedicarse y buscar atención médica inmediata si el dolor persiste o empeora.



Basándome en el contexto proporcionado, te sugiero que consideres las siguientes opciones:



Aspirina Bayer: Este medicamento contiene ácido acetilsalicílico y se utiliza para aliviar el dolor de cabeza y reducir la inflamación. Sin embargo, es importante tener en cuenta que la Aspirina no es recomendada para el dolor de pecho, ya que puede aumentar el riesgo de sangrado y no es adecuada para este tipo de síntomas.



Gaviscon Suspensión: Este medicamento contiene alginato de sodio, bicarbonato de sodio y carbonato de calcio, y se utiliza para aliviar la acidez y el dolor de pecho asociado con el reflujo gastroesofágico. Sin embargo, es importante tener en cuenta que el dolor de pecho puede ser un síntoma de una condición médica grave, como un ataque cardíaco, y no debe ser ignorado.



Si tienes dolor de pecho, te recomiendo que consultes a un profesional de la salud lo antes posible. Es importante no automedicarse y buscar atención médica inmediata si el dolor persiste o empeora.



\*\*Pregunta:\*\* "cual es la capital de Francia"

\*\*Respuesta:\*\* No encontre informacion sobre esto en el catalogo disponible.

Recomiendo consultar a un profesional de la salud para obtener una respuesta precisa sobre la capital de Francia.



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


Puedes encontrar la captura de la ejecucion en la nube en:
docs/captura_deploy.png



\## Politica de uso



Ver docs/politica\_uso\_alcance.md. FarmaKnow es un proyecto educativo; la informacion

es orientativa y no sustituye la valoracion de un profesional de la salud.

