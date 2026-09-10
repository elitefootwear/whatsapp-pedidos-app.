import streamlit as st
import urllib.parse

# ---------------------------------------------------------
# Configuración de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Catálogo de Pedidos",
    page_icon="🛍️",
    layout="wide"
)

# ---------------------------------------------------------
# Estilos visuales personalizados (Colores de WhatsApp)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Estilo del botón verde principal de WhatsApp */
    div.stButton > button:first-child {
        background-color: #25D366 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
    }
    
    /* Efecto al pasar el mouse sobre el botón */
    div.stButton > button:first-child:hover {
        background-color: #128C7E !important;
        color: white !important;
    }

    /* Color de títulos principales */
    h1, h2, h3 {
        color: #128C7E;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Inicialización del estado del catálogo
# ---------------------------------------------------------
if 'catalogo' not in st.session_state:
    st.session_state.catalogo = [
        {
            "id": 1,
            "nombre": "Calzado Deportivo",
            "precio": 150000,
            "imagen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"
        }
    ]

# ---------------------------------------------------------
# Barra Lateral (Sidebar): Configuración y administración
# ---------------------------------------------------------
st.sidebar.header("⚙️ Configuración del Negocio")
nombre_tienda = st.sidebar.text_input("Nombre de la Tienda:", value="Mi Tienda")
telefono_whatsapp = st.sidebar.text_input("Número de WhatsApp (con código país):", value="595981123456")

st.sidebar.markdown("---")
st.sidebar.header("➕ Agregar Nuevo Producto")

nuevo_nombre = st.sidebar.text_input("Nombre del producto:")
nuevo_precio = st.sidebar.number_input("Precio (Gs.):", min_value=0, step=5000)
nueva_imagen = st.sidebar.text_input("URL de foto (opcional):", value="https://via.placeholder.com/150")

if st.sidebar.button("Añadir Producto al Catálogo"):
    if nuevo_nombre and nuevo_precio > 0:
        nuevo_id = len(st.session_state.catalogo) + 1
        st.session_state.catalogo.append({
            "id": nuevo_id,
            "nombre": nuevo_nombre,
            "precio": nuevo_precio,
            "imagen": nueva_imagen if nueva_imagen else "https://via.placeholder.com/150"
        })
        st.sidebar.success(f"¡'{nuevo_nombre}' agregado con éxito!")
    else:
        st.sidebar.error("Por favor completa el nombre y un precio válido.")

if st.sidebar.button("Limpiar todo el catálogo"):
    st.session_state.catalogo = []
    st.sidebar.warning("Catálogo vaciado.")

# ---------------------------------------------------------
# Pantalla Principal: Vista del Cliente
# ---------------------------------------------------------
st.title(f"🛍️ Catálogo de {nombre_tienda}")
st.write("Selecciona los productos y envía tu pedido directamente por WhatsApp.")

pedido = {}
cols = st.columns(3)

for idx, prod in enumerate(st.session_state.catalogo):
    with cols[idx % 3]:
        if prod.get("imagen"):
            st.image(prod["imagen"], use_container_width=True)
        st.subheader(prod["nombre"])
        st.write(f"**Precio:** Gs. {prod['precio']:,}")
        
        cantidad = st.number_input(
            f"Cantidad", 
            min_value=0, 
            max_value=20, 
            value=0, 
            key=f"prod_{prod['id']}"
        )
        if cantidad > 0:
            pedido[prod["nombre"]] = {
                "cantidad": cantidad,
                "precio_unitario": prod["precio"],
                "subtotal": cantidad * prod["precio"]
            }

st.markdown("---")

# ---------------------------------------------------------
# Resumen del Pedido y Generador de Enlace WhatsApp
# ---------------------------------------------------------
if pedido:
    st.header("📋 Resumen de tu Pedido")
    total = 0
    texto_mensaje = f"Hola *{nombre_tienda}*, me gustaría realizar el siguiente pedido:\n\n"
    
    for item, datos in pedido.items():
        st.write(f"- **{item}** x{datos['cantidad']} = Gs. {datos['subtotal']:,}")
        texto_mensaje += f"• {item} x{datos['cantidad']} = Gs. {datos['subtotal']:,}\n"
        total += datos["subtotal"]
        
    st.markdown(f"### **Total a Pagar:** Gs. {total:,}")
    texto_mensaje += f"\n*Total:* Gs. {total:,}\n\n¡Quedo a la espera de su confirmación!"
    
    # Crear enlace URL formateado para WhatsApp
    mensaje_encoded = urllib.parse.quote(texto_mensaje)
    link_whatsapp = f"https://wa.me/{telefono_whatsapp}?text={mensaje_encoded}"
    
    st.markdown(f'<a href="{link_whatsapp}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:12px 24px; font-size:16px; font-weight:bold; border-radius:8px; cursor:pointer;">📲 Enviar Pedido por WhatsApp</button></a>', unsafe_allow_html=True)
else:
    st.info("Selecciona al menos 1 unidad de algún producto para generar el pedido.")
