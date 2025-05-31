# ☢️⚡ Gamma Spectroscopy: Live Denoising and Gamma Spectrum Analysis

This repository demonstrates a modern, **fully digital (software-based, not hardware-DSP)** pipeline for **gamma spectroscopy**, developed to replace bulky and expensive analog systems with efficient, portable software solutions. The project tackles key challenges in real-time denoising, pile-up correction, and memory-efficient pulse extraction — all at high data acquisition rates.

> 🔬 **Note: The full software is proprietary and not included. My contribution included:
> - ✅ Live signal denoising  
> - ✅ Baseline and pile-up correction  
> - ✅ SNIP-based background subtraction  

This repository focuses specifically on the **live signal denoising component**.

---

## 💡 Why This Matters

Traditional gamma spectroscopy depends on analog modules like shaping amplifiers and multi-channel analyzers (MCAs). These components:
- Lack flexibility and are hard to reconfigure
- Add latency and complexity to the system
- Are expensive and bulky

Our goal was to demonstrate how software can replace these components without sacrificing resolution or responsiveness — enabling portable, scalable systems.

---

## 🏗️ Pipeline Stages

Here’s how the signal is processed:

```text
Detector
→ Pre-Amplifier
→ Analog-to-Digital Converter (ADC)
→ Template Matching Filter (FFT-based)
→ Baseline & Pile-Up Correction
→ Pulse Detection + Pulse Height Extraction + Timestamping
→ Pulse-Level Data Storage (compressed)
→ SNIP Background Subtraction
→ Spectrum Building (Histogram)
```

---

## 🧰 System Comparison

| Feature                   | Traditional Setup                                  | Digital Setup                                  | This Project (Software Pipeline)                      |
|---------------------------|----------------------------------------------------|------------------------------------------------|-------------------------------------------------------|
| Detector                  | HPGe / NaI(Tl), etc.                               | Same                                           | Same                                                  |
| Preamp                    | Charge-sensitive                                   | Same                                           | Same                                                  |
| Signal Processing         | Shaping amp + Analog pile-up & noise filters       | Basic digital filtering (FPGA)                 | ✅ All handled in software (Python)                   |
| Spectrum Building         | MultiChannel Analyzer (MCA)                        | ❌ Replaced by software histogramming          | ✅ Fully replaced by software (Python)               |
| Flexibility               | Low                                                | Medium                                         | ✅ High                                               |

---

## ⚙️ How It Works

### 🎯 Template Matching Filter

At the core of this system is a **template matching filter** — a pattern-matching algorithm that detects pulses in noisy signals by comparing the signal to a known ideal pulse shape (typically the preamp output).

#### Steps:
1. Define a reference template (fast rise, long tail — characteristic of preamp output)
2. Reverse and conjugate the template
3. Perform FFT-based convolution with the digitized signal using `scipy.signal.fftconvolve`
4. Detect peaks in the output correlation — these correspond to actual pulses

> Think of it like noise-canceling headphones — but tuned to detect gamma-ray events.

---

## ⚖️ Why Template Matching?

| ✅ Pros                                             | ❌ Cons                                                  |
|-----------------------------------------------------|-----------------------------------------------------------|
| Excellent noise rejection                           | Requires a known pulse shape                              |
| High sensitivity to weak or overlapping pulses      | Computationally more intensive than basic filters         |
| Avoids arbitrary smoothing (preserves resolution)   | Can be affected by baseline drift if not corrected        |

---

## 📦 Storage Optimization

In this setup, waveform-level data is stored **only around detected pulses**, not continuously. This allows for:
- Baseline correction
- Pulse shape analysis
- Post-hoc pile-up recovery

Each pulse record contains:
- Amplitude (energy)
- Timestamp
- Baseline-corrected snippet
- Pulse width
- Pile-up flag

➡️ This reduces storage size **by over 90%** compared to raw waveform logging.

---

## 📉 Background Subtraction

We apply **SNIP (Statistics-sensitive Nonlinear Iterative Peak-clipping)** to the final histogram to remove continuum and Compton background. This step:

- Improves peak-to-background ratio
- Enables better isotope identification
- Supports unfolding and quantitative analysis

---

## 🚀 Achievements

- ✅ Successfully handled 1.8 million samples per second in real-time
- ✅ Significantly reduced memory/storage requirements
- ✅ Preserved high-resolution pulse detection without analog shaping

---

## 📊 Visual Example

![Example](https://github.com/AyubSherif/GammaSpectroscopySoftwareAddOns/blob/main/img/Example.png)

---

## 🧪 Example: Actual Data

**Template Pulse:**

![Template](https://github.com/AyubSherif/GammaSpectroscopySoftwareAddOns/blob/main/img/Template.png)

**Raw Signal vs Filtered Output:**

![Filtered](https://github.com/AyubSherif/GammaSpectroscopySoftwareAddOns/blob/main/img/Raw%20vs%20Filtered.png)

This filtering technique preserves the key pulse shape while removing random noise.

---

## 📁 Files Included

- `Template_Match.py`: Main implementation of the FFT-based template matching filter with a built-in demo.
- *(Note: The full gamma spectroscopy system is proprietary and not included here.)*

---

## 🛠️ How to Use

This module is designed to integrate into an existing acquisition and analysis pipeline.

### Basic Usage:

```python
from Template_Match import template_match

# Your digitized signal and reference template
corr, match_indices = template_match(signal, template, threshold=5)
```

You can then apply thresholding, timestamp alignment, and energy extraction from matched pulse regions.

---

## 🔭 Final Thoughts

This project demonstrates how a flexible, software-first architecture can achieve real-time gamma pulse analysis — replacing expensive and rigid analog systems while opening the door for smarter, portable, and scalable spectroscopy tools.

Feel free to reach out for collaboration.
