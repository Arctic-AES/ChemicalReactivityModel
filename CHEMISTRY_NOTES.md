# Chemistry Notes — Chemical Reactivity Model

A plain-language reference for the thermodynamic equations in `chemical_reactivity_model.py`.
Sections are ordered to match the script's execution flow.

---

## Overview: The Variables

| Symbol | Name | Units | Physical Meaning |
|---|---|---|---|
| ΔH_sys | Enthalpy change | kJ/mol | Heat absorbed (+) or released (−) by the reaction |
| ΔS_sys | Entropy change | J/(mol·K) | Change in disorder of the system |
| ΔS_surr | Entropy of surroundings | J/(mol·K) | Disorder change in everything outside the system |
| ΔS_univ | Entropy of the universe | J/(mol·K) | Combined disorder change — the true spontaneity judge |
| ΔG° | Standard Gibbs Free Energy | kJ/mol | Net driving force under standard conditions |
| R | Gas constant | J/(mol·K) | Universal proportionality constant: 8.314 |
| T | Temperature | K | Must always be in Kelvin for thermodynamic equations |
| K | Equilibrium constant | dimensionless | Ratio of products to reactants at equilibrium |
| Q | Reaction quotient | dimensionless | Ratio of products to reactants *right now* |

> **Unit trap:** ΔH is typically given in **kJ/mol**, while ΔS and R use **J**. You must
> multiply ΔH by 1000 before mixing it into any equation with ΔS or R. Forgetting this
> is the most common error in Gen Chem 2 thermodynamics problems.

---

## Section 1 — The Second Law of Thermodynamics

### Core Statement
A process is **spontaneous** if and only if the total entropy of the universe increases:

```
ΔS_univ > 0  →  spontaneous
ΔS_univ = 0  →  equilibrium
ΔS_univ < 0  →  non-spontaneous
```

### Entropy of the Surroundings

The surroundings are everything outside the reaction flask. When the system releases heat
(exothermic, ΔH < 0), that heat flows into the surroundings, increasing their disorder.

At constant temperature, the entropy gained by the surroundings equals the heat they receive
divided by the temperature at which they receive it:

```
ΔS_surr = q_surr / T
```

Since energy is conserved, the surroundings gain exactly what the system loses:

```
q_surr = -ΔH_sys
```

Substituting:

```
ΔS_surr = -ΔH_sys / T
```

**Why does temperature appear?** At high T, the surroundings are already highly disordered,
so receiving the same amount of heat has a smaller relative impact. The entropy gain is
inversely proportional to T.

### Entropy of the Universe

```
ΔS_univ = ΔS_sys + ΔS_surr
```

For the Haber process (exothermic, ΔH < 0 and ΔS_sys < 0):
- The negative ΔH dumps heat into surroundings → large positive ΔS_surr at low T
- The negative ΔS_sys always works against spontaneity
- As T increases, ΔS_surr shrinks, and the negative ΔS_sys eventually wins
- The crossover point (ΔS_univ = 0) defines the **thermal spontaneity boundary**

---

## Section 2 — Gibbs Free Energy

### The Gibbs Equation

Gibbs Free Energy repackages the Second Law into a single system-only criterion, eliminating
the need to track the surroundings explicitly. It is derived directly from ΔS_univ:

Starting from:
```
ΔS_univ = ΔS_sys + ΔS_surr
       = ΔS_sys + (-ΔH_sys / T)
```

Multiply both sides by −T:
```
-T · ΔS_univ = ΔH_sys - T · ΔS_sys
```

Define ΔG° ≡ −T · ΔS_univ:
```
ΔG° = ΔH_sys - T · ΔS_sys
```

Because ΔS_univ and ΔG° are related by a negative constant (−T), the spontaneity
sign flips:

| ΔG° | ΔS_univ | Outcome |
|---|---|---|
| < 0 | > 0 | Spontaneous — products favored |
| = 0 | = 0 | Equilibrium |
| > 0 | < 0 | Non-spontaneous — reactants favored |

### Temperature Dependence

For reactions where ΔH and ΔS have the same sign (as in the Haber process, both negative),
there is a **crossover temperature** where ΔG° = 0:

```
0 = ΔH - T_crossover · ΔS
T_crossover = ΔH / ΔS
```

For the Haber process:
```
T_crossover = -92,220 J/mol / -198.75 J/(mol·K) ≈ 464 K
```

Below 464 K → ΔG° < 0 → spontaneous  
Above 464 K → ΔG° > 0 → non-spontaneous

---

## Section 3 — Equilibrium Constant (K)

### Derivation from ΔG°

At equilibrium, ΔG = 0 and Q = K. Starting from the non-standard equation (derived below):

```
ΔG = ΔG° + RT ln(Q)
```

Setting ΔG = 0 and Q = K:
```
0 = ΔG° + RT ln(K)
ΔG° = -RT ln(K)
```

Solving for K:
```
ln(K) = -ΔG° / RT
K = exp(-ΔG° / RT)
```

### Physical Interpretation

| K value | Meaning |
|---|---|
| K >> 1 | Products strongly favored at equilibrium |
| K ≈ 1 | Roughly equal products and reactants |
| K << 1 | Reactants strongly favored at equilibrium |

### Temperature Dependence for Exothermic Reactions

For the Haber process (ΔH < 0, exothermic), as T increases:
- ΔG° becomes less negative (eventually positive)
- The exponent −ΔG°/RT becomes smaller
- K = exp(smaller number) → K decreases

This is a mathematical expression of **Le Chatelier's Principle**: adding heat to an
exothermic reaction shifts equilibrium toward reactants.

---

## Section 4 — Non-Standard Free Energy and Q

### The Reaction Quotient Q

K describes where the system *will be* at equilibrium. Q describes where the system *is right now*.

- Q is calculated the same way as K, but using current concentrations/pressures instead of equilibrium values.

### Non-Standard Gibbs Free Energy

When conditions differ from standard (Q ≠ 1):

```
ΔG = ΔG° + RT ln(Q)
```

### Direction of Reaction

| Comparison | ΔG | Direction |
|---|---|---|
| Q < K | < 0 | Forward — more products will form |
| Q = K | = 0 | Equilibrium — no net change |
| Q > K | > 0 | Reverse — products will convert back to reactants |

For this model, Q = 0.5 (ln(0.5) ≈ −0.693), which makes the RT ln(Q) term negative,
pushing ΔG more negative than ΔG° — meaning the reaction has extra thermodynamic
driving force to proceed forward beyond what standard conditions alone predict.

---

## Worked Example — Haber Process at T = 298 K

Manual spot-check to verify the script's output at the first temperature point.

**Inputs:**
```
ΔH_sys = -92,220 J/mol    (converted from -92.22 kJ/mol)
ΔS_sys = -198.75 J/(mol·K)
T      = 298 K
R      = 8.314 J/(mol·K)
Q      = 0.5
```

**Step 1 — ΔS_surr:**
```
ΔS_surr = -(-92,220) / 298 = +309.46 J/(mol·K)
```

**Step 2 — ΔS_univ:**
```
ΔS_univ = -198.75 + 309.46 = +110.71 J/(mol·K)   → spontaneous ✓
```

**Step 3 — ΔG°:**
```
ΔG° = -92,220 - (298 × -198.75)
    = -92,220 + 59,227.5
    = -32,992.5 J/mol
    ≈ -33.0 kJ/mol
```

**Step 4 — K:**
```
K = exp(32,992.5 / (8.314 × 298))
  = exp(13.314)
  ≈ 6.0 × 10⁵
```

**Step 5 — ΔG (non-standard, Q = 0.5):**
```
ΔG = -32,992.5 + (8.314 × 298 × ln(0.5))
   = -32,992.5 + (2477.6 × -0.6931)
   = -32,992.5 - 1716.9
   ≈ -34,709 J/mol
   ≈ -34.7 kJ/mol
```

These values should match (within rounding) the first element of each output array
when `chemical_reactivity_model.py` is run.
