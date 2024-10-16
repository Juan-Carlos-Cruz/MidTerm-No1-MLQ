# process.py

class Process:
    def __init__(self, label, burst_time, arrival_time, queue, priority):
        self.label = label
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.queue = queue
        self.priority = priority

        # Inicializamos los atributos para las métricas de planificación
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.turnaround_time = None
        self.waiting_time = None
        self.response_time = None
        self.original_arrival_time = arrival_time  # Para MLQ

    def __repr__(self):
        return (f"Process({self.label}, BT={self.burst_time}, AT={self.arrival_time}, "
                f"Q={self.queue}, P={self.priority})")
