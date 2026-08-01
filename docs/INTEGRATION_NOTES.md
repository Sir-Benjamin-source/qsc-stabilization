# Integration Notes — QSC Stabilization ↔ Head-to-Head ↔ Core

**Date:** 2026-08-01

## Roles

| Repository | Role |
|------------|------|
| **spiral-head-to-head** | Public testing ground. Classical baselines vs Spiral-inspired feature refinement on standard OpenML/UCI tasks. Full provenance, pre-registration, reproducible harness. |
| **qsc-stabilization** | Continuous process substrate: readiness field, residual-stability control (v3 + adaptive + TCRF), Poetry/SRM association, examination metrics. |
| **spiral-theory-core / Spiral-Path** | Discrete algebraic and relational cores (Path, Syncratude, TRE, Generosity Exponent, Spiral Operator). |

## Integration principles

1. Head-to-head is the competition surface. Claims of tabular (or other) improvement are tested there under pre-registered protocol.
2. QSC / TCRF is the continuous stabilizer. Mature control ideas may later be mapped into feature routines that head-to-head evaluates.
3. Ethical gates remain active (Generosity / E-shield style floors, harm-horizon). TCRF carries `e_shield_floor`.
4. No silent transfer. Cross-domain mapping must be explicit, logged, and re-tested.

## Current TCRF (tightened)

- Residual stability: 0.674 → **0.747** (+0.073)
- Residual std reduction: **−24 %**
- Adaptive surface still holds the residual-stability record at **0.863**.

---

*Reality is the only authority. Everything else is hypothesis. Head-to-head is the testing ground.*
