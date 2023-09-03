from UTM.data_viz import Plotter

class TimeStampedValue:
    """Object representation of a value collected at a given timestamp"""
    def __init__(self, timestamp: int, value: any):
        self.timestamp = timestamp
        """The timestamp at which this value was collected"""
        self.value = value
        """The value that was collected at the given timestamp"""
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return str({"timestamp": self.timestamp, "value": self.value})

class DataSink:
    """
    A sink for data.
    Essentially this class collects data and writes them to a file once it's data has been updated update_freq times.
    """
    def __init__(self, name: str, update_freq:int = 200000):
        self.name = name
        """The name of this sink, and also the name of the file this sink will save it's data at. File saves will automatically add a ".log" suffix."""
        self.sink = dict()
        """The data that is being collected constantly."""
        self.__num_updates = 0
        """Internal variable counting the number of times the data in this sink has been updated"""
        self.update_freq = update_freq
        """Once data in the sink has been updated update_freq times, the file will be updated."""
        self.plotter = Plotter(self.name, "Drone ID", "")

    def update(self, id: str, value: any, timestamp: int = None):
        """
        Update data in this sink. 
        id: a unique identifier for this data. if the id exists, the data will be appended to a list of the previously updated data. If the id does not exist, a new list will be created with the current value as the first value of the id.
        value: the value of the data that we are storing in the sink.
        timestamp: the timestamp at which the data is being updated. If it is provided the data will be stored as TimeStampedValue otherwise it will be stored as the value passed in.
        """
        if id in self.sink:
            self.sink[id] += [TimeStampedValue(timestamp, value) if timestamp is not None else value]
        else:
            self.sink[id] = [TimeStampedValue(timestamp, value) if timestamp is not None else value]
        self.__num_updates += 1

        if self.plotter:
            self.plot()

        #self.plotter.update(id, value)
    
    def plot(self):
        xs = []
        ys = []
        colors = []
        for id in self.sink:
            for i in range(len(self.sink[id])):
                if type(self.sink[id][i]) == TimeStampedValue:
                    xs += [self.sink[id][i].timestamp]
                    ys += [self.sink[id][i].value]
                    colors += [id]
                else:
                    xs += [i]
                    ys += [self.sink[id][i]]
                    colors += [id]
        self.plotter.replot(*self.preprocess(xs, ys, colors))

    def preprocess(self, xs, ys, colors):
        return (xs, ys, colors)

    # def preprocess(self, xs, ys, colors):
    #     import pandas as pd
    #     df = pd.DataFrame({'y': ys, 'id': colors})
    #     df = df.groupby(['id']).std().reset_index()
    #     return df['id'], df['y']

    def __repr__(self):
        return str(self.sink)
    
    def __str__(self):
        return self.__repr__()
    
    def save(self, force: bool =False):
        """
        Write the data to the file if there have been more updates than the update_freq.
        force: when true it will force a write even if the __num_updates is not more than the update_freq
        """
        #TODO: change repr to use only append mode!!
        if force or self.__num_updates > self.update_freq:
            with open("logs/" + self.name + ".log", "w") as f:
                f.write(str(self))

