"""
force_plate_velocity_sample.py

Public, runnable sample adapted from my original project code:
Drive-foot force plate profiling and pitch velocity.

This script mirrors the project workflow:
1) Generate synthetic pitch-by-frame force plate data (no real data included)
2) Clean + validate columns
3) Normalize forces by body weight (lbf -> N; then /BW)
4) Align time to ball release (t=0), standardize forward-force sign
5) Engineer per-pitch features (peaks, impulses, RFD, timing)
6) Aggregate to pitcher-level summaries
7) Fit an OLS model (normal equation) linking mechanics to velocity
8) Plot relationships + example mean/SD force–time profiles

Author: Anna Busatto
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple


# -----------------------------
# Parameters
# -----------------------------
FS = 300.0
DT = 1.0 / FS

WIN_T_MIN = -1.0
WIN_T_MAX = 0.0

LBF_TO_N = 4.448

RANDOM_SEED = 4


# -----------------------------
# Column names
# -----------------------------
COLS = {
    "PITCH_ID": "pitch_id",
    "PITCHER_ID": "pitcher_id",
    "PITCHER_THROWS": "throws",
    "WEIGHT_LB": "weight_lb",
    "VELOCITY_MPH": "velocity_mph",
    "FRAME": "frame",
    "BALL_RELEASE": "ball_release",
    "FORCE_X_LBF": "force_x_lbf",
    "FORCE_Y_LBF": "force_y_lbf",
    "FORCE_Z_LBF": "force_z_lbf",
    "TORQUE_Z_NM": "torque_z_nm",
}


# -----------------------------
# Synthetic demo data generator
# -----------------------------
def make_synthetic_force_plate_data(
    n_pitchers: int = 8,
    pitches_per_pitcher: int = 12,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """
    Creates a synthetic, pitch-by-frame dataset with the same structure as the original project.
    One row = one frame of one pitch.

    Shapes are constructed so you get realistic "more coordinated" vs "less coordinated"
    force-time patterns across pitchers.
    """
    rng = np.random.default_rng(seed)

    # 1-second window sampled at 300 Hz -> ~301 samples including t=0
    t = np.arange(WIN_T_MIN, WIN_T_MAX + DT / 2, DT)
    n_frames = len(t)

    rows = []
    pitcher_ids = [f"P{p:02d}" for p in range(1, n_pitchers + 1)]
    throws = rng.choice(["R", "L"], size=n_pitchers, p=[0.75, 0.25])

    # Assign half pitchers to be "more coordinated" (later peak, smoother), half less coordinated
    coord_flag = np.array([1] * (n_pitchers // 2) + [0] * (n_pitchers - n_pitchers // 2))
    rng.shuffle(coord_flag)

    for i, pid in enumerate(pitcher_ids):
        is_coord = coord_flag[i] == 1

        # body weight (lb)
        weight_lb = float(rng.normal(205, 20))

        # base velo distribution (mph)
        # coordinated pitchers slightly faster on average
        vel_base = rng.normal(93, 2) if is_coord else rng.normal(86, 2)

        for j in range(pitches_per_pitcher):
            pitch_id = f"{pid}_pitch{j:03d}"

            # ball release frame index: align t=0 to final frame for simplicity
            ball_release = int(n_frames - 1)

            # Create synthetic forward force FY (lbf)
            # Build-up then peak near release; coordinated peaks later + smoother
            peak_time = -0.22 if is_coord else -0.45
            peak_width = 0.16 if is_coord else 0.22
            peak_amp = (180 if is_coord else 140) + rng.normal(0, 8)

            fy = peak_amp * np.exp(-0.5 * ((t - peak_time) / peak_width) ** 2)

            # Add small early load bump
            fy += (25 + rng.normal(0, 3)) * np.exp(-0.5 * ((t + 0.85) / 0.18) ** 2)

            # Add noise and slight dip post-peak (unloading)
            fy += rng.normal(0, 3, size=n_frames)
            fy -= (40 if is_coord else 25) * np.exp(-0.5 * ((t + 0.05) / 0.08) ** 2)

            # Some pitches will have negative sign
            if rng.random() < 0.25:
                fy *= -1.0

            # Vertical force FZ (lbf): broader hump + steadier
            fz_amp = (260 if is_coord else 230) + rng.normal(0, 10)
            fz = fz_amp * np.exp(-0.5 * ((t + 0.30) / 0.35) ** 2) + rng.normal(0, 4, size=n_frames)

            # Torque Z (Nm): coordinated has clearer rise and peak closer to force rise
            tz_peak_time = -0.28 if is_coord else -0.55
            tz_amp = (85 if is_coord else 65) + rng.normal(0, 4)
            tz = tz_amp * np.exp(-0.5 * ((t - tz_peak_time) / 0.22) ** 2) + rng.normal(0, 2, size=n_frames)

            # Velocity per pitch
            velocity = float(vel_base + rng.normal(0, 0.8))

            for k in range(n_frames):
                rows.append(
                    {
                        COLS["PITCH_ID"]: pitch_id,
                        COLS["PITCHER_ID"]: pid,
                        COLS["PITCHER_THROWS"]: throws[i],
                        COLS["WEIGHT_LB"]: weight_lb,
                        COLS["VELOCITY_MPH"]: velocity,
                        COLS["FRAME"]: k,
                        COLS["BALL_RELEASE"]: ball_release,
                        COLS["FORCE_X_LBF"]: 0.0,  # unused in this sample
                        COLS["FORCE_Y_LBF"]: float(fy[k]),
                        COLS["FORCE_Z_LBF"]: float(fz[k]),
                        COLS["TORQUE_Z_NM"]: float(tz[k]),
                    }
                )

    return pd.DataFrame(rows)


# -----------------------------
# Feature engineering
# -----------------------------
def compute_pitch_features_from_raw(pitch_df_raw: pd.DataFrame, tmin=WIN_T_MIN, tmax=WIN_T_MAX) -> Dict[str, float]:
    sub = pitch_df_raw[(pitch_df_raw["REL_TIME"] >= tmin) & (pitch_df_raw["REL_TIME"] <= tmax)].copy()
    sub = sub.sort_values("REL_TIME")
    base = pitch_df_raw.iloc[0]

    def stub():
        return {
            "pitch_id": base[COLS["PITCH_ID"]],
            "pitcher_id": base[COLS["PITCHER_ID"]],
            "throws": base[COLS["PITCHER_THROWS"]],
            "weight_lb": base[COLS["WEIGHT_LB"]],
            "velocity_mph": base[COLS["VELOCITY_MPH"]],
            "PEAK_FY_BW": np.nan,
            "T_PEAK_FY": np.nan,
            "PEAK_FZ_BW": np.nan,
            "T_PEAK_FZ": np.nan,
            "PEAK_TZ": np.nan,
            "T_PEAK_TZ": np.nan,
            "T_TO_PEAK_FY": np.nan,
            "RFD_FY": np.nan,
            "IMP_FY_BW": np.nan,
            "IMP_FZ_BW": np.nan,
            "IMP_TZ": np.nan,
        }

    if sub.empty:
        return stub()

    t = sub["REL_TIME"].to_numpy()
    fy_bw = sub["FY_BW_SIGNED"].to_numpy()
    fz_bw = sub["FZ_BW"].to_numpy()
    tz = sub[COLS["TORQUE_Z_NM"]].to_numpy()

    def safe_argmax(a, use_abs=False):
        if a.size == 0 or np.all(np.isnan(a)):
            return None
        arr = np.abs(a) if use_abs else a
        return int(np.nanargmax(arr))

    pfy = safe_argmax(fy_bw)
    pfz = safe_argmax(fz_bw)
    ptz = safe_argmax(tz, use_abs=True)

    peak_fy = fy_bw[pfy] if pfy is not None else np.nan
    peak_fz = fz_bw[pfz] if pfz is not None else np.nan
    peak_tz = tz[ptz] if ptz is not None else np.nan

    t_peak_fy = t[pfy] if pfy is not None else np.nan
    t_peak_fz = t[pfz] if pfz is not None else np.nan
    t_peak_tz = t[ptz] if ptz is not None else np.nan

    t_to_peak_fy = t_peak_fy - t[0] if (len(t) and np.isfinite(t_peak_fy)) else np.nan
    if isinstance(t_to_peak_fy, (int, float)) and t_to_peak_fy <= 0:
        t_to_peak_fy = np.nan

    imp_fy = np.trapz(np.nan_to_num(fy_bw, nan=0.0), np.nan_to_num(t, nan=0.0))
    imp_fz = np.trapz(np.nan_to_num(fz_bw, nan=0.0), np.nan_to_num(t, nan=0.0))
    imp_tz = np.trapz(np.abs(np.nan_to_num(tz, nan=0.0)), np.nan_to_num(t, nan=0.0))

    fy0 = fy_bw[0] if len(fy_bw) else np.nan
    rfd_fy = (
        (peak_fy - fy0) / t_to_peak_fy
        if (np.isfinite(peak_fy) and np.isfinite(fy0) and np.isfinite(t_to_peak_fy) and t_to_peak_fy > 0)
        else np.nan
    )

    return {
        "pitch_id": base[COLS["PITCH_ID"]],
        "pitcher_id": base[COLS["PITCHER_ID"]],
        "throws": base[COLS["PITCHER_THROWS"]],
        "weight_lb": base[COLS["WEIGHT_LB"]],
        "velocity_mph": base[COLS["VELOCITY_MPH"]],
        "PEAK_FY_BW": peak_fy,
        "T_PEAK_FY": t_peak_fy,
        "PEAK_FZ_BW": peak_fz,
        "T_PEAK_FZ": t_peak_fz,
        "PEAK_TZ": peak_tz,
        "T_PEAK_TZ": t_peak_tz,
        "T_TO_PEAK_FY": t_to_peak_fy,
        "RFD_FY": rfd_fy,
        "IMP_FY_BW": imp_fy,
        "IMP_FZ_BW": imp_fz,
        "IMP_TZ": imp_tz,
    }


# -----------------------------
# Visualization helpers
# -----------------------------
def scatter_with_fit(x, y, xlabel, ylabel, title):
    plt.figure(figsize=(6.5, 4.8))
    plt.scatter(x, y, alpha=0.6)
    A = np.column_stack([x, np.ones(len(x))])
    m, b = np.linalg.lstsq(A, y, rcond=None)[0]
    x_line = np.linspace(np.min(x), np.max(x), 100)
    y_line = m * x_line + b
    plt.plot(x_line, y_line)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()
    print(f"{title} - n={len(x)}, slope={m:.3f}, intercept={b:.3f}")


def _moving_avg(x, w=7):
    if w < 3 or w % 2 == 0:
        return x
    pad = w // 2
    y = np.full_like(x, np.nan, dtype=float)
    for i in range(pad, len(x) - pad):
        y[i] = np.nanmean(x[i - pad : i + pad + 1])
    return y


def mean_profile_with_sd_clean(group_df, col, fs=FS, tmin=WIN_T_MIN, tmax=WIN_T_MAX, min_coverage=0.5, smooth_window=7):
    dt = 1.0 / fs
    grid = np.arange(tmin, tmax + dt / 2, dt)

    tmp = group_df[["REL_TIME", col, COLS["PITCH_ID"]]].copy()
    tmp["bin"] = (tmp["REL_TIME"] / dt).round().astype(int)

    grid_df = pd.DataFrame({"bin": (grid / dt).round().astype(int), "REL_TIME": grid})
    merged = grid_df.merge(tmp[["bin", COLS["PITCH_ID"], col]], on="bin", how="left")

    n_total = group_df[COLS["PITCH_ID"]].nunique()
    contrib = (
        merged.dropna(subset=[col])
        .groupby("bin")[COLS["PITCH_ID"]]
        .nunique()
        .reindex(grid_df["bin"].values)
        .fillna(0)
        .to_numpy()
    )
    coverage = contrib / max(n_total, 1)

    mean = merged.groupby("bin")[col].mean().reindex(grid_df["bin"].values).to_numpy()
    sd = merged.groupby("bin")[col].std().reindex(grid_df["bin"].values).to_numpy()

    low = coverage < float(min_coverage)
    mean[low] = np.nan
    sd[low] = np.nan

    if smooth_window and smooth_window >= 3 and smooth_window % 2 == 1:
        mean = _moving_avg(mean, w=int(smooth_window))

    return grid, mean, sd, coverage


# -----------------------------
# Main
# -----------------------------
def main():
    # 1) Synthetic data
    df = make_synthetic_force_plate_data(n_pitchers=10, pitches_per_pitcher=10)

    # 2) Basic validation + type coercion
    expected_cols = list(COLS.values())
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    num_cols = [
        COLS["WEIGHT_LB"],
        COLS["VELOCITY_MPH"],
        COLS["FRAME"],
        COLS["BALL_RELEASE"],
        COLS["FORCE_X_LBF"],
        COLS["FORCE_Y_LBF"],
        COLS["FORCE_Z_LBF"],
        COLS["TORQUE_Z_NM"],
    ]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(
        subset=[
            COLS["PITCH_ID"],
            COLS["PITCHER_ID"],
            COLS["PITCHER_THROWS"],
            COLS["WEIGHT_LB"],
            COLS["VELOCITY_MPH"],
            COLS["FRAME"],
            COLS["BALL_RELEASE"],
            COLS["FORCE_Y_LBF"],
            COLS["FORCE_Z_LBF"],
            COLS["TORQUE_Z_NM"],
        ]
    ).copy()

    print(f"Rows after cleaning: {len(df):,}")
    print(f"Unique pitchers: {df[COLS['PITCHER_ID']].nunique()}")

    # 3) Normalize forces by BW (lbf->N then /BW) + align to release
    df["BW_N"] = df[COLS["WEIGHT_LB"]] * LBF_TO_N
    df["FY_BW"] = df[COLS["FORCE_Y_LBF"]] * LBF_TO_N / df["BW_N"]
    df["FZ_BW"] = df[COLS["FORCE_Z_LBF"]] * LBF_TO_N / df["BW_N"]

    df["REL_FRAME"] = df[COLS["FRAME"]] - df[COLS["BALL_RELEASE"]]
    df["REL_TIME"] = df["REL_FRAME"] * DT

    # 4) Standardize FY sign so + = toward home (median in window)
    in_win = (df["REL_TIME"] >= WIN_T_MIN) & (df["REL_TIME"] <= WIN_T_MAX)
    med_by_pitch = df.loc[in_win].groupby(COLS["PITCH_ID"])["FY_BW"].median()
    flip_ids = med_by_pitch[med_by_pitch < 0].index

    df["FY_BW_SIGNED"] = df["FY_BW"]
    df.loc[df[COLS["PITCH_ID"]].isin(flip_ids), "FY_BW_SIGNED"] *= -1
    print(f"Pitches flipped (FY -> +home): {len(flip_ids)}")

    # 5) Per-pitch features
    feat_rows = df.groupby(COLS["PITCH_ID"], sort=False).apply(lambda g: compute_pitch_features_from_raw(g))
    pitch_feats = pd.DataFrame(list(feat_rows))

    all_pitches = df[[COLS["PITCH_ID"], COLS["PITCHER_ID"], COLS["PITCHER_THROWS"], COLS["WEIGHT_LB"], COLS["VELOCITY_MPH"]]].drop_duplicates()
    all_pitches = all_pitches.rename(
        columns={
            COLS["PITCH_ID"]: "pitch_id",
            COLS["PITCHER_ID"]: "pitcher_id",
            COLS["PITCHER_THROWS"]: "throws",
            COLS["WEIGHT_LB"]: "weight_lb",
            COLS["VELOCITY_MPH"]: "velocity_mph",
        }
    )

    pitch_feats = all_pitches.merge(
        pitch_feats,
        on=["pitch_id", "pitcher_id", "throws", "weight_lb", "velocity_mph"],
        how="left",
    )

    print("\nPer-pitch features (head):")
    print(pitch_feats.head(8).to_string(index=False))

    # 6) Pitcher-level aggregation (mean features + velocity mean/std + N pitches)
    agg_funcs = {
        "velocity_mph": ["mean", "std", "count"],
        "PEAK_FY_BW": "mean",
        "PEAK_FZ_BW": "mean",
        "PEAK_TZ": "mean",
        "RFD_FY": "mean",
        "T_TO_PEAK_FY": "mean",
        "IMP_FY_BW": "mean",
        "IMP_FZ_BW": "mean",
        "IMP_TZ": "mean",
    }

    pitcher_summary = pitch_feats.groupby(["pitcher_id", "throws"], as_index=False).agg(agg_funcs)
    pitcher_summary.columns = [
        "_".join([str(c) for c in col if c not in ("", None)]) if isinstance(col, tuple) else col
        for col in pitcher_summary.columns
    ]
    pitcher_summary = pitcher_summary.rename(
        columns={
            "velocity_mph_mean": "VEL_MEAN",
            "velocity_mph_std": "VEL_STD",
            "velocity_mph_count": "N_PITCHES_tmp",
        }
    )

    unique_counts = pitch_feats.groupby(["pitcher_id", "throws"])["pitch_id"].nunique().reset_index(name="N_PITCHES")
    pitcher_summary = pitcher_summary.drop(columns=["N_PITCHES_tmp"]).merge(unique_counts, on=["pitcher_id", "throws"], how="left")

    print("\nPitcher summary (head):")
    print(pitcher_summary.head(6).to_string(index=False))

    # 7) OLS model (normal equation) on per-pitch features
    model_df = pitch_feats[["velocity_mph", "PEAK_FY_BW", "RFD_FY", "IMP_FY_BW", "PEAK_TZ"]].dropna()
    X = np.column_stack(
        [
            np.ones(len(model_df)),
            model_df["PEAK_FY_BW"].values,
            model_df["RFD_FY"].values,
            model_df["IMP_FY_BW"].values,
            model_df["PEAK_TZ"].values,
        ]
    )
    y = model_df["velocity_mph"].values

    beta = np.linalg.pinv(X.T @ X) @ (X.T @ y)
    y_hat = X @ beta
    resid = y - y_hat
    ss_res = np.sum(resid**2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot

    coef_names = ["Intercept", "PEAK_FY_BW", "RFD_FY", "IMP_FY_BW", "PEAK_TZ"]
    coef_table = pd.DataFrame({"feature": coef_names, "coef": beta})
    coef_table["units"] = ["MPH", "MPH per BW", "MPH per (BW/s)", "MPH per (BW*s)", "MPH per Nm"]

    print("\nOLS coefficients (synthetic demo):")
    print(coef_table.to_string(index=False))
    print(f"R2: {r2:.3f} | n={len(model_df)}")

    # 8) Scatter plots
    for feat, xl in [
        ("PEAK_FY_BW", "Peak FY (BW)"),
        ("RFD_FY", "RFD FY (BW/s)"),
        ("IMP_FY_BW", "Impulse FY (BW*s)"),
        ("PEAK_TZ", "Peak Torque Z (Nm)"),
    ]:
        cur = pitch_feats[[feat, "velocity_mph"]].dropna()
        if len(cur) > 5:
            scatter_with_fit(cur[feat].values, cur["velocity_mph"].values, xl, "Velocity (MPH)", f"Velocity vs {xl}")

    # 9) Example mean/SD profiles: pick one high-velo and one low-velo pitcher (synthetic)
    vel_by_pitcher = pitch_feats.groupby("pitcher_id")["velocity_mph"].mean()
    high_pid = vel_by_pitcher.sort_values(ascending=False).index[0]
    low_pid = vel_by_pitcher.sort_values(ascending=True).index[0]

    for pid, label in [(high_pid, "Example A (higher-velocity profile)"), (low_pid, "Example B (lower-velocity profile)")]:
        g = df[df[COLS["PITCHER_ID"]] == pid].copy()

        t_fy, mu_fy, sd_fy, _ = mean_profile_with_sd_clean(g, "FY_BW_SIGNED")
        t_tz, mu_tz, sd_tz, _ = mean_profile_with_sd_clean(g, COLS["TORQUE_Z_NM"])

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6.5), sharex=True)
        fig.suptitle(f"{label}", fontsize=14)

        mask1 = np.isfinite(mu_fy) & np.isfinite(sd_fy)
        ax1.plot(t_fy, mu_fy, linewidth=2)
        ax1.fill_between(t_fy[mask1], (mu_fy - sd_fy)[mask1], (mu_fy + sd_fy)[mask1], alpha=0.18)
        ax1.axvline(0, linestyle="--")
        ax1.axhline(0, linewidth=0.8)
        ax1.grid(alpha=0.25, linestyle=":")
        ax1.set_ylabel("FY / BW (forward)")
        ax1.set_title("Average Drive Force Profile (± SD)", pad=6)

        mask2 = np.isfinite(mu_tz) & np.isfinite(sd_tz)
        ax2.plot(t_tz, mu_tz, linewidth=2)
        ax2.fill_between(t_tz[mask2], (mu_tz - sd_tz)[mask2], (mu_tz + sd_tz)[mask2], alpha=0.18)
        ax2.axvline(0, linestyle="--")
        ax2.axhline(0, linewidth=0.8)
        ax2.grid(alpha=0.25, linestyle=":")
        ax2.set_xlabel("Time to Release (s)")
        ax2.set_ylabel("Torque Z (Nm)")
        ax2.set_title("Average Rotational Torque Profile (± SD)", pad=6)

        ax2.set_xlim(WIN_T_MIN, WIN_T_MAX)
        plt.tight_layout(rect=[0, 0.02, 1, 0.95])
        plt.show()


if __name__ == "__main__":
    main()

