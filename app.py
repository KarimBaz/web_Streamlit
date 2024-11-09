import streamlit as st
import pandas as pd

import auth
import menu
import logica as lg

# Configuración de la página
st.set_page_config(
    page_title="Dimex", 
    page_icon="./favicon.ico"  
)

st.title(':green[Dimex]')

if 'usuario' not in st.session_state:
    st.header(':orange[Login]')
    auth.generarLogin()
else:
    if st.session_state['usuario'] == 'admin':
        st.header(':orange[Registrar]')
        auth.generarRegistro()
    else:
        if st.session_state['puesto'] == 'PaP':
            st.header('Página de :orange[Gestión Puerta a Puerta]')
            st.write(lg.mostrar_datosPaP())
        elif st.session_state['puesto'] == 'CC':
            st.header('Página de :orange[Call Center]')
            st.write(lg.mostrar_datosCC())
        elif st.session_state['puesto'] == 'AE':
            st.header('Página de :orange[Agencias Especializadas]')
            st.write(lg.mostrar_datosAE())

        #st.header('Página :orange[principal]')
        menu.generarMenu(st.session_state['usuario'])

        # Cargar el DataFrame cada vez que se abre la página
        df = lg.cargar_datos()
        
        # Agregar un selectbox para elegir una fila
        selected_row = st.selectbox('Seleccione una fila:', df.index)

        # Mostrar la fila seleccionada
        st.write('Fila seleccionada:')
        st.write(df.loc[selected_row].to_frame().T)
        
        # Botón para abrir el formulario de detalles del cliente
        with st.form(key='detalle_cliente_form', clear_on_submit=True):
            # Selectboxes para resultado y promesa
            resultado = st.selectbox('Resultado:', ['Atendió cliente', 'Atendió un tercero', 'No localizado'], key='resultado')
            promesa = st.selectbox('Promesa:', ['Si', 'No', 'None'], key='promesa')
            
            # Botón de envío
            submit_button = st.form_submit_button(label='Guardar')
        
            # Lógica de guardado al enviar el formulario
            if submit_button:
                if 'puesto' in st.session_state:
                    lg.guardar_datos(selected_row, st.session_state['puesto'], resultado, promesa)
                    st.success('Datos guardados exitosamente')
                    st.experimental_set_query_params(page="pages/page1.py")
                    #st.experimental.rerun()  # Recargar la página para actualizar la tabla
                else:
                    st.error('Error: puesto no definido en session_state')
