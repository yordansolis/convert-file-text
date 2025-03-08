import openai
import PyPDF2
import docx
import pandas as pd
from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import uvicorn

# Configura tu clave API de OpenAI
openai.api_key = 'tu_clave_api'  # Reemplaza 'tu_clave_api' por tu clave API de OpenAI

# Crea la aplicación FastAPI
app = FastAPI()

# Función para leer archivos PDF
def leer_pdf(file: BytesIO):
    reader = PyPDF2.PdfReader(file)
    texto = ""
    for pagina in range(len(reader.pages)):
        texto += reader.pages[pagina].extract_text()
    return texto

# Función para leer archivos DOCX
def leer_docx(file: BytesIO):
    doc = docx.Document(file)
    texto = ""
    for para in doc.paragraphs:
        texto += para.text + "\n"
    return texto

# Función para leer archivos Excel (solo el contenido de las celdas)
def leer_excel(file: BytesIO):
    df = pd.read_excel(file)
    texto = df.to_string(index=False)
    return texto



# Función para procesar texto con OpenAI utilizando el endpoint de chat
def procesar_con_openai(texto):
    # Llamada a la API de OpenAI para procesar el texto con un modelo de chat
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Usa el modelo adecuado, por ejemplo, "gpt-4"
        messages=[
            {"role": "system", "content": "Eres un asistente que ayuda a procesar documentos."},
            {"role": "user", "content": texto}
        ],
        max_tokens=1500  # Ajusta la cantidad de tokens según lo necesario
    )
    return response['choices'][0]['message']['content'].strip()


# http://localhost:8084/procesar_archivo/
# Endpoint para recibir archivos y procesarlos
@app.post("/procesar_archivo/")
async def procesar_archivo(file: UploadFile = File(...)):
    # Obtener el nombre del archivo y su extensión
    extension = file.filename.split('.')[-1].lower()

    # Leer el archivo según su tipo
    contenido = await file.read()
    archivo = BytesIO(contenido)

    if extension == 'pdf':
        texto = leer_pdf(archivo)

    elif extension == 'docx':
        texto = leer_docx(archivo)

    elif extension in ['xls', 'xlsx']:
        texto = leer_excel(archivo)
    else:
        return {"error": "Formato de archivo no soportado."}

    # Enviar el texto a OpenAI para que lo procese
    resultado = procesar_con_openai(texto)
    print(resultado)
    return {"texto_procesado": resultado}



# Servidor  
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn main:app --host localhost --port 8081 --reload