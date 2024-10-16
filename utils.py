# utils.py

from process import Process

def leer_datos(archivo):
    procesos = []
    try:
        with open(archivo, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split(';')
                if len(parts) < 5:
                    print(f"Línea inválida en el archivo: {line}")
                    continue
                label = parts[0].strip()
                burst_time = int(parts[1].strip())
                arrival_time = int(parts[2].strip())
                queue = int(parts[3].strip())
                priority = int(parts[4].strip())
                proceso = Process(label, burst_time, arrival_time, queue, priority)
                procesos.append(proceso)
        return procesos
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo}' no fue encontrado.")
        return []
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return []

def calcular_promedios(procesos):
    total_tat = sum(proceso.turnaround_time for proceso in procesos if proceso.turnaround_time is not None)
    total_wt = sum(proceso.waiting_time for proceso in procesos if proceso.waiting_time is not None)
    total_rt = sum(proceso.response_time for proceso in procesos if proceso.response_time is not None)
    total_ct = sum(proceso.completion_time for proceso in procesos if proceso.completion_time is not None)
    n = len(procesos)

    promedio_tat = total_tat / n
    promedio_wt = total_wt / n
    promedio_rt = total_rt / n
    promedio_ct = total_ct / n

    promedios = {
        'WT': promedio_wt,
        'CT': promedio_ct,
        'RT': promedio_rt,
        'TAT': promedio_tat
    }

    return promedios

def escribir_resultados(salida_path, archivo_nombre, procesos, promedios):
    try:
        with open(salida_path, 'w') as f:
            # Escribir encabezados
            f.write(f"# archivo: {archivo_nombre}\n")
            f.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n\n")
            # Escribir datos de cada proceso
            for proceso in sorted(procesos, key=lambda p: p.label):
                linea = (f"{proceso.label};{proceso.burst_time};{proceso.original_arrival_time};"
                         f"{proceso.queue};{proceso.priority};{proceso.waiting_time};"
                         f"{proceso.completion_time};{proceso.response_time};{proceso.turnaround_time}\n")
                f.write(linea)
            f.write("\n")
            # Escribir promedios
            f.write(f"WT={promedios['WT']}; CT={promedios['CT']}; RT={promedios['RT']}; TAT={promedios['TAT']};\n")
    except Exception as e:
        print(f"Error al escribir el archivo de salida '{salida_path}': {e}")
