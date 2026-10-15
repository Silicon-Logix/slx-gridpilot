<!-- Copyright (c) 2026 Marco Pezzullo / Silicon LogiX. See LICENSE. -->
# Dependency source provenance

Native dependency source archives are prepared from the exact checked commits and included under `third_party/sources/` inside the Windows ZIP. They contain open62541 1.4.14 and FORTE 2.0.1 with their licenses/notices. The original GridPilot controller application is provided as part of the compiled evaluation runtime. Upstream repositories are not modified by the integration.

`ua-nodeset.zip` contains the pinned OPC Foundation UA-Nodeset sources used to generate namespace zero: commit `d1bb6a22125bd7cd986272b1ee98a18a91d76fff`. Copyright and license notices are retained in those sources and `licenses/OPC-Foundation-MIT.txt`.

Rust dependency sources can be obtained from crates.io using the exact package versions and source URLs in the Rust inventory. The Slint example adapter's exact source is the v1.12.1 tag. The build metadata and Rust license inventory identify repository/version/license information without local machine paths.

The Windows distribution includes `third_party/slint-renderer`, an application-integrated local override of `i-slint-renderer-femtovg` 1.12.1. `upstream.json` records the original published archive checksum/revision, and `PATCH.md` identifies the two modified files and surface-recovery behavior. Its original copyright and license texts are preserved. Other Rust dependencies use their locked registry sources.

The exact unmodified `dwrote` 0.11.5 source package is included in `third_party/sources/dwrote-0.11.5.crate` under MPL-2.0. The Rust inventory records direct source-package URLs, declared authors and preserved notices. Workspace-level notices obtained from upstream repositories include their exact revision, source URL and SHA-256. For packages without a standalone license file, the original published Cargo declaration, declared authors and full license text are retained together; no upstream copyright statement is invented.

The existing MinGW GCC 13.1 runtime DLLs are supplied unmodified. GCC sources: https://gcc.gnu.org/releases.html and https://gcc.gnu.org/git.html; MinGW-w64 sources: https://www.mingw-w64.org/downloads/. These upstream sources and runtime licenses remain independent of the GridPilot numerical SDK.
