import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Generador de Gráficos de Puntos",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 Generador de Gráficos de Puntos")
st.markdown("Ingresa los valores para X, Y y R (máximo 12 elementos cada uno)")

# Inicializar session state para almacenar datos
if 'datos' not in st.session_state:
    st.session_state.datos = {
        'x': [],
        'y': [], 
        'r': []
    }

if 'contador' not in st.session_state:
    st.session_state.contador = 0

# Función para agregar datos
def agregar_dato():
    if (st.session_state.contador < 12 and 
        st.session_state.input_x != "" and 
        st.session_state.input_y != "" and 
        st.session_state.input_r != ""):
        try:
            x_val = float(st.session_state.input_x)
            y_val = float(st.session_state.input_y)
            r_val = float(st.session_state.input_r)
            
            st.session_state.datos['x'].append(x_val)
            st.session_state.datos['y'].append(y_val)
            st.session_state.datos['r'].append(r_val)
            st.session_state.contador += 1
            
            # Limpiar inputs
            st.session_state.input_x = ""
            st.session_state.input_y = ""
            st.session_state.input_r = ""
            
        except ValueError:
            st.error("❌ Por favor ingresa números válidos")

# Función para limpiar datos
def limpiar_datos():
    st.session_state.datos = {'x': [], 'y': [], 'r': []}
    st.session_state.contador = 0

# Función para generar gráfico
def generar_grafico():
    if len(st.session_state.datos['x']) > 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Crear scatter plot
        scatter = ax.scatter(
            st.session_state.datos['x'], 
            st.session_state.datos['y'], 
            c=st.session_state.datos['r'],
            cmap='viridis', 
            s=100, 
            alpha=0.7,
            edgecolors='black',
            linewidth=0.5
        )
        
        # Añadir etiquetas a cada punto
        for i, (x, y, r) in enumerate(zip(
            st.session_state.datos['x'], 
            st.session_state.datos['y'], 
            st.session_state.datos['r']
        )):
            ax.annotate(
                f'({x:.1f}, {y:.1f})\nR={r:.1f}', 
                (x, y), 
                xytext=(8, 8), 
                textcoords='offset points',
                fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8)
            )
        
        # Personalizar el gráfico
        ax.set_xlabel('Valores X', fontsize=12, fontweight='bold')
        ax.set_ylabel('Valores Y', fontsize=12, fontweight='bold')
        ax.set_title('Gráfico de Puntos - X vs Y (Color: R)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Añadir barra de color
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Valores R', fontsize=10)
        
        # Ajustar límites del gráfico
        if len(st.session_state.datos['x']) > 1:
            margin_x = (max(st.session_state.datos['x']) - min(st.session_state.datos['x'])) * 0.1
            margin_y = (max(st.session_state.datos['y']) - min(st.session_state.datos['y'])) * 0.1
            ax.set_xlim(min(st.session_state.datos['x']) - margin_x, max(st.session_state.datos['x']) + margin_x)
            ax.set_ylim(min(st.session_state.datos['y']) - margin_y, max(st.session_state.datos['y']) + margin_y)
        
        return fig
    else:
        st.warning("⚠️ No hay datos para generar el gráfico")
        return None

# Sidebar para ingreso de datos
with st.sidebar:
    st.header("➕ Ingresar Datos")
    st.write(f"**Puntos agregados:** {st.session_state.contador}/12")
    
    # Inputs para datos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.text_input(
            "Valor X:",
            key="input_x",
            placeholder="0.0",
            help="Ingresa un valor numérico para X"
        )
    
    with col2:
        st.text_input(
            "Valor Y:",
            key="input_y", 
            placeholder="0.0",
            help="Ingresa un valor numérico para Y"
        )
    
    with col3:
        st.text_input(
            "Valor R:",
            key="input_r",
            placeholder="0.0", 
            help="Ingresa un valor numérico para R"
        )
    
    # Botones de acción
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        st.button(
            "➕ Agregar Punto",
            on_click=agregar_dato,
            use_container_width=True,
            disabled=st.session_state.contador >= 12
        )
    
    with col_btn2:
        st.button(
            "🗑️ Limpiar Todo", 
            on_click=limpiar_datos,
            use_container_width=True
        )
    
    st.markdown("---")
    st.info("💡 **Instrucciones:**\n1. Ingresa valores para X, Y y R\n2. Haz clic en 'Agregar Punto'\n3. Repite hasta tener todos los puntos\n4. Haz clic en 'Generar Gráfico'")

# Área principal
col_left, col_right = st.columns([2, 1])

with col_left:
    st.header("📈 Visualización del Gráfico")
    
    # Botón para generar gráfico
    if st.button(
        "🚀 Generar Gráfico", 
        use_container_width=True,
        type="primary",
        disabled=len(st.session_state.datos['x']) == 0
    ):
        fig = generar_grafico()
        if fig:
            st.pyplot(fig)

with col_right:
    st.header("📋 Datos Ingresados")
    
    if len(st.session_state.datos['x']) > 0:
        # Mostrar datos en tabla
        df = pd.DataFrame({
            'Punto': range(1, len(st.session_state.datos['x']) + 1),
            'X': st.session_state.datos['x'],
            'Y': st.session_state.datos['y'],
            'R': st.session_state.datos['r']
        })
        
        st.dataframe(df, use_container_width=True, height=400)
        
        # Estadísticas rápidas
        st.subheader("📊 Estadísticas")
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.metric("Total Puntos", len(st.session_state.datos['x']))
            st.metric("X Promedio", f"{np.mean(st.session_state.datos['x']):.2f}")
            
        with col_stat2:
            st.metric("Y Promedio", f"{np.mean(st.session_state.datos['y']):.2f}")
            st.metric("R Promedio", f"{np.mean(st.session_state.datos['r']):.2f}")
    else:
        st.info("📝 No hay datos ingresados aún")

# Sección de ejemplos
with st.expander("🎯 Ejemplos de Uso"):
    st.markdown("""
    **Ejemplo 1: Datos simples**
    ```
    X: 1.0, 2.0, 3.0, 4.0
    Y: 2.0, 4.0, 6.0, 8.0  
    R: 1.0, 2.0, 3.0, 4.0
    ```
    
    **Ejemplo 2: Datos con decimales**
    ```
    X: 1.5, 2.3, 3.7, 4.1
    Y: 2.1, 3.8, 1.2, 5.6
    R: 0.5, 1.5, 2.5, 3.5
    ```
    
    **Ejemplo 3: Datos aleatorios**
    ```
    X: Valores entre 0 y 10
    Y: Valores entre 0 y 10
    R: Valores entre 1 y 5
    ```
    """)

# Footer
st.markdown("---")
st.caption("✨ Aplicación creada con Streamlit - Generador de Gráficos de Puntos")
