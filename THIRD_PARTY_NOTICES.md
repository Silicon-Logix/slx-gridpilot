<!-- Copyright (c) 2026 Marco Pezzullo / Silicon LogiX. See LICENSE. -->
# Third-party notices

Slint 1.12.1 is used under the royalty-free desktop license. Its AboutSlint widget is accessible on the top-level About page, satisfying the attribution option in section 2(a). The separately reused Bevy adapter example is MIT licensed and retains its original attribution.

The application includes a local surface-recovery patch to `i-slint-renderer-femtovg` 1.12.1. It retries/reconfigures a lost or outdated WGPU surface and skips transient unavailable frames. The Windows distribution retains the crate's original notices and records the original archive checksum/revision and modified files in `third_party/slint-renderer/upstream.json` and `PATCH.md`. These integrated third-party sources retain their Slint license terms.

Bevy and wgpu are MIT/Apache-2.0. Eclipse 4diac FORTE 2.0.1 is EPL-2.0; open62541 1.4.14 is MPL-2.0 with independently licensed plugins, including CC0. nlohmann/json 3.12.0 is MIT. MinGW-w64 compiler runtime libraries have their independent runtime-exception terms. Asyncua 1.1.8 is an optional LGPL-3.0 test dependency and is not bundled into the product runtime.

Exact license text and dependency notices are retained in `licenses/` inside the Windows ZIP. The generated Rust dependency inventory records the locked graph; it is a superset across platforms and does not claim every listed package is used on Windows. Dependency sources and source provenance are described in [THIRD_PARTY_SOURCE.md](THIRD_PARTY_SOURCE.md).

lxml 5.4.0 is an optional verification dependency used to validate exported NodeSet XML against the OPC Foundation schema. It is not part of the desktop runtime.

## Inter font

Inter is copyright 2016 The Inter Project Authors (https://github.com/rsms/inter), licensed under SIL Open Font License 1.1. The unmodified regular and semibold fonts are embedded in the desktop executable. See `assets/fonts/OFL.txt` in the Windows ZIP.

## OPC Foundation namespace model

The OPC UA namespace-zero model is supplied by OPC Foundation UA-Nodeset at commit `d1bb6a22125bd7cd986272b1ee98a18a91d76fff` (model 1.05.02). Its OPC Foundation MIT License 1.00 is retained in `licenses/OPC-Foundation-MIT.txt` and in the corresponding source archive.
