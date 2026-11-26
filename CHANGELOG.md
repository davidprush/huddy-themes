# HUDdy Themes 1.1 — Changes

Colour-only update of HUDdy Themes 1.0. Source of truth: HUDdy Soft Contrast Spec 1.0 (sha256 `8626a226adcd441356bd87a21b5db5a5e345997084d33602a7e440978686e5f9`). No hue shift beyond ±2°, no accent or status-colour changes, and no `#ffffff` left in any theme file.

## Tokens that changed

| Token | 1.0 | 1.1 |
|---|---|---|
| Background | `#03060b` | `#080e19` |
| Surface | `#0a1322` | `#0d192c` |
| Panel | `#0f1c30` | `#112138` |
| Foreground (body text) | `#d6e4f2` | `#c2cfdc` |
| Ink-high / ANSI 15 / selection text | `#ffffff` | `#d6e4f2` |
| Hairline | `#172634` | `#1b2e41` |
| Text on accent | `#03060b` | `#080e19` |

Everything else is unchanged, including `selected_bg` / `selected_fg` in btop and bpytop (accent on the selected tint) and the 1.0 graph gradients.

## Per app

- **Ghostty 1.1:** background, foreground, cursor text, selection foreground and ANSI 15 updated as in the spec §4.1 table.
- **btop / bpytop 1.1:** `main_bg`, `main_fg`, and btop `meter_bg` only.
- **Obsidian 1.1.0:** manifest version 1.1.0; background, surface, panel, hairline, body, bold/ink-high and text-on-accent tokens; `versions.json` added (`1.0.0` and `1.1.0`, both `minAppVersion` 1.0.0).
- **VS Code `davidprush.huddy-theme` 1.0.1:** same extension ID as 1.0.0. Workbench, terminal and token colours follow spec §4.3 and §4.1. The integrated terminal now uses the solid selected-tint background with ink-high text, and cursor text is `#080e19`. Packaged as `huddy-theme-1.0.1.vsix` with `vsce`; not published.

## What you need to do to ship the community updates

These steps are yours; nothing in this pack was pushed or published.

### VS Code 1.0.1 (update the existing listing)

1. Use `vscode/huddy-theme-1.0.1.vsix` from this pack (sha256 is in `SHA256SUMS.txt`), or paste the VS Code block to recreate it in `${TMPDIR:-/tmp}/huddy-themes-1.1/`.
2. Open https://marketplace.visualstudio.com/manage/publishers/davidprush and sign in as the `davidprush` publisher.
3. On the existing **HUDdy** row, click **⋯**, then **Update**, and upload `huddy-theme-1.0.1.vsix`. Do not create a new extension.
4. Wait until the row shows version **1.0.1**. A version number can never be reused.

Microsoft retires PAT-based `vsce publish` on 1 December 2026. The web upload needs no token. See the install guide, Step 5, Route A.

### Obsidian community theme 1.1.0

1. In your public theme repo (the one used for 1.0.0, or a new repo if you have not submitted yet), put `manifest.json` (version `1.1.0`), `theme.css`, `versions.json`, `README.md`, `LICENSE` and `screenshot.png` at the root.
2. Create a GitHub release whose tag is exactly `1.1.0` (do not reuse `1.0.0`). Attach `manifest.json` and `theme.css`.
3. If the theme is already in the Community directory, the new release is the update. If it is not, sign in at https://community.obsidian.md, link GitHub, and add the theme from the repo.

## Paste blocks

Working folder is `${TMPDIR:-/tmp}/huddy-themes-1.1`. Pre-check (docked, Ollama, swap) still runs first and is report-only. Existing theme files are backed up before overwrite. Decode remains `base64 -D`. No `/Volumes/Work` and no `~/Desktop`.
