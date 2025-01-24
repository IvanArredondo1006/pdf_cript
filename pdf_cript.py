import os
import streamlit as st
import pikepdf
from pathlib import Path
import tempfile

# Diccionario con los NITs de los bancos
BANCO_NITS = {
    "Bancolombia": "890903938",
    "Banco Occidente": "860012288",
    "Banco Bogotá": "860003020",
}

def crear_pdf_con_adjunto(archivo_correo, archivo_adjunto, archivo_final, password):
    """Crea un PDF protegido con contraseña que incluye un archivo adjunto."""
    try:
        with pikepdf.open(archivo_correo) as pdf_correo:
            adjunto_nombre = os.path.basename(archivo_adjunto.name)
            with archivo_adjunto:
                adjunto_data = archivo_adjunto.read()
                pdf_correo.attachments[adjunto_nombre] = adjunto_data

            pdf_correo.save(archivo_final, encryption=pikepdf.Encryption(owner=password, user=password))
        return True, f"Archivo PDF generado correctamente: {archivo_final}"
    except Exception as e:
        return False, f"Error al generar el PDF: {str(e)}"

# Interfaz con Streamlit
st.title("Generador de PDF Seguro con Adjuntos")  

st.write("Seleccione el banco, suba los archivos y genere un PDF protegido.")

# Seleccionar banco
banco_seleccionado = st.selectbox("Seleccione el banco", list(BANCO_NITS.keys()))
nit_banco = BANCO_NITS[banco_seleccionado]

# Cargar archivos
archivo_correo = st.file_uploader("Suba el PDF del correo", type=["pdf"])
archivo_adjunto = st.file_uploader("Suba el PDF del adjunto", type=["pdf"])

if st.button("Generar PDF"):
    if not archivo_correo or not archivo_adjunto:
        st.error("Por favor, suba ambos archivos.")
    else:
        # Nombre del archivo final
        nombre_archivo = f"mailfrom_{banco_seleccionado.replace(' ', '').lower()}@grupomegag_com.pdf"
        
        # Crear archivo temporal para el PDF generado
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            archivo_final = tmp_file.name

        # Crear PDF
        exito, mensaje = crear_pdf_con_adjunto(
            archivo_correo,
            archivo_adjunto,
            archivo_final,
            password=nit_banco
        )

        if exito:
            st.success(mensaje)
            with open(archivo_final, "rb") as f:
                st.download_button(
                    label="Descargar PDF generado",
                    data=f,
                    file_name=nombre_archivo,
                    mime="application/pdf"
                )
            # Elimina el archivo temporal después de la descarga
            os.remove(archivo_final)
        else:
            st.error(mensaje)
