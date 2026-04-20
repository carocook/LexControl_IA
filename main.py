import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
import time

load_dotenv()

# ==============================
# CONFIGURACIÓN DE LA API LOCAL Y EN LA NUBE
# ==============================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# ==============================
# CONFIGURACIÓN DE LA PÁGINA
# ==============================
st.set_page_config(page_title="LexControl AI", page_icon="⚖️")

st.title("LexControl AI ⚖️")
st.subheader("Asistente inteligente para gestión de plazos")
st.markdown("---")

# ==============================
# DESCRIPCIÓN
# ==============================
st.write(
    "Aplicación web que utiliza inteligencia artificial para analizar eventos procesales "
    "y sugerir acciones legales en base al derecho procesal argentino."
)

# ==============================
# CÓMO FUNCIONA
# ==============================
st.subheader("¿Cómo funciona?")
st.write("""
1. Ingresás un evento procesal (ej: notificación, demanda, audiencia).
2. La inteligencia artificial analiza el contexto legal.
3. Se genera una respuesta estructurada.
4. Se indican plazos, acciones y nivel de urgencia.
""")

st.markdown("---")

# ==============================
# INPUT DEL USUARIO
# ==============================
evento = st.text_area(
    "Evento procesal:",
    placeholder="Ej: Se notificó sentencia de primera instancia desfavorable..."
)

# ==============================
# BOTÓN DE ACCIÓN
# ==============================
if st.button("Analizar"):
    if evento:
        with st.spinner("Analizando normativa procesal..."):
            try:
                # PROMPT
                prompt = f"""
Actuá como un abogado especialista en derecho procesal argentino.

Analizá el siguiente evento y respondé en formato estructurado:

### 📌 Interpretación del evento
(explicación clara)

### ⏱ Plazo legal estimado
(indicar plazo aproximado si corresponde)

### ⚖️ Acciones recomendadas
(lista de pasos a seguir)

### 🚨 Nivel de urgencia
(indicar: alta, media o baja)

Evento: {evento}
"""

                # 🔥 MODELOS A PROBAR 
                modelos = [
                    "models/gemini-2.5-flash",
                    "models/gemini-2.5-pro",
                    "models/gemini-2.0-flash"
                    "models/gemma-3-12b-it"
                    "models/gemma-3n-e2b-it"
                    "models/gemini-flash-lite-latest"
                ]

                resultado = None

                for modelo in modelos:
                    for intento in range(3):  # reintentos
                        try:
                            response = client.models.generate_content(
                                model=modelo,
                                contents=prompt
                            )
                            resultado = response.text
                            break
                        except Exception as e:
                            if "503" in str(e):
                                time.sleep(2)  # espera y reintenta
                            else:
                                break
                    if resultado:
                        break

                # RESULTADO
                if resultado:
                    st.markdown("### 📋 Análisis y Sugerencia:")
                    st.markdown(resultado)

                    st.caption(
                        "Nota: Esta información es orientativa y debe ser validada por un profesional matriculado."
                    )
                else:
                    st.error("⚠️ La IA está saturada en este momento. Intentá nuevamente en unos segundos.")

            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ Cuota agotada. Intentá nuevamente más tarde.")
                elif "404" in str(e):
                    st.error("⚠️ Modelo no disponible. Revisá configuración.")
                else:
                    st.error(f"❌ Error inesperado: {e}")

    else:
        st.warning("⚠️ Por favor, ingresá un evento procesal.")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown("<small>Desarrollado para LexControl AI - 2026</small>", unsafe_allow_html=True)