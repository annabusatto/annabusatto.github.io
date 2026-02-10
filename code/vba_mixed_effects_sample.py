"""
vba_mixed_effects_sample.py

Public, runnable sample that mirrors my project workflow for estimating
context-neutral (intrinsic) Vertical Bat Angle (VBA) with a mixed-effects model.

- Uses a tiny synthetic demo dataset
- Modeling + adjusted VBA extraction are adapted directly from my project notebook:
  - center covariates (*_c)
  - MIN_SWINGS filter for stability
  - MixedLM with random intercept by batter-side key
  - EB shrinkage fallback if random-effects covariance is singular

Author: Anna Busatto
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


# -----------------------------
# Parameters
# -----------------------------
MIN_SWINGS = 20
RANDOM_SEED = 1


# -----------------------------
# Synthetic demo data
# -----------------------------
def make_synthetic_vba_data(
    n_swings: int = 12000,
    n_batters: int = 220,
    seed: int = RANDOM_SEED
) -> pd.DataFrame:
    """
    Create a synthetic swing-level dataset with the same column structure used
    in the project. This is only to make the code runnable without publishing data.

    The synthetic VBA outcome is generated from:
    - pitch context (location/velocity/movement/count)
    - pitch type effects
    - a batter-side intrinsic offset (random intercept)
    """
    rng = np.random.default_rng(seed)

    batter_ids = rng.integers(10000, 99999, size=n_swings).astype(str)
    batter_side = rng.choice(["L", "R"], size=n_swings, p=[0.45, 0.55])
    batter_key = np.char.add(np.char.add(batter_ids, "_"), batter_side)

    pitch_type = rng.choice(["FF", "SI", "SL", "CU", "CH"], size=n_swings, p=[0.40, 0.15, 0.20, 0.10, 0.15])

    balls = rng.integers(0, 4, size=n_swings)
    strikes = rng.integers(0, 3, size=n_swings)

    # Context features (roughly realistic scales)
    location_x = rng.normal(0.0, 0.75, size=n_swings)
    location_z = rng.normal(2.5, 0.60, size=n_swings)
    velocity = rng.normal(92.0, 3.5, size=n_swings)

    release_x = rng.normal(0.0, 0.70, size=n_swings)
    release_z = rng.normal(5.6, 0.35, size=n_swings)

    spin = rng.normal(2200, 250, size=n_swings)
    break_x = rng.normal(0.0, 7.0, size=n_swings)
    break_z = rng.normal(0.0, 7.0, size=n_swings)

    # Batter-side intrinsic offsets (random intercept by batter_key)
    unique_keys, key_idx = np.unique(batter_key, return_inverse=True)
    u = rng.normal(0.0, 2.0, size=len(unique_keys))  # between batter-side SD in degrees

    # Pitch type effect (synthetic)
    pt_eff = {"FF": 0.0, "SI": -0.8, "SL": -0.5, "CU": -1.1, "CH": -0.6}
    pitch_type_term = np.vectorize(pt_eff.get)(pitch_type)

    # Generate observed VBA (degrees; more negative = steeper)
    noise = rng.normal(0.0, 3.2, size=n_swings)
    vba = (
        -24.0
        + 1.1 * (location_z - 2.5)      # higher pitch -> slightly flatter (less negative)
        + 0.05 * location_x
        + 0.12 * (velocity - 92.0)
        + 0.015 * (spin - 2200)
        + 0.02 * break_x
        - 0.02 * break_z
        - 0.20 * (balls - 1.5)
        + 0.15 * (strikes - 1.0)
        + pitch_type_term
        + u[key_idx]
        + noise
    )

    return pd.DataFrame(
        {
            "BATTER_ID": batter_ids,                # synthetic placeholder ID
            "BATTER_SIDE": batter_side,
            "BATTER_KEY": batter_key,
            "VERTICAL_BAT_ANGLE": vba,
            "PITCH_TYPE": pitch_type,
            "BALLS": balls,
            "STRIKES": strikes,
            "VELOCITY": velocity,
            "LOCATION_X": location_x,
            "LOCATION_Z": location_z,
            "RELEASE_X": release_x,
            "RELEASE_Z": release_z,
            "PITCH_SPIN_RATE": spin,
            "BREAK_X": break_x,
            "BREAK_Z": break_z,
        }
    )


# -----------------------------
# Main workflow (adapted)
# -----------------------------
def main() -> None:
    # In the public version, I generate synthetic swings instead of loading files.
    vba = make_synthetic_vba_data()

    # ---- Basic cleaning ----
    essential = [
        "BATTER_ID",
        "BATTER_SIDE",
        "VERTICAL_BAT_ANGLE",
        "PITCH_TYPE",
        "LOCATION_X",
        "LOCATION_Z",
    ]
    vba = vba.dropna(subset=essential).copy()

    vba["BATTER_ID"] = vba["BATTER_ID"].astype(str)
    vba["BATTER_SIDE"] = vba["BATTER_SIDE"].astype(str).str.upper().str.strip()
    vba["BATTER_KEY"] = vba["BATTER_ID"] + "_" + vba["BATTER_SIDE"]

    num_cols = [
        "BALLS",
        "STRIKES",
        "VELOCITY",
        "LOCATION_X",
        "LOCATION_Z",
        "RELEASE_X",
        "RELEASE_Z",
        "PITCH_SPIN_RATE",
        "BREAK_X",
        "BREAK_Z",
    ]
    for c in num_cols:
        vba[c] = pd.to_numeric(vba[c], errors="coerce")

    vba = vba.dropna(subset=["VERTICAL_BAT_ANGLE"] + num_cols).copy()

    # Center continuous covariates so the intercept represents an average pitch context
    for c in num_cols:
        vba[c + "_c"] = vba[c] - vba[c].mean()

    # Minimum swings per batter-side for stability
    counts = vba.groupby("BATTER_KEY").size().rename("N_SWINGS")
    keep_keys = counts[counts >= MIN_SWINGS].index
    vba = vba[vba["BATTER_KEY"].isin(keep_keys)].copy()

    print(f"Eligible batter-sides (N_SWINGS >= {MIN_SWINGS}): {vba['BATTER_KEY'].nunique()}")

    # ---- Mixed-effects model ----
    formula = (
        "VERTICAL_BAT_ANGLE ~ BATTER_SIDE "
        "+ LOCATION_X_c + LOCATION_Z_c + VELOCITY_c + RELEASE_X_c + RELEASE_Z_c "
        "+ PITCH_SPIN_RATE_c + BREAK_X_c + BREAK_Z_c + BALLS_c + STRIKES_c "
        "+ C(PITCH_TYPE)"
    )

    md = smf.mixedlm(formula, vba, groups=vba["BATTER_KEY"], re_formula="1")
    m = md.fit(method="lbfgs", reml=True)

    print("\nMixedLM fit summary (synthetic demo):")
    print(m.summary())

    # ---- Extract adjusted VBA per batter-side ----
    fe = m.fe_params.copy()
    key_to_side = vba.drop_duplicates("BATTER_KEY").set_index("BATTER_KEY")["BATTER_SIDE"]

    def fixed_base_for_side(side: str) -> float:
        base = fe["Intercept"]
        side_term = 0.0
        # Look for BATTER_SIDE fixed-effect term (e.g., BATTER_SIDE[T.R])
        for term in fe.index:
            if term.startswith("BATTER_SIDE[T.") and term.endswith(side + "]"):
                side_term = fe[term]
                break
        return base + side_term

    # Try standard Best Linear Unbiased Predictors (BLUPs); if covariance is singular, fall back to EB shrinkage
    try:
        re = m.random_effects
        use_sm_blups = True
    except Exception:
        use_sm_blups = False

    rows = []
    if use_sm_blups:
        for key, eff in re.items():
            # eff can be dict-like or array-like depending on statsmodels version
            try:
                u_hat = float(list(eff.values())[0])
            except Exception:
                u_hat = float(np.array(eff).ravel()[0])

            side = key_to_side.loc[key]
            adj_vba = fixed_base_for_side(side) + u_hat
            rows.append({"BATTER_KEY": key, "BATTER_SIDE": side, "ADJ_VERTICAL_BAT_ANGLE": adj_vba})
    else:
        # EB fallback (method-of-moments shrinkage)
        y = vba["VERTICAL_BAT_ANGLE"].values
        X_fe = m.model.exog
        beta = m.fe_params.values
        yhat_fe = X_fe @ beta
        resid = y - yhat_fe

        grp_df = pd.DataFrame({"BATTER_KEY": vba["BATTER_KEY"].values, "resid": resid})
        grp_stats = (
            grp_df.groupby("BATTER_KEY")
            .agg(mean_resid=("resid", "mean"), n=("resid", "size"))
            .reset_index()
        )

        sigma2 = float(m.scale)  # residual variance
        mbar = float(grp_stats["mean_resid"].mean())
        S2 = float(((grp_stats["mean_resid"] - mbar) ** 2).sum() / max(1, (len(grp_stats) - 1)))
        Eninv = float((1.0 / grp_stats["n"]).mean())
        tau2 = max(0.0, S2 - sigma2 * Eninv)

        grp_stats["weight"] = tau2 / (tau2 + sigma2 / grp_stats["n"])
        grp_stats["u_hat"] = grp_stats["weight"] * grp_stats["mean_resid"]

        side_map = key_to_side.to_dict()
        for _, r in grp_stats.iterrows():
            key = r["BATTER_KEY"]
            side = side_map[key]
            base = fixed_base_for_side(side)
            adj_vba = base + float(r["u_hat"])
            rows.append({"BATTER_KEY": key, "BATTER_SIDE": side, "ADJ_VERTICAL_BAT_ANGLE": adj_vba})

    adj = pd.DataFrame(rows)

    # Split BATTER_KEY
    adj[["BATTER_ID", "BATTER_SIDE_FROM_KEY"]] = adj["BATTER_KEY"].str.split("_", n=1, expand=True)
    adj["BATTER_ID"] = adj["BATTER_ID"].astype(str)

    # Merge swing counts and finalize "stakeholder style" output table
    adj = adj.merge(counts.rename("N_SWINGS"), left_on="BATTER_KEY", right_index=True, how="left")
    adj = adj[["BATTER_ID", "BATTER_SIDE", "N_SWINGS", "ADJ_VERTICAL_BAT_ANGLE"]].sort_values(
        "ADJ_VERTICAL_BAT_ANGLE"
    )

    print("\nAdjusted VBA leaderboard (synthetic demo; head):")
    print(adj.head(12).to_string(index=False))


if __name__ == "__main__":
    main()

