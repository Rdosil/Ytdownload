import streamlit as st
import yt_dlp
import os
import base64

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
        info = ydl.extract_info(url, download=True)
        return f"{info['title']}.mp3"

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
    return href

st.set_page_config(page_title="YouTube MP3 Downloader", layout="wide")

st.markdown("""
<style>
.stApp {
    max-width: 800px;
    margin: 0 auto;
}
.stTextInput > div > div > input {
    font-size: 16px;
}
.stButton > button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("YouTube MP3 Downloader")

col1, col2 = st.columns([3, 1])

with col1:
    url_video = st.text_input("URL del video de YouTube:", key="url_input")

with col2:
    st.write("")
    st.write("")
    if st.button("Descargar MP3", key="download_button"):
        if url_video:
            try:
                with st.spinner("Descargando..."):
                    output_path = "downloads"
                    os.makedirs(output_path, exist_ok=True)
                    nombre_archivo = descargar_mp3(url_video, output_path)
                    file_path = os.path.join(output_path, nombre_archivo)
                st.success(f"Descarga completada: {nombre_archivo}")
                st.markdown(get_binary_file_downloader_html(file_path, 'MP3'), unsafe_allow_html=True)
                st.audio(file_path)
            except Exception as e:
                st.error(f"Error al descargar: {str(e)}")
        else:
            st.warning("Por favor, introduce una URL de YouTube válida.")

st.markdown("**Nota**: Asegúrate de tener los derechos necesarios para descargar y usar el contenido.")

expander = st.expander("Instrucciones de uso")
expander.write("""
1. Pega la URL del video de YouTube en el campo de texto.
2. Haz clic en el botón "Descargar MP3".
3. Espera a que se complete la descarga.
4. Usa el enlace "Descargar MP3" para guardar el archivo en tu dispositivo.
5. Puedes escuchar una vista previa del audio directamente en la aplicación.
""")