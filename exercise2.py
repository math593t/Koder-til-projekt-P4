import numpy as np
import matplotlib.pyplot as plt

# LECTURE6 - Exercise 2

Fs = 400
Ts = 1 / Fs
N = 80
n = np.arange(N)
w1 = 2 * np.pi * 100 * Ts
w2 = 2 * np.pi * 110 * Ts

v = np.cos(w1 * n) + 0.8 * np.cos(w2 * n)
V = np.fft.fft(v)

plt.figure()
plt.stem(n * Fs / N, np.abs(V))
plt.title('FFT, N=80')

# Zero-padding
v0 = np.concatenate([v, np.zeros(1024 - 80)])
N0 = 1024

plt.figure()
plt.stem(np.arange(N0) * Fs / N0, np.abs(np.fft.fft(v0)))
plt.title('FFT with zero-padding N0=1024')

# Lower N
Nlower = 50
nlower = np.arange(Nlower)
vlower = np.cos(w1 * nlower) + 0.8 * np.cos(w2 * nlower)

plt.figure()
freqs_lower = np.arange(0, Fs, Fs / Nlower)
plt.stem(freqs_lower, np.abs(np.fft.fft(vlower)))
plt.title('FFT, N=50')

# Higher N
Nhigher = 100
nhigher = np.arange(Nhigher)
vhigher = np.cos(w1 * nhigher) + 0.8 * np.cos(w2 * nhigher)

plt.figure()
freqs_higher = np.arange(0, Fs, Fs / Nhigher)
plt.stem(freqs_higher, np.abs(np.fft.fft(vhigher)))
plt.title('FFT, N=100')

# Final FFT(v, 1024)
plt.figure()
plt.stem(np.abs(np.fft.fft(v, 1024)))
plt.title('FFT(v, 1024)')

plt.show()
