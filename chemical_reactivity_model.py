import numpy as np

# Ashira Sahunalu April 15, 2026
# chemical_reactivity_model.py 

# =============================================================================
# CHEMICAL REACTIVITY MODEL
# =============================================================================


# --- SECTION 1: USER INPUTS ---
# Press Enter to accept the default value shown in brackets.
# Default values correspond to the Haber Process (N2 + 3H2 → 2NH3).

def prompt_float(message, default):
    while True:
        raw = input(message).strip()
        if not raw:
            return default
        try:
            return float(raw)
        except ValueError:
            print(f"  Invalid input — enter a number or press Enter for [{default}]")

print("=" * 62)
print("  CHEMICAL REACTIVITY MODEL — Input Parameters")
print("  (Press Enter to use the default Haber Process values)")
print("=" * 62)

reaction_name  = input("\n  Reaction name [Haber Process: N2 + 3H2 → 2NH3]: ").strip()
if not reaction_name:
    reaction_name = "Haber Process: N2 + 3H2 → 2NH3"

delta_H_sys_kJ = prompt_float("  delta_H_sys (kJ/mol)          [-92.22]: ", -92.22)
delta_S_sys_J  = prompt_float("  delta_S_sys (J/mol·K)        [-198.75]: ", -198.75)
Q              = prompt_float("  Q — reaction quotient            [0.5]: ",  0.5)
T_start        = prompt_float("  T_start (K)                     [298]: ",  298.0)
T_end          = prompt_float("  T_end   (K)                     [800]: ",  800.0)
T_step         = prompt_float("  T_step  (K)                     [100]: ",  100.0)

R = 8.314    # Universal gas constant [J/(mol·K)]


# --- SECTION 2: EXPLICIT UNIT CONVERSION ---
# delta_H must be in Joules to match the units of delta_S and R.

delta_H_sys_J = delta_H_sys_kJ * 1000     # kJ/mol  →  J/mol


# --- SECTION 3: THERMAL GRADIENT ---
# Build the temperature array from user-supplied start, end, and step values.

T = np.arange(T_start, T_end + 1, T_step)


# =============================================================================
# FEATURE 1: ENTROPY OF THE UNIVERSE  (Second Law Engine)
# =============================================================================
# The Second Law states a process is spontaneous only if delta_S_univ > 0.
#
# Step 1 — Entropy of the surroundings:
#   The surroundings absorb heat equal and opposite to the system's enthalpy.
#   delta_S_surr = q_surr / T = -delta_H_sys / T
#
# Step 2 — Entropy of the universe:
#   delta_S_univ = delta_S_sys + delta_S_surr

delta_S_surr = -delta_H_sys_J / T
delta_S_univ = delta_S_sys_J + delta_S_surr


# =============================================================================
# FEATURE 2: GIBBS FREE ENERGY
# =============================================================================
# Gibbs Free Energy combines enthalpy and entropy into a single spontaneity
# criterion evaluated at constant temperature and pressure.
#
#   delta_G_standard = delta_H_sys - (T * delta_S_sys)
#
# Sign convention:
#   delta_G < 0  →  spontaneous (products favored)
#   delta_G = 0  →  equilibrium
#   delta_G > 0  →  non-spontaneous (reactants favored)

delta_G_standard_J  = delta_H_sys_J - (T * delta_S_sys_J)
delta_G_standard_kJ = delta_G_standard_J / 1000


# =============================================================================
# FEATURE 3: CHEMICAL EQUILIBRIUM
# =============================================================================

# --- 3a. Equilibrium Constant (K) ---
# Derived from delta_G_standard = -RT ln(K)
# Solving for K:  K = exp(-delta_G_standard / RT)
#
# Interpretation:
#   K >> 1  →  products strongly favored at equilibrium
#   K ~  1  →  mixture of products and reactants
#   K << 1  →  reactants strongly favored at equilibrium

exponent = -delta_G_standard_J / (R * T)
K = np.exp(exponent)

# --- 3b. Non-Standard Free Energy (delta_G) ---
# When conditions differ from standard (Q ≠ 1), use the reaction quotient Q.
#   delta_G = delta_G_standard + RT ln(Q)
#
# Direction of reaction:
#   Q < K  →  reaction proceeds forward (delta_G < 0)
#   Q = K  →  system is at equilibrium (delta_G = 0)
#   Q > K  →  reaction proceeds in reverse (delta_G > 0)

delta_G_nonstandard_J  = delta_G_standard_J + (R * T * np.log(Q))
delta_G_nonstandard_kJ = delta_G_nonstandard_J / 1000


# =============================================================================
# OUTPUT CONSOLE
# =============================================================================

np.set_printoptions(precision=4, suppress=True)

print("\n" + "=" * 62)
print(f"  CHEMICAL REACTIVITY MODEL  |  {reaction_name}")
print("=" * 62)

print(f"\nInputs")
print(f"  delta_H_sys  = {delta_H_sys_kJ} kJ/mol")
print(f"  delta_S_sys  = {delta_S_sys_J} J/(mol·K)")
print(f"  Q (current)  = {Q}")

print(f"\n{'─'*62}")
print(f"  THERMAL GRADIENT")
print(f"{'─'*62}")
print(f"  T (K)                   : {T}")

print(f"\n{'─'*62}")
print(f"  FEATURE 1 — ENTROPY OF THE UNIVERSE")
print(f"{'─'*62}")
print(f"  delta_S_surr (J/mol·K)  : {delta_S_surr}")
print(f"  delta_S_univ (J/mol·K)  : {delta_S_univ}")

# --- Crossover marker: first temperature where reaction becomes non-spontaneous ---
crossover_indices = np.where(delta_S_univ < 0)[0]
if crossover_indices.size > 0:
    crossover_T = T[crossover_indices[0]]
    print(f"\n   Non-spontaneous (delta_S_univ < 0) from T = {crossover_T} K onward")
else:
    print(f"\n   Spontaneous (delta_S_univ > 0) across entire gradient")

print(f"\n{'─'*62}")
print(f"  FEATURE 2 — GIBBS FREE ENERGY")
print(f"{'─'*62}")
print(f"  delta_G_standard (kJ/mol): {delta_G_standard_kJ}")

print(f"\n{'─'*62}")
print(f"  FEATURE 3 — CHEMICAL EQUILIBRIUM")
print(f"{'─'*62}")
print(f"  Equilibrium Constant K  : {K}")
print(f"  delta_G_nonstd (kJ/mol) : {delta_G_nonstandard_kJ}")

print(f"\n{'─'*62}")
print(f"  NOTE: K decreases with rising T — consistent with Le Chatelier's")
print(f"  Principle for an exothermic reaction (delta_H < 0).")
print("=" * 62)
