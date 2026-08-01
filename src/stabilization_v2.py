"""
QSC Stabilization Control Surface — v2

Improved control law that raises residual stability.

R_stab(t) = A * (t/T)^D * [sin(ωt) * breath(t) * osc_amp(t)] * exp(-λt) + C
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime
import json

from qsc_core import QSCParams, readiness


@dataclass
class StabilizationParams:
    breath_amp: float = 0.12
    breath_freq: float = 0.25
    osc_decay: float = 0.08
    target_stability: float = 0.80


def stabilized_readiness(
    t: np.ndarray,
    qsc: QSCParams,
    sp: StabilizationParams,
) -> np.ndarray:
    t = np.asarray(t, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        power = np.where(t > 0, (t / qsc.T) ** qsc.D, 0.0)
    breath = 1.0 + sp.breath_amp * np.sin(2 * np.pi * sp.breath_freq * t)
    osc_amp = np.exp(-sp.osc_decay * t)
    rhythmic = np.sin(qsc.omega * t) * breath * osc_amp
    decay = np.exp(-qsc.lambda_ * t)
    return qsc.A * power * rhythmic * decay + qsc.C


def residual_from_growth(t: np.ndarray, r: np.ndarray, qsc: QSCParams) -> np.ndarray:
    t = np.asarray(t, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        power = np.where(t > 0, (t / qsc.T) ** qsc.D, 1e-12)
    power = np.maximum(power, 1e-12)
    return (r - qsc.C) / power


def stability_score(signal: np.ndarray, window: int = 50) -> float:
    signal = np.asarray(signal, dtype=float)
    n = len(signal)
    local_std = np.zeros(n)
    half = window // 2
    for i in range(n):
        lo = max(0, i - half)
        hi = min(n, i + half + 1)
        local_std[i] = np.std(signal[lo:hi])
    mean_std = float(np.mean(local_std))
    return 1.0 / (1.0 + mean_std)


def run_v2_trial(
    t_max: float = 10.0,
    dt: float = 0.01,
    qsc: Optional[QSCParams] = None,
    sp: Optional[StabilizationParams] = None,
) -> Dict[str, Any]:
    if qsc is None:
        qsc = QSCParams()
    if sp is None:
        sp = StabilizationParams()

    t = np.arange(0.0, t_max + dt / 2, dt)
    r_base = readiness(t, qsc)
    r_stab = stabilized_readiness(t, qsc, sp)

    resid_base = residual_from_growth(t, r_base, qsc)
    resid_stab = residual_from_growth(t, r_stab, qsc)

    score_base = stability_score(resid_base)
    score_stab = stability_score(resid_stab)

    metrics = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "qsc_params": qsc.to_dict(),
        "stabilization_params": asdict(sp),
        "stability_score_base_residual": score_base,
        "stability_score_stabilized_residual": score_stab,
        "improvement": score_stab - score_base,
        "residual_std_base": float(np.std(resid_base)),
        "residual_std_stabilized": float(np.std(resid_stab)),
    }
    return {"t": t, "R_base": r_base, "R_stabilized": r_stab, "metrics": metrics}


if __name__ == "__main__":
    trial = run_v2_trial()
    print(json.dumps(trial["metrics"], indent=2))
