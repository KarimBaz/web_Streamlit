import streamlit as st
import pandas as pd

import menu as menu

# Validación simple de usuario y clave con un archivo csv
def validarUsuario(usuario,clave):    
    """Permite la validación de usuario y clave

    Args:
        usuario (str): usuario a validar
        clave (str): clave del usuario

    Returns:
        bool: True usuario valido, False usuario invalido
    """    
    dfusuarios = pd.read_csv('usuarios.csv')
    if len(dfusuarios[(dfusuarios['usuario']==usuario) & (dfusuarios['password']==clave)])>0:
        return True
    else:
        return False
    
def validarPuesto(usuario):
    """Permite la validación del puesto del usuario

    Args:
        usuario (str): usuario a validar

    Returns:
        str: puesto del usuario
    """    
    dfusuarios = pd.read_csv('usuarios.csv')
    puesto = dfusuarios[dfusuarios['usuario']==usuario]['puesto'].values[0]
    return puesto

def generarLogin():
    """Genera la ventana de login o muestra el menú si el login es valido
    """    
    # Validamos si el usuario ya fue ingresado    
    if 'usuario' in st.session_state:
        menu.generarMenu(st.session_state['usuario']) # Si ya hay usuario cargamos el menu        
    else: 
        # Cargamos el formulario de login       
        with st.form('frmLogin'):
            parUsuario = st.text_input('Usuario')
            parPassword = st.text_input('Password',type='password')
            btnLogin=st.form_submit_button('Ingresar',type='primary')
            if btnLogin:
                if validarUsuario(parUsuario,parPassword):
                    st.session_state['usuario'] =parUsuario
                    st.session_state['puesto'] =validarPuesto(parUsuario)
                    # Si el usuario es correcto reiniciamos la app para que se cargue el menú
                    st.rerun()
                else:
                    # Si el usuario es invalido, mostramos el mensaje de error
                    st.error("Usuario o clave inválidos",icon=":material/gpp_maybe:")                    

def generarRegistro():
    """Genera la ventana de registro de nuevos usuarios
    """
    with st.form('frmRegistro'):
        parNombre = st.text_input('Nombre')
        parUsuario = st.text_input('Usuario')
        parPassword = st.text_input('Password', type='password')
        parPuesto = st.selectbox('Puesto', ['Puerta a Puerta', 'Call Center', 'Agencia Externa'])
        parPuesto = {'Puerta a Puerta': 'PaP', 'Call Center': 'CC', 'Agencia Externa': 'AE'}.get(parPuesto, parPuesto)
        btnRegistro = st.form_submit_button('Registrar', type='primary')
        if btnRegistro:
            dfusuarios = pd.read_csv('usuarios.csv')
            if parUsuario in dfusuarios['usuario'].values:
                st.error("El usuario ya existe", icon=":material/gpp_maybe:")
            else:
                nuevo_usuario = pd.DataFrame({
                    'nombre': [parNombre],
                    'usuario': [parUsuario],
                    'password': [parPassword],
                    'puesto': [parPuesto],
                })
                dfusuarios = pd.concat([dfusuarios, nuevo_usuario], ignore_index=True)
                dfusuarios.to_csv('usuarios.csv', index=False)
                st.success("Usuario registrado exitosamente", icon=":material/check:")
    
    # Botón para cerrar la sesión fuera del formulario
    btnSalir = st.button("Salir")
    if btnSalir:
        st.session_state.clear()
        # Luego de borrar el Session State reiniciamos la app para mostrar la opción de usuario y clave
        st.rerun()