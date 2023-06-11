import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.ion()
figure = plt.figure()
subplot = 1
BUFFER = 200

class Plotter:
    # def __init__(self, title, x_label, y_label):
    #     global animators
    #     self.fig = plt.figure()

    #     self.title = title
    #     self.x_label = x_label
    #     self.y_label = y_label
        
    #     self.ax = self.fig.add_subplot(1, 1, 1)
    #     self.xs = [0] * 20
    #     self.ys = [0] * 20

    #     self.shown = False


    #     # Format plot
    #     # plt.xticks(rotation=45, ha='right')
    #     # plt.subplots_adjust(bottom=0.30)
    #     self.fig.suptitle(self.title)
    #     self.ax.set_ylabel(self.y_label)
    #     self.ax.set_xlabel(self.x_label)

    # def _update(self):
    #     # Draw x and y lists
    #     self.ax.clear()
    #     self.ax.plot(self.xs, self.ys)

    # def update(self, x, y):
    #     self.xs += [x]
    #     self.ys += [y]
    #     self.xs = self.xs[-20:]
    #     self.ys = self.ys[-20:]

    #     if not self.shown:
    #         self.fig.show()
    #         self.shown = True

    #     self._update()

    def __init__(self, title, x_label, y_label):
        global subplot, figure
        self.title = title
        self.xs = []
        self.ys = []
        self.ax = figure.add_subplot(2, 2, subplot)
        self.ax.title.set_text(self.title)
        self.ax.set_xticks([])
        self.plot_no = subplot
        self.frames = 0
        subplot += 1

        # def _update(i):
        #     self.ax.clear()
        #     self.ax.plot(self.xs, self.ys)
        #     # self.figure.pause(0.001)
        #     print("plotted", i)
        #     # plt.pause(0.01)
        
        # self.ani = animation.FuncAnimation(self.figure, _update, interval=10,  repeat=False)
        # plt.show(block = False)
        # plt.pause(0.01)
    
    def update(self, x, y):
        self.frames += 1
        self.xs += [x]
        self.ys += [y]
        # self.figure.clear()
        # print(self.ani)
        if self.frames >= BUFFER:
            self.ax.scatter(self.xs, self.ys)
            plt.draw()
            plt.gcf().canvas.draw_idle()
            plt.gcf().canvas.start_event_loop(0.1)
            self.frames = 0
    
        # self.figure.pause(0.001)
        # print("plotted", i)


        # print(self.title, sum(self.ys) / len(self.ys))


def plot_cont(fun):
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    def update(i):
        if i < 20:
            return
        x = [j * 0.1 for j in range(i-20, i)]
        y = [fun(j) for j in x]
        ax.clear()
        ax.plot(x, y)

    a = animation.FuncAnimation(fig, update, interval=10, repeat=False)
    plt.show()

# from math import sin
# plot_cont(sin)
# print("started")
