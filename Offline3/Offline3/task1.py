import numpy as np
import matplotlib.pyplot as plt

# Define the functions
def parabolic_function(x):
    return np.where((-2 <= x) & (x <= 2), x**2, 0)

def triangular_function(x):
    return np.where((-2 <= x) & (x <= 2), 1 - np.abs(x / 2), 0)

def sawtooth_function(x):
    return np.where((-2 <= x) & (x <= 2), x + 2, 0)

def rectangular_function(x):
    return np.where((-2 <= x) & (x <= 2), 1, 0)

# Fourier Transform using trapezoidal integration
def fourier_transform(signal, frequencies, sampled_times):
    real_part = np.zeros(len(frequencies))
    imag_part = np.zeros(len(frequencies))
    for i, freq in enumerate(frequencies):
        exponential = np.exp(-2j * np.pi * freq * sampled_times)
        real_part[i] = np.trapz(signal * np.real(exponential), sampled_times)
        imag_part[i] = np.trapz(signal * np.imag(exponential), sampled_times)
    return real_part, imag_part

# Inverse Fourier Transform using trapezoidal integration
def inverse_fourier_transform(ft_signal, frequencies, sampled_times):
    reconstructed_signal = np.zeros(len(sampled_times))
    ft_combined = ft_signal[0] + 1j * ft_signal[1]
    for t_idx, t in enumerate(sampled_times):
        exponential = np.exp(2j * np.pi * frequencies * t)
        reconstructed_signal[t_idx] = np.trapz(ft_combined * exponential, frequencies).real
    return reconstructed_signal

# Define sampled times and frequency ranges
sampled_times = np.linspace(-5, 5, 1000)
frequencies_list = [np.linspace(-1, 1, 500), np.linspace(-2, 2, 500), np.linspace(-5, 5, 500)]
functions = {
    "Parabolic Function": parabolic_function,
    "Triangular Function": triangular_function,
    "Sawtooth Function": sawtooth_function,
    "Rectangular Function": rectangular_function,
}

# Plotting for each function
for function_name, func in functions.items():
    y_values = func(sampled_times)
    
    plt.figure(figsize=(10, 6))
    plt.plot(sampled_times, y_values, label=f"Original {function_name}")
    plt.title(f"Original {function_name}")
    plt.xlabel("Time (t)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()

    # Fourier Transform and Frequency Spectrum
    for freq_range in frequencies_list:
        ft_signal = fourier_transform(y_values, freq_range, sampled_times)
        reconstructed_signal = inverse_fourier_transform(ft_signal, freq_range, sampled_times)

        plt.figure(figsize=(10, 6))
        plt.plot(freq_range, np.sqrt(ft_signal[0]**2 + ft_signal[1]**2), label="Frequency Spectrum")
        plt.title(f"Frequency Spectrum for {function_name} (Freq Range {freq_range[0]} to {freq_range[-1]})")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.legend()
        plt.grid()
        plt.show()

        # Reconstructed Signal
        plt.figure(figsize=(10, 6))
        plt.plot(sampled_times, y_values, label=f"Original {function_name}", color='blue')
        plt.plot(sampled_times, reconstructed_signal, label=f"Reconstructed {function_name}", color='red', linestyle='--')
        plt.title(f"Reconstructed {function_name} (Freq Range {freq_range[0]} to {freq_range[-1]})")
        plt.xlabel("Time (t)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.grid()
        plt.show()
