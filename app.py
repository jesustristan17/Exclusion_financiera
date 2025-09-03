import streamlit as st
import pandas as pd
import joblib

# Cargar modelo entrenado
modelo = joblib.load("modelo_exclusion_financiera.pkl")

# Codificaciones
codificaciones = {
    "INGRESO_BINNED": {
        "Sin ingreso":5,
        "Ingreso menor a 1,200 pesos": 4,
        "Ingreso entre 1,201 y 2,000 pesos": 1,
        "Ingreso entre 2,001 y 3,500 pesos": 2,
        "Ingreso entre 3,501 y 10,000 pesos": 0,
        "Ingreso superior a  10,000 pesos": 3
    },
    "BAÑOS_BINNED": {
        "Sin baño": 4,
        "1 baño": 0,
        "2 a 4 baños": 1,
        "5 baños": 2,
        "6 o más baños": 3
    },
    "ESCOLARIDAD": {
        "Ninguno": 0,
        "Preescolar-Kinder": 1,
        "Primaria": 2,
        "Secundaria": 3,
        "Normal básica": 4,
        "Preparatoria": 6,
        "Carrera técnica": 7,
        "Licenciatura": 8,
        "Especialidad": 9,
        "Maestría": 10,
        "Doctorado": 11
    },
    "STATUS_LABORAL": {
        "Empleado": 1,
        "Informal": 2,
        "Desempleado": 3,
        "Negocio propio": 4,
        "Jubilado/pensionado": 5,
        "Estudiante": 6,
        "Ama de casa": 7,
        "No activo por discapacidad/accidente": 8,
        "Otro": 8,
    },
    "TLOC": {
        "100,000 y más habitantes": 1,
        "15,000 a 99,999 habitantes": 2,
        "2,500 a 14,999 habitantes": 3,
        "Menos de 2,500 habitantes": 4,
    },
    "ENTIDAD": {
      "Aguascalientes": 1,
      "Baja California": 2,
      "Baja California Sur": 3,
      "Campeche": 4,
      "Coahuila de Zaragoza": 5,
      "Colima": 6,
      "Chiapas": 7,
      "Chihuahua": 8,
      "Ciudad de México": 9,
      "Durango": 10,
      "Guanajuato": 11,
      "Guerrero": 12,
      "Hidalgo": 13,
      "Jalisco": 14,
      "Estado de México": 15,
      "Michoacán de Ocampo": 16,
      "Morelos": 17,
      "Nayarit": 18,
      "Nuevo León": 19,
      "Oaxaca": 20,
      "Puebla": 21,
      "Querétaro": 22,
      "Quintana Roo": 23,
      "San Luis Potosí": 24,
      "Sinaloa": 25,
      "Sonora": 26,
      "Tabasco": 27,
      "Tamaulipas": 28,
      "Tlaxcala": 29,
      "Veracruz de Ignacio de la Llave": 30,
      "Yucatán": 31,
      "Zacatecas": 32
  }
,
    "TIEMPO_AHORROS": {
        "No sabe":0,
        "Menos de una semana/ No tiene ahorros": 1,
        "Al menos una semana, pero menos de un mes": 2,
        "Al menos un mes, pero menos de tres meses": 3,
        "Al menos tres meses, pero menos de seis meses": 4,
        "Seis meses o más": 5,
    },
    "COMPRAS_INF_500": {
        "Transferencia electrónica o aplicación de celular": 1,
        "Uso físico de tarjeta de débito o crédito": 2,
        "Efectivo": 3,
    },
        "COMPRAS_SUP_500": {
        "Transferencia electrónica o aplicación de celular": 1,
        "Uso físico de tarjeta de débito o crédito": 2,
        "Efectivo": 3,
    },
        "RECHAZO_PRESTAMO": {
        "Si": 1,
        "No": 2,
        "Nunca lo he solicitado": 3,
    },
        "PAGOS_TARJETA": {
        "En todos": 1,
        "En la mayoría": 2,
        "En algunos": 3,
        "En pocos": 4,
        "En ninguno": 5,
        "No sé":0
    }
}

# Descripciones de cada pregunta
descripciones = {
    "USO_ATM": "En el último año, ¿Has utilizado cajeros automáticos para retirar o consultar saldo?",
    "COMPRAS_SUP_500": "Cuándo realizas compras mayores a $500, ¿Con qué metodo las pagas?",
    "INGRESO_BINNED": "Selecciona el rango que describe tu ingreso mensual aproximado.",
    "ESCOLARIDAD": "Indica el nivel máximo de estudios que has alcanzado.",
    "RECHAZO_PRESTAMO": "¿Alguna vez te han rechazado una solicitud de préstamo?",
    "USO_SUCURSALES": "En el último año ¿has utilizado alguna sucursal de un banco o institución financiera?",
    "COMPRAS_INF_500": "Cuándo realizas compras menores a $500, ¿Con qué metodo las pagas?",
    "STATUS_LABORAL": "Selecciona la opción que mejor describe tu situación laboral actual.",
    "PAGOS_TARJETA": "En los lugares que regularmente compras, ¿En cuántos de ellos aceptan pago con tarjeta o transferencia?",
    "DOMICILIACION": "¿Tienes servicios como luz, agua o internet domiciliados a tu cuenta?",
    "OFRECIMIENTOS": "¿Has recibido ofertas de productos financieros (como tarjetas o seguros)?",
    "TLOC": "Aproximadamente, cuantos habitantes tiene el municipio en el que actualmente vives",
    "CELULAR": "¿Tienes acceso a un teléfono inteligente?",
    "INTERNET": "¿Cuentas con acceso a internet en tu hogar o celular?",
    "CLONACION_TARJETAS": "¿Has experimentado clonación de tarjeta alguna vez?",
    "ENTIDAD": "Selecciona el estado o entidad federativa donde vives.",
    "TIEMPO_AHORROS": "Si dejaras de recibir ingresos, ¿por cuánto tiempo podrías cubrir tus gastos con tus ahorros?",
    "BAÑOS_BINNED": "Número de baños disponibles en tu vivienda.",
    "PAGOS_DIGITALES": "¿Utilizas plataformas digitales para realizar pagos? (CODI, DIMO)",
    "USO_ALIANZAS": "En el último años, ¿has hecho pagos de servicios o depositos a cuentas en tiendas de conveniencia como Oxxo, 7-eleven o supermercados?"
}

# Orden de columnas según entrenamiento
orden_columnas = [
    "USO_ATM",
    "COMPRAS_SUP_500",
    "INGRESO_BINNED",
    "ESCOLARIDAD",
    "RECHAZO_PRESTAMO",
    "USO_SUCURSALES",
    "COMPRAS_INF_500",
    "STATUS_LABORAL",
    "PAGOS_TARJETA",
    "DOMICILIACION",
    "OFRECIMIENTOS",
    "TLOC",
    "CELULAR",
    "INTERNET",
    "ENTIDAD",
    "TIEMPO_AHORROS",
    "BAÑOS_BINNED",
    "PAGOS_DIGITALES",
    "USO_ALIANZAS",
    "CLONACION_TARJETAS"
]


# ⚙Configuración de la app
st.set_page_config(page_title="Evaluación Financiera", layout="centered")
st.title("🔍 Evaluación de Exclusión Financiera")

# Entrada de nombre
nombre_usuario = st.text_input(" Ingresa tu nombre ", "")
if nombre_usuario:
    st.write(f"Hola, **{nombre_usuario}** 👋 Bienvenido a la evaluación de exclusión financiera.")
else:
    st.write("Bienvenido a la evaluación de exclusión financiera.")

st.write("Completa el formulario para estimar tu probabilidad de exclusión del sistema financiero.")
# Inputs categóricos codificados
df_input = {}
for var in orden_columnas:
    if var in codificaciones:
        st.write(f"**{var.replace('_', ' ').title()}**")
        st.caption(descripciones.get(var, ""))
        seleccion = st.selectbox("", list(codificaciones[var].keys()), key=var)
        df_input[var] = codificaciones[var][seleccion]

# Inputs binarios tipo Sí/No
binarios_si_no = [
    "USO_ATM", "USO_SUCURSALES",
    "DOMICILIACION", "OFRECIMIENTOS", "CELULAR", "INTERNET", "CLONACION_TARJETAS",
    "PAGOS_DIGITALES", "USO_ALIANZAS"
]


for var in binarios_si_no:
    if var not in df_input:
        st.write(f"**{var.replace('_', ' ').title()}**")
        st.caption(descripciones.get(var, ""))
        valor = st.selectbox("", ["Sí", "No"], key=var)
        df_input[var] = 1 if valor == "Sí" else 0

# Construir DataFrame y asegurar orden correcto
df_input = pd.DataFrame([df_input])
df_input = df_input[orden_columnas]

# Predicción con interpretación de riesgo y acciones
if st.button("Calcular probabilidad de exclusión"):
    proba = modelo.predict_proba(df_input)[0][1]
    st.metric("Probabilidad de exclusión financiera", f"{proba:.2%}")

    # Interpretación por rangos
    if proba <= 0.25:
        estado = "✅ No excluido"
        detalle = "Tu perfil muestra acceso financiero adecuado."
    elif proba <= 0.50:
        estado = "🟡 Riesgo leve de exclusión"
        detalle = "Presentas algunas barreras financieras que podrían limitar tu acceso."
    elif proba <= 0.75:
        estado = "🟠 Excluido financieramente"
        detalle = "Tu acceso a servicios financieros es limitado. Requiere atención."
    else:
        estado = "🔴 Alta exclusión financiera"
        detalle = "Tu perfil refleja una alta probabilidad de estar excluido del sistema financiero."

    # Mostrar interpretación
    st.subheader("Interpretación")
    st.success(estado)
    st.write(detalle)

    # Acciones recomendadas
    st.markdown("### 🧭 ¿Qué puedes hacer para mejorar tu situación financiera?")
    if proba <= 0.25:
        st.markdown("""
            Tu acceso financiero es adecuado. ¡Bien hecho!  
            - Sigue usando los servicios que ya tienes (cuentas, cajeros, pagos digitales).
            - Solo repite esta evaluación si cambias de trabajo, tus ingresos bajan o tu situación personal cambia.
        """)
    elif proba <= 0.50:
        st.markdown("""
            Estás en una etapa temprana de riesgo. Es buen momento para actuar:  
            - Aprende más sobre cómo manejar tu dinero. Hay cursos gratuitos en línea y en tu comunidad.
            - Si necesitas un préstamo, busca opciones que se puedan solicitar desde el celular, sin ir al banco.
            - Usa cajeros automáticos cuando puedas, y si no hay cerca, pregunta por cajeros móviles o tiendas que den servicios financieros.
            - Repite esta evaluación dentro de **1 año** para ver si has mejorado.
        """)
    elif proba <= 0.75:
        st.markdown("""
            Tienes acceso limitado a servicios financieros. Hay formas de avanzar:  
            - Pregunta en tu trabajo o comunidad si hay programas para abrir cuentas bancarias básicas.
            - Aprende a usar apps para pagar, ahorrar o enviar dinero. Muchas son fáciles y seguras.
            - Busca cuentas que premien el uso digital (como no cobrar comisiones si usas la app).
            - Repite esta evaluación dentro de **6 meses** para revisar tu progreso.
        """)
    else:
        st.markdown("""
            Tu situación muestra una alta exclusión financiera. No estás solo, y hay formas de empezar:  
            - Acércate a programas sociales (educación, salud, empleo) que también ayudan a abrir cuentas bancarias.
            - Pregunta por cuentas sin comisiones que se puedan abrir en persona, sin necesidad de internet.
            - Si no tienes celular o internet, busca centros comunitarios donde puedas conectarte o recibir ayuda.
            - Participa en talleres o apoyos para aprender sobre dinero, ahorro y pagos digitales.
            - Repite esta evaluación dentro de **3 meses** para seguir tu avance.
        """)

