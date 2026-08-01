"""
QSC Stabilization Control Surface — v3

Parameter-optimized control law.
Residual stability: 0.7518 → 0.8395  (+0.0877)
Residual std:       0.4645 → 0.3177  (−31.6 %)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime
import json

from qsc_core import QSCParams, readiness


@dataclass
class StabilizationParamsV3:
    breath_amp: float = 0.05
    breath_freq: float = 0.40
    osc_decay: float = 0.15
    target_stability: float = 0.83


def stabilized_readiness(t, qsc, sp):
    t = np.asarray(t, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        power = np.where(t > 0, (t / qsc.T) ** qsc.D, 0.0)
    breath = 1.0 + sp.breath_amp * np.sin(2 * np.pi * sp.breath_freq * t)
    osc_amp = np.exp(-sp.osc_decay * t)
    rhythmic = np.sin(qsc.omega * t) * breath * osc_amp
    decay = np.exp(-qsc.lambda_ * t)
    return qsc.A * power * rhythmic * decay + qsc.C


def residual_from_growth(t, r, qsc):
    t = np.asarray(t, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        power = np.where(t > 0, (t / qsc.T) ** qsc.D, 1e-12)
    power = np.maximum(power, 1e-12)
    return (r - qsc.C) / power


def stability_score(signal, window=50):
    signal = np.asarray(signal, dtype=float)
    n = len(signal)
    local_std = np.zeros(n)
    half = window // 2
    for i in range(n):
        lo = max(0, i - half)
        hi = min(n, i + half + 1)
        local_std[i] = np.std(signal[lo:hi])
    return 1.0 / (1.0 + float(np.mean(local_std)))


def run_v3_trial(t_max=10.0, dt=0.01, qsc=None, sp=None):
    if qsc is None: qsc = QSCParams()
    if sp is None: sp = StabilizationParamsV3()
    t = np.arange(0.0, t_max + dt / 2, dt)
    r_base = readiness(t, qsc)
    r_stab = stabilized_readiness(t, qsc, sp)
    resid_base = residual_from_growth(t, r_base, qsc)
    resid_stab = residual_from_growth(t, r_stab, qsc)
    score_base = stability_score(resid_base)
    score_stab = stability_score(resid_stab)
    metrics = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "v3",
        "stability_score_base_residual": score_base,
        "stability_score_stabilized_residual": score_stab,
        "improvement": score_stab - score_base,
        "residual_std_base": float(np.std(resid_base)),
        "residual_std_stabilized": float(np.std(resid_stab)),
        "relative_std_reduction": float((np.std(resid_base) - np.std(resid_stab)) / np.std(resid_base)),
        "stabilization_params": asdict(sp),
    }
    return {"t": t, "R_base": r_base, "R_stabilized": r_stab, "metrics": metrics}


if __name__ == "__main__":
    print(json.dumps(run_v3_trial()["metrics"], indent=2))
