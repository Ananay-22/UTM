class TimeStampedValue:
    def __init__(self, timestamp: str, value: any):
        self.timestamp = timestamp
        self.value = value
    
    def __str__(self):
        return str({"timestamp": self.timestamp, "value": self.value})
    
    def __repr__(self):
        return str(self)

class DataSink:
    def __init__(self, name: str):
        self.name = name
        self.sink = dict()
        self.__num_updates = 0

    def update(self, id: str, value: any, timestamp: int = None):
        if id in self.sink:
            self.sink[id] += [TimeStampedValue(timestamp, value) if timestamp is not None else value]
        else:
            self.sink[id] = [TimeStampedValue(timestamp, value) if timestamp is not None else value]
        self.__num_updates += 1

    def __repr__(self):
        return str(self.sink)
    
    def __str__(self):
        return str(self.sink)
    
    def save(self, force=False):
        #TODO: change repr to use only append mode!!
        if force or self.__num_updates > 100:
            with open("logs/" + self.name + ".log", "w") as f:
                f.write(str(self))

