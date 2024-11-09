import pandas as pd

# Ruta del archivo CSV
CSV_FILE_PATH = './df.csv'

# Cargar datos desde el archivo CSV
def cargar_datos():
    df = pd.read_csv(CSV_FILE_PATH)
    df.set_index('Solicitud_id', inplace=True)
    return df

def mostrar_datosPaP():
    df = cargar_datos()
    columns_to_select = ['Numero_tlf', 'Direccion', 'Interacciones']
    existing_columns = [col for col in columns_to_select if col in df.columns]
    new_df = df[existing_columns]
    return new_df

def mostrar_datosCC():
    df = cargar_datos()
    columns_to_select = ['Numero_tlf', 'Interacciones']
    existing_columns = [col for col in columns_to_select if col in df.columns]
    new_df = df[existing_columns]
    return new_df

def mostrar_datosAE():
    df = cargar_datos()
    columns_to_select = ['Numero_tlf', 'Interacciones','Linea credito,tasa interés','Plazo_Meses','Pago,Nivel_Atraso','Edad_cliente']
    existing_columns = [col for col in columns_to_select if col in df.columns]
    new_df = df[existing_columns]
    return new_df

# Función para guardar datos en el archivo CSV
def guardar_datos(row, tp, resultado, promesa):
    # Mapear el tipo de gestión
    tipo_gestion_map = {
        'PaP': 'Gestión Puerta a Puerta',
        'CC': 'Call Center',
        'AE': 'Agencias Especializadas'
    }
    tp = tipo_gestion_map.get(tp, tp)
    
    # Nueva interacción
    nueva_interaccion = {
        'Tipo_Gestión': tp,
        'Resultado': resultado,
        'Promesa_Pago': promesa
    }
    
    # Cargar datos actuales
    df = cargar_datos()
    
    # Convertir la cadena JSON a una lista de diccionarios
    interacciones = eval(df.at[row, 'Interacciones'])
    
    # Añadir la nueva interacción
    interacciones.append(nueva_interaccion)
    
    # Convertir la lista de diccionarios de nuevo a una cadena JSON
    df.at[row, 'Interacciones'] = str(interacciones)
    
    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(CSV_FILE_PATH, index=True)