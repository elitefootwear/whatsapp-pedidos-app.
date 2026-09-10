import streamlit as st
import urllib.parse

st.set_page_config(page_title="Generador de Pedidos WhatsApp", layout="wide", page_icon="🛍️")

# Inicializar lista de productos en la sesión si no existe
if "productos" not in st.session_state:
    st.session_state.productos = [
        {"nombre": "Calzado Deportivo", "precio": 150000, "imagen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"},
        {"nombre": "Camiseta Casual", "precio": 80000, "imagen": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=400"}
    ]

# --- BARRA LATERAL: CONFIGURACIÓN DEL COMERCIANTE ---
with st.sidebar:
    st.header("⚙️ Tu Negocio")
    nombre_tienda = st.text_input("Nombre de tu Negocio:", value="Mi Tienda")
    telefono = st.text_input("WhatsApp (con código país):", value="595981123456", help="Ejemplo: 595981123456 para Paraguay")

    st.divider()
    st.header("➕ Agregar Nuevo Producto")
    nuevo_nombre = st.text_input("Nombre del producto:")
    nuevo_precio = st.number_input("Precio (Gs.):", min_value=0, step=5000)
    nueva_imagen = st.text_input("URL de foto (opcional):", placeholder="https://...")

    if st.button("Añadir Producto al Catálogo", type="primary"):
        if nuevo_nombre and nuevo_precio > 0:
            img_url = nueva_imagen if nueva_imagen else "https://via.placeholder.com/150"
            st.session_state.productos.append({
                "nombre": nuevo_nombre,
                "precio": int(nuevo_precio),
                "imagen": img_url
            })
            st.success(f"¡'{nuevo_nombre}' agregado con éxito!")
            st.rerun()
        else:
            st.warning("Completa el nombre y precio del producto.")

    if st.button("Limpiar todo el catálogo"):
        st.session_state.productos = []
        st.rerun()

# --- PÁGINA PRINCIPAL: CATÁLOGO Y PEDIDOS ---
st.title(f"🛍️ Catálogo de {nombre_tienda}")
st.write("Selecciona los productos y envía tu pedido directamente por WhatsApp.")

if not st.session_state.productos:
    st.info("👈 Tu catálogo está vacío. Agrega productos desde el menú de la izquierda.")
else:
    carrito = []
    total = 0

    # Desplegar productos en tarjetas/columnas
    cols = st.columns(3)
    for index, prod in enumerate(st.session_state.productos):
        with cols[index % 3]:
            st.image(prod["imagen"], use_container_width=True)
            st.subheader(prod["nombre"])
            st.write(f"**Precio:** Gs. {prod['precio']:,}")
            
            cant = st.number_input(f"Cantidad", min_value=0, max_value=20, key=f"prod_{index}")
            if cant > 0:
                subtotal = prod["precio"] * cant
                carrito.append(f"- {cant}x {prod['nombre']} (Gs. {subtotal:,})")
                total += subtotal

    st.divider()

    # --- RESUMEN DE COMPRA Y BOTÓN WHATSAPP ---
    if total > 0:
        st.subheader(f"Total a Pagar: Gs. {total:,}")
        
        # Armar el mensaje para WhatsApp
        mensaje = f"Hola *{nombre_tienda}*, quiero realizar el siguiente pedido:\n\n"
        mensaje += "\n".join(carrito)
        mensaje += f"\n\n*Total:* Gs. {total:,}\n\n¿Me confirman disponibilidad y forma de pago?"
        
        mensaje_url = urllib.parse.quote(mensaje)
        enlace_wa = f"https://wa.me/{telefono}?text={mensaje_url}"
        
        st.link_button("📲 Enviar Pedido por WhatsApp", enlace_wa, type="primary")