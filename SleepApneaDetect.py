import numpy as np
import matplotlib.pyplot as plt
import time
# import test_menu as tm
import sys


class SleepApneaDetect:
    def __init__(self):
        self.record_length = 5  # We are keeping 15 seconds worth of data
        self.graph_length = 30
        self.record = np.zeros(self.graph_length)  # Array to store data
        self.num_item_in_list = 0
        self.sleep_apnea = False
        self.update_rate = 1  # updating every second
        plt.rcParams['toolbar'] = 'None'
        self.fig, self.ax = plt.subplots()
        self.line1, = self.ax.plot(self.record)
        self.fig.show()
        plt.xlim(0, 30)
        plt.ylim(0, 12)
        plt.xlabel("Seconds (s)")
        plt.ylabel("Delta to Beta Ratio")

    def update(self, new_value, plot_graph="True"):
        # Using np.roll to simulate a queue structure
        self.record = np.roll(self.record, -self.update_rate)
        self.record[(self.graph_length - self.update_rate)] = new_value
        # print(self.record[self.graph_length - 1])
        self.num_item_in_list += 1
        if plot_graph:
            self.plot_data()

        if not self.sleep_apnea:
            temp_bool = self.detect_start()
            if temp_bool:
                self.sleep_apnea = temp_bool
                print("Sleep Apnea")
                return True
        else:
            temp_bool = self.detect_end()
            if temp_bool is False:
                self.sleep_apnea = temp_bool
                print("Safe")
                return False
        # time.sleep(1)
        return self.sleep_apnea

    def plot_data(self):
        self.line1.set_ydata(self.record)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def detect_start(self):
        drop, old = 2, 3  # data compare ratio

        if self.num_item_in_list >= self.record_length:
            # Calculating average
            old_avg = sum(self.record[(self.graph_length - self.record_length):
                                      (self.graph_length - old + 1)]) / old
            drop_avg = sum(self.record[(self.graph_length - old + 1):]) / drop
            # spike_avg = sum(self.record[self.graph_length - drop:]) / spike

            # Detection based on ratio difference
            drop_ratio = 0.5
            # print(self.record)
            """print(self.record[(self.graph_length - self.record_length - 1):(self.graph_length - drop - spike)])
            print(self.record[(self.graph_length - drop - spike):self.graph_length - drop])
            print(self.record[self.graph_length - drop:])
            print(old_avg, drop_avg, spike_avg)
            print(spike_ratio * old_avg, drop_ratio * drop_avg)"""
            if drop_avg < drop_ratio * old_avg:
                return True  # Sleep Apnea

    def detect_end(self):
        length = 3  # number of seconds over which we are averaging the value
        detection_ratio = 2.5

        if self.num_item_in_list >= self.record_length:
            overall_avg = sum(self.record[(self.graph_length - self.record_length)
                                          :(self.graph_length - length)]) / (self.record_length - length)
            high_avg = sum(self.record[(self.graph_length - length):]) / length

            """print(self.record[(self.graph_length - self.record_length):(self.graph_length - length)])
            print(self.record[(self.graph_length - length):])
            print(overall_avg, high_avg)
            print(overall_avg * detection_ratio)"""
            # Detection base on ratio difference
            if high_avg > overall_avg * detection_ratio:
                return False

    def print_data(self):
        for d in self.record:
            print(d)


if __name__ == "__main__":
    data = SleepApneaDetect()
    app = tm.QApplication(sys.argv)
    win = tm.MenuWindow()
    win.show()
    testData = [5.715187348624481, 5.673257720967051, 5.649467225521545, 5.665105595989914,
                5.737902873218203, 5.731773638799287, 5.7283130478142565, 5.565140710684277, 2.5610874026885915,
                1.1098416466178829, 1.484445742223451,
                2.5610874026885915, 1.484125376672232,
                2.5610874026885915, 1.4921133700125906,
                1.5028568339920239, 1.4894132977722276,
                1.481514487902809, 2.0934834070644106,
                1.3146429767970262, 7.828288934925429,
                5.7372248170443925, 5.773551077845704,
                7.828288934925429, 5.775365285511127,
                7.828288934925429]
    for i in testData:
        data.update(i)
        win.sa_bool = data.sleep_apnea
    sys.exit(app.exec())
