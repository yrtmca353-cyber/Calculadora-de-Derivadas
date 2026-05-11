"""
Calculadora de Derivadas - App Web con Streamlit
¡Funciona en tu teléfono desde el navegador!
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sympy as sp
from derivatives_calculator import DerivativesCalculator

# Configuración de página
st.set_page_config(
    page_title="Calculadora de Derivadas",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .title {
        text-align: center;
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("# 📐 Calculadora de Derivadas")
st.markdown("---")

# Inicializar calculadora
if 'calc' not in st.session_state:
    st.session_state.calc = DerivativesCalculator('x')

calc = st.session_state.calc

# SIDEBAR - Entrada
st.sidebar.markdown("## ⚙️ Configuración")
st.sidebar.markdown("---")

# Entrada de expresión
expresion = st.sidebar.text_input(
    "📝 Ingrese la expresión matemática",
    value="x**2 + 3*x + 2",
    help="Ejemplos: x**2, sin(x), exp(x), log(x), sqrt(x)"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔢 Ejemplos")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("x²"):
        st.session_state.expr_example = "x**2"
    if st.button("sin(x)"):
        st.session_state.expr_example = "sin(x)"
    if st.button("e^x"):
        st.session_state.expr_example = "exp(x)"
with col2:
    if st.button("ln(x)"):
        st.session_state.expr_example = "log(x)"
    if st.button("√x"):
        st.session_state.expr_example = "sqrt(x)"
    if st.button("1/x"):
        st.session_state.expr_example = "1/x"

if 'expr_example' in st.session_state:
    expresion = st.session_state.expr_example
    st.session_state.expr_example = None

# MAIN CONTENT
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 📊 Resultados")
    
    if expresion.strip():
        try:
            # Tabs para diferentes cálculos
            tab1, tab2, tab3, tab4 = st.tabs([
                "1ª Derivada", 
                "2ª Derivada", 
                "Simplificar",
                "Evaluación"
            ])
            
            with tab1:
                st.markdown("### Primera Derivada")
                result1 = calc.symbolic_derivative(expresion, order=1)
                simplified1 = calc.simplify_derivative(expresion, order=1)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Expresión original:**")
                    st.code(expresion, language="python")
                with col_b:
                    st.markdown("**Derivada:**")
                    st.code(result1, language="python")
                
                st.markdown("**Simplificada:**")
                st.info(simplified1)
            
            with tab2:
                st.markdown("### Segunda Derivada")
                result2 = calc.symbolic_derivative(expresion, order=2)
                simplified2 = calc.simplify_derivative(expresion, order=2)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Expresión original:**")
                    st.code(expresion, language="python")
                with col_b:
                    st.markdown("**Segunda Derivada:**")
                    st.code(result2, language="python")
                
                st.markdown("**Simplificada:**")
                st.info(simplified2)
            
            with tab3:
                st.markdown("### Simplificar Derivada")
                simplified = calc.simplify_derivative(expresion, order=1)
                st.markdown("**Derivada simplificada:**")
                st.code(simplified, language="python")
            
            with tab4:
                st.markdown("### Evaluar en un punto")
                x_valor = st.number_input(
                    "Ingrese el valor de x:",
                    value=1.0,
                    step=0.1
                )
                
                resultado_eval = calc.evaluate_derivative(expresion, x_valor, order=1)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Valor de x", x_valor)
                with col_b:
                    st.metric("f'(x)", f"{resultado_eval:.4f}")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Verifique que la expresión sea válida. Ejemplos: x**2, sin(x), exp(x)")
    else:
        st.warning("⚠️ Por favor ingrese una expresión matemática")

with col2:
    st.markdown("## 📚 Ayuda")
    st.markdown("""
    **Funciones disponibles:**
    - `sin(x)` - Seno
    - `cos(x)` - Coseno
    - `tan(x)` - Tangente
    - `exp(x)` - e^x
    - `log(x)` - ln(x)
    - `sqrt(x)` - √x
    - `x**2` - x²
    - `x**3` - x³
    - `1/x` - 1/x
    
    **Operadores:**
    - `+` suma
    - `-` resta
    - `*` multiplicación
    - `/` división
    - `**` potencia
    """)

# GRÁFICOS
st.markdown("---")
st.markdown("## 📈 Gráficos")

if expresion.strip():
    try:
        # Preparar función
        var = sp.symbols('x')
        expr_obj = sp.sympify(expresion)
        f = sp.lambdify(var, expr_obj, 'numpy')
        f_prime = sp.diff(expr_obj, var)
        f_prime_func = sp.lambdify(var, f_prime, 'numpy')
        
        # Rango
        col_range1, col_range2 = st.columns(2)
        with col_range1:
            x_min = st.number_input("x mínimo:", value=-5.0, step=0.5)
        with col_range2:
            x_max = st.number_input("x máximo:", value=5.0, step=0.5)
        
        x_vals = np.linspace(x_min, x_max, 300)
        
        try:
            y_vals = f(x_vals)
            y_prime_vals = f_prime_func(x_vals)
        except:
            x_vals = np.linspace(-2, 2, 300)
            y_vals = f(x_vals)
            y_prime_vals = f_prime_func(x_vals)
        
        # Gráfico con Plotly
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode='lines',
            name='f(x)',
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_prime_vals,
            mode='lines',
            name="f'(x)",
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=f"Función y su Derivada",
            xaxis_title="x",
            yaxis_title="y",
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error al graficar: {str(e)}")

# SERIE DE TAYLOR
st.markdown("---")
st.markdown("## 🔧 Serie de Taylor")

if expresion.strip():
    try:
        col_taylor1, col_taylor2 = st.columns(2)
        with col_taylor1:
            punto_taylor = st.number_input("Punto de expansión:", value=0.0, step=0.5)
        with col_taylor2:
            n_terminos = st.slider("Número de términos:", 2, 10, 5)
        
        serie = calc.taylor_series(expresion, point=punto_taylor, n_terms=n_terminos)
        st.info(f"**Expansión:** {serie}")
        
    except Exception as e:
        st.error(f"Error en serie de Taylor: {str(e)}")

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    📐 Calculadora de Derivadas con Streamlit | v1.0
</div>
""", unsafe_allow_html=True)
