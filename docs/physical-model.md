<!-- Copyright (c) 2026 Marco Pezzullo / Silicon LogiX. See LICENSE. -->
# Physical model

Configuration is `assets/config/plant.json`, validated before startup. Fixed integration step defaults to 0.1 s. Speed only changes wall-clock pacing; pause skips physical/controller ticks while fresh device heartbeats continue.

Rotor presentation interpolates only between two confirmed telemetry poses, including the recorded number and direction of turns. It never advances beyond the latest confirmed pose; pause and stale telemetry stop motion. Recorded physical state and energy accounting remain unchanged.

For upper and lower volumes `Vu`, `Vl`, reservoir areas `Au`, `Al` and floor elevations `bu`, `bl`:

```
zu = bu + Vu/Au; zl = bl + Vl/Al; H = zu - zl
Qi = Qmax * inlet_actual * wicket_actual * rpm_actual/rated_rpm
dV = (Q1 + Q2) * dt; Vu -= dV; Vl += dV
Phyd = rho * g * mean(H_before, H_after) * Qi
Pgen = eta_generation * Phyd
Ppump = Phyd / eta_pump                     # negative power
```

Density is 1000 kg/m³ and gravity is 9.81 m/s². Efficiencies are constant 0.90 and 0.85. The two groups share their instantaneous head. Linear slew limits represent valve, wicket and rotor dynamics. Requested positions are distinct from confirmed positions. Rotor angle integrates signed rpm on the simulation clock.

The combined transfer is limited against both reservoir envelopes (default 10–90%), then the original flow split is preserved. The limit event counter increments when a physical step is clipped. FORTE uses the envelope input as an interlock on subsequent ticks. The simulator's numerical clamp remains a physical bound even when a controller is unavailable.

Potential energy is calculated consistently as:

```
Ep = rho*g*(bu*Vu + Vu²/(2*Au) + bl*Vl + Vl²/(2*Al))
residual = Ep - Ep_initial + E_generated - E_absorbed + E_losses
```

Mean head makes this identity exact for the constant-area model. Reported losses are hydraulic-to-electric conversion loss; no auxiliary consumer is configured in version 0.2. The electrical-disconnection fault sets exported power to zero. Downward flow dissipates hydraulic energy. Disconnected pumping transfers no uphill water because stored kinetic energy is absent from this model.

The model does not include water hammer, pressure-wave propagation, cavitation, rotor inertia energy, grid frequency, synchronization angle, generator excitation or commercial protection qualification. Sensor mismatch produces a repeatable +60 r/min measured-sensor offset, uncertain UA quality and an injected controller validity flag; it is not an independently calibrated sensor model. OPC UA engineering measures are simulation data.

The original geometry is a scaled plant scenario. Physical reservoir levels are mapped into the authored ±0.65 m display range using fill fractions; this display mapping is separate from the actual head calculation. Site gates follow the largest confirmed inlet opening as a simplified common-services display proxy. The crane is only exercised by the original audited inspection clip; no arbitrary crane control is exposed.
