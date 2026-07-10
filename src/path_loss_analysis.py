from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import deepmimo as dm

from plot_style import (
    new_dark_figure, style_axes, style_legend,
    LINE_ACCENT, LOS_COLOR, NLOS_COLOR, GRID,
)

def load_scenario(scenario_name: str = "asu_campus_3p5"):
    dm.download(scenario_name)
    return dm.load(scenario_name)


def compute_3d_distance(user_coords: np.ndarray, tx_coord: np.ndarray) -> np.ndarray:
    return np.sqrt(np.sum((user_coords - tx_coord) ** 2, axis=1))


def friis_path_loss(distances: np.ndarray, frequency_mhz: float,
                     num_tx_antennas: int, num_rx_antennas: int) -> np.ndarray:
    distances_safe = np.where(distances == 0, 1, distances)

    standard_friis = 20 * np.log10(distances_safe) + 20 * np.log10(frequency_mhz) - 27.55

    g_tx = 10 * np.log10(num_tx_antennas)
    g_rx = 10 * np.log10(num_rx_antennas)

    return standard_friis - g_tx - g_rx


def downsample(*arrays, factor: int = 10):
    return tuple(arr[::factor] for arr in arrays)


def plot_path_loss_scatter(distances, path_loss, los_status, theoretical_loss):

    los_mask = los_status == 1
    nlos_mask = los_status == 0
    sort_idx = np.argsort(distances)

    fig, ax = new_dark_figure(figsize=(10, 5))

    ax.scatter(distances[nlos_mask], path_loss[nlos_mask],
               alpha=0.25, color=NLOS_COLOR, s=1.5, label="NLoS (Obstructed Path)")
    ax.scatter(distances[los_mask], path_loss[los_mask],
               alpha=0.65, color=LOS_COLOR, s=2.0, label="LoS (Direct Path)")
    ax.plot(distances[sort_idx], theoretical_loss[sort_idx],
            color=LINE_ACCENT, linewidth=1.8, linestyle="--",
            label="Theoretical Free-Space Model (Friis + 9.03 dB TX Gain)")

    ax.invert_yaxis()
    style_axes(ax,
               title="5G Channel Attenuation Profile vs. Free-Space Theory\n"
                     "ASU Campus Ray-Tracing Scenario (DeepMIMO)",
               xlabel="True 3D Distance from Base Station (m)",
               ylabel="Path Loss (dB)")
    style_legend(ax)

    plt.tight_layout()
    return fig, ax


def build_binned_profile(distances, path_loss, los_status, bin_size=10):

    df = pd.DataFrame({"distance": distances, "path_loss": path_loss, "los": los_status})
    df["dist_bin"] = np.round(df["distance"] / bin_size) * bin_size

    los_profile = df[df["los"] == 1].groupby("dist_bin")["path_loss"].agg(["mean", "std"]).reset_index()
    nlos_profile = df[df["los"] == 0].groupby("dist_bin")["path_loss"].agg(["mean", "std"]).reset_index()
    return los_profile, nlos_profile


def plot_binned_profile(los_profile, nlos_profile, distances, theoretical_loss):
    sort_idx = np.argsort(distances)

    fig, ax = new_dark_figure(figsize=(11, 6), panel_bg=True)

    ax.plot(los_profile["dist_bin"], los_profile["mean"],
            color=LOS_COLOR, linewidth=2.5, label="LoS Mean (Direct Path)")
    ax.fill_between(los_profile["dist_bin"],
                     los_profile["mean"] - los_profile["std"],
                     los_profile["mean"] + los_profile["std"],
                     color=LOS_COLOR, alpha=0.15)

    ax.plot(nlos_profile["dist_bin"], nlos_profile["mean"],
            color=NLOS_COLOR, linewidth=2.5, label="NLoS Mean (Obstructed Path)")
    ax.fill_between(nlos_profile["dist_bin"],
                     nlos_profile["mean"] - nlos_profile["std"],
                     nlos_profile["mean"] + nlos_profile["std"],
                     color=NLOS_COLOR, alpha=0.10)

    ax.plot(distances[sort_idx], theoretical_loss[sort_idx],
            color="#FFFFFF", linewidth=1.5, linestyle="--", alpha=0.7,
            label="Theoretical 3D Free-Space Limit (Friis + 9.03 dB Array Gain)")

    ax.invert_yaxis()
    ax.set_xlim(0, max(distances) * 1.02)

    style_axes(ax,
               title="LoS vs NLoS Path Loss: How Buildings Reshape 5G Signal Propagation",
               xlabel="3D Distance from Base Station (m)",
               ylabel="Path Loss Intensity (dB)",
               title_loc="left")

    ax.grid(True, linestyle='-', linewidth=0.6, color='#ffffff', alpha=0.06)

    ax.annotate("NLoS Shadow Fading\n(~25 dB Building Penetration Loss)",
                xy=(225, 118), xytext=(130, 130),
                fontweight="bold", color=NLOS_COLOR, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=NLOS_COLOR, lw=1.2))
    ax.annotate("Multipath Propagation\n(Local interference & variance)",
                xy=(280, 88), xytext=(305, 75),
                fontweight="bold", color=LOS_COLOR, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=LOS_COLOR, lw=1.2))

    style_legend(ax, fontsize=9.5)

    plt.tight_layout()
    return fig, ax


def run_path_loss_analysis(dataset, frequency_mhz=3500, num_tx_antennas=8,
                            num_rx_antennas=1, downsample_factor=10,
                            save_dir=None):
    user_coords = dataset.rx_pos
    tx_coord = dataset.tx_pos[0]

    distances = compute_3d_distance(user_coords, tx_coord)
    path_loss = dataset.pathloss
    los_status = dataset.los

    theoretical_loss = friis_path_loss(distances, frequency_mhz,
                                        num_tx_antennas, num_rx_antennas)

    d_sub, pl_sub, los_sub, theo_sub = downsample(
        distances, path_loss, los_status, theoretical_loss,
        factor=downsample_factor,
    )

    fig1, _ = plot_path_loss_scatter(d_sub, pl_sub, los_sub, theo_sub)

    los_profile, nlos_profile = build_binned_profile(d_sub, pl_sub, los_sub)
    fig2, _ = plot_binned_profile(los_profile, nlos_profile, d_sub, theo_sub)

    if save_dir is None:
        save_dir = Path(__file__).resolve().parents[1] / "plots"
    else:
        save_dir = Path(save_dir)

    save_dir.mkdir(parents=True, exist_ok=True)
    fig1.savefig(save_dir / "asu_campus_3p5_path_loss_scatter.png",
                 dpi=300, bbox_inches="tight")
    fig2.savefig(save_dir / "asu_campus_3p5_los_nlos_path_loss_profile.png",
                 dpi=300, bbox_inches="tight")

    return {
        "distances": d_sub,
        "path_loss": pl_sub,
        "los_status": los_sub,
        "theoretical_loss": theo_sub,
        "los_profile": los_profile,
        "nlos_profile": nlos_profile,
        "figures": (fig1, fig2),
    }