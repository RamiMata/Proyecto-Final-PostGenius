import streamlit as st
import openai
import os

# Cargar API Key desde Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Crear el cliente de OpenAI
client = openai.Client()

st.title("PostGenius - Generador de Ideas para Redes Sociales")
st.write("Bienvenido a PostGenius, la herramienta que utiliza inteligencia artificial para ayudarte a generar ideas de contenido para tus redes sociales.")

st.header("Cómo funciona")
st.write("""
1. Ingresa tu nicho de contenido (ejemplo: fitness, tecnología, moda).
2. Selecciona la plataforma para la cual deseas generar ideas (Instagram, TikTok, Twitter, YouTube, LinkedIn).
3. Elige el objetivo de la publicación (engagement, atraer seguidores, generar ventas, educar a la audiencia).
4. Selecciona el formato de contenido (imagen, carrusel, video, historia, encuesta, reel).
5. Presiona el botón para generar ideas y obtendrás tres sugerencias detalladas para tus publicaciones.
""")

# Inputs del usuario
nicho = st.text_input("Nicho de contenido")
plataforma = st.selectbox("Selecciona la plataforma", ["Instagram", "TikTok", "Twitter", "YouTube", "LinkedIn"])
objetivo = st.selectbox("Elige el objetivo de la publicación", ["Engagement", "Atraer seguidores", "Generar ventas", "Educar a la audiencia"])
formato = st.selectbox("Selecciona el formato de contenido", ["Imagen", "Carrusel", "Video", "Historia", "Encuesta", "Reel"])

# Función para generar ideas
def generar_ideas(nicho, plataforma, objetivo, formato):
    prompt = f"""
    Genera tres ideas de publicaciones para una cuenta de {plataforma} sobre {nicho}, cuyo objetivo es {objetivo}.
    Las ideas deben ser detalladas e incluir los siguientes elementos:
    - Un título llamativo.
    - Una descripción completa explicando el contenido.
    - Un llamado a la acción (CTA) para incentivar la interacción del público.
    - Hashtags sugeridos para mejorar el alcance.
    
    Formato: {formato}.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.7
        )

        ideas = response.choices[0].message.content.strip().split("\n\n")  # Separar ideas por bloques
        return ideas[:3]  # Tomar solo las primeras 3 ideas

    except openai.APIConnectionError:
        st.error("Error de conexión con OpenAI. Verifica tu conexión a Internet.")
    except openai.APIError:
        st.error("Error en la API de OpenAI. Intenta más tarde.")
    except openai.BadRequestError:
        st.error("Error en la solicitud. Verifica los datos ingresados.")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")

    return []

# Botón para generar ideas
if st.button("Generar Ideas"):
    if not nicho or not plataforma or not objetivo or not formato:
        st.error("Por favor, completa todos los campos.")
    else:
        ideas = generar_ideas(nicho, plataforma, objetivo, formato)
        if ideas:
            st.header("Ideas Generadas")
            for i, idea in enumerate(ideas, start=1):
                st.subheader(f"Idea {i}")
                st.write(idea)

st.write("© 2025 PostGenius. Todos los derechos reservados.")


