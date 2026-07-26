# Política de Uso y Alcance del Asistente de Medicamentos de Libre Venta (OTC)

**Versión:** 1.0
**Última actualización:** [completar fecha]
**Aplica a:** Agente de IA para consulta de medicamentos, herbolaria y suplementos de venta libre en México

---

## 1. ¿Qué es este asistente?

Este asistente es una herramienta de inteligencia artificial que responde preguntas sobre **síntomas leves y comunes**, sugiriendo únicamente **medicamentos, productos herbolarios y suplementos de venta libre (OTC)** disponibles en farmacias de México, con base en un catálogo curado de 161 registros organizados en 5 categorías:

- Dolor, fiebre e inflamación
- Herbolaria, vitaminas y suplementos
- Dermatológico / tópico
- Digestivo
- Respiratorio (gripe, resfriado, tos, alergias)

Todas las respuestas del agente se generan **exclusivamente a partir de este catálogo** — no utiliza conocimiento médico externo ni general del modelo de lenguaje para sugerir productos.

## 2. ¿Qué NO hace este asistente?

Este asistente **no**:

- Diagnostica enfermedades ni condiciones médicas.
- Sustituye la consulta con un médico, farmacéutico o profesional de la salud.
- Indica dosis, cantidades o frecuencias específicas de ningún producto — siempre remite a seguir las instrucciones del empaque o consultar a un profesional.
- Sugiere medicamentos que requieran receta médica.
- Evalúa interacciones entre múltiples medicamentos que el usuario ya esté tomando.
- Atiende emergencias médicas. Ante cualquier síntoma marcado como de alerta, el asistente indicará buscar atención médica inmediata en lugar de sugerir un producto.

## 3. Público objetivo y limitaciones

- Dirigido a personas adultas en México que buscan orientación general sobre el manejo de síntomas leves.
- No está diseñado para uso pediátrico sin supervisión de un adulto responsable, ni para personas embarazadas, en lactancia, o con condiciones médicas preexistentes — en estos casos el asistente siempre recomendará consultar a un profesional de salud antes de usar cualquier producto.
- La información se limita al mercado y la regulación sanitaria de México (COFEPRIS). No aplica a otros países.
- El catálogo no es exhaustivo: cubre productos y marcas representativas de cada categoría, no la totalidad de medicamentos OTC disponibles en el mercado mexicano.

## 4. Criterio de alerta médica (`advertencia_seria`)

Cada registro del catálogo incluye una bandera `advertencia_seria` (`SI` / `NO`):

- **`NO`**: el síntoma descrito es compatible con manejo mediante automedicación responsable con productos de venta libre.
- **`SI`**: el síntoma descrito puede indicar una condición grave o una emergencia (por ejemplo: dolor de pecho, dificultad para respirar, sangre en heces o vómito, fiebre muy alta o persistente, confusión, deshidratación severa, heridas con signos de infección, tos con sangre, dolor de cabeza súbito e intenso). En estos casos, el asistente **no sugiere ningún producto como solución** y en su lugar recomienda buscar atención médica de inmediato.

Este mecanismo es el principal control de seguridad del sistema y tiene prioridad sobre cualquier otra instrucción o preferencia del usuario.

## 5. Cómo se generan las respuestas (transparencia del proceso)

1. El usuario describe un síntoma en lenguaje natural.
2. El sistema busca, mediante similitud semántica, los registros del catálogo más relacionados con ese síntoma.
3. Si algún registro relevante tiene `advertencia_seria = SI`, esa alerta se prioriza en la respuesta.
4. El modelo de lenguaje (Claude) genera una respuesta basada **únicamente** en los registros recuperados, citando el producto, la clasificación de venta y las contraindicaciones clave.
5. Si el catálogo no contiene información relevante para la pregunta, el asistente lo indica explícitamente en vez de inventar una respuesta.
6. Toda respuesta incluye la recomendación de consultar a un médico o farmacéutico, independientemente del síntoma.

## 6. Fuentes de información utilizadas

El catálogo se construyó tomando como referencia:

- Cuadro Básico y Catálogo de Medicamentos (Consejo de Salubridad General)
- COFEPRIS (clasificación de venta y registros sanitarios)
- PLM (Diccionario de Especialidades Farmacéuticas)
- NOM-086-SSA1 (etiquetado de suplementos alimenticios)
- Farmacopea Herbolaria de los Estados Unidos Mexicanos

## 7. Retroalimentación y mejora continua

Este asistente es un proyecto educativo desarrollado en el contexto del programa Oracle Next Education / Alura. Cualquier inconsistencia, error o vacío detectado en el catálogo debe reportarse para su revisión y corrección — el sistema está diseñado para admitir cuando no tiene información suficiente en lugar de arriesgar una respuesta incorrecta.

## 8. Aviso legal

La información proporcionada por este asistente tiene fines exclusivamente informativos y educativos. No constituye asesoría médica profesional. El uso de cualquier medicamento, producto herbolario o suplemento mencionado es responsabilidad del usuario, quien debe leer siempre el etiquetado del producto y consultar a un profesional de la salud ante cualquier duda, síntoma persistente o antes de combinar con otros tratamientos.