<!-- Copyright (c) 2026 Marco Pezzullo / Silicon LogiX. See LICENSE. -->
# Pinned integration kit

| Component | Pin | Integration / license |
|---|---|---|
| Rust | 1.88.0, x86_64-pc-windows-gnu | Coordinator, numerical model and desktop |
| Slint | 1.12.1, commit `1bf6ee83713d3458f65d4c9466ac7abcb695e9a1` for reference adapter | Winit + FemtoVG/wgpu; royalty-free desktop license |
| Bevy | 0.16.1 | glTF scenes, PBR, animation, manual texture target; MIT or Apache-2.0 |
| wgpu | 24.0.5, shared Slint/Bevy graph | Vulkan graphics; MIT or Apache-2.0 |
| FORTE | 2.0.1, commit `8fde57e880174a401c7e711a584822c07ac434f8` | External BasicFB module; EPL-2.0 |
| open62541 | 1.4.14, commit `76e425ee963e8c16c0414f2f6bd0c7a5761a92c3` | Local UA client/server; MPL-2.0, CC0 plugins |
| nlohmann/json | 3.12.0 | Native device JSON pipe/schema parsing; MIT |
| MinGW-w64 GCC | GCC 13.1 x64 | Native C/C++; compiler/runtime independent licenses |
| asyncua | 1.1.8 | Independent acceptance client only; LGPL-3.0 |

The proprietary build pins its complete Rust dependency graph. The Rust inventory in the Windows ZIP records the exact dependency versions, source URLs, licenses and notices, including `typed-index-collections` 3.2.3 for Rust 1.88 compatibility. Qt is not part of the build or runtime.

Compatibility was established from the [official Slint 1.12.1 Bevy example](https://github.com/slint-ui/slint/tree/v1.12.1/examples/bevy), its shared wgpu 24 interfaces, the [Bevy 0.16 release](https://bevyengine.org/news/bevy-0-16/), [open62541 1.4.14 documentation](https://open62541.org/doc/v1.4.14/), and the [FORTE external-module build documentation](https://eclipse.dev/4diac/documentation/html/installation/install.html). License conditions are recorded from the exact downloaded source versions: [Slint desktop license](https://github.com/slint-ui/slint/blob/v1.12.1/LICENSES/LicenseRef-Slint-Royalty-free-2.0.md), [FORTE license](https://github.com/eclipse-4diac/4diac-forte/blob/2.0.1/LICENSE.md), [open62541 license](https://github.com/open62541/open62541/blob/v1.4.14/LICENSE), [Bevy license](https://github.com/bevyengine/bevy/blob/v0.16.1/LICENSE-MIT).


Vulkan is the supported Windows graphics configuration. See [verification scope](validation.md).
