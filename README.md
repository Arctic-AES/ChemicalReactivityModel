# Chemical Reactivity Model

A Python command-line tool that models the thermodynamic viability, spontaneity, and
equilibrium of a chemical reaction across a temperature gradient.

---

## Setup

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install the only dependency
pip install numpy

# Run the model
python chemical_reactivity_model.py
```

Press **Enter** on any prompt to accept the default Haber Process values and run immediately.

---

## Project Files

```
ChemicalKineticModel/
├── chemical_reactivity_model.py   Main script — prompts, computation, output
├── CHEMISTRY_NOTES.md             Equation derivations and worked example
├── README.md                      This file
└── .gitignore                     Excludes venv/ and Python cache
```

---

## Inputs

The script prompts for seven values. All fields have working defaults for the Haber Process
(`N2 + 3H2 → 2NH3`). Entering a non-numeric value will re-prompt rather than crash.

| Field | Symbol | Unit | Default |
|---|---|---|---|
| Reaction name | — | — | Haber Process: N2 + 3H2 → 2NH3 |
| Standard enthalpy | ΔH_sys | kJ/mol | −92.22 |
| Standard entropy | ΔS_sys | J/(mol·K) | −198.75 |
| Reaction quotient | Q | — | 0.5 |
| Temperature start | T_start | K | 298 |
| Temperature end | T_end | K | 800 |
| Temperature step | T_step | K | 100 |

---

## How It Works

The script runs in six explicit sections. Each one corresponds to a distinct step in a
thermodynamics problem.

**1. User Inputs**
Collects the values above. `R = 8.314 J/(mol·K)` is hard-coded and not configurable.

**2. Unit Conversion**
Converts ΔH from kJ/mol to J/mol (`× 1000`) before any calculations begin. Unit mismatch
between kJ and J is the most common source of error in Gen Chem 2 thermodynamics.

**3. Thermal Gradient**
Builds a NumPy array from `T_start` to `T_end` in steps of `T_step`. All three features
below run across the entire array at once — no loops needed.

---

**Feature 1 — Entropy of the Universe**

The Second Law says a reaction is spontaneous only when `ΔS_univ > 0`.

```
ΔS_surr = −ΔH_sys / T         (surroundings gain heat the system releases)
ΔS_univ = ΔS_sys + ΔS_surr   (total disorder change)
```

The output includes a crossover marker — the first temperature where `ΔS_univ` goes
negative and the reaction is no longer spontaneous.

---

**Feature 2 — Gibbs Free Energy**

Gibbs combines enthalpy and entropy into one spontaneity number, evaluated per temperature:

```
ΔG° = ΔH_sys − (T × ΔS_sys)
```

- `ΔG° < 0` → spontaneous, products favored
- `ΔG° = 0` → equilibrium
- `ΔG° > 0` → non-spontaneous, reactants favored

When ΔH and ΔS share the same sign, there is a crossover temperature `T = ΔH / ΔS`
where ΔG° changes sign. For the Haber Process this is ≈ 464 K.

---

**Feature 3 — Chemical Equilibrium**

The equilibrium constant K comes from solving `ΔG° = −RT ln(K)`:

```
K = exp(−ΔG° / RT)
```

K tells you where the reaction sits at equilibrium. For exothermic reactions (ΔH < 0),
K shrinks as temperature rises — Le Chatelier's Principle in equation form.

The non-standard free energy accounts for the current reaction quotient Q:

```
ΔG = ΔG° + RT ln(Q)
```

- `Q < K` → reaction drives forward (ΔG < 0)
- `Q = K` → system is at equilibrium
- `Q > K` → reaction reverses (ΔG > 0)

---

## Example Output

```
==============================================================
  CHEMICAL REACTIVITY MODEL  |  Haber Process: N2 + 3H2 → 2NH3
==============================================================

Inputs
  delta_H_sys  = -92.22 kJ/mol
  delta_S_sys  = -198.75 J/(mol·K)
  Q (current)  = 0.5

──────────────────────────────────────────────────────────────
  THERMAL GRADIENT
──────────────────────────────────────────────────────────────
  T (K)                   : [298. 398. 498. 598. 698. 798.]

──────────────────────────────────────────────────────────────
  FEATURE 1 — ENTROPY OF THE UNIVERSE
──────────────────────────────────────────────────────────────
  delta_S_surr (J/mol·K)  : [309.4631 231.7085 185.1807 154.214  132.1203 115.5639]
  delta_S_univ (J/mol·K)  : [110.7131  32.9585 -13.5693 -44.536  -66.6297 -83.1861]

  Non-spontaneous (delta_S_univ < 0) from T = 498.0 K onward

──────────────────────────────────────────────────────────────
  FEATURE 2 — GIBBS FREE ENERGY
──────────────────────────────────────────────────────────────
  delta_G_standard (kJ/mol): [-32.9925 -13.1175   6.7575  26.6325  46.5075  66.3825]

──────────────────────────────────────────────────────────────
  FEATURE 3 — CHEMICAL EQUILIBRIUM
──────────────────────────────────────────────────────────────
  Equilibrium Constant K  : [607109.6328  52.6793   0.1955   0.0047   0.0003   0.    ]
  delta_G_nonstd (kJ/mol) : [ -34.7098  -15.4111   3.8876  23.1863  42.485   61.7838]
```

---

## Dependencies

Python 3 and NumPy only. No pandas, no plotting libraries.

For equation derivations and a hand-worked example at 298 K, see
[`CHEMISTRY_NOTES.md`](CHEMISTRY_NOTES.md).
