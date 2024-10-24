import numpy as np
import matplotlib.pyplot as plt

class DiscreteSignal:
    def __init__(self, INF):
        """
        Initialize the DiscreteSignal with a numpy array of signal values within the range (-INF, INF).
        :param INF: A constant that determines the range of the signal values.
        """
        self.INF = INF
        self.values = np.zeros(2 * INF + 1)  # Create a signal array of size 2 * INF + 1 (to cover -INF to INF)
        self.time_indices = np.arange(-INF, INF + 1)

    def set_value_at_time(self, time, value):
        """
        Sets the value of the signal at a specific time index.
        :param time: Time index at which the value is set.
        :param value: The value to be set at the time index.
        """
        if -self.INF <= time <= self.INF:
            self.values[time + self.INF] = value  # Shift the index for proper placement
        else:
            raise ValueError("Time index out of range")

    def shift_signal(self, shift):
        """
        Shift the signal by the specified amount and return a new DiscreteSignal object.
        :param shift: The amount to shift the signal by.
        :return: A new DiscreteSignal instance with the shifted signal.
        """
        shifted_signal = DiscreteSignal(self.INF)
        shifted_signal.values = np.roll(self.values, shift)
        return shifted_signal

    def add(self, other):
        """
        Add another DiscreteSignal to the current signal.
        :param other: The DiscreteSignal instance to add.
        :return: A new DiscreteSignal instance representing the sum.
        """
        if self.INF != other.INF:
            raise ValueError("Both signals must have the same INF value")
        added_signal = DiscreteSignal(self.INF)
        added_signal.values = self.values + other.values
        return added_signal

    def multiply(self, other):
        """
        Perform element-wise multiplication with another DiscreteSignal.
        :param other: The DiscreteSignal instance to multiply with.
        :return: A new DiscreteSignal instance representing the element-wise product.
        """
        if self.INF != other.INF:
            raise ValueError("Both signals must have the same INF value")
        multiplied_signal = DiscreteSignal(self.INF)
        multiplied_signal.values = self.values * other.values
        return multiplied_signal

    def multiply_const_factor(self, factor):
        """
        Multiply the signal by a constant factor.
        :param factor: The scalar factor to multiply the signal with.
        :return: A new DiscreteSignal instance multiplied by the factor.
        """
        scaled_signal = DiscreteSignal(self.INF)
        scaled_signal.values = self.values * factor
        return scaled_signal

    def plot(self, title="Discrete Signal", color='blue'):
        """
        Plot the signal values against the time indices.
        :param title: The title of the plot.
        :param color: The color of the plot.
        """
        plt.stem(self.time_indices, self.values)
        plt.title(title)
        plt.xlabel("Time Index")
        plt.ylabel("Signal Value")
        plt.grid()
        plt.show()
    

# Example Usage:
if __name__ == "__main__":
    INF = 5  # Define the range of the signal
    signal1 = DiscreteSignal(INF)

    # Set values for signal1
    signal1.set_value_at_time(0, 1)
    signal1.set_value_at_time(1, 2)
    signal1.set_value_at_time(2, 3)

    # Plot the original signal
    signal1.plot(title="Original Signal")

    # Shift the signal by 2 units
    shifted_signal = signal1.shift_signal(2)
    shifted_signal.plot(title="Shifted Signal")

    # Add two signals
    signal2 = DiscreteSignal(INF)
    signal2.set_value_at_time(0, 2)
    signal2.set_value_at_time(1, 4)
    added_signal = signal1.add(signal2)
    added_signal.plot(title="Added Signal")

    # Multiply two signals element-wise
    multiplied_signal = signal1.multiply(signal2)
    multiplied_signal.plot(title="Multiplied Signal")

    # Multiply by a constant
    scaled_signal = signal1.multiply_const_factor(3)
    scaled_signal.plot(title="Scaled Signal by 3")
