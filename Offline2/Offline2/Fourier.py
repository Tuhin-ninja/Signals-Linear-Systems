import numpy as np
import matplotlib.pyplot as plt

class FourierSeries:
    def __init__(self, func, L, terms=10):
        """
        Initialize the FourierSeries class with a target function, 2*np.pi L, and number of terms.
        
        Parameters:
        - func: The target function to approximate.
        - L: Half the 2*np.pi of the target function.
        - terms: Number of terms to use in the Fourier series expansion.
        """
        self.func = func
        self.L = L
        self.terms = terms

    def calculate_a0(self, N=1000):
        """
        Compute the a0 coefficient, which is the average (DC component) of the function over one 2*np.pi.
        
        Parameters:
        - N: Number of points to use for integration.
        
        Returns:
        - a0: The computed a0 coefficient.
        """
        x = np.linspace(-self.L, self.L, N)
        y = self.func(x)
        a0 = np.trapz(y, x) / ( self.L)  # Trapezoidal integration
        return a0

    def calculate_an(self, n, N=1000):
        """
        Compute the an coefficient for the nth cosine term in the Fourier series.
        
        Parameters:
        - n: Harmonic number to calculate the nth cosine coefficient.
        - N: Number of points to use for numerical integration.
        
        Returns:
        - an: The computed an coefficient.
        """
        x = np.linspace(-self.L, self.L, N)
        y = self.func(x) * np.cos(n * np.pi * x / self.L)
        an = np.trapz(y, x) / self.L
        return an

    def calculate_bn(self, n, N=1000):
        """
        Compute the bn coefficient for the nth sine term in the Fourier series.
        
        Parameters:
        - n: Harmonic number to calculate the nth sine coefficient.
        - N: Number of points to use for numerical integration.
        
        Returns:
        - bn: The computed bn coefficient.
        """
        x = np.linspace(-self.L, self.L, N)
        y = self.func(x) * np.sin(n * np.pi * x / self.L)
        bn = np.trapz(y, x) / self.L
        return bn

    def approximate(self, x):
        """
        Use the calculated coefficients to build the Fourier series approximation.
        
        Parameters:
        - x: Points at which to evaluate the Fourier series.
        
        Returns:
        - The Fourier series approximation evaluated at each point in x.
        """
        a0 = self.calculate_a0()
        result = a0 / 2
        for n in range(1, self.terms + 1):
            an = self.calculate_an(n)
            bn = self.calculate_bn(n)
            result += an * np.cos(n * np.pi * x / self.L) + bn * np.sin(n * np.pi * x / self.L)
        return result

    def plot(self):
        """
        Plot the original function and its Fourier series approximation.
        """
        x = np.linspace(-self.L, self.L, 1000)
        original = self.func(x)
        approximation = self.approximate(x)

        plt.figure(figsize=(10, 6))
        plt.plot(x, original, label="Original Function", color="blue")
        plt.plot(x, approximation, label=f"Fourier Series Approximation (N={self.terms})", color="red", linestyle="--")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.title("Fourier Series Approximation")
        plt.grid(True)
        plt.show()


def target_function(x, function_type="square"):
    if function_type == "square":
        # return np.sign(np.sin((2 * np.pi / 6) * x))  # Square wave with 2*np.pi 6
        return np.where(np.sin(x) >= 0, 1, -1)
    elif function_type == "sawtooth":
        return 2 * (x / (2 * np.pi) - np.floor(x / (2 * np.pi) + 0.5))  # Sawtooth wave
    
    elif function_type == "triangle":
        return 2 * np.abs(2 * (x / (2 * np.pi) - np.floor(x / (2 * np.pi) + 0.5))) - 1  # Triangle wave
        # return 2 * np.abs(2 * (x / 2*np.pi - np.floor(x / (2*np.pi) + 0.5)))

    elif function_type == "sine":
        return np.sin(x)  # Sine wave

    elif function_type == "cosine":
        return np.cos(x)  # Cosine wave

    else:
        raise ValueError("Invalid function_type. Choose from 'square', 'sawtooth', 'triangle', 'sine', or 'cosine'.")

# Example of using these functions in the FourierSeries class
if __name__ == "__main__":
    L = np.pi  # Half-2*np.pi for all functions
    terms = 3  # Number of terms in Fourier series

    # Test each type of target function
    for function_type in ["square", "sawtooth", "triangle", "sine", "cosine"]:
        print(f"Plotting Fourier series for {function_type} wave:")
        
        # Define the target function dynamically
        fourier_series = FourierSeries(lambda x: target_function(x, function_type=function_type), L, terms)
        
        # Plot the Fourier series approximation
        fourier_series.plot()
