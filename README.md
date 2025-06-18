# Pure Rain Smooth – Rain Filter on Meshes

> **Abstract**  
> *Pure Rain Smooth* is a stochastic mesh–smoothing add‑on for Blender.  It applies noise droplets **always pushing inward**—never zero, never outward—exactly as prescribed by the original [Rain Filter](https://github.com/infamedavid/NoiseFilter).  Curvature‐conditioned magnitude and antifase direction yield an emergent low‑pass effect without explicit convolutions.  Real‑time burst mode and tangential options are extra sprinkles, not core doctrine.

---

## Introduction

The [**Rain Filter**](https://github.com/infamedavid/NoiseFilter/tree/main) proposes a smoothing approach in which **random noise acts as an emergent filter**.  Unlike deterministic methods—e.g. classical Laplacian—this model drops *stochastic perturbations* onto the mesh and applies them **in antifase with the vertex normal**. The final result is global smoothing, yet the magic lies in **the intermediate steps and their controlled randomness**.

---

## Core Doctrine – features that are *non‑negotiable*

| Principle | Implementation in v1.5.1 |
|-----------|--------------------------|
| **Antifase push** | Displacement direction is always `‑normal` (or tangents when enabled). |
| **Droplets never zero** | Every selected vertex has a non‑zero chance (`density`) each sub‑pass; magnitude `random(0,1)` ensures *some* push. |
| **Curvature‑weighted magnitude** | `logCoeff = log(1+steepness·κ)/log(1+steepness)` (κ ≥ 0). Peaks ≈ 1, planes ≈ ½, valleys > 0. |
| **No deterministic kernels** | Smoothing emerges from repeated noise impacts—no Laplacian matrix, no explicit diffusion. |

### Optional 

| Extra | Purpose |
|-------|---------|
| **Tangential Passes** | Hits along two orthogonal directions for isotropic feel. |
| **Interleaved Tangents** | Shuffle order Normal → T1 → T2 within each iteration (acts like a "detangler"). |
| **Burst Rain Mode** | Timer‑driven loop; click **Play** for continuous drizzle, **Pause** to stop. |

---

## Algorithm

1. **Local relief**  κ = max((v − centroid) · n, 0)  
2. **Log gain**  `logCoeff = log(1 + steepness · κ) / log(1 + steepness)`  
3. **Drop magnitude**  `|Δ| = intensity · rand(0,1) · logCoeff`  
4. **Direction**  `–n` or tangents (optional).  
5. **Clamp**  `|Δ| ≤ maxDisp`  
6. **Iterate**  Fixed **Iterations** per click, or endless timer in **Burst** mode.

> **Note:** Exponential growth from early prototypes has been removed; droplets now rely purely on curvature‑log gain—consistent with the original paper.

---

## Parameters

| UI Control | Range | Core / Extra | Notes |
|------------|-------|--------------|-------|
| Intensity | 0 – 5 | Core | Global strength multiplier. |
| Density | 0 – 1 | Core | Probability each vertex is hit per sub‑pass. |
| Iterations | 1 – 500 | Core | Hidden in Burst mode. |
| Steepness | 0.1 – 10 | Core | 0.1 ≈ linear, 10 very logarithmic. |
| Max Disp | 0.001 – 1 BU | Core | Safety clamp per droplet. |
| Tangent Rain | bool | Extra | Add two orthogonals. |
| Interleaved Tangents | bool | Extra | Cycle N→T1→T2 every loop. |
| Interval (s) | 0.01 – 5 | Extra | Timer period in Burst mode. |

---

## Usage

1. **Edit Mode** → select the vertices you want to tame.  
2. Set sliders (`Intensity`, `Density`, etc.).  
3. • One‑shot: press **Rain**.  
   • Continuous: open *Burst Rain Mode*, set *Interval*, press **Play** (stop with **Pause**).  
4. Optionally enable **Tangential Passes** or **Interleaved** for a rounder wash.

---

## Roadmap

* Weight‑map modulation (paint where it rains harder).  
* Shape‑key morph sequence to animate the storm.  
* Optional Laplacian relief *measurement* (still emergent in action).  
* Audio port for the same concept in DSP.

---

## Credits

*Algorithm & concept* — **David Rodríguez**  
**El Mar, que fue mi inspiracion y refencia.**

