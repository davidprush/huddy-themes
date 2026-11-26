# HUDdy palette (HUDdy Themes 1.1)

Source of truth: [HUDdy Soft Contrast Spec 1.0](docs/HUDdy-Soft-Contrast-Spec-1.0.md) (sha256 `8626a226adcd441356bd87a21b5db5a5e345997084d33602a7e440978686e5f9`). These are the HUDdy Themes 1.0 tokens with lifted near-black backgrounds, body text capped at the web body colour, and ink-high / ANSI 15 / selection text capped at the web headline colour. Accents, status colours and decorative derived tokens are unchanged. Every theme in this pack is generated from these values by one script, so they match exactly.

| Role | 1.0 | 1.1 | Notes |
|---|---|---|---|
| Background | `#03060b` | `#080e19` | web panel fill; +1.3° hue |
| Surface (panels) | `#0a1322` | `#0d192c` | keeps the 1.09:1 step above background |
| Panel-2 / raised | `#0f1c30` | `#112138` | keeps the 1.09:1 step above surface |
| Text | `#d6e4f2` | `#c2cfdc` | web body copy; hue 210.0° unchanged |
| Muted text | `#7d93ad` | `#7d93ad` | unchanged |
| Accent cyan | `#5ee1ff` | `#5ee1ff` | unchanged |
| Secondary (ink-soft) | `#93a8bf` | `#93a8bf` | unchanged |
| OK / up (green) | `#3dffa8` | `#3dffa8` | unchanged |
| Warn (amber) | `#ffb547` | `#ffb547` | unchanged |
| Danger / down (red) | `#ff5470` | `#ff5470` | unchanged |
| Neon cyan | `#3ef0ff` | `#3ef0ff` | unchanged |
| Midnight blue | `#64d2ff` | `#64d2ff` | unchanged |
| Ink-high (strongest text, ANSI 15, selection text) | `#ffffff` | `#d6e4f2` | web headlines; no pure white |
| Pane border | `#275e6d` | `#275e6d` | unchanged |
| Hairline | `#172634` | `#1b2e41` | web panel divider; +1.0° hue |
| Selected tint | `#142c3d` | `#142c3d` | unchanged |
| Corner bracket | `#47aac2` | `#47aac2` | unchanged |
| Disabled | `#2e3744` | `#2e3744` | unchanged |
| Text on accent | `#03060b` | `#080e19` | = new background |
| Magenta / purple | `#c792ff` | `#c792ff` | **Derived** (HUDdy has no magenta) |
| Bright red / green / yellow / blue / magenta | `#ff879b` `#77ffc2` `#ffcb7e` `#92e0ff` `#d8b3ff` | same | **Derived**: base colour 30% toward white |
| Inactive text | `#404c5c` | `#404c5c` | **Derived** in 1.0; kept (spec §2) |
| Faint text | `#5e7084` | `#5e7084` | **Derived** in 1.0; kept (spec §2) |
| Dim graph starts | `#1a6a4a` `#2a586d` `#684c23` `#682533` | same | **Derived** in 1.0; kept (spec §4.2) |

## Terminal ANSI palette (Ghostty, VS Code terminal)

| # | Name | Hex | # | Name | Hex |
|---|---|---|---|---|---|
| 0 | black | `#2e3744` | 8 | bright black | `#7d93ad` |
| 1 | red | `#ff5470` | 9 | bright red | `#ff879b` |
| 2 | green | `#3dffa8` | 10 | bright green | `#77ffc2` |
| 3 | yellow | `#ffb547` | 11 | bright yellow | `#ffcb7e` |
| 4 | blue | `#64d2ff` | 12 | bright blue | `#92e0ff` |
| 5 | magenta | `#c792ff` | 13 | bright magenta | `#d8b3ff` |
| 6 | cyan | `#5ee1ff` | 14 | bright cyan | `#3ef0ff` |
| 7 | white | `#93a8bf` | 15 | bright white | `#d6e4f2` |

Ghostty also sets cursor `#5ee1ff` with `#080e19` text, selection `#142c3d` with `#d6e4f2` text, and split dividers `#275e6d`.

## Contrast (from the spec)

| Pair | Ratio | Required |
|---|---|---|
| Body `#c2cfdc` on background `#080e19` | 12.19:1 | ≥ 7:1 |
| Body on surface `#0d192c` | 11.11:1 | ≥ 7:1 |
| Ink-high `#d6e4f2` on background | 14.94:1 | ≥ 7:1 |
| Text on accent `#080e19` on `#5ee1ff` | 12.59:1 | ≥ 4.5:1 |
| Ink-high on selected tint `#142c3d` | 9.09:1 | ≥ 4.5:1 |
