# Methodology

This document describes the mathematical framework and data processing methodology used to analyze the **DeepMIMO ASU Campus 3.5 GHz** ray-tracing scenario.

---

## 1. Propagation Environment

The analysis uses the **DeepMIMO ASU Campus (`asu_campus_3p5`)** ray-tracing scenario, which models wireless propagation in an urban campus environment. Physical obstructions such as buildings influence signal propagation and create different propagation conditions.

Receiver locations are categorized as:

*   **Line-of-Sight (LoS):** A direct, unobstructed propagation path exists between the transmitter (TX) and receiver (RX).
*   **Non-Line-of-Sight (NLoS):** The direct propagation path is obstructed, causing the received signal to arrive primarily through reflected, diffracted, or scattered propagation mechanisms.

---

## 2. Theoretical Reference Model

The ray-traced path loss provided by DeepMIMO is compared with the theoretical **Friis Free-Space Path Loss (FSPL)** model, which serves as an ideal free-space reference.

### Friis Free-Space Path Loss

For a transmitter–receiver separation $d$ (meters) and carrier frequency $f_c$ (MHz),

$$FSPL(\text{dB}) = 20\log_{10}(d) + 20\log_{10}(f_c) - 27.55$$

where:
*   $d$ = transmitter–receiver distance (m)
*   $f_c$ = carrier frequency (MHz)

For this analysis,

$$f_{\mathrm{c}} = 3500\ \text{MHz}$$

---

## 3. Antenna Array Gain

The DeepMIMO scenario uses an **8-element transmit antenna array** and a **single receive antenna**.

Assuming ideal coherent array gain, the transmit antenna gain is

$$G_{\mathrm{TX}} = 10\log_{10}(N)$$

where:

$$N = 8$$

giving:

$$G_{\mathrm{TX}} \approx 9.03\ \text{dB}$$

The receive antenna gain is assumed to be:

$$G_{\mathrm{RX}} = 0\ \text{dBi}$$

The theoretical free-space path-loss reference is computed as:

$$PL_{\mathrm{theoretical}} = FSPL - G_{\mathrm{TX}} - G_{\mathrm{RX}}$$

This serves as the theoretical free-space reference against which the DeepMIMO ray-traced path loss is compared.

---

## 4. Distance Calculation

For every receiver location, the transmitter–receiver separation is computed using the three-dimensional Euclidean distance:

$$d = \sqrt{(x-x_{\mathrm{TX}})^2 + (y-y_{\mathrm{TX}})^2 + (z-z_{\mathrm{TX}})^2}$$

Using the full 3D distance accounts for both horizontal separation and antenna height differences.

---

## 5. Generated Visualizations

### Scatter Plot
Displays individual LoS and NLoS receiver path-loss values together with the theoretical Friis reference.

### Mean Path-Loss Profile
Displays the mean path loss for LoS and NLoS receivers as a function of distance, together with one standard deviation about the mean.