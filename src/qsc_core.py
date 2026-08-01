"""
Quantum Spiral of Consciousness (QSC) — Core Implementation
Clean, reproducible version of the readiness function.

R(t) = A * (t / T)**D * sin(ω t) * exp(-λ t) + C
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class QSCParams:
    A: float = 1.0
    T: float = 1.0
    D: float = 1.5
    omega: float = 2 * np.pi
    lambda_: float = 0.1
    C: float = 0.5
    hbar: float = 1.0545718e-34

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


def readiness(t: np.ndarray, params: QSCParams) -> np.ndarray:
    t = np.asarray(t, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        power = np.where(t > 0, (t / params.T) ** params.D, 0.0)
    rhythmic = np.sin(params.omega * t)
    decay = np.exp(-params.lambda_ * t)
    return params.A * power * rhythmic * decay + params.C


def simulate_trajectory(
    t_max: float = 10.0,
    dt: float = 0.01,
    params: Optional[QSCParams] = None,
) -> Dict[str, Any]:
    if params is None:
        params = QSCParams()
    t = np.arange(0.0, t_max + dt / 2, dt)
    r = readiness(t, params)
    return {
        "t": t,
        "R": r,
        "summary": {
            "mean_R": float(np.mean(r)),
            "std_R": float(np.std(r)),
            "min_R": float(np.min(r)),
            "max_R": float(np.max(r)),
            "params": params.to_dict(),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
    }
