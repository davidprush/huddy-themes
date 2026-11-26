# David's App Design Template 1.1

**Version 1.1 (Tue Nov 24, 2026, ET): HUDdy Soft Contrast.** David found HUDdy too contrasty outside the NuzeHub web desk (pt139u) and approved the soft-contrast plan (pt140u). In 1.1 the TUI HUDdy defaults lift the near-black background to the web panel colour, and text is capped at the web's two text levels. No hue changes: every changed token stays within ±2° HSL hue, and every accent, status and branch colour is unchanged. New: §2.1.1 soft tokens, §2.5 selection rule, V14 and V15. The full measurements are in `HUDdy-Soft-Contrast-Spec-1.0.md`. Version 1.0 is kept unchanged beside this file as `App-Design-Template-1.0.md` (sha256 `de823a6df78b4ae469ee463f83682d702e64166516de03aa31055372e9d53e56`). Shipped apps change only in their briefed soft builds: SSHush 1.0.3, NuzeHub TUI 0.2.3, Dirlume 2.0.0-a4 and HUDdy Themes 1.1.

---


**Status:** version 1.0 (V13 TUI review **CONFIRMED** by David on Monday, November 23, 2026, 8:26 PM EST). David's decisions were applied on Mon Nov 23, 2026, 1:40 PM ET (§9), and on Mon Nov 23, 2026, 8:25 PM EST David approved **NuzeHub TUI 0.2.0 Desk** live in Ghostty as the official TUI template moving forward with the **God's Eye HUD** theme as default—confirming the TUI HUD palette (`secondary`/`branches`), `◆◇■□` glyphs, and 256/16-colour fallback maps. Only §3.1 (HUD strips for non-news web apps) remains **(proposed)** until the first non-news web app review.
**Theme name (Nov 23, 2026, 11:24 PM EST):** David named the default TUI God's Eye HUD theme **`HUDdy`** across all TUI apps (single-word display name; settings loaders keep `gods-eye-hud` as a backwards-compatible alias so existing configs keep working cleanly).
**Shipped apps keep their current look and default theme** (Dirlume and SSHush on Powerlevel10k, NuzeHub TUI on GitHub Dark, NuzeHub web on God's Eye HUD) until David asks for a build that adopts this template. Adoption is always a deliberate, briefed change, and it will change that app's snapshots.
The draft this replaces is kept unchanged as `App-Design-Template-1.0-DRAFT.md`.
**What it is:** the one written template that every new app of David's starts from, and that every build is verified against.
**What it merges:**
- **The look** comes from the NuzeHub web desk, theme **God's Eye HUD**. David calls it the best interface he has seen.
- **The frame and controls** come from the TUI template (Dirlume 1.7.x → SSHush 0.7.0/1.0.0 → NuzeHub TUI 0.1.x), which David also loves.
- **The rule:** appearance matters as much as function. An app that works but looks plainer than this template is not done.

### Source key (every token below is cited to one of these project sources)

| Tag | Source | What it supplies |
|---|---|---|
| **W** | `nuzehub-2026-11/src/` (NuzeHub web) | `styles.css` (theme CSS, `.hud-*` classes), `lib/desk/theme.ts` (theme ids), `components/hud/*` (panel, controls, ops-panels, ops-home, layers-panel, focus-sheet, nav), `components/desk/shell.tsx` (top bar, rail), `lib/desk/globe-prefs.ts` |
| **WC** | `grok-chat-nuzehub-design-2026-10/` | design brief: local LLM only, keyboard navigation, dark/light, "deep blue tones with neon accent" |
| **D** | `dirlume-2026-11/releases/dirlume-1.7.3.zip` → `dirlume/dirlume/` | `layout.py` (button roles, `BTN_*`), `tui.py` (frame CSS, status bar `_seg`), `menubar.py`, `remote.py`, `termgfx.py`, `themes.py`; `CHANGELOG.md` 1.7.0–1.7.3; `tools/frame_scan.py` |
| **S** | `sshush-2026-11/sshush-repo/` (commit `6a741fc` = 0.7.0, `ca5c4a8` = 1.0.0) and `sshush-2026-11/releases/sshush-0.7.0-changes.md` | the full look-and-process template: mapping table, see-through dialogs, compact buttons, `tests/test_070_restyle.py` |
| **N** | `nuzehub-tui-2026-11/nuzehub-tui-repo/src/nuzehub_tui/` | `themes.py` (22 palettes, `DEFAULT = "github-dark"`, `button_tokens`), `ui/dlayout.py`, `ui/dialogs.py`, `ui/app.py`, `ui/menubar.py`, `desk.py` (`sparkline`) |
| **B** | `nuzehub-tui/brief/NuzeHub-TUI-Brief-0.2.0-Desk.md` (FINAL) and `…-0.1.1.md` | web→Textual element map, refresh and CPU budgets, the ssh colour finding |
| **R** | David's 13 web-desk screenshots (Nov 23) | the visual reference (described in the brief; confirmed against W below) |

Values marked **(derived)** are computed from a cited source value (for example an rgba line composited over the background, because a terminal has no alpha). Values marked **(proposed)** are not in any source. David confirms them at the first real Ghostty visual review of a HUD-default TUI.

---

## 1. Principles

| # | Principle | What it means in practice | Source |
|---|---|---|---|
| P1 | **Look equals function** | Every element is designed, not defaulted. If an element is plainer than its reference without a stated terminal or platform limit, the build fails (§8). | David, Nov 23; B "Visual standard" |
| P2 | **Consistency across apps** | Same tokens, the same component forms, the same menu/status/dialog frame and the same theme list in every app. A user who knows one app knows the next. | S mapping table; N/D/S share `menubar.py`, `dlayout.py`, the 22 palettes |
| P3 | **Keyboard first** | Every action has a key. Menus: F10 and alt+letter (D `menubar.py`). Web: ⌘K search, 1–8 layers, Q/R/P, Esc closes sheets (W `shell.tsx`, `focus-sheet.tsx`). The mouse works too, but it is never required. | WC "keyboard navigation"; S 0.7.0 tests "every menu item by keyboard and by mouse" |
| P4 | **Local first** | Local model servers only, with Ollama first and LM Studio as a fallback that never warns while Ollama works. Data stays on the Macs. No terminal queries (env-only detection). | WC "Local LLM only… Privacy by design"; D CHANGELOG 1.7.0 / 1.7.3 |
| P5 | **Calm motion** | Motion carries information: one slow tape, rotating alerts and a pulse only for "live/checking". No decorative animation. Everything honours reduced motion and pauses when hidden. | W `styles.css` `@media (prefers-reduced-motion)`, `globe-view.tsx` `document.hidden` pause; B §5 |

---

## 2. Design tokens (shared by web and TUI)

### 2.1 Colour roles

The web defines its colours as CSS variables (`W styles.css`: `html[data-theme="hud"]` at lines 147–163, `html[data-theme="github"]` at 165–179, and the `@theme` defaults at 6–24). The TUI defines them as `Palette(...)` fields (`N themes.py`, `D themes.py`) turned into Textual variables (`$background`, `$surface`, `$panel`, `$primary`, `$accent`, `$success`, `$warning`, `$error`, `$text-muted`, plus `$btn-*`).

| Role | Web variable | TUI variable | **God's Eye HUD**, web (W) | **God's Eye HUD**, TUI | **GitHub Dark**, web (W) | **GitHub Dark**, TUI (template 1.0: unified on the web accent) |
|---|---|---|---|---|---|---|
| background | `--color-bg` | `$background` | `#03060b` (page frame only; content sits on `#080e19` panels) | **`#080e19`** (1.1; was `#03060b`) | `#0d1117` | `#0d1117` |
| panel (surface) | `--surface-solid` (`--color-surface` = it at 78% glass; renders `#080e19`) | `$surface` | `#0a1322` | **`#0d192c`** (1.1; was `#0a1322`) | `#161b22` | `#161b22` |
| panel-2 / raised | `--surface-2-solid` | `$panel` | `#0f1c30` | **`#112138`** (1.1; was `#0f1c30`) | `#21262d` | `#30363d` (N uses border grey here) |
| border (hairline) | `--color-line` | `$primary 40%` for pane borders; `$panel` for rules | `rgb(120 196 255 / 0.17)` | pane `#275e6d` (derived: `$primary` 40% on bg), hairline **`#1b2e41`** (1.1, the web's rendered divider; was `#172634`) | `#30363d` | pane `#234571` (derived: `$primary` `#4493f8` 40% on bg) |
| accent | `--color-accent` | `$primary` (focus, borders) and `$accent` (titles) | `#5ee1ff` | `#5ee1ff` / `#5ee1ff` | `#4493f8` | `#4493f8` / `#39c5cf` (title colour kept, see notes) |
| accent-fg (text on accent) | `--color-accent-fg` | `$background` in status labels (D `_seg`) | `#021018` | **`#080e19`** (1.1 = `$background`; was `#03060b`) | `#0d1117` (template; NuzeHub web ships `#ffffff`, which fails, see notes) | `#0d1117` |
| accent-glow | `--hud-glow`, `.bg-accent` shadow, panel dot `shadow-[0_0_8px_var(--color-accent)]` | none (a terminal has no glow); use accent + bold | `0 0 0 1px rgb(94 225 255/.06), 0 12px 40px rgb(0 0 0/.45), 0 0 28px rgb(94 225 255/.05)`; `.bg-accent` `0 0 18px rgb(94 225 255/.22)` | n/a | none of its own (only the dot's `0 0 8px accent`) | n/a |
| corner bracket | `.hud-panel::before` `--c` = accent 75% | border colour on focus = `$primary` | `#47aac2` (derived) | `#5ee1ff` on focus | `#3672c0` (derived) | `#4493f8` on focus |
| text | `--color-fg` | `$foreground` | `#d6e4f2` (ink-soft `#93a8bf`, ink-high `#ffffff`; renders: headlines `#d6e4f2`, body copy `#c2cedc`) | **`#c2cfdc`** (1.1; was `#d6e4f2`). Ink-high / strongest text **`#d6e4f2`** (1.1; was `#ffffff`) | `#e6edf3` | `#e6edf3` |
| muted | `--color-muted` | `$text-muted` | `#7d93ad` | `#7d93ad` | `#8b949e` | `#8b949e` |
| ok / up | `--color-up` | `$success` | `#3dffa8` | `#3dffa8` | `#3fb950` | `#3fb950` |
| warn | `--color-warn` | `$warning` | `#ffb547` | `#ffb547` | `#d29922` (from `@theme` default) | `#d29922` |
| danger / down | `--color-down` | `$error` | `#ff5470` | `#ff5470` | `#f85149` | `#f85149` |
| selected tint | `color-mix(accent 10–12%)` (`.hud-row--on`, rail, `aria-pressed`) | `$btn-*-pressed-bg` / derived tint | accent 12% on panel | `#142c3d` (derived) | accent 12% | `#1c293c` (derived) |

Notes:
- The web has **no separate ok/danger tokens**. `up`/`down` serve as ok/danger, and `warn` covers warnings. The TUI uses `success`/`error`/`warning`. The template treats them as one role each: **ok = up = success**, **danger = down = error**.
- **The TUI God's Eye HUD palette does not exist yet.** It is the **default for every new TUI** (Decision 1), and NuzeHub TUI 0.2.0 Decision 5 adds it as an extra theme. Its values above are the web values, one for one. The `Palette` still needs a `secondary` and 8 `branches`, which are not in the web source **(proposed; David confirms them at the first Ghostty review of a HUD-default TUI: secondary `#93a8bf` = the web's `--ink-soft`; branches = accent, up, warn, down, `#93a8bf`, `#7d93ad`, `#3ef0ff` (Neon accent), `#64d2ff` (Midnight accent))**.
- The computed `$btn-*` tokens for that proposed HUD palette, from `N themes.py _compute_button_tokens`, are: primary border `#238f61` / text `#54fbb3`; neutral border `#545b64` / text `#97a1ad`; dismiss border `#465464` / text `#7d93ad`; danger border `#8e3143` / text `#f96a84`; focus `#5ee1ff`; disabled `#526274`/`#2e3744`.
- **GitHub Dark is unified on the web values** (Decision 2): `$primary` = `#4493f8` and `$text-muted` = `#8b949e` in web and TUI alike. Every other GitHub Dark TUI field (background, surface, panel, foreground, secondary `#bc8cff`, success, warning, error) is unchanged from N/D `themes.py`. The 8 graph `branches` keep `#58a6ff` as their first data-series colour. That is a chart colour, not the accent.
- **The TUI `$accent` title colour stays `#39c5cf`** (cyan). It does not conflict: it passes on bg (9.07:1), surface (8.29:1) and panel (5.85:1), and it stays clearly apart from the blue `$primary` borders. The web uses one accent; the TUI keeps its second title colour on purpose.
- Recomputed GitHub Dark `$btn-*` tokens (`_compute_button_tokens` with `#4493f8`/`#8b949e`):
  - **unchanged:** primary border `#286d36` / text `#58c168`; neutral border `#61666c` / text `#a5abb1`; danger border `#8e3432` / text `#f56862`;
  - **changed:** every `*-focus` → `#4493f8`; dismiss border `#525961`, hover `#8b949e`, pressed `#a2aab3`, pressed-bg `#1f232a`, text `#8b949e`, text-hover `#afb8c0`; disabled text `#5f666f` / border `#393f46`.
- **Contrast results (WCAG ratio, 4.5:1 for text).**

  | Pair | God's Eye HUD | GitHub Dark (unified) |
  |---|---|---|
  | text on bg / surface | 15.69 / 14.38 | 16.02 / 14.64 |
  | muted on bg / surface | 6.43 / 5.89 | 6.15 / 5.62 |
  | muted on panel-2 (`$panel`) | 5.41 | **3.97 FAIL** |
  | accent on bg / surface | 13.23 / 12.12 | 6.11 / 5.58 |
  | accent on panel-2 (`$panel`) | 11.14 | **3.94 FAIL** |
  | title `$accent` on bg / surface / panel | (same as accent) | 9.07 / 8.29 / 5.85 |
  | up / warn / down on surface | 14.23 / 10.59 / 5.98 | 6.81 / 6.85 / 5.16 |
  | text / accent on selected tint | 11.14 / – | 12.41 / 4.73 |
  | **text on accent, web** (`--color-accent-fg`) | `#021018` on `#5ee1ff`: 12.56 | **`#ffffff` on `#4493f8`: 3.10 FAIL** |
  | **text on accent, TUI** (status label `$background` on `$primary`) | 1.1: `#080e19` on `#5ee1ff`: 12.59 (1.0: 13.23) | `#0d1117` on `#4493f8`: 6.11 |
  | status labels on up / warn / down | 15.53 / 11.55 / 6.53 | 7.45 / 7.50 / 5.65 |
  | focus border vs bg (non-text, 3:1) | 13.23 | 6.11 |
  | unfocused pane border vs bg (non-text, deliberately subtle) | `#275e6d`: 2.81 | `#234571`: 1.95 |

  **Fixes for the three failures:**
  - **Web text on the GitHub Dark accent:** template apps set GitHub Dark `--color-accent-fg: #0d1117` (6.11:1), the same as the TUI. (The other way to fix it is a darker fill such as `#1f6feb` with white text at 4.63:1, but that changes the accent, so it is not used.) NuzeHub web keeps `#ffffff` until a briefed adoption build.
  - **Muted or accent text on `$panel` (`#30363d`):** don't place them there. On `$panel` (menu bar, status bar), use `$foreground` (10.33:1). Where a muted or accent tone is needed on `$panel`, use the lifted values from `themes.readable(…, 4.5)`: muted `#979fa8`, accent `#60a3f9`. The status bar's values already sit on `$surface`, so they pass.
  - The HUD palette has no failures.
- **Adopting the unified GitHub Dark changes the look of an existing TUI** (borders, focus and muted text all shift slightly). For NuzeHub TUI, Dirlume and SSHush, it changes their SVG snapshots, so it happens only in a deliberate, briefed build that says which snapshots are regenerated.

### 2.1.1 HUDdy Soft Contrast (1.1 default for every TUI and HUDdy app theme)

The 1.0 contrast table above stays as the historical record. These are the 1.1 values (WCAG, from the Soft Contrast Spec):

| Pair | 1.0 | 1.1 |
|---|---|---|
| text on bg / surface / panel | 15.69 / 14.38 / 13.21 | 12.19 / 11.11 / 10.21 |
| ink-high on bg | 20.29 (`#ffffff`) | 14.94 (`#d6e4f2`) |
| muted on bg / surface / panel | 6.43 / 5.89 / 5.41 | 6.12 / 5.58 / 5.12 |
| accent on bg / surface / panel | 13.23 / 12.12 / 11.14 | 12.59 / 11.48 / 10.54 |
| up / warn / down on surface | 14.23 / 10.59 / 5.98 | 13.47 / 10.02 / 5.66 |
| text on selected tint `#142c3d` | 11.14 | 9.09 |
| text on accent (`$background` on `$primary`) | 13.23 | 12.59 |
| unfocused pane border `#275e6d` vs bg | 2.81 | 2.67 |
| web reference: headline / body on panel `#080e19` | 14.94 / 12.10 | (target) |

Rules:
- **Backgrounds only get lighter, text only gets darker.** Never change a hue (±2° HSL hue at most, from 8-bit rounding). Accent, status and branch colours stay as they are.
- **No `#ffffff` in HUDdy.** The strongest text is `#d6e4f2`, which is the brightest colour the web desk draws.
- **Terminal ANSI:** 0 `#2e3744`, 7 `#93a8bf`, 8 `#7d93ad`, and **15 `#d6e4f2`** (was `#ffffff`). The colour variants are unchanged. Terminal foreground is `#c2cfdc`, background `#080e19`, selection text `#d6e4f2`.
- **SSHush's own HUDdy variant** (until it moves to the canonical set): background `#080e19`, surface `#0d192c`, panel `#132643`, text `#c0d0da`, secondary `#94f1fb`. All its other tokens are unchanged.
- **GitHub Dark is unchanged** apart from the §2.5 selection rule.
- **The 256/16 fallback maps are unchanged.**

### 2.2 Typography

| Token | Web (W) | TUI | Rule |
|---|---|---|---|
| Mono telemetry face | `--font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo…`; HUD adds `font-feature-settings: "zero" 1` (slashed zero) | the terminal font (Ghostty) | All numbers, codes, labels and chips are mono. The body text can stay sans on the web. |
| Tabular digits | `html[data-theme="hud"] body { font-variant-numeric: tabular-nums }`, `.hud-num` | built in (monospace cells) | Right-align numbers in columns; fixed decimals (`changePct.toFixed(2)`). |
| Label (`.hud-label`) | 11px (`0.6875rem`), weight 500, `letter-spacing: 0.16em`, uppercase, `--color-muted` | UPPERCASE, `$text-muted`; **no letter-spacing** (David, Decision 4) | The panel meta, tile labels and section eyebrows. |
| Panel title | `.hud-label` with `!text-fg` | `$accent` bold (D/N `.dlg-title`) or `$foreground` bold in the border title | Uppercase. |
| Stat value | `.hud-num text-lg` (18px), weight 500, leading-none | bold, `$foreground`; `$warning` when the warn condition holds | One big number per tile. |
| Chip/button text | 11px mono, `letter-spacing: 0.08em`, uppercase; `--sm` 10px | label text as written, no bold (Decision 3) | Buttons: uppercase on the web, sentence case in the TUI (Dirlume role words). |
| Page skin | `.hud-page`: h1 capped at 15px/600, body 11.5–14px, `p.uppercase` mono with 0.14em tracking | n/a | Pages inside sheets never shout. The largest text is a stat figure. |
| Rail code | mono 8.5px, `tracking-[0.12em]` | the tab label or code | |

### 2.3 Spacing and shape

| Token | Web (W) | TUI (N/S/D) |
|---|---|---|
| Panel header padding | `.hud-head` `0.625rem 0.875rem`, gap `0.75rem`, bottom hairline | border title in the top border, 1-cell padding in panes (`TabPane { padding: 0 1 }`) |
| List row | `.hud-row` `0.5rem 0.75rem`, hairline `line 60%` | 1 row per item (2 for a title row), no blank rows |
| Gaps between panels | `gap-2` (0.5rem); desk inset `top-3 … left-3` | 1 cell (`#main-tabs { margin: 0 0 0 1 }`) |
| Control height | `.hud-btn`/`.hud-chip` `min-height: 1.75rem`, `--sm` `1.375rem` | button `BTN_H = 3` (border, label, border); `1` row frameless when the screen has under `SHORT_H = 30` rows |
| Button padding | `0 0.5rem` | `BTN_PAD = 1` cell each side, `BTN_GAP = 1`, `BTN_MIN_W = 6` (N/S `ui/dlayout.py`) |
| Radius | panel 3px, sheet 4px, chip/button/input 2px; HUD squares off `rounded-*` to 3px | `round` borders (╭╮╰╯) on panes, dialogs and buttons; `ascii` in ASCII mode |
| Border width | 1px | 1 cell |

### 2.4 Borders

- **Web:** `1px solid var(--color-line)` everywhere. `.hud-panel` adds **corner brackets**: 12×1px and 1×12px strokes at each corner in accent 75% (`styles.css` `.hud-panel::before`).
- **TUI:**
  - Panes use `border: round $primary 40%` and change to `round $primary` on `:focus-within`.
  - Dialogs use `round $primary` on `$surface`.
  - Menu drop-downs and select overlays use `round $accent`.
  - Rules use `solid $panel`.
  - These come from D `tui.py` CSS and S/N `ui/app.py`.

### 2.5 Selected and highlighted rows (1.1)

On a solid accent or primary fill (focused tab, menu item, list item, tree node, table cursor), the text is the theme's **`$background`** token: HUDdy `#080e19` on `#5ee1ff` (12.59:1), GitHub Dark `#0d1117` on `#4493f8` (6.11:1). That is the Dirlume look. An unfocused selection uses the selected tint with `$foreground` text. To apply it, `Palette.textual()` sets the Textual variables `block-cursor-foreground = background` and `block-cursor-background = primary` for every dark theme whose background passes 4.5:1 on its primary. Other themes keep Textual's automatic contrast. No app CSS may override the colour of an accent-filled item with `$foreground`. SSHush 1.0.2's `#main-tabs Tabs Tab.-active { color: $foreground; }` did that and drew white on cyan at 1.36:1.

---

## 3. Component catalogue (web form | TUI form)

**Origin key:** **W** = inherited from the web; **T** = inherited from the TUI; **M** = merged (the web look applied to a TUI form, or the reverse).

| # | Component | Web form (source) | TUI / Textual form (source) | Origin |
|---|---|---|---|---|
| 1 | **Panel + header** | `HudPanel` (`components/hud/panel.tsx`):<br>- glass `.hud-panel` (surface 70%, `backdrop-filter: blur(16px) saturate(140%)`, radius 3, `--shadow-panel`);<br>- header `.hud-head`: a 6px accent square with an 8px glow, an optional icon, the title `.hud-label !text-fg`, then the meta in muted (`INTEL FEED 60 of 591`, `LAYERS 1–8`), and actions right-aligned. | A `Vertical` with `border: round $primary 40%` and `:focus-within` `$primary`.<br>- `border_title = "[$accent]■[/] INTEL FEED [$text-muted]60 of 591[/]"`: the accent square bullet `■`, an UPPERCASE title, then the muted meta.<br>- The right-hand count goes in the border subtitle or a count badge (D "bottom-right count badge").<br>- Actions are compact outline buttons in the header row. | M |
| 2 | **Corner brackets** | `.hud-panel::before`, 12px accent-75% L-strokes | **Limit:** a terminal can't colour corner cells apart from their edges, and it has no glow. **Form:** border colour carries it. Unfocused panes use `$primary 40%` (`#275e6d` HUD, close to the web's hairline-to-bracket range). Focused panes use the full `$primary` (`#5ee1ff`). The title uses accent and bold. | M (stated limit) |
| 3 | **Stat tile** | `Stat` (`panel.tsx`): 1px line border, radius 2, bg 45%, label 9px uppercase `tracking 0.06em`, value `.hud-num text-lg`, tone `text-warn` when warn (`< 2h` tile in `SitrepPanel`) | A Textual `Grid` of 4 tiles with 1-cell `round $panel` borders. Label: UPPERCASE `$text-muted`, 1 row. Value: bold, 1 row, `$warning` when its warn condition holds (B §6 row 12). At 80x24, `LABEL value` is inline. | M |
| 4 | **List row with badge** | `IntelFeed` row (`ops-panels.tsx`):<br>- meta line `source · age` 10.5px muted, with a pulsing warn dot when under 2 h;<br>- title 13px, 2-line clamp, accent on hover;<br>- **country badge**: `iso2` in a 1px line border, radius 2, 10.5px accent, accent border and 12% fill on hover;<br>- `.hud-row--on` = accent 10% fill + 2px left accent bar. | `OptionList`/`DataTable` row:<br>- `● Reuters · 12m` with a steady `●` in `$warning` (no blink);<br>- the title on the next row;<br>- the badge as `[GB]` in `$accent`, right-aligned;<br>- selected row: `▌` in `$primary` + tint `#142c3d` (HUD) / `#1e2c3d` (GH Dark);<br>- `c` filters by the badge (B row 22). | M |
| 5 | **Outline button** | `.hud-btn` (`styles.css`, `controls.tsx HudButton`): 1px line border, radius 2, mono 11px uppercase 0.08em, muted text, surface 50%; hover = fg text + accent-50% border; variants `--primary` (accent text, accent 8% fill), `--quiet`, `--danger` (down on hover), `--icon`, `--sm`, `--link`; arrow glyph `ArrowUpRight` (`BRIEF ↗`, `ALL ↗`, `CHARTS ↗`) | **Dirlume 1.7.x outline, compact:**<br>- a rounded border round one label row, `BTN_H 3`, `BTN_PAD 1`, transparent face, **no bold** (focus shows as a `$primary` border);<br>- roles from the label (`button_role`): primary = green, neutral = grey, dismiss = muted, danger = red, all from `$btn-*`;<br>- states: hover = full hue, pressed = pressed-bg tint, disabled;<br>- under 30 rows: 1 row, frameless, focus = reverse (N/S `ui/dlayout.py button_tcss`).<br>- **Merged:** a link-out button ends with ` ↗` (`Brief ↗`).<br>- **Focus = the `$primary` border only, never bold** (Decision 3; Dirlume's `BTN_FOCUS_STYLE = "bold"` is not used). | M |
| 6 | **Segmented group** | `LayersPanel` "Render · Q": `grid-cols-3` of `.hud-chip` with `aria-pressed`, labels `Photo / Tactical / Flat` (`globe-prefs.ts GLOBE_QUALITIES`). Pressed = accent text, accent-60% border, accent 10% fill. | A `Horizontal` of compact neutral buttons. The pressed one gets the class `-on` (`$primary` border + `$accent` text + the pressed-bg tint). Arrows move and Enter selects. At 80 columns it drops to `[Tactical|Flat]` text toggles. | M |
| 7 | **Diamond radio / box checkbox** | `HudOptBox` (`controls.tsx`): a 12px box with a 1px line border; checked = accent border, accent 25% fill, inset accent square. `--radio` = the same box rotated 45° and scaled 0.86 (diamond). | Radio `◆` checked / `◇` unchecked in `$accent`/`$text-muted`. Checkbox `■`/`□` the same way. This replaces Textual's `X`/`▐▌` glyphs. Keys and labels are unchanged. **(proposed glyphs; N 0.1.x still uses Textual's `Checkbox`.)** | M |
| 8 | **Chip** | `.hud-chip` (same box as `.hud-btn`). Top bar: `FEEDS 18/19` with a dot (up when all feeds answer, warn when some fail, down when none or an error, accent pulse while loading), `STORIES 613`, `MODEL OLLAMA` (dot + `text-up`), `+ CAPTURE`, `LINK X` (`shell.tsx` lines 386–449) | **Status-bar segment** (D `tui.py _seg`): ` LABEL ` in bold `$background` on the role colour, then ` value ` in `$foreground` on `$surface`. Role colours: up/warn/down for FEEDS, `$success` for MODEL online. This is the TUI's pill. | M |
| 9 | **Nav rail** (required in every web app, Decision 5) | `RailLink` (`shell.tsx`): 44px button, icon + 3-letter code (8.5px mono), codes from `nav.ts NAV` (OPS GEO PTS SIT INT MKT COM DAY IDX MEM LOG AUT + CFG). **Selected:** accent text, accent 12% fill, 2px left accent bar with a 10px glow; tooltip label on hover. | **Tabs + menu replace the rail** (B §4, Decision 4). Tab labels are short words with number keys (`0` Desk, `1…`). The 3-letter codes show in help and tooltips. The selected tab uses Textual's underline in `$accent`. Under 140 columns, short tab labels are used (D 1.6.9 rule). | T (web codes kept as text) |
| 10 | **Top bar with breadcrumb and clocks** (required in every web app) | `shell.tsx` header, `desk-bar` (bg 92% + blur 12px), height 40px:<br>- brand lockup mono 13px uppercase, then `// GOD'S EYE` in accent 10px tracking 0.18em;<br>- breadcrumb `▸ Ops ▸ News`, muted 11px uppercase 0.16em;<br>- search 28px high with `⌘K` hint;<br>- `Telemetry` `UTC hh:mm:ss` + local zone (`useClock(1000)`);<br>- chips. | **Menu bar** (D `menubar.py`, 1 row, `$panel`) with the brand badge `App x.y.z` (bold, primary background, shortened under 100 columns). The breadcrumb is the active tab. **Clocks and chips go in the status bar**, right-aligned: `UTC 18:02:11 · EST 13:02` (B row 3). | M |
| 11 | **Alerts bar** (required in every web app; content per §3.1) | `AlertsTicker` (`ops-panels.tsx`):<br>- a `hud-panel` 32px high;<br>- bell (warn when any alert, else muted), `ALERTS` label in warn, `hh:mm` muted, the tag label in accent (`PRICE MOVES`, `HAZARD ALERTS`…), the text in fg (truncated), then `n/m` muted at the right;<br>- rotates every **7 s**;<br>- empty: "Quiet. Rules on Automate post here." | A 1-row `Static` with a `round` border, or a bare row on short screens: `🔔 ALERTS 14:02 PRICE MOVES NVDA +3.09%, … 2/5`. ALERTS is in `$warning`, the tag in `$accent`, the count in `$text-muted`. It rotates every 7 s and pauses when hidden. Enter opens the text. ASCII mode uses `!` for the bell. | W |
| 12 | **Scrolling tape** (required in every web app; content per §3.1) | `MarketTape`:<br>- `desk-bar` 32px high with a top hairline;<br>- `MKT` label in accent on an accent 10% fill;<br>- each item: label (mono 10.5px muted uppercase), price (`.hud-num` 12px fg), `▲`/`▼` + `abs(%)` in up/down;<br>- a right hairline between items;<br>- `.hud-marquee`: a **70 s** linear loop over a doubled strip; pauses on hover; stops under reduced motion. | 1-row `Static` shifted by offset, at most **4 cells/s** from one `set_interval` (B §5). ` MKT ` is a status-style segment (accent label). The separator is `│` in `$panel`. Colours are up/down. It pauses when hidden, unfocused or behind a modal. A "static tape" setting covers reduced motion. | W |
| 13 | **Sparkline** | `Spark` (`panel.tsx`): an SVG polyline, viewBox 100×28, stroke **1.4** in up/down, last 30 closes (`WatchPanel`). The row grid is `3.75rem 1fr 4.5rem 3.75rem` (symbol, spark, price, %). | Block sparkline `▁▂▃▄▅▆▇█` (N `desk.py sparkline`) in `$success`/`$error`; Braille 2×4 dots at ≥ 120 columns; Kitty image only inside a big chart. Row: `NVDA ▁▂▄▆█▇ 181.20 +1.24%`, numbers right-aligned. | M |
| 14 | **Dialog with see-through backdrop** (every web view outside the desk opens this way) | `FocusSheet` (`focus-sheet.tsx`):<br>- a `HudPanel` fixed in the free centre region (max 1000px), glass, so the globe shows through blurred;<br>- header: the view icon, the title, then the muted code (`News INT`), and `×` (Esc closes);<br>- **eyebrow** in muted uppercase (`Current events`, `news.tsx` line 454) above a large title (`News`; `.hud-page h1` is capped at 15px/600). | `ModalScreen { align: center middle; background: transparent; }`, so the desk stays visible. **Only the box is opaque:** `.dialog { border: round $primary; background: $surface; }` (S `ui/dialogs.py`, N `ui/dialogs.py`, D 1.7.3).<br>- Title row: `.dlg-title` (`$accent` bold), then the code in `$text-muted`, with `×`/Esc to close.<br>- The eyebrow is a muted UPPERCASE row above the title.<br>- Width 80, max 94%; height auto, max 88%. | M |
| 15 | **Status bar** | (no single web status bar; the top-bar telemetry and chips play its part) | `#hud` (D/S/N): 2 rows, `$panel`, labelled segments via `_seg` (` LABEL ` bold on the role colour + ` value ` on `$surface`), truncated with an ellipsis, `HELP ? keys F10 menu`. Above it, optionally, the activity panel (8 rows, `$surface`, top rule `solid $panel`; hidden by default under 30 rows). | T |
| 16 | **Dock strip** (required in every web app; content per §3.1) | `DayDock` (`ops-panels.tsx`): a `hud-panel` with 3 cells divided by hairlines:<br>- `NEXT EVENT` (time in accent, title);<br>- `TASKS done/total` + a 4px bar (`bg-line` track, `bg-accent` fill) + the first open task;<br>- `FOCUS`: `25m`/`50m` chips or an `mm:ss` countdown in accent + a bar. | A `Horizontal` of 3 cells with `│` dividers in `$panel`. Labels are UPPERCASE muted. The bar is `ProgressBar` or blocks `█░` in `$primary` on `$panel`. Focus uses compact buttons `25m` `50m`. The countdown ticks at 1 s only while running (B rows 25–27). | M |
| 17 | **Menu bar** | (none on the web) | D 1.7.3 `menubar.py`:<br>- 1 row on `$panel`;<br>- the drop-down is `round $accent` on `$surface` over `MenuScreen { background: transparent }`;<br>- equal-width rows with right-aligned dim shortcuts, ✓/● marks and a `✗ item: why` footer for disabled items;<br>- F10, alt+letter, ←/→, Esc and mouse all work;<br>- a **Themes** menu lists every theme as radio items (S 0.7.0). | T |
| 18 | **Input / search** | `.hud-input`: 28px, 1px line, radius 2, bg 60%, mono 12px, accent border on hover/focus; the search shows a `⌘K` hint (`shell.tsx` line 326) | `Input { height: 1; border: none; background: $surface; }` (N `ui/app.py`). Focus shows as the `$accent` cursor. Ctrl+K palette later (0.2.0 Desk brief, its Q4). | M |
| 19 | **Pulse / fresh marker** | `.hud-pulse` 1.6 s opacity 1→0.35; used for loading and for stories under 2 h | Steady `●` in `$warning`/`$accent`. **No blinking** in a terminal (P5). | M (stated limit) |

### 3.1 Alerts bar, tape and dock when an app has no live market or news data (proposed)

Decision 5 requires the full HUD shell in every new web app, so these three strips are always present. They must **never be empty and never show fake data**. When an app has no markets or news, they show the app's own real state. This guidance is **(proposed)**; David confirms it at the first review of a non-news web app.

| Strip | Shows (in priority order) | Format (same components as §3 rows 11, 12, 16) | Empty state |
|---|---|---|---|
| **Alerts bar** | the app's own notices: failed or finished jobs, health changes (model server down/up, disk or swap warnings), approvals waiting, rule or schedule results | `🔔 ALERTS hh:mm TAG text n/m`, with TAG = `JOBS`, `HEALTH`, `APPROVAL`, `RULES`, `BACKUP`… (accent); rotates every 7 s; Enter opens the source | `Quiet. Nothing needs you.` in muted (same as the web's quiet line) |
| **Tape** (label = a 3-letter app code instead of `MKT`, e.g. `SYS`, `JOB`) | live health and counters: model server (`OLLAMA ▲ up` / `▼ down`), queue depth, last run age, disk free, swap used, items processed, error count | `LABEL value ▲/▼ change` in up/down only when there is a real direction; otherwise value only; same 70 s web loop / ≤ 4 cells/s TUI | It never scrolls an empty strip. With fewer than 3 items it stays still and lists them. |
| **Dock** (3 cells) | **NEXT** (the next scheduled job or event and its time), **TASKS/JOBS** done/total + bar + the first open item, **FOCUS** 25m/50m (kept in every app) or the app's main one-key action | the `DayDock` cell form: muted label, accent figure, one line of text | `Nothing scheduled` / `All clear` |

Rules:
- Every value is read from the app's own state or a local health check. Nothing is invented or decorative.
- The same refresh limits apply (§5), and all three pause when hidden.
- For TUIs, Decision 5 is about web apps only. TUIs keep the menu-bar/status-bar frame; a TUI shows an alerts row, tape or dock only where its brief asks for them (as the NuzeHub TUI Desk does), using the same content rules.

---

## 4. Layout patterns

| Pattern | Web (W `ops-home.tsx`, `shell.tsx`) | TUI (B §4, S/N frame) |
|---|---|---|
| **App shell** (every new web app, Decision 5) | **Always the full HUD shell:** top bar 40px (fixed; brand `// SUBTITLE`, breadcrumb, search with ⌘K, clocks, status chips), left rail 56px with 3-letter codes, the alerts bar at the top of the centre column, the dock at the bottom of the centre column, and the tape pinned to the bottom (32px). Views outside the desk open as centred see-through sheets. Strip content per §3.1. | Menu bar (1 row). Body. Optional activity panel (8). Status bar (2). |
| **Desk grid** | Left column `w-[19rem]` (`2xl` 21rem): Sitrep (flex) + Layers. Right column `w-[21rem]` (`2xl` 23rem): Intel (flex 3) + Watch (flex 2). Centre: Alerts (max 44rem) and the Inspector. Bottom centre: Day dock. Edge: tape. | At ≥ 120 columns, three columns mirroring the web zones (left about 30, centre 1fr, right about 38); 200x50 widens the sides. Under 100 columns: one column in the `OpsMobile()` order (Alerts, Sitrep, map, Day dock, Intel, Watch, Layers). |
| **Centre stage** | The live globe (`globe-stage.tsx`) fills the stage behind everything, with a vignette and scanline overlay (`.hud-vignette`). Star field = `public/globe/night-sky.jpg`, only in Photo mode (Tactical has none). | The map is the centre pane: a Kitty image in Ghostty, Braille elsewhere, a text table when the output is not UTF-8. At 80x24 it collapses to `Map: n countries · press m`. |
| **Side columns** | Panels float over the globe (`pointer-events-none` container, `pointer-events-auto` panels). | Bordered panes. Tab focus moves between them, and the focused pane gets the full `$primary` border. |
| **Two-pane app** (non-desk apps) | n/a | D/S frame: left list pane 38% (min 24, auto-hides under 88 columns, `b` toggles) + right `TabbedContent` with a border title and a badge. |
| **Dialogs over the desk** | Non-immersive views (everything but OPS/GEO/PTS, `nav.ts isImmersive`) open as a `FocusSheet` centred in the free region between the side columns, so the panels stay visible. Esc returns. | `ModalScreen` with a transparent background, centred. Only the `.dialog` box is opaque. Buttons sit in the dialog's last row. Esc or Cancel closes. |

---

## 5. Motion and load

| Item | Web value (W) | TUI value (B §5 unless noted) |
|---|---|---|
| Tape speed | `hud-marquee` 70 s per loop (strip doubled, `translateX(-50%)`), linear | at most 4 cell shifts/s, one timer |
| Alerts rotation | 7 s (`setInterval 7000`) | 7 s |
| Clocks | `useClock(1000)` top bar; 60 s in Sitrep | 1 s only while the clock or a focus countdown is visible, otherwise 60 s |
| Entry animation | `hud-in` 260 ms fade + 4px rise | none (instant) |
| Pulse | `hud-pulse` 1.6 s | none (steady glyph) |
| Hover/press transitions | 140–180 ms ease | n/a |
| Deep-link highlight | `hud-flash` 2.2 s accent glow | the focused pane's border turns `$primary`, and the row is selected |
| Globe spin | `autoRotateSpeed = 0.28`, pixel ratio capped at 2 | Spin ≤ 2 fps, image mode only |
| Pause when hidden | globe `pauseAnimation()` on `document.hidden` or when covered; tape pauses on hover | tape, polls and the map pause when the tab is hidden, the app is unfocused or a modal is open |
| Reduced motion | `@media (prefers-reduced-motion)` stops marquee/pulse and swaps the flash for an outline | a "static tape" setting; no other motion exists |
| Data refresh | as each view needs (hazards `refreshMin 10`; panels 30 s) | news 10 min, quotes 5 min, hazards 10 min, instance 60 s, `r` refreshes at any time |
| **CPU budget** | n/a (browser) | idle desk ≤ **3 %** over 60 s; spin ≤ **15 %**; hidden ≈ 0 % |
| **Memory / swap** | n/a | RSS growth ≤ 20 MB over 30 min; **swap stays near zero** (swap stays near zero under load) |
| Network | never blocks the UI | workers with timeouts; stale data is marked (`stale 5m`), never blanked |

---

## 6. Terminal rules (TUI only)

1. **Colour detection, from the environment only.** Never query the terminal (D 1.7.3 `remote.py`).
   - **Full colour when** any of these holds: `COLORTERM` is `truecolor`/`24bit`; `TERM` contains `direct`/`truecolor`; `TERM` is `xterm-ghostty`/`xterm-kitty`; `TERM_PROGRAM=ghostty`; or `KITTY_WINDOW_ID` is set.
   - **Force before the App exists:** `force_truecolor()` sets `COLORTERM=truecolor` in-process before the Textual App and its console are created. This is needed because Rich treats `xterm-ghostty` without `COLORTERM` as **16-colour** (B 0.1.1 brief, line 13).
   - **Never force** without a signal, and never override `NO_COLOR`.
2. **Over ssh,** ssh does not forward `COLORTERM`, so:
   - every ssh launcher prefixes the remote command with `COLORTERM=truecolor` when the **local** terminal has a signal (B 0.1.1, change 2);
   - the README documents `SetEnv COLORTERM=truecolor` / `AcceptEnv COLORTERM`;
   - when colour still can't be confirmed, the status pane shows the compact Dirlume SSH warning (`remote.WARNING_SHORT`), which fits at 80 columns.
3. **Graphics ladder** (D `termgfx.py`):
   1. **Kitty graphics** (`textual-image` + Pillow) when `remote.kitty_env()` is true and the output is a tty outside tmux/screen.
   2. Otherwise **Braille** (2×4 dots per cell, pure text, ssh-safe).
   3. Otherwise, when the output is not UTF-8, a **plain text** table or message. Never `?`.
   - An `APP_GRAPHICS=kitty|sixel|braille` env override is allowed (D `DIRLUME_GRAPHICS`).
4. **256- and 16-colour fallbacks must keep the hierarchy.** Measured with Rich 14, nearest-colour downgrades collapse it:
   - **HUD in 256 colours:** bg `#03060b` and panel `#0a1322` both become index 16 (`#000000`), while panel-2 `#0f1c30` and the hairline become index 17 (`#00005f`, saturated blue).
   - **GitHub Dark in 256 colours:** bg and surface both become 16.
   - **In 16 colours:** every background becomes black.
   - The **rule:** each theme ships an explicit fallback map instead of trusting nearest-colour. Because God's Eye HUD is now the default for new TUIs, these maps matter. **HUD background and panel must stay visibly distinct in 256 and in 16 colours.** **(Proposed values; David confirms them at the first Ghostty review of a HUD-default TUI.)**

   | Role | 256 HUD | 256 GitHub Dark | 16-colour (both themes) |
   |---|---|---|---|
   | background | 16 `#000000` | 16 `#000000` | black (0) |
   | surface / panel (`$surface`) | 234 `#1c1c1c` | 234 `#1c1c1c` | **blue (4)** |
   | raised: status bar, menu bar, rules (`$panel`) | 236 `#303030` | 236 `#303030` | bright_black (8) |
   | pane border (unfocused) | 24 `#005f87` | 25 `#005faf` | cyan (6) |
   | focus border / accent / primary | 81 `#5fd7ff` | 69 `#5f87ff` | bright_cyan (14) |
   | text | 189 `#d7d7ff` | 195 `#d7ffff` | bright_white (15) |
   | muted (on surface only) | 103 `#8787af` | 246 `#949494` | white (7) |
   | up / warn / down | 85 / 215 / 203 | 71 / 172 / 203 | bright_green / bright_yellow / bright_red |

   - **Distinctness, measured** (contrast ratio between the two fills; truecolor HUD bg/panel is only 1.09):
     - 256: bg/surface 1.23; bg/raised 1.59; surface/raised 1.29.
     - 16 (Rich's standard palette; the real Ghostty palette is checked at the review): bg black / panel blue 1.58; blue / bright_black 1.78. Blue was picked over bright_black for panels because muted and down text fail on bright_black (3.21, 2.37).
   - **Text contrast in the maps:**
     - 256 HUD on 234: text 12.22, muted 4.96, accent 10.27, down 5.72.
     - 256 GitHub Dark on 234: text 15.94, muted 5.62, accent 5.19, up 6.32, warn 5.97, down 5.72; accent on bg 6.40.
     - 16-colour on blue: bright_white 13.29, white 5.72, bright_cyan 10.84, bright_green 10.01, bright_yellow 12.46.
     - **bright_red on blue is 4.23 (FAIL).** Fix: in 16 colours, a down value on a panel is drawn as a reverse chip (black on bright_red, 6.68) and always keeps its `▼`.
     - Muted on raised fails in 256 (103 on 236: 3.84; 246 on 236: 4.35), so muted text never sits on `$panel` (same rule as §2.1).
   - The nearest-colour indexes for accent, text, up, warn and down are Rich's own, except 81/69 for focus. The fills and borders are hand-picked.
   - In 16 colours, focus shows as **reverse** (as short-screen buttons already do).
5. **ASCII mode:** `.ascii-mode` swaps `round` for `ascii` borders, `⚠`→`!`, `▲▼`→`+-`, `◆◇`→`(*)( )`, and sparklines→`_.-^`.
6. **Size fit:** every bordered row must fit inside its border at **80x24, 120x40 and 200x50**, with no broken corners and no doubled `╯╰` (D `tools/frame_scan.py`; S `tests/test_070_restyle.py::test_every_bordered_row_fits_its_border`). Under 30 rows, short-screen rules apply: 1-row frameless buttons, the activity panel hidden by default, and folded sections. Under 100 columns the brand shortens. Under 88 columns the list pane hides.

---

## 7. Themes

- **Every new app ships at least God's Eye HUD (the default) and GitHub Dark (the required second theme),** each with its 256/16 fallback map (§6.4).
  - New TUIs use the shared 22 palettes (N/D/S `themes.py`, with GitHub Dark unified per §2.1) plus **God's Eye HUD** as the 23rd, and set `DEFAULT` to it.
  - Web apps ship the NuzeHub web set: dark = God's Eye HUD, GitHub Dark, GitHub Dim, Neon, Graphite, Midnight; light = GitHub Light (`primer`), Frost, Daylight, Linen (W `theme.ts DARK_THEMES/LIGHT_THEMES`). They also ship the look controls appearance (system/dark/light), ink, shade, glass (solid/frosted/clear), accent and density (W `styles.css`).
- **Theme switching:** a Themes menu with every theme as radio items, plus `t` next / `T` picker (S 0.7.0). Web: Settings ▸ Appearance.
- **Defaults** (stated per app; a theme a user already saved is never overwritten). Shipped apps keep their current default until David asks for a build that adopts this template:

| App | Default today (source) | Template default |
|---|---|---|
| NuzeHub web | God's Eye HUD (`lib/desk/store.ts` `darkTheme: "hud"`) | God's Eye HUD |
| NuzeHub TUI | GitHub Dark (N `themes.py DEFAULT = "github-dark"`, Decision A; 0.2.0 Desk brief Decision 5 keeps it) | **keeps GitHub Dark** until David asks for an adoption build |
| Dirlume 1.7.3 | **Powerlevel10k** (D `themes.py DEFAULT`) | **keeps Powerlevel10k** until David asks for an adoption build |
| SSHush 1.0.0 | **Powerlevel10k** (S `themes.py DEFAULT`) | **keeps Powerlevel10k** until David asks for an adoption build |
| **Any new web app** | n/a | God's Eye HUD |
| **Any new TUI** | n/a | **God's Eye HUD** (Decision 1); GitHub Dark required as the second theme |

---

## 8. Verification checklist (every build, before David sees it)

Run by the builder, then rerun once independently on a verification machine. Evidence goes in `evidence/` in the release folder.

| # | Check | Pass condition |
|---|---|---|
| V1 | **Golden screenshots, real Ghostty, locally** at 80x24, 120x40 and 200x50, in God's Eye HUD (the default) and GitHub Dark | Saved as PNG with the env (`TERM`, `TERM_PROGRAM`, `COLORTERM`) recorded outside the app |
| V2 | **The same over ssh** through the app's launcher, with **no** pre-set `COLORTERM` in the harness (B 0.1.1 §5) | Identical to V1 apart from live data |
| V3 | **Pixel checks of key tokens** on the V1/V2 shots (`pixels.txt`) | bg exactly `#0d1117` (GitHub Dark) / `#080e19` (HUDdy, 1.1; `#03060b` in 1.0 builds); body-text glyph core `#c2cfdc` (HUDdy); focused border = `$primary`; one up, one down, one warn and one accent sample exact |
| V4 | **Fallback runs:** forced 256-colour, forced 16-colour, `*_GRAPHICS=braille`, non-UTF-8 | Hierarchy visible (bg ≠ surface ≠ panel in 256); text table instead of graphics; never `?` |
| V5 | **Border-width check** (`frame_scan` + bordered-row fit test) at the 3 sizes | Zero findings; buttons within `BTN_*` rules |
| V6 | **SVG snapshots** (Textual `snap_compare`) of every tab, menu and dialog | New ones added; existing ones byte-identical unless the brief says otherwise |
| V7 | **See-through check** | Every dialog and menu screen has a transparent backdrop; only the box is opaque |
| V8 | **Keyboard and mouse coverage** | Every menu item, shortcut, alt+letter and tab, by keyboard and by mouse (S `test_052_menus`) |
| V9 | **Motion and load** | §5 budgets measured and logged; timers counted before and after tab switching (no stacking); tape paused when hidden |
| V10 | **Side-by-side review** against the reference screenshots (web desk R, or the app's own golden set), view by view, in a table: element · reference · build · verdict | **Any element plainer than its reference without a stated limit (§3 "stated limit", §6) FAILS** |
| V11 | **Contrast** | Text ≥ 4.5:1 on its own background in both required themes and in the 256/16 maps (`themes.contrast`); text-on-accent checked both ways (§2.1) |
| V12 | **Scope diff** | Only the requested changes; no removed features; parity table for every reused element |
| V13 | **First HUD-default TUI only** | **PASSED (Nov 23, 2026, 8:25 PM EST)** on NuzeHub TUI 0.2.0 Desk in live Ghostty: David confirmed God's Eye HUD, the HUD palette (`secondary`/`branches`), the 256/16 maps, and the `◆◇■□` glyphs as the official TUI template moving forward. (§3.1 web strip guidance remains proposed until the first non-news web app review.) |
| V14 | **Soft contrast (1.1)** | HUDdy tokens equal §2.1.1; a hue-guard test shows every changed token within ±2° of its 1.0 value and every accent, status and branch token unchanged; no `#ffffff` in any HUDdy theme file; pixel samples in real Ghostty (local and ssh) show bg `#080e19` and text cores `#c2cfdc` |
| V15 | **Selection rule (1.1, §2.5)** | An automated test plus a Ghostty pixel sample show `$background` text on the accent fill for a focused tab and a focused list or table row, in HUDdy and GitHub Dark |

---

## 9. Decisions (David, Nov 23, 2026, 1:40 PM ET)

| # | Question | David's answer | What changed in this document |
|---|---|---|---|
| 1 | Default theme for new TUIs | **God's Eye HUD is the default for new TUIs** (already the web default). GitHub Dark is the required second theme. Shipped apps keep their defaults until David asks for an adoption build. | Status line; §2.1 HUD notes; §6.4 maps now keep HUD bg and panel distinct in 256 and 16 colours; §7 defaults table; V1 and the new V13. The HUD extras, the fallback maps and the glyphs stay **proposed** until the first Ghostty review of a HUD-default TUI. |
| 2 | GitHub Dark had two accents | **Unify on the web values:** accent `#4493f8`, muted `#8b949e` for web and TUI. | §2.1 table and notes: pane border `#234571`, bracket `#3672c0`, selected tint `#1c293c`, focus `#4493f8`, button tokens recomputed, full contrast table. Text on accent: web `#ffffff` fails (3.10), so template apps use `#0d1117` (6.11). TUI `$accent` titles stay `#39c5cf`. §6.4 GitHub 256 accent is 69. Adopting this in a shipped TUI is a briefed, snapshot-changing build. |
| 3 | Button focus style | **Focus = the `$primary` border only, no bold.** | §2.2 chip row and §3 row 5 now cite Decision 3. |
| 4 | Letter-spaced labels in a terminal | **Plain UPPERCASE, no letter spacing.** | §2.2 label row cites Decision 4. |
| 5 | How much HUD shell a new web app gets | **The full HUD shell in every new web app, always:** top bar, nav rail, centred see-through sheets, alerts bar, tape and dock. | §3 rows 9–12, 14 and 16 marked required; new §3.1 (proposed) says what the strips show without market or news data; §4 app-shell row. |

---

## Appendix: tokens not found in the source (or different from the screenshot description)

| Expected | What the source actually has |
|---|---|
| A separate **ok** / **danger** colour | None. The web uses `--color-up` / `--color-down` (and `--color-warn`). Mapped as ok = up, danger = down. |
| **accent-glow** for GitHub Dark | None. The glow tokens (`--hud-glow`, `.bg-accent` 18px shadow, `.gh-active` inset 24px) are HUD-only. In every theme, the panel dot has `shadow 0 0 8px accent`. |
| A **CSS star field** | None in CSS. The stars are the globe's `backgroundImageUrl="/globe/night-sky.jpg"` (`globe-view.tsx` line 386; the file is in `public/globe/`), Photo mode only. The HUD body uses two radial gradients, and `.hud-vignette` adds a vignette and 1-in-3px scanlines. |
| **Selected rail item "boxed with a cyan glow"** | An accent 12% fill (`rounded-[3px]`) plus a **2px left accent bar** with a 10px glow. There is no full border box. |
| **A blurred backdrop behind dialogs** | The sheet itself is glass (`.hud-panel` blur 16px, surface 70%), so the desk shows through it blurred. `.hud-dim` (bg 62% + blur 3px) and `.hud-sheet` (blur 22px) are defined in `styles.css` but **not used by any component**. |
| **Spacing tokens** | None of its own; Tailwind utilities. The values in §2.3 are read from the components. |
| A **TUI God's Eye HUD palette** | Not in any TUI source yet (0.2.0 Desk Decision 5 adds it as an extra theme; this template makes it the default for new TUIs). `secondary` and `branches` are **proposed**, confirmed at the first Ghostty review of a HUD-default TUI (§2.1). |
| **256/16-colour fallback maps** | None in any app. The §6.4 table is **proposed** (confirmed at the same review). Nearest-colour values were measured with Rich 14, and the 16-colour ratios use Rich's standard palette. |
| Diamond/box **glyphs** `◆◇■□` for TUI options | Not in the TUIs (they use Textual `Checkbox`). **Proposed** for the template, confirmed at the same review. |
| **Alerts bar, tape and dock content for apps without market or news data** | Not in any source (NuzeHub always has that data). §3.1 is **proposed**. |
| A unified **GitHub Dark** | The shipped TUIs use `#58a6ff`/`#7d8590`, and NuzeHub web uses `--color-accent-fg: #ffffff`. Template 1.0 uses `#4493f8`/`#8b949e` and accent-fg `#0d1117` (Decision 2). Shipped apps change only in a briefed adoption build. |
| Web **light-theme warn** colour | Only the `@theme` default `#d29922` (no per-theme override outside HUD). |

### V13 TUI Confirmation (David, Nov 23, 2026, 8:25 PM EST)
After running **NuzeHub TUI 0.2.0 Desk** live in Ghostty (local and over `nuzehub-remote` SSH), David declared it a major success and confirmed it as **the official TUI app template moving forward, with God's Eye HUD as the default theme**. All TUI **(proposed)** items above (HUD `secondary`/`branches`, `◆◇■□` option glyphs, and 256/16-colour fallback maps) are now **confirmed**. Manual-only map/ticker interaction (no idle auto-spin or auto-scroll animations) is also established as the calm, low-CPU TUI pattern (~1.5% idle CPU, 0 swap).

### Changes in 1.1 (Tue Nov 24, 2026, ET)
- §2.1: the HUDdy TUI column is updated to the soft values (background `#080e19`, surface `#0d192c`, panel `#112138`, text `#c2cfdc`, ink-high `#d6e4f2`, hairline `#1b2e41`, text on accent `#080e19`).
- New §2.1.1 (soft contrast table and rules) and §2.5 (selection rule).
- V3 pixel targets updated; V14 and V15 added.
- Source: `HUDdy-Soft-Contrast-Spec-1.0.md`. Its colours were measured after converting David's Display P3 screenshots to sRGB.
