# HUDdy Soft Contrast Spec 1.0

**Written:** Tuesday, November 24, 2026, about 4:45 PM ET, by Brainstorm (Stage 0 of the approved HUDdy Soft Contrast plan; David approved it at t140u).
**Applies to:** the `HUDdy` theme in NuzeHub TUI, Dirlume and SSHush, and the HUDdy themes for Ghostty, btop/bpytop, Obsidian and VS Code.
**Goes into:** App Design Template 1.1 (§2.1 HUD column, the new §2.5 selection rule, and checks V14–V15).
**Does not change:** any hue, the accent colours, GitHub Dark's palette, the 256/16-colour fallback maps, or any app behaviour.

## 1. What the screenshots show

All three of David's screenshots are tagged **Display P3**, not sRGB. Raw pixel values read straight from the files are shifted (for example, the web text reads `#d9e4f1` and the panels read `#090e18`). Every value in this spec comes from the screenshots after they were converted to sRGB with the embedded ICC profile (LittleCMS, relative colorimetric), so they compare one for one with terminal and theme colours. Text colours are the **glyph-core cluster**: the single most common colour among the brightest 4% of pixels in the text box, which leaves out antialiased edges. Every cluster below was 100% one value.

| Element (web, NuzeHub desk) | sRGB value | Where (pixels in the 3024×1874 shot) |
|---|---|---|
| Page / chrome background (top bar, rail, ticker) | `#03050b` | top bar 1500–2000 × 5–60 (78%), rail 0–100 × 400–700 (93%) |
| Globe surround (space) | `#000000`–`#040404` | photographic starfield; not a UI token |
| **Panel fill** (Sitrep, Intel Feed, Layers, Alerts) | **`#080e19`** | 100% of 2520–2920 × 215–240 and 400–700 × 1140–1170 |
| Inset tile fill (Stories/Geo tiles) | `#050a13` | 250–285 × 340–365 |
| Raised strip (Hazards row) | `#0b1423` | 470–520 × 400–412 |
| Panel divider and tile border | `#1b2e41` / `#1a293a` | row y 196–197; column x 162–163 |
| **Primary text** (headlines, panel titles, numbers, layer names) | **`#d6e4f2`** | 1,356-px cluster, 2355–2920 × 255–315 |
| **Body copy** (Sitrep brief paragraph) | **`#c2cedc`** | 10,830-px cluster, 163–710 × 515–1010 (it is `#d6e4f2` at about 90% over the panel) |
| Secondary / dim text (`CNBC · 4h`, `LAST BRIEF`, `NEXT EVENT`, `Calendar clear`) | `#7d93ad` | e.g. 2350–2470 × 215–242 |
| Accent text (`PRICE MOVES`, badges) | `#5fe1ff` (= `#5ee1ff`) | 1089–1275 × 114–144 |
| Amber (`ALERTS`, `185`) | `#ffb547` | 465–530 × 330–362 |
| Green / red (watchlist %) | `#3effa8` / `#ff5470` | 2850–2990 × 1305–1335 / 1240–1270 |
| Corner bracket | `#4eb4d0` | 128–142 × 95–110 |
| Brightest pixel anywhere in the web UI | `#d6e4f2` | (`#e9e9e9` exists only inside the browser's own tooltip) |

| Element (HUDdy 1.0 themes today) | sRGB value |
|---|---|
| VS Code editor, activity bar, title bar | `#04060a` (= `#03060b` after the P3 round trip) |
| VS Code sidebar, tab strip, code blocks | `#091322` (= `#0a1322`) |
| VS Code text (editor, preview, sidebar, headings) | `#d6e4f2` |
| Obsidian main pane, ribbon, header | `#04060a` |
| Obsidian sidebar, tab bar, filter panel | `#091322` |
| Obsidian text / file tree / muted | `#d6e4f2` / `#93a9bf` / `#7c94ad` |

**Finding.** HUDdy 1.0 already uses the web's exact text and accent colours. The extra contrast David sees comes from two things:
1. **The field the text sits on.** In the web, almost all text sits on the `#080e19` panel; the near-black `#03050b` is only a thin frame (top bar, rail, ticker). In the TUIs, VS Code and Obsidian the big working area is the near-black `#03060b`. Text on it measures 15.69:1, against 14.94:1 (headlines) and 12.10:1 (body copy) in the web.
2. **The brightest whites.** The web never draws anything brighter than `#d6e4f2`, and its long-form copy is `#c2cedc`. HUDdy 1.0 uses `#ffffff` (ink-high) for active tabs, bold text, selection text and ANSI bright white (20.29:1), and SSHush's own HUDdy variant uses `#e2f4ff` for all of its text (17.99:1).

So the soft values lift the near-black field to the web panel colour and cap text at the web's own two levels. Nothing else moves.

## 2. Final token table (canonical HUDdy: NuzeHub TUI 0.2.2 `themes.py`, Dirlume 2.0.0-a3, HUDdy Themes 1.0 `PALETTE.md`)

Hue = HSL hue. "Before" uses the old pair, "After" the new pair. Text pairs need at least 4.5:1; non-text marks need 3:1 except the unfocused pane border and hairline, which are deliberately subtle (template §2.1).

| Token | Old | New | ΔHue | Source pixel / reason | Contrast pair | Before | After |
|---|---|---|---|---|---|---|---|
| background `$background` | `#03060b` | `#080e19` | 217.5°→218.8° (+1.3°) | web panel fill `#080e19`, 100% of pixels in Intel Feed (2520–2920, 215–240), Layers (400–700, 1140–1170), Alerts strip (1400–2000, 100–108) | `#d6e4f2`→`#c2cfdc` on it | 15.69 | 12.19 |
| surface `$surface` | `#0a1322` | `#0d192c` | 217.5°→216.8° (-0.7°) | derived: keeps the approved 1.09:1 surface/background step above the new background, same hue (web raised strip `#0b1423` is the nearest web pixel) | `#d6e4f2`→`#c2cfdc` on it | 14.38 | 11.11 |
| panel `$panel` (raised) | `#0f1c30` | `#112138` | 216.4°→215.4° (-1.0°) | derived: keeps the approved 1.09:1 panel/surface step, same hue | `#d6e4f2`→`#c2cfdc` on it | 13.21 | 10.21 |
| foreground `$foreground` (body text) | `#d6e4f2` | `#c2cfdc` | 210.0°→210.0° (+0.0°) | web body copy: SITREP brief text, 10,830-pixel glyph-core cluster `#c2cedc` (163–710, 515–1010); hue set back to 210.0° | on background | 15.69 | 12.19 |
| ink-high (strongest text, ANSI 15, selection text) | `#ffffff` | `#d6e4f2` | n/a (white has no hue; new = text hue 210.0°) | web headlines, panel titles, numbers: 1,356-pixel glyph-core cluster `#d6e4f2` (2355–2920, 255–315); brightest non-browser pixel on the page | on background | 20.29 | 14.94 |
| muted `$text-muted` | `#7d93ad` | `#7d93ad` | 0 | unchanged; web `CNBC · 4h`, `LAST BRIEF`, `NEXT EVENT` cores are exactly `#7d93ad` | on background | 6.43 | 6.12 |
| secondary (ink-soft) | `#93a8bf` | `#93a8bf` | 0 | unchanged (mid-tone, not a bright white) | on background | 8.31 | 7.90 |
| primary / accent | `#5ee1ff` | `#5ee1ff` | 0 | unchanged; web `PRICE MOVES` core `#5fe1ff` | on background | 13.23 | 12.59 |
| success / up | `#3dffa8` | `#3dffa8` | 0 | unchanged; web watchlist `+0.93%` core `#3effa8` | on surface | 14.23 | 13.47 |
| warning | `#ffb547` | `#ffb547` | 0 | unchanged; web `185` and `ALERTS` cores `#ffb547` | on surface | 10.59 | 10.02 |
| error / down | `#ff5470` | `#ff5470` | 0 | unchanged; web watchlist `-6.98%` core `#ff5470` | on surface | 5.98 | 5.66 |
| neon cyan (branch 7) | `#3ef0ff` | `#3ef0ff` | 0 | unchanged | on background | 14.61 | 13.90 |
| midnight blue (branch 8) | `#64d2ff` | `#64d2ff` | 0 | unchanged | on background | 11.79 | 11.23 |
| hairline / rules | `#172634` | `#1b2e41` | 209.0°→210.0° (+1.0°) | web panel divider and tile border `#1b2e41` (2330–2990, 196–197) | vs surface (non-text) | 1.21 | 1.27 |
| pane border (unfocused) | `#275e6d` | `#275e6d` | 0 | unchanged (primary 40%; deliberately subtle) | vs background (non-text) | 2.81 | 2.67 |
| corner bracket | `#47aac2` | `#47aac2` | 0 | unchanged (web bracket measures `#4eb4d0`, the same hue) | vs background (non-text) | 7.53 | 7.17 |
| selected tint | `#142c3d` | `#142c3d` | 0 | unchanged (already above the new surface) | text on it | 11.14 | 9.09 |
| disabled / ANSI 0 black | `#2e3744` | `#2e3744` | 0 | unchanged | vs background (non-text) | 1.69 | 1.61 |
| text on accent (selected-row text, cursor text, badges, status labels) | `#03060b` | `#080e19` | 217.5°→218.8° (+1.3°) | = new background (rule §4) | on `#5ee1ff` | 13.23 | 12.59 |
| inactive text | `#404c5c` | `#404c5c` | 0 | unchanged (decorative) | on background | 2.33 | 2.21 |
| faint text | `#5e7084` | `#5e7084` | 0 | unchanged | on background | 3.99 | 3.80 |

Other pairs that builds must keep at or above 4.5:1 (template V11):

| Pair | Before | After |
|---|---|---|
| foreground on surface | 14.38 | 11.11 |
| foreground on panel | 13.21 | 10.21 |
| ink-high on background | 20.29 | 14.94 |
| muted on surface | 5.89 | 5.58 |
| muted on panel (rule: avoid) | 5.41 | 5.12 |
| accent on surface | 12.12 | 11.48 |
| accent on panel | 11.14 | 10.54 |
| secondary on panel | 6.99 | 6.62 |
| text-on-accent on success / warning / error | 15.53/11.55/6.53 | 14.78/10.99/6.21 |
| ANSI 0 `#2e3744` vs background | 1.69 | 1.61 |

Every hue moves by at most 1.3°, inside the ±2° rule. Only lightness (and, for `$foreground`, saturation, to match the web body copy) changes. Background tokens only get lighter and text tokens only get darker. Accent, status and branch colours stay exactly as they are, because they already match the web pixel for pixel.

### 2.1 SSHush's own HUDdy variant

SSHush 1.0.1 shipped a slightly different HUDdy set: panel `#11223b`, text `#e2f4ff`, muted `#78a2be`, secondary `#a5f3fc`, success `#34d399`, warning `#fbbf24` and error `#fb7185`. Moving SSHush onto the canonical values would change some hues (text 202.8° → 210°, success, warning and error), so this pass softens SSHush's own values at their own hues instead (see open question 1).

| SSHush token | Old | New | Hue old → new | On background, before → after |
|---|---|---|---|---|
| background | `#03060b` | `#080e19` | 217.5° → 218.8° | n/a |
| surface | `#0a1322` | `#0d192c` | 217.5° → 216.8° | 1.09 → 1.10 (step vs bg) |
| panel | `#11223b` | `#132643` | 215.7° → 216.3° | 1.27 → 1.27 (step vs bg) |
| foreground | `#e2f4ff` | `#c0d0da` | 202.8° → 203.1° | 17.99 → 12.21 |
| secondary | `#a5f3fc` | `#94f1fb` | 186.2° → 185.8° | 16.26 → 14.93 (capped at the web's brightest-text luminance) |
| text on accent | `#03060b` / Textual `auto 87%` | `#080e19` | as background | see §3 |
| muted, accent, success, warning, error, branches | unchanged | unchanged | 0 | muted 7.45 → 7.09 |

### 2.2 GitHub Dark

GitHub Dark keeps its published palette (`#0d1117` background, `#e6edf3` text). It is not part of the soft pass (see open question 2). It does get the selection rule in §3, because SSHush shows the same bug there.

### 2.3 256- and 16-colour fallback maps

Unchanged in 1.1. The maps already put HUDdy's background on index 16 and keep surface (234) and panel (236) distinct. No lower step of the same hue exists for text 189 in the 256 cube. These maps are used only without truecolor, which none of David's Ghostty sessions lack, locally or over ssh.

## 3. Rule: selected and highlighted rows use dark text on the accent fill

**Rule (all TUIs, every theme whose background reaches at least 4.5:1 on its primary):** a row, tab, menu item, list item, tree node or table cursor drawn on a solid accent or primary fill uses the theme's **background** token as its text colour. For HUDdy that is `#080e19` on `#5ee1ff` (12.59:1). For GitHub Dark it is `#0d1117` on `#4493f8` (6.11:1). An unfocused selection keeps the selected-tint fill (`#142c3d`) with `$foreground` text (9.09:1). Light themes, and any dark theme whose background fails 4.5:1 on its primary, keep Textual's automatic contrast.

**How to apply it (one place per app):** in `Palette.textual()`, set the Textual theme variables `block-cursor-foreground` to the palette's `background` (where the 4.5:1 check passes) and `block-cursor-background` to its `primary`. Remove any rule that overrides the colour of a focused or active accent-filled item with `$foreground`.

**Measured today (headless Textual 8.2.8 pilot, 120×40, demo data, scratch state dir):**

| App | Element | Text on fill today | Ratio | Status |
|---|---|---|---|---|
| SSHush 1.0.2, HUDdy | focused view tab (Inventory, Topology, Enrollment, Keys, Jobs, Settings) | `#e2f4ff` on `#5ee1ff` | **1.36:1** | **Bug.** Caused by `#main-tabs Tabs Tab.-active { color: $foreground; }` in `ui/app.py`, which beats Textual's `Tabs:focus .-active` block-cursor colours |
| SSHush 1.0.2, GitHub Dark | the same tab | `#e6edf3` on `#4493f8` | **2.62:1** | **Bug, same cause.** The fix gives `#0d1117` on `#4493f8`, 6.11:1, with no hue change |
| SSHush 1.0.2 | View and other menus, Keys/Jobs table cursor | about `#0c1d21` (Textual `auto 87%`) on accent | ≈12 | Dark already; switch to the explicit token |
| Dirlume 2.0.0-a3, NuzeHub TUI 0.2.2 | tabs, menus, tables | Textual `auto 87%` (dark) | ≈12 | Correct look; switch to the explicit token so all three apps render identically |

## 4. Per-app guidance (HUDdy Themes 1.1, Stage 4)

All values are the new tokens from §2. Anything not listed keeps its HUDdy Themes 1.0 value.

### 4.1 Terminals (Ghostty, and VS Code's integrated terminal)

| Setting | 1.0 | 1.1 |
|---|---|---|
| `background` | `#03060b` | `#080e19` |
| `foreground` | `#d6e4f2` | `#c2cfdc` |
| `cursor-color` / `cursor-text` | `#5ee1ff` / `#03060b` | `#5ee1ff` / `#080e19` |
| `selection-background` / `selection-foreground` | `#142c3d` / `#ffffff` | `#142c3d` / `#d6e4f2` |
| `split-divider-color` | `#275e6d` | `#275e6d` |

| # | Name | 1.0 | 1.1 | # | Name | 1.0 | 1.1 |
|---|---|---|---|---|---|---|---|
| 0 | black | `#2e3744` | `#2e3744` (1.61:1 vs bg, still clearly above it) | 8 | bright black | `#7d93ad` | `#7d93ad` |
| 1 | red | `#ff5470` | same | 9 | bright red | `#ff879b` | same |
| 2 | green | `#3dffa8` | same | 10 | bright green | `#77ffc2` | same |
| 3 | yellow | `#ffb547` | same | 11 | bright yellow | `#ffcb7e` | same |
| 4 | blue | `#64d2ff` | same | 12 | bright blue | `#92e0ff` | same |
| 5 | magenta | `#c792ff` | same | 13 | bright magenta | `#d8b3ff` | same |
| 6 | cyan | `#5ee1ff` | same | 14 | bright cyan | `#3ef0ff` | same |
| 7 | white | `#93a8bf` | same | 15 | **bright white** | **`#ffffff`** | **`#d6e4f2`** |

Notes:
- ANSI 7 (`#93a8bf`) stays below the default foreground and ANSI 15 above it, so programs that print "white" or "bold white" keep their order: 7 < foreground < 15.
- Leave Ghostty's `bold-is-bright` at its default (`false`), so bold text stays `#c2cfdc` and doesn't jump to bright white.
- The bright colour variants (9–14) are coloured, not white, so they stay. That keeps the hue rule.
- TUIs paint their own truecolor background, so a TUI shows `#080e19` only after its own soft build (Stages 1–3), whatever the Ghostty theme.

### 4.2 btop and bpytop

`main_bg` `#080e19` (was `#03060b`), `main_fg` `#c2cfdc` (was `#d6e4f2`), `meter_bg` `#1b2e41` (btop only, was hairline `#172634`). Everything else stays: `selected_fg` is already the accent `#5ee1ff`, `selected_bg` `#142c3d`, `div_line` the pane border `#275e6d`, `inactive_fg` `#404c5c`, titles, highlights, graphs and gradients. In `btop.conf`, leave `theme_background = true` (the default) so the soft background draws instead of the terminal's.

### 4.3 VS Code (`davidprush.huddy-theme` 1.0.1)

- **`#080e19`** (was `#03060b`): editor, gutter, minimap, activity bar, panel, title bar, status bar if it used bg, `tab.activeBackground`, `terminal.background`, `editorStickyScroll`, `peekViewResult`, `galleryBanner.color`.
- **`#0d192c`** (was `#0a1322`): sideBar, tab strip, inactive tabs, widgets, inputs, dropdowns, hovers, code blocks, line highlight.
- **`#112138`** (was `#0f1c30`): status bar, `button.secondaryBackground`, `peekViewTitle`, inactive list selection.
- **`#c2cfdc`** (was `#d6e4f2`): `foreground`, `editor.foreground`, `sideBar.foreground`, and the default token colour in the syntax rules.
- **`#d6e4f2`** (was `#ffffff`): `tab.activeForeground`, `list.activeSelectionForeground`, `inputOption.activeForeground`, `peekViewTitleLabel.foreground`, `menu.selectionForeground`, `quickInputList.focusForeground`, `terminal.ansiBrightWhite`, and the `markup.bold` token rule. After the build, no `#ffffff` is left anywhere in the theme JSON.
- **`#1b2e41`** (was `#172634`): every border and hairline that used it.
- **`#080e19`** (was `#03060b`): `button.foreground`, `badge.foreground`, `activityBarBadge.foreground`, `editorCursor.background`.

### 4.4 Obsidian (HUDdy theme 1.1.0)

`--color-base-00` and `--background-primary`, `--titlebar-background`, `--tab-container-background`, `--ribbon-background` → `#080e19`. `--color-base-05` → mix of the new bg and surface. `--color-base-10` and `--background-secondary` → `#0d192c`. `--color-base-20` and `--background-secondary-alt` → `#112138`. `--color-base-30`, `--background-modifier-border`, `--divider-color`, `--hr-color`, `--graph-line` → `#1b2e41`. `--color-base-100`, `--text-normal`, `--code-normal`, `--italic-color` → `#c2cfdc`. `--bold-color`, headings and `--color-accent-1` mixes that used ink-high → `#d6e4f2`. `--text-on-accent`, `--text-on-accent-inverted`, `--checkbox-marker-color` → `#080e19`. The muted tokens are unchanged.

## 5. What every soft build must prove (copied into the three briefs)

1. **Pixel sampling in real Ghostty, locally and over ssh, with `COLORTERM` never preset:** the HUDdy background is exactly `#080e19`, body text glyph cores are `#c2cfdc` (`#c0d0da` in SSHush), at least one panel or surface sample is `#0d192c`, and GitHub Dark is still exactly `#0d1117`. Sample glyph cores the way this spec does: the single most common colour among the brightest few percent of pixels, not edges.
2. **Selection rule:** a focused accent-filled tab or row shows `#080e19` text (`#0d1117` in GitHub Dark) on the accent, sampled from pixels, and an automated test asserts it.
3. **Hue guard test:** every changed HUDdy token is within ±2° HSL hue of its old value, and no accent, status or branch token changed. The table lives in the test.
4. **Contrast test:** every pair in §2 meets its threshold, using `themes.contrast`.
5. **Snapshots:** they change on purpose. Before/after PNGs are saved and the changed snapshot list is reviewed, not bulk-accepted without a look.

## 6. Open questions for David

1. **SSHush's own HUDdy hues.** SSHush still uses its 1.0.1 variant (text `#e2f4ff` at 202.8°, success `#34d399`, warning `#fbbf24`, error `#fb7185`), while NuzeHub and Dirlume use the canonical set. This pass keeps SSHush's hues as they are. Do you want a later step to put SSHush on the canonical HUDdy set, so all three apps match exactly? That would shift a few hues slightly.
2. **GitHub Dark.** Should the soft treatment also apply to GitHub Dark? Its background `#0d1117` is already lighter than HUDdy's new one, and its text is `#e6edf3`. Today only the selection fix touches it.
3. **Surface level.** The spec lifts `$surface` to `#0d192c` so the panes stay as distinct from the background as you approved in the V13 review. The web's own raised strip is a touch darker, `#0b1423`. If the surfaces look too light in the first Ghostty review, `#0b1423` is the fallback. Same hue, no other change.
