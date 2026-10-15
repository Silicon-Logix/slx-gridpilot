<!-- Copyright (c) 2026 Marco Pezzullo / Silicon LogiX. See LICENSE. -->
# Verification scope

The delivered Windows application was checked using independent OPC UA clients, native integration checks, numerical consistency checks and actual desktop captures. These checks concern the demonstrator; they do not qualify a physical plant or establish OPC UA certification.

| Area | Checked behavior |
|---|---|
| OPC UA and control | Three independent servers, typed methods, startup, stop, reversal, faults and recovery |
| Information model | Browse/Read, engineering units, source timestamps, data quality, NodeSet2 schema and independent import |
| Monitoring and alarms | Dedicated watchlists, revised intervals, deadband, standard conditions, refresh and acknowledgement |
| Workbench | Historical trends, actual timed-test results, recorded-state replay and seeking |
| Numerical model | Repeatable fixed steps, actuator limits, water and energy accounting |
| Desktop | Actual 3D rendering, unit identification, Studio learning tour and 125/150/200% UI scaling |
| Portable package | Launch with only Windows on PATH, confirmed generation, controlled stop and shutdown of child processes |
| Publication | Exact file inventory, headers, credentials, personal paths, stripped binaries and dependency attribution |

The supported graphics configuration is Windows x64 with a Vulkan-capable driver. Direct3D 12 and other operating systems are outside the validated configuration. Fixed simulation steps do not imply hard real-time guarantees. Model limits are documented in [physical assumptions](physical-model.md); endpoint security is documented in [OPC UA](opcua.md).

Raw logs, test fixtures, machine-specific reports and user sessions are excluded from the repository and release package. CI independently checks the published repository inventory and disclosure rules on every push.
