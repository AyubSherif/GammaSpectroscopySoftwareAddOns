import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

def template_match(signal, template, threshold=None):
    signal = np.asarray(signal)
    template = np.asarray(template)

    if signal.ndim != 1 or template.ndim != 1:
        raise ValueError("Invalid input: signal and template must be 1D arrays.")

    template = np.conj(template[::-1])
    corr = fftconvolve(signal, template, mode='valid')

    if threshold is not None:
        match_indices = np.where(corr >= threshold)[0]
        return corr, match_indices

    return corr, None


#############################
### --- Example Usage --- ###
#############################

np.random.seed(0)
signal = np.random.normal(0, 0.2, 1000)
template = np.hanning(50)  # Gaussian-shape template

injected_indices = [200, 500, 750]
for idx in injected_indices:
    signal[idx:idx+50] += template

corr, matches = template_match(signal, template, threshold=5)

fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=False)

axs[0].plot(template, label="Template", color='green')
axs[0].set_title("Template")
axs[0].legend()

axs[1].plot(signal, label="Original Signal")
axs[1].set_title("Raw Data")
axs[1].legend()

axs[2].plot(corr, label="Template Matching Output", color='orange')
if matches is not None:
    axs[2].vlines(matches, ymin=min(corr), ymax=max(corr), color='red', linestyle='--', label="Detected Matches")
axs[2].set_title("Filtered Data")
axs[2].legend()

plt.tight_layout()
plt.show()
