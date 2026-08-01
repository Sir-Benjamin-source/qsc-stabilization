# Examination Metrics — Compact Status

**Date:** 2026-08-01

## Purpose

Make association-chain length and examination depth explicit, logged quantities inside a small lattice driven by the stabilized QSC readiness function.

## Current Numbers (n_themes=10, t∈[0,6])

| Metric | Base (no stab.) | Stabilized v3 |
|--------|-----------------|---------------|
| Mean coherence | 0.493 | **0.519** |
| Mean association chain | 2.59 | 2.58 |
| Max association chain | 5 | 5 |
| Mean examination depth | 5.50 | **5.51** |
| Residual stability (on R) | 0.655 | **0.732** |

Adaptive controller (separate trial) still leads residual stability: **0.863** (+0.111 vs pure base).

## Interpretation

- Stabilization reliably lifts residual stability and mean coherence.
- Association-chain and examination-depth metrics are now live and measurable.
- Chain length is not yet strongly differentiated; next target is a control law that also lengthens or stabilizes association runs.
- Lattice kept small so the process stays inspectable and space-efficient.

---

*Reality is the only authority. Everything else is hypothesis.*
