# 📄 API de Procesamiento de Documentos con IA

## Descripción

Esta API permite procesar automáticamente archivos PDF, Word (DOCX) y Excel utilizando inteligencia artificial a través de OpenAI. La aplicación extrae el texto de estos documentos y lo envía a OpenAI para analizarlo, resumirlo o procesarlo según tus necesidades.

## Características

- ✅ Soporte para múltiples formatos de archivos:
  - Documentos PDF
  - Documentos Word (DOCX)
  - Hojas de cálculo Excel (XLS/XLSX)
- ✅ Procesamiento inteligente con OpenAI (modelo GPT-4)
- ✅ API RESTful fácil de integrar en cualquier aplicación
- ✅ Implementado con FastAPI para alto rendimiento

## Requisitos

```
fastapi==0.115.6
pandas==2.2.3
PyPDF2==3.0.1
uvicorn==0.34.0
openai==0.28
python-docx
python-multipart
```

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/document-processor-api.git
   cd document-processor-api
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura tu clave de API de OpenAI:
   - Edita el archivo principal y reemplaza `'tu_clave_api'` con tu clave API real de OpenAI.
   - Alternativamente, configúrala como variable de entorno para mayor seguridad.

## Uso

### Iniciar el servidor

```bash
uvicorn main:app --host localhost --port 8081 --reload
```

O ejecuta directamente el script:

```bash
python main.py
```

El servidor se iniciará en `http://localhost:8000` (si usas el script) o en `http://localhost:8081` (si usas el comando uvicorn).

### Realizar solicitudes

Puedes enviar archivos para procesar a través del endpoint `/procesar_archivo/`:

```
POST http://localhost:8081/procesar_archivo/
```

**Ejemplo usando curl:**

```bash
curl -X POST "http://localhost:8081/procesar_archivo/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@tu_documento.pdf"
```

**Ejemplo usando Python (requests):**

```python
import requests

url = "http://localhost:8081/procesar_archivo/"
files = {"file": open("tu_documento.pdf", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Respuesta

La API responderá con un JSON que contiene el resultado del procesamiento:

```json
{
  "texto_procesado": "Aquí aparecerá el texto procesado por la IA..."
}
```

## Cómo funciona

1. **Envío de archivo**: El usuario envía un archivo (PDF, DOCX o Excel) a través del endpoint.
2. **Extracción de texto**: La API extrae todo el texto contenido en el documento:
   - Para PDFs: Extrae el texto de todas las páginas.
   - Para DOCX: Extrae el texto de todos los párrafos.
   - Para Excel: Convierte las celdas en texto formateado.
3. **Procesamiento con IA**: El texto extraído se envía a OpenAI (GPT-4) para su procesamiento.
4. **Respuesta**: La API devuelve el resultado procesado en formato JSON.

## Personalización

### Modificar el comportamiento de la IA

Puedes modificar las instrucciones del sistema para cambiar cómo la IA procesa los documentos. Edita la función `procesar_con_openai()`:

```python
def procesar_con_openai(texto):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente que ayuda a procesar documentos. [INSTRUCCIONES PERSONALIZADAS AQUÍ]"},
            {"role": "user", "content": texto}
        ],
        max_tokens=1500
    )
    return response['choices'][0]['message']['content'].strip()
```

### Añadir soporte para más formatos

Puedes extender la API para soportar más formatos de archivo añadiendo nuevas funciones de lectura y actualizando el endpoint `procesar_archivo()`.

## Limitaciones

- El procesamiento está limitado por los límites de tokens de OpenAI.
- Para documentos muy grandes, es posible que necesites implementar estrategias de fragmentación.
- La API actualmente no procesa imágenes dentro de los documentos.

## Seguridad

- No almacena los archivos subidos ni los contenidos procesados.
- Asegúrate de proteger tu clave API de OpenAI.
- Considera implementar autenticación si planeas desplegar la API públicamente.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar esta API:

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Sube la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## Licencia

[Especifica aquí la licencia de tu proyecto, por ejemplo: MIT, GPL, etc.]
