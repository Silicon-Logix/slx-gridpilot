<!-- Copyright (c) 2026 Marco Pezzullo / Silicon LogiX. See LICENSE. -->
# Contributing

SLX GridPilot is available for study and business evaluation under its [product license](LICENSE). Discuss distribution of modifications and production integrations with Silicon LogiX before proceeding.

For an issue, provide the application version, Windows version, GPU/driver, reproduction steps and expected/observed behavior. Diagnostic exports are local and may contain operator commands; inspect their contents before sharing. Do not include plant credentials or confidential project data.

Frontend changes should preserve the OPC UA command path, distinguish queued receipts from controller acceptance and physical completion, retain source timestamps/quality and keep geometry animation tied to confirmed feedback. Keep third-party attributions and the AboutSlint widget accessible.

The public repository accepts documentation and reproducible application issues under the product license. The proprietary application implementation and its build/test infrastructure are not included. To verify the public material, run `python tools/audit-publication.py . --repository`. The prepared Windows package runs directly from its executable.
