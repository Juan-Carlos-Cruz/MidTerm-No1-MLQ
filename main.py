# main.py

import os
from process import Process
from schedulers import  MLQ_Scheduler
from utils import leer_datos, calcular_promedios, escribir_resultados

def main():
    # Preguntar al usuario por el número de archivos a procesar
    num_files = int(input("Ingrese el número de archivos txt a procesar: "))
    
    # Carpeta donde se encuentran los archivos de entrada
    entradas_folder = 'entradas'
    salidas_folder = 'salidas'  # Carpeta para los archivos de salida
    
    # Verificar si la carpeta de entradas existe
    if not os.path.exists(entradas_folder):
        print(f"La carpeta '{entradas_folder}' no existe.")
        return
    
    # Crear la carpeta de salidas si no existe
    if not os.path.exists(salidas_folder):
        os.makedirs(salidas_folder)
    
    # Obtener la lista de archivos .txt en la carpeta 'entradas'
    all_files = [f for f in os.listdir(entradas_folder) if f.endswith('.txt')]
    
    if not all_files:
        print(f"No se encontraron archivos txt en la carpeta '{entradas_folder}'.")
        return
    
    # Asegurarse de no exceder el número de archivos disponibles
    if num_files > len(all_files):
        print(f"Solo hay {len(all_files)} archivos disponibles. Se procesarán todos ellos.")
        num_files = len(all_files)
    
    # Seleccionar los archivos a procesar
    files_to_process = all_files[:num_files]
    
    # Procesar cada archivo
    for archivo in files_to_process:
        print(f"\nProcesando archivo: {archivo}")
        archivo_path = os.path.join(entradas_folder, archivo)
        procesos = leer_datos(archivo_path)
    
        if not procesos:
            print(f"No se pudieron leer procesos del archivo '{archivo}'.")
            continue  # Pasar al siguiente archivo
    
        # Solo usaremos MLQ
        num_colas = int(input("Ingrese el número de colas para MLQ: "))
        algoritmos_por_cola = []
        quantum_por_cola = []

        for i in range(num_colas):
            algoritmo_cola = input(f"Seleccione el algoritmo para la cola {i+1} (RR, SJF, FCFS, STCF): ").strip().upper()
            algoritmos_por_cola.append(algoritmo_cola)
            if algoritmo_cola == "RR":
                quantum = int(input(f"Ingrese el quantum para la cola {i+1}: "))
                quantum_por_cola.append(quantum)
            else:
                quantum_por_cola.append(None)
    
        scheduler = MLQ_Scheduler(procesos, num_colas, algoritmos_por_cola, quantum_por_cola)
    
        # Ejecutar el planificador
        scheduler.schedule()
    
        # Calcular promedios
        promedios = calcular_promedios(procesos)
    
        # Escribir los resultados en un archivo de salida
        salida_path = os.path.join(salidas_folder, archivo)
        escribir_resultados(salida_path, archivo, procesos, promedios)
    
        print(f"Resultados guardados en '{salida_path}'")
    
    print("\nProcesamiento completado para todos los archivos.")

if __name__ == "__main__":
    main()
