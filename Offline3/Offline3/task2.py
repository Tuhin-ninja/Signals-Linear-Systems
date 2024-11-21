import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt

import os
print(os.getcwd())

# Step 1: Load the audio file
sample_rate, data = wavfile.read('buzzjc.wav')
data = data / np.max(np.abs(data))  # Normalize to -1 to 1

# If stereo, convert to mono by averaging channels
if len(data.shape) > 1:
    data = data.mean(axis=1)

# Step 1.1: Plot the original audio signal in the time domain
plt.figure(figsize=(12, 4))
time = np.linspace(0, len(data) / sample_rate, num=len(data))
plt.plot(time, data)
plt.title("Original Audio Signal (Time Domain)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# Step 2: Down-sample the audio for faster processing
interval_step = 1  # Adjust this for sampling every 'interval_step' data points  
data_sampled = data[::interval_step]
max_time = len(data_sampled) / (sample_rate / interval_step)
sampled_times = np.linspace(0, max_time, num=len(data_sampled))

# Define frequencies for Fourier Transform
max_freq = sample_rate / (2 * interval_step)
num_freqs = len(data_sampled)
frequencies = np.linspace(-max_freq, max_freq, num=num_freqs)

# Step 3: Fourier Transform using trapezoidal integration
def fourier_transform(signal, frequencies, sampled_times):
    real_part = np.zeros(len(frequencies))
    imag_part = np.zeros(len(frequencies))
    for i, freq in enumerate(frequencies):
        exponential = np.exp(-2j * np.pi * freq * sampled_times)
        real_part[i] = np.trapz(signal * np.real(exponential), sampled_times)
        imag_part[i] = np.trapz(signal * np.imag(exponential), sampled_times)
    return real_part, imag_part

# Apply Fourier Transform to the audio
ft_data = fourier_transform(data_sampled, frequencies, sampled_times)

# Step 3.1: Visualize the frequency spectrum
plt.figure(figsize=(12, 6))
plt.plot(frequencies, np.sqrt(ft_data[0]**2 + ft_data[1]**2))
plt.title("Frequency Spectrum of the Audio Signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()

# Step 4: Identify and Remove Noise Frequencies
filtered_ft_data = np.zeros((2, num_freqs))
filtered_ft_data[0] = ft_data[0].copy()
filtered_ft_data[1] = ft_data[1].copy()

# Filter out high frequencies (e.g., keep only up to 1000 Hz)
threshold_frequency = 1000
low_pass_filter = np.abs(frequencies) <= threshold_frequency
filtered_ft_data[0] *= low_pass_filter
filtered_ft_data[1] *= low_pass_filter

# Step 4.1: Visualize the filtered frequency spectrum
plt.figure(figsize=(12, 6))
plt.plot(frequencies, np.sqrt(filtered_ft_data[0]**2 + filtered_ft_data[1]**2))
plt.title("Filtered Frequency Spectrum (High-Frequency Noise Removed)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()

# Step 5: Inverse Fourier Transform using trapezoidal integration
def inverse_fourier_transform(ft_signal, frequencies, sampled_times):
    reconstructed_signal = np.zeros(len(sampled_times))
    ft_combined = ft_signal[0] + 1j * ft_signal[1]
    for t_idx, t in enumerate(sampled_times):
        exponential = np.exp(2j * np.pi * frequencies * t)
        reconstructed_signal[t_idx] = np.trapz(ft_combined * exponential, frequencies).real
    return reconstructed_signal

# Reconstruct the denoised audio signal
filtered_data = inverse_fourier_transform(filtered_ft_data, frequencies, sampled_times)

# Step 5.1: Plot the reconstructed signal
plt.figure(figsize=(12, 4))
plt.plot(sampled_times, filtered_data)
plt.title("Reconstructed (Denoised) Audio Signal (Time Domain)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# Step 6: Normalize and Save the Denoised Audio
filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)  # Convert to int16
wavfile.write('denoised_audio.wav', sample_rate, filtered_data)

print("Denoised audio saved as 'denoised_audio.wav'")
