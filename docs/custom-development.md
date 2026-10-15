<!-- Copyright (c) 2026 Marco Pezzullo / Silicon LogiX. See LICENSE. -->
# Custom engineering proposals

The Custom engineering page presents **unimplemented development proposals**. Scope, delivery, performance and acceptance criteria require a feasibility study and an agreed validation plan.

| Module | Goal | Validation |
|---|---|---|
| Live PLC / SCADA integration | Connect real plant devices and command interfaces. | Interface contracts, independent telemetry, command / reconnection trials. |
| Secure industrial OPC UA | Certificates, authenticated identities, roles and deployment policies. | Certificate lifecycle, permissions and security review. |
| Calibrated hydraulic dynamics | Site calibration, variable efficiency, pressure transients and cavitation studies. | Measured points, uncertainty and independent transient fixtures. |
| Advanced energy dispatch | Tariff scheduling, reservoir optimisation and grid-service studies. | Historical replay, constraints and independent benchmarks. |
| Enterprise historian / hardware-in-the-loop | Existing historian integration and real-controller coupling. | Clock alignment, retention, latency and recovery trials. |
| Custom plant twin and SDK | Plant-specific CAD, multiple sites, dashboards and core integration. | Tag mapping, numerical API fixtures and agreed scenarios. |

Select modules and enter project, objective and constraints. Save local brief writes JSON and text to Documents/Silicon LogiX/GridPilot/briefs. Every module is marked implemented:false in the JSON. Briefs are requirement documents, separate from session/strategy reports.

The contact button opens Silicon LogiX's contact page. The application never sends the brief. Included capabilities and model limits are presented separately in Model & validation; proposals are never displayed as working controls.
