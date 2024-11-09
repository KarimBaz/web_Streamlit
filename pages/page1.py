import streamlit as st
import pandas as pd

import auth
import logica as lg

auth.generarLogin()
if 'usuario' in st.session_state:
    st.header('Página :blue[1]')

