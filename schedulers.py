# schedulers.py

from process import Process

class Scheduler:
    def __init__(self, processes):
        self.processes = processes

    def schedule(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

class FCFS_Scheduler(Scheduler):
    def schedule(self):
        current_time = 0
        for process in sorted(self.processes, key=lambda p: p.arrival_time):
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.start_time = current_time
            process.response_time = process.start_time 
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time

class SJF_Scheduler(Scheduler):
    def schedule(self):
        current_time = 0
        completed = 0
        n = len(self.processes)
        processes = self.processes.copy()
        ready_queue = []
        while completed < n:
            # Agregamos los procesos que han llegado a la cola de listos
            for process in processes:
                if process.arrival_time <= current_time and process not in ready_queue and process.completion_time is None:
                    ready_queue.append(process)
            if ready_queue:
                # Seleccionamos el proceso con el menor burst_time
                if completed == 0:
                    current_process = max(ready_queue, key=lambda p: p.burst_time)
                else:
                    current_process = min(ready_queue, key=lambda p: p.burst_time)
                if current_time < current_process.arrival_time:
                    current_time = current_process.arrival_time
                current_process.start_time = current_time
                current_process.response_time = current_process.start_time 
                current_time += current_process.burst_time
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                completed += 1
                ready_queue.remove(current_process)
            else:
                # Avanzamos el tiempo al siguiente proceso que llega
                future_processes = [p for p in processes if p.completion_time is None and p.arrival_time > current_time]
                if future_processes:
                    current_time = min(p.arrival_time for p in future_processes)
                else:
                    break  # No quedan procesos por planificar
        self.processes = processes

class STCF_Scheduler(Scheduler):
    def schedule(self):
        current_time = 0
        completed = 0
        n = len(self.processes)
        processes = self.processes.copy()
        while completed < n:
            # Obtenemos los procesos que han llegado y tienen tiempo restante
            ready_queue = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
            if ready_queue:
                # Seleccionamos el proceso con el menor tiempo restante
                current_process = min(ready_queue, key=lambda p: p.remaining_time)
                if current_process.start_time is None:
                    current_process.start_time = current_time
                    current_process.response_time = current_process.start_time 
                current_process.remaining_time -= 1
                current_time += 1
                if current_process.remaining_time == 0:
                    current_process.completion_time = current_time
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    completed += 1
            else:
                # Avanzamos el tiempo si no hay procesos listos
                future_processes = [p for p in processes if p.remaining_time > 0 and p.arrival_time > current_time]
                if future_processes:
                    current_time = min(p.arrival_time for p in future_processes)
                else:
                    break  # No quedan procesos por planificar
        self.processes = processes

class RR_Scheduler(Scheduler):
    def __init__(self, processes, quantum):
        super().__init__(processes)
        self.quantum = quantum

    def schedule(self):
        current_time = 0
        queue = []
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        processes_left = processes.copy()
        while processes_left or queue:
            # Agregamos los procesos que han llegado a la cola
            while processes_left and processes_left[0].arrival_time <= current_time:
                process = processes_left.pop(0)
                queue.append(process)
            if not queue:
                # Avanzamos el tiempo al siguiente proceso si la cola está vacía
                if processes_left:
                    current_time = processes_left[0].arrival_time
                else:
                    break
                continue
            process = queue.pop(0)
            if process.start_time is None:
                process.start_time = current_time
                process.response_time = process.start_time 
            execution_time = min(self.quantum, process.remaining_time)
            process.remaining_time -= execution_time
            current_time += execution_time
            # Agregamos nuevos procesos que hayan llegado durante la ejecución
            while processes_left and processes_left[0].arrival_time <= current_time:
                queue.append(processes_left.pop(0))
            if process.remaining_time > 0:
                queue.append(process)
            else:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
        self.processes = processes

class MLQ_Scheduler(Scheduler):
    def __init__(self, processes, num_queues, algorithms_per_queue, quantums_per_queue=None):
        super().__init__(processes)
        self.num_queues = num_queues
        self.algorithms_per_queue = algorithms_per_queue
        self.quantums_per_queue = quantums_per_queue
        self.queues = [[] for _ in range(num_queues)]
        self.schedulers = []

    def assign_processes_to_queues(self):
        for process in self.processes:
            queue_num = process.queue - 1  # Asumiendo que las colas empiezan desde 1
            if 0 <= queue_num < self.num_queues:
                self.queues[queue_num].append(process)
            else:
                print(f"Proceso {process.label} tiene un número de cola inválido: {process.queue}")
        
    def assign_processes_to_queues(self):
        for process in self.processes:
            queue_num = process.queue - 1  # Asumiendo que las colas empiezan desde 1
            if 0 <= queue_num < self.num_queues:
                self.queues[queue_num].append(process)
            else:
                print(f"Proceso {process.label} tiene un número de cola inválido: {process.queue}")

    def schedule(self):
        self.assign_processes_to_queues()
        current_time = 0
        for i in range(self.num_queues):
            queue_processes = self.queues[i]
            if not queue_processes:
                continue
            algorithm = self.algorithms_per_queue[i]
            print(f"\nEjecutando la cola {i + 1} con el algoritmo {algorithm}:")
            if algorithm == 'RR':
                quantum = self.quantums_per_queue[i] if self.quantums_per_queue and i < len(self.quantums_per_queue) else None
                if quantum is None:
                    print(f"Error: Quantum no proporcionado para la cola {i + 1}")
                    return
                scheduler = RR_Scheduler(queue_processes, quantum)
            elif algorithm == 'SJF':
                scheduler = SJF_Scheduler(queue_processes)
            elif algorithm == 'FCFS':
                scheduler = FCFS_Scheduler(queue_processes)
            elif algorithm == 'STCF':
                scheduler = STCF_Scheduler(queue_processes)
            else:
                print(f"Error: Algoritmo no reconocido para la cola {i + 1}")
                return
            # Actualizamos el tiempo de llegada si es necesario
            for process in queue_processes:
                if process.arrival_time < current_time:
                    process.arrival_time = current_time
            scheduler.schedule()
            self.schedulers.append(scheduler)
            if queue_processes:
                current_time = max(process.completion_time for process in queue_processes)
            # Actualizamos TAT y WT para cada proceso
            for process in queue_processes:
                process.turnaround_time = process.completion_time - process.original_arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
