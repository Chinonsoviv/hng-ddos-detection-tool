import statistics

class BaselineManager:
    def __init__(self):
        # Store counts per second for the last 1800 seconds (30 mins)
        self.history = [0] * 1800 
        self.mean = 0.0
        self.stddev = 1.0 # Start at 1 to avoid div by zero

    def update_history(self, current_rate):
        self.history.pop(0)
        self.history.append(current_rate)
        
    def recalculate(self):
        if len(self.history) > 1:
            self.mean = statistics.mean(self.history)
            self.stddev = statistics.stdev(self.history)
            if self.stddev == 0: self.stddev = 0.1 # Floor value
