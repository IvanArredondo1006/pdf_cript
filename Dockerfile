# Imagen base
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar Streamlit
CMD ["streamlit", "run", "pdf_cript.py", "--server.port=8000", "--server.address=0.0.0.0"]
