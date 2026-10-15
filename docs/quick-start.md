<!-- Copyright (c) 2026 Marco Pezzullo / Silicon LogiX. See LICENSE. -->
# Demo walkthrough

Use the portable Windows package for immediate launch; it does not download or build anything. The public repository contains documentation and screenshots; use the Windows ZIP to run the demonstrator.

The initial **OPC UA Studio** explains the live command/feedback path and separates real OPC UA/FORTE processes from simulated equipment. Start with its five-step guided tour to browse U1, request power, confirm a stop, inspect uncertain quality and acknowledge/recover an alarm. The buttons unlock from actual server feedback. Read [Explore OPC UA](opcua-learning.md); return to Studio at any time with Ctrl+0. Existing preferences open Studio once on this update, then retain the selected page on later launches.

1. Double-click `SLX GridPilot.exe` in the portable win64 folder. Wait for **OPC UA CONNECTED** and the plant geometry. Services start automatically.
2. Select **Run scenario**. At 5 s the first group starts, at 30 s higher demand inserts group 2, at 60 s both stop, at 85 s pumping starts and at 120 s demand returns to zero. Simulation pacing is 5×; the fixed step remains 100 ms.
3. Explore **Twin**: choose Cutaway or Unit detail, drag to orbit, wheel to zoom, click a mesh for its identity and current telemetry. U1 is teal and U2 amber. Select a unit in the console or its scene identifier; **Locate** in its card frames it in the cutaway. Unit detail binds to the selected U1 or U2. Guided clip selection transfers transform ownership away from live process binding. Choose **Live** to restore confirmed poses.
4. Open **OPC UA tools**. Browse a device, search for a variable and select its row. Use Node detail, Watchlist or Method terminal. **Copy connection** supplies the external-client recipe; **Export nodes** creates JSON / CSV metadata. Use `read`, `setpoint 1.2`, `stop`, or JSON in the selected device terminal. A queued receipt is followed by coordinator acceptance and achieved state on telemetry.
   Unit-card commands enter manual dispatch, retaining the other unit's confirmed power as its initial manual request. Opposing manual directions are interlocked; stop the other unit before requesting a reversal. The header displays acceptance or rejection.
5. In **Events**, select a group and inject a fault. Jam the inlet before starting to see a timeout. Sensor/electrical faults trip immediately; communication loss closes the real group endpoint and trips after the 2 s grace period. Clear & recover requests safe recovery. A frozen-open valve must be cleared before the inlet can close.
6. In **Dispatch**, run comparison. It resets the live session and executes the identical 160 s profile twice, at 10× pacing. Observe progression and read `workspace/reports/strategy-comparison.json` after completion. Reset cancels an in-progress campaign.
7. In **Sessions**, start recording, operate the plant and stop recording. Replay latest feeds the recorded states back through OPC UA. Process commands are rejected during replay; reset returns to a new live session. Prior recordings are archived before a new one starts.
   Playback pause/speed and current command feedback are presentation metadata. Physical values and the event journal come from the recording; a rejected live command remains visible in LastCommand.
8. Open **Workbench**. Sequence diagnostics explain current U1/U2 feedback. In Trends & history, select numeric channels or load a saved file/session and move the time slider. Export CSV when needed.
9. In Test plans, load **Example**, review timed commands and expected results, then select **Validate & run**. The plan resets the session and reports observed pass/fail results. Edit rows or add checks and save a local copy. Cancel & stop requests a controlled stop.
10. In Workbench Replay, select a recording and seek to a simulation time. In Preferences, adjust watchlist sampling/publishing/deadband and panel widths, then save. The control Snapshot has an independent 100 ms subscription.
11. Export reports, events or a diagnostic bundle in **Sessions** and review the local files. Select modules in **Extensions** to save a project brief for additional engineering. Open About for identity, evaluation terms, notices and contacts.
12. Close the desktop. Devices receive shutdown/EOF, FORTE receives KILL, and the Windows job releases all descendants.

If startup fails, inspect `workspace/logs/coordinator.log`, `forte.log`, `services.log`, `unit1.log`, `unit2.log`. Existing endpoint ports are never forcibly reclaimed. Use `--connect-only` only when deliberately attaching the desktop to an already running local coordinator.

