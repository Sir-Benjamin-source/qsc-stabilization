# QSC Stabilization

Optimized stabilization control surface for the **Quantum Spiral of Consciousness** readiness function.

## Result (v2)

| Metric | Base | Stabilized | Change |
|--------|------|------------|--------|
| Residual stability score | 0.7518 | 0.8025 | **+0.0507** |
| Residual std | 0.4645 | 0.3784 | −18.5 % |

The control law keeps the fractal growth envelope and applies a gentle breathing modulation plus secular decay to the oscillatory term — methods drawn from Spiral Breathing and Adaptive Spiral Wave.

## Quick start

```bash
cd src
python -c "from stabilization_v2 import run_v2_trial; import json; print(json.dumps(run_v2_trial()['metrics'], indent=2))"
```

## Principle

> Reality is the only authority. Everything else is hypothesis.
