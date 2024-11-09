import streamlit as st
import auth

auth.generarLogin()
if 'usuario' in st.session_state:
    st.header('Página :green[3]')