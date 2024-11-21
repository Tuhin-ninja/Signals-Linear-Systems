import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

class FourierSeries:
    def __init__(self, L, func_type):
        self.L = L
        self.func_type = func_type

    def target_function(self, x):
        # Define target periodic functions
        if self.func_type == 'square':
            return np.sign(np.sin(np.pi * x / self.L))
        elif self.func_type == 'sawtooth':
            return (x % (2 * self.L)) / self.L - 1
        elif self.func_type == 'triangle':
            return 2 * np.abs(2 * ((x / self.L) - np.floor((x / self.L) + 0.5))) - 1
        elif self.func_type == 'sine':
            return np.sin(np.pi * x / self.L)
        elif self.func_type == 'cosine':
            return np.cos(np.pi * x / self.L)
        else:
            raise ValueError("Unsupported function type")

    def calculate_a0(self):
        result, _ = quad(lambda x: self.target_function(x), -self.L, self.L)
        return result / (2 * self.L)

    def calculate_an(self, n):
        result, _ = quad(lambda x: self.target_function(x) * np.cos(n * np.pi * x / self.L), -self.L, self.L)
        return result / self.L

    def calculate_bn(self, n):
        result, _ = quad(lambda x: self.target_function(x) * np.sin(n * np.pi * x / self.L), -self.L, self.L)
        return result / self.L

    def approximate(self, x, terms=10):
        # Fourier Series approximation up to the specified number of terms
        a0 = self.calculate_a0()
        sum_terms = a0 / 2
        for n in range(1, terms + 1):
            an = self.calculate_an(n)
            bn = self.calculate_bn(n)
            sum_terms += an * np.cos(n * np.pi * x / self.L) + bn * np.sin(n * np.pi * x / self.L)
        return sum_terms

    def plot(self, terms=10):
        x_vals = np.linspace(-self.L, self.L, 500)
        original_y_vals = [self.target_function(x) for x in x_vals]
        approx_y_vals = [self.approximate(x, terms) for x in x_vals]

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, original_y_vals, label="Original Function")
        plt.plot(x_vals, approx_y_vals, label=f"Fourier Series Approximation (n={terms})", linestyle='--')
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.title(f"Fourier Series Approximation of {self.func_type.capitalize()} Wave")
        plt.grid(True)
        plt.show()

# Example usage
L = 1  # half-period of the function
fs = FourierSeries(L, func_type='square')
fs.plot(terms=10)
