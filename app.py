import streamlit as st
st.set_page_config(page_title="Calculadora AGB", layout="wide")

import pandas as pd
import plotly.graph_objects as go
from modules.calculadora import calcular_interes_compuesto

# Inicializar variable de sesión
if "mostrar" not in st.session_state:
    st.session_state["mostrar"] = False

# Encabezado con logo y caricaturas (Responsive con columnas adaptativas)
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.image("assets/AGBIMAGEN.jpg", width=800)
    st.title("💰 Calculadora de interés compuesto - AGBROTHERS")

with col2:
    st.image("assets/BASEBALLAGB.jpg", width=400)

with col3:
    st.image("assets/wc.jpg", width=400)

# Sidebar con inputs mejorados
st.sidebar.header("Parámetros de inversión")
capital = st.sidebar.number_input("Depósito inicial ($)", min_value=0.0, step=100.0, key="capital_inicial")
tasa = st.sidebar.number_input("Tasa de interés anual (%)", min_value=0.0, step=0.1, key="tasa_interes")
años = st.sidebar.number_input("Años a invertir", min_value=1, step=1, key="anios")
frecuencia = st.sidebar.selectbox("Frecuencia de interés", ["Anualmente", "Mensualmente"], key="frecuencia")
aporte = st.sidebar.number_input("Aportes adicionales por periodo ($)", min_value=0.0, step=100.0, key="aportes_adicionales")

# Botón para iniciar o actualizar cálculo
btn_label = "🔁 Actualizar" if st.session_state["mostrar"] else "🚀 Generar cálculo"
st.sidebar.button(btn_label, on_click=lambda: st.session_state.update({"mostrar": True}))

# Mostrar resultados si ya se activó el botón
if st.session_state["mostrar"]:
    try:
        df, total_aportes, total_interes, total_final = calcular_interes_compuesto(
            capital, tasa, años, frecuencia, aporte
        )

        etiquetas = [f"{i} año" if i == 1 else f"{i} años" for i in df['Año']]

        # Gráfico con colores personalizados
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Depósito inicial', x=etiquetas, y=[capital]*len(df), marker_color='#1f77b4', hovertemplate='%{y:,.2f}'))
        fig.add_trace(go.Bar(name='Aportes acumulados', x=etiquetas, y=df['Aportes acumulados'], marker_color="#0c7959", hovertemplate='%{y:,.2f}'))
        fig.add_trace(go.Bar(name='Interés acumulado', x=etiquetas, y=df['Interés acumulado'], marker_color="#2c9ea0", hovertemplate='%{y:,.2f}'))
        fig.update_layout(barmode='stack', title='Cálculo de interés compuesto')
        st.plotly_chart(fig, use_container_width=True)

        # Resultados
        st.subheader("Resultados")
        card_template = """
        <div style="border:1px solid #eee; border-radius:8px; padding:20px; text-align:center; box-shadow:2px 2px 8px rgba(0,0,0,0.05)">
            <div style="font-size:28px; color:gray;">{icon}</div>
            <div style="font-weight: bold; color: #555;">{title}</div>
            <div style="margin-top:10px; background-color:{bg}; padding:10px; border-radius:5px; font-size:20px; font-weight:bold;">
                ${value:,.2f}
            </div>
        </div>
        """

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(card_template.format(icon="💼", title="Depósito inicial", value=capital, bg="#4db8ff"), unsafe_allow_html=True)
        with col2:
            st.markdown(card_template.format(icon="🪙", title="Depósitos adicionales acumulados", value=total_aportes, bg="#3a9ec9"), unsafe_allow_html=True)
        with col3:
            st.markdown(card_template.format(icon="📈", title="Interés acumulado", value=total_interes, bg="#75f0c3"), unsafe_allow_html=True)
        with col4:
            st.markdown(card_template.format(icon="💵", title="Total", value=total_final, bg="#6dcbbd"), unsafe_allow_html=True)

        st.caption(f"📆 Proyección total al año {años}: **${total_final:,.2f}**")

        # Resumen textual adicional
        st.markdown(f"""
        🧮 Con una inversión inicial de **${capital:,.2f}** y aportes de **${aporte:,.2f}** por período,
        obtendrías un total de **${total_final:,.2f}** después de **{años} años** con una tasa del **{tasa}%**.
        """)

        # Expander con cálculos detallados y descarga
        with st.expander("📊 Cálculos detallados"):
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar CSV", data=csv, file_name="resultado_calculo.csv", mime="text/csv")

    except ValueError:
        st.warning("❗ Los campos deben contener números válidos.")

# Pie de página
st.write("---")
st.write("🔎 ** Tool desarrollada por AGBROTHERS - Interes Compuesto**")