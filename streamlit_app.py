import streamlit as st
import yt_dlp
import os

def descargar_mp3(url, output_path):
    opciones = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }
    
    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])
        info = ydl.extract_info(url, download=False)
        return f"{info['title']}.mp3"

st.title("YouTube MP3 Downloader")

url_video = st.text_input("Introduce la URL del video de YouTube:")
output_path = st.text_input("Introduce la ruta de salida para el archivo MP3:", value=".")

if st.button("Descargar MP3"):
    if url_video:
        try:
            with st.spinner("Descargando..."):
                nombre_archivo = descargar_mp3(url_video, output_path)
            st.success(f"Descarga completada: {nombre_archivo}")
            st.audio(os.path.join(output_path, nombre_archivo))
        except Exception as e:
            st.error(f"Error al descargar: {str(e)}")
    else:
        st.warning("Por favor, introduce una URL de YouTube válida.")

st.markdown("**Nota**: Asegúrate de tener los derechos necesarios para descargar y usar el contenido.")