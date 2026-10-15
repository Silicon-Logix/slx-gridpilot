<!-- Copyright (c) 2026 Marco Pezzullo / Silicon LogiX. See LICENSE. -->
# OPC UA contract v1

Servers use open62541 1.4.14, independent processes and loopback URLs `4840` (services), `4841` (unit1), `4842` (unit2). Resolve namespace URI `urn:siliconlogix:gridpilot:v1`, rather than assuming the index. String NodeIds below are stable within schema 1.

| NodeId | Type | Unit / meaning |
|---|---|---|
| `Device` | Object | Named process identity |
| `Snapshot` | String | Complete coherent schema-1 JSON plant state |
| `Tick` | Double | Simulation integration tick, dimensionless |
| `SimTime` | Double | Seconds on the simulation clock |
| `Power` | Double | MW, plant or owning-unit signed exported power |
| `RequestedPower` | Double | MW, requested plant power |
| `Head` | Double | Metres |
| `LastCommand` | String | Request ID, accepted/rejected result |
| `State` | String | Unit sequence state; services LIVE / PAUSED / REPLAY mode |
| `UpperVolume`, `LowerVolume` | Double | m³, services |
| `UpperLevel`, `LowerLevel` | Double | m, services |
| `GeneratedEnergy`, `AbsorbedEnergy` | Double | MWh, services |
| `ValvePosition`, `ValveRequested` | Double | Actual/requested inlet opening, 0–1 |
| `WicketPosition`, `WicketRequested` | Double | Actual/requested wicket opening, 0–1 |
| `Speed`, `SpeedRequested` | Double | Actual/requested signed r/min |
| `SpeedSensor` | Double | Simulated measured r/min; +60 r/min offset and UncertainSensorNotAccurate under sensor injection |
| `Flow` | Double | m³/s, positive downwards |
| `Alarm` | Double | Unit alarm bit mask |
| `Request` | Method | JSON String input and queued receipt String output |

Measures are read-only AnalogItems with `EngineeringUnits` EUInformation properties, source timestamps and UA status quality. The source timestamp is UTC sample publication time, while `SimTime` is the process simulation time. A paused physical clock therefore still produces fresh source timestamps. Numeric leaves are convenience measures; read the `Snapshot` when coherent multi-variable data is required. All leaves in a publication share its source timestamp.

UNECE unit codes follow the [OPC Foundation engineering-unit mapping](https://reference.opcfoundation.org/specs/OPC-10000-8/5): MAW/5062999 for MW, MWH/5068616 for MWh, MTQ/5067857 for m³, MTR/5067858 for m and MQS/5067091 for m³/s.

The snapshot subscription requests `StatusValueTimestamp` notifications, 100 ms publishing and a one-sample queue. The GUI preserves the last confirmed state on connection failure, marks it stale after 2 s without a fresh source timestamp, and reconnects independently to each endpoint. Live rotor poses freeze on stale telemetry. A virtual device without a coordinator heartbeat marks `Snapshot` BadNoCommunication after 2 s.

## Requests

```json
{"action":"setpoint","mw":1.2}
{"action":"unit","unit":1,"mw":-1.2}
{"action":"strategy","name":"Balanced"}
{"action":"stop"}
{"action":"fault","unit":1,"kind":"valve"}
{"action":"recover","unit":1}
{"action":"acknowledge"}
{"action":"pause","value":true}
{"action":"speed","value":5}
{"action":"demo"}
{"action":"compare"}
{"action":"reset"}
{"action":"record"}
{"action":"replay"}
```

Power requests must be finite and within ±5 MW for the plant or ±2.5 MW per unit. Dispatch respects instantaneous hydraulic capacity, so acceptance does not promise full requested power. Opposing manual directions are rejected. Strategies are `Priority` or `Balanced`. Fault kinds are `valve`, `sensor`, `communication`, `electrical`; recovery clears the injected cause and requests the controller's fault release.

`Request` returns `{"id":"services-1","status":"queued"}`. Commands cross the device pipe to the coordinator, are range/mode checked, then are presented to FORTE on the next physical tick. `LastCommand` reports accepted/rejected. Device, GUI or terminal receipt is never displayed as the achieved physical position.

`acknowledge` adds an operator ACK journal event describing the active unit alarm masks. It leaves physical faults and FORTE latches unchanged. The desktop browser performs actual Browse / Read calls, including EUInformation and per-variable status; it does not synthesise a node table from the JSON snapshot. The command-line terminal also supports `browse`.

## Fault and communication policy

| Alarm bit | Meaning |
|---|---|
| 1 | Actuator sequence timeout (>12 simulated seconds) |
| 2 | Sensor mismatch validity input |
| 4 | Control communication missing for ≥2 simulated seconds |
| 8 | Electrical trip |
| 16 | Reservoir envelope interlock |
| 32 | Latched fault awaiting recovery |

The communication injection actually shuts down the selected UA endpoint. FORTE continues local control during the declared 2 s simulation grace period, then enters FAULT and closes wicket gates, removes speed demand after gate closure, and closes the inlet after the rotor rests. Reconnect does not automatically clear a latched fault. Losing only a supervisor connection leaves local control running. An exited group process is restarted with communication fault latched.

Policy None and anonymous access are appropriate to this local demonstration. This version does not implement certificate provisioning, encryption or a user-role model. No listener is configured on a public interface.

## Engineering services

`SetPower(Double PowerMW)` and `Stop()` return a String queue receipt. Unit devices additionally expose `Recover()`. Their arguments are ordinary OPC UA `Argument` metadata; Request remains available for the complete JSON contract. `SequencePhase`, `InterlockReason` and `TestPlanStatus` are timestamped String variables. Namespace URI discovery remains required.

Watchlists use a separate subscription from the coherent Snapshot. Sampling and publishing requests range from 50 to 5000 ms. The native client reports revised server intervals, per-item status/timestamp/notification count and session connection count. Zero deadband requests status/value/timestamp notifications. Positive absolute deadband requests status/value changes for numeric variables; text remains unfiltered. Deadband units follow each selected variable.

Each device exposes `U1Alarm` and/or `U2Alarm` instances of standard `OffNormalAlarmType` under Device. Subscribe to Device events, inspect Severity, Message, ActiveState/Id, AckedState/Id and Retain, and call the condition's standard Acknowledge with EventId and LocalizedText comment. ConditionRefresh republishes retained conditions. Physical causes and the FORTE fault latch remain active until recovery. The plant's acknowledgement counters synchronize acknowledged state across the device processes. The standard comment belongs to the condition receiving the method call. Conditions are recreated after a device process restart. This evaluation uses open62541 1.4.14's experimental A&C implementation; no OPC UA conformance certification is claimed.

Event filters support up to 64 selected fields. With asyncua, subscribing to `ConditionType` or providing a compact explicit filter stays within this limit; automatically selecting every optional field of `OffNormalAlarmType` exceeds it. The independent engineering test demonstrates condition subscriptions, refresh and acknowledgement.

Export nodes writes `GridPilot.NodeSet2.xml` beside JSON/CSV metadata and the connection recipe. It describes the browsed Device instances, variable data types/type definitions/engineering units and actual method argument declarations with the application namespace remapped to index 1. Runtime values and condition event history are omitted; a String preview is not treated as a complete stored value. Standard types are referenced in namespace zero. The file describes the device information model, rather than a server backup or executable method implementation.

Test plans use `{"action":"scenario","plan":...}`; cancel with `{"action":"scenario_cancel"}`. Create and validate plans in Workbench; its actions are limited to power, stop, fault, recover and dispatch strategy. Nested resets/replays or arbitrary control actions are rejected before a session is changed. `Snapshot.scenario_report` contains observed results.

Replay accepts a basename in `{"action":"replay","file":"latest.jsonl"}`. Seek uses `{"action":"seek","time_s":12.5}` and pauses at the first recorded frame at/after the requested time, clamped to the recording range. Paths outside the recordings directory are rejected.
