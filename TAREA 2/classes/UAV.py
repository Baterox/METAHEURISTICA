class UAV:
    def __init__(self, index:int, early_time:int, preferred_time:int, late_time:int):
        self.index = index
        self.early_time = early_time
        self.preferred_time = preferred_time
        self.late_time = late_time
        self.separation_time = list()