import json
import os

# Ruta relativa desde la carpeta backend
ruta_archivo = os.path.join("config", "firebase-key.json")

def diagnosticar_archivo():
    print(f"--- Diagnosticando: {ruta_archivo} ---")
    
    if not os.path.exists(ruta_archivo):
        print(f"El archivo no existe en: {os.path.abspath(ruta_archivo)}")
        return

    tamanio = os.path.getsize(ruta_archivo)
    print(f"Tamaño del archivo: {tamanio} bytes")

    if tamanio == 0:
        print("ERROR: El archivo está vacío. Debes copiar el contenido del JSON de Firebase.")
        return

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            print("¡ÉXITO! El JSON es válido.")
            print(f"ID del Proyecto: {datos.get('project_id')}")
    except json.JSONDecodeError as e:
        print(f"ERROR de formato JSON: {e}")
        print("Sugerencia: Abre el archivo en VS Code y asegúrate de que no tenga texto extra fuera de las llaves { }.")

if __name__ == "__main__":
    diagnosticar_archivo()