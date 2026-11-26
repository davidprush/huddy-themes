import json, os, colorsys
from palette import *
OUT = os.environ.get('OUT', '/workspace/huddy-1.1-src/pack')
def w(rel, text):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text)

# ---------------- Ghostty ----------------
g = ["# HUDdy for Ghostty 1.1 — HUDdy Soft Contrast Spec 1.0. MIT, David Rush.",
     "# Install: ~/.config/ghostty/themes/HUDdy, then `theme = HUDdy` in your Ghostty config."]
g += [f"palette = {i}={c}" for i, c in enumerate(ANSI)]
g += [f"background = {BG}", f"foreground = {FG}", f"cursor-color = {ACCENT}", f"cursor-text = {ON_ACCENT}",
      f"selection-background = {SEL}", f"selection-foreground = {INK_HIGH}", f"split-divider-color = {PANE}"]
w('ghostty/HUDdy', '\n'.join(g) + '\n')

# ---------------- bpytop / btop ----------------
def grad(s, m, e): return (s, m, e)
common = [
    ('main_bg', BG, 'Main background'), ('main_fg', FG, 'Main text'), ('title', ACCENT, 'Box titles'),
    ('hi_fg', WARN, 'Highlighted key letters'), ('selected_bg', SEL, 'Selected process row'),
    ('selected_fg', ACCENT, 'Selected process text'), ('inactive_fg', INACTIVE, 'Inactive / unused graph text'),
]
btop_only_mid = [('graph_text', MUTED, 'Graph labels and dimmed text (btop)'), ('meter_bg', HAIRLINE, 'Meter background (btop)')]
rest = [
    ('proc_misc', OK, 'Process box mini cpu graph, misc'),
    ('cpu_box', BRACKET, 'CPU box outline'), ('mem_box', BRACKET, 'Memory box outline'),
    ('net_box', BRACKET, 'Net box outline'), ('proc_box', BRACKET, 'Process box outline'),
    ('div_line', PANE, 'Box dividers'),
]
grads = [
    ('temp', (MIDNIGHT, WARN, ERR), 'Temperature'), ('cpu', (OK, WARN, ERR), 'CPU usage'),
    ('free', (DIM(OK), '', OK), 'Free memory'), ('cached', (DIM(MIDNIGHT), '', MIDNIGHT), 'Cached memory'),
    ('available', (DIM(WARN), '', WARN), 'Available memory'), ('used', (DIM(ERR), '', ERR), 'Used memory'),
    ('download', (PANE, ACCENT, mix(ACCENT, MIX_WHITE, 0.5)), 'Download'),  # 1.0 gradient end, unchanged
    ('upload', (DIM(OK), OK, bright(OK)), 'Upload'),
]
def theme_file(prog, extra_mid, extra_end):
    L = [f"#HUDdy theme for {prog} 1.1 — HUDdy Soft Contrast Spec 1.0. MIT, David Rush.", ""]
    for k, v, d in common + extra_mid + rest:
        L += [f"#{d}", f'theme[{k}]="{v}"', ""]
    for k, (s, m, e), d in grads + extra_end:
        L += [f"#{d} graph gradient (start, mid, end)", f'theme[{k}_start]="{s}"', f'theme[{k}_mid]="{m}"', f'theme[{k}_end]="{e}"', ""]
    return '\n'.join(L)
w('bpytop/huddy.theme', theme_file('bpytop', [], []))
w('btop/huddy.theme', theme_file('btop', btop_only_mid, [('process', (OK, WARN, ERR), 'Process cpu usage')]))

# ---------------- Obsidian ----------------
hh, ll, ss = colorsys.rgb_to_hls(*(v / 255 for v in (int(ACCENT[i:i+2], 16) for i in (1, 3, 5))))
cols = dict(red=ERR, orange=WARN, yellow=bright(WARN), green=OK, cyan=ACCENT, blue=MIDNIGHT, purple=MAGENTA, pink=bright(ERR))
css = f"""/* HUDdy for Obsidian 1.1.0 — HUDdy Soft Contrast Spec 1.0. MIT, David Rush.
   Dark only: HUDdy has no light palette, so Obsidian's own light colours are used if you switch to light mode. */

.theme-dark {{
  color-scheme: dark;
  --color-base-00: {BG};
  --color-base-05: {mix(BG, SURFACE, 0.5)};
  --color-base-10: {SURFACE};
  --color-base-20: {PANEL};
  --color-base-25: {SEL};
  --color-base-30: {HAIRLINE};
  --color-base-35: {PANE};
  --color-base-40: {INACTIVE};
  --color-base-50: {FAINT};
  --color-base-60: {MUTED};
  --color-base-70: {SECONDARY};
  --color-base-100: {FG};

""" + ''.join(f"  --color-{n}-rgb: {rgb(c)};\n  --color-{n}: {c};\n" for n, c in cols.items()) + f"""
  --accent-h: {round(hh * 360)};
  --accent-s: {round(ss * 100)}%;
  --accent-l: {round(ll * 100)}%;
  --color-accent: {ACCENT};
  --color-accent-1: {mix(ACCENT, INK_HIGH, 0.2)};
  --color-accent-2: {NEON};
  --text-on-accent: {ON_ACCENT};
  --text-on-accent-inverted: {ON_ACCENT};
  --interactive-accent: {ACCENT};
  --interactive-accent-hover: {NEON};

  --background-primary: {BG};
  --background-primary-alt: {SURFACE};
  --background-secondary: {SURFACE};
  --background-secondary-alt: {PANEL};
  --background-modifier-border: {HAIRLINE};
  --background-modifier-border-hover: {PANE};
  --background-modifier-border-focus: {ACCENT};
  --background-modifier-hover: rgba({rgb(ACCENT)}, 0.08);
  --background-modifier-active-hover: rgba({rgb(ACCENT)}, 0.14);
  --background-modifier-error: {ERR};
  --background-modifier-success: {OK};
  --titlebar-background: {BG};
  --titlebar-background-focused: {SURFACE};
  --tab-container-background: {BG};
  --ribbon-background: {BG};
  --divider-color: {HAIRLINE};

  --text-normal: {FG};
  --text-muted: {SECONDARY};
  --text-faint: {MUTED};
  --text-accent: {ACCENT};
  --text-accent-hover: {NEON};
  --text-error: {ERR};
  --text-success: {OK};
  --text-warning: {WARN};
  --text-selection: rgba({rgb(ACCENT)}, 0.22);
  --text-highlight-bg: rgba({rgb(WARN)}, 0.30);
  --text-highlight-bg-active: rgba({rgb(WARN)}, 0.45);

  --h1-color: {ACCENT};
  --h2-color: {MIDNIGHT};
  --h3-color: {OK};
  --h4-color: {WARN};
  --h5-color: {SECONDARY};
  --h6-color: {MUTED};
  --bold-color: {INK_HIGH};
  --italic-color: {FG};
  --link-color: {ACCENT};
  --link-color-hover: {NEON};
  --link-external-color: {MIDNIGHT};
  --link-unresolved-color: {WARN};
  --tag-color: {ACCENT};
  --tag-background: rgba({rgb(ACCENT)}, 0.10);
  --tag-border-color: rgba({rgb(ACCENT)}, 0.35);
  --blockquote-border-color: {ACCENT};
  --hr-color: {HAIRLINE};
  --checkbox-color: {ACCENT};
  --checkbox-marker-color: {ON_ACCENT};
  --code-background: {SURFACE};
  --code-normal: {FG};
  --code-comment: {MUTED};
  --code-function: {MIDNIGHT};
  --code-keyword: {ACCENT};
  --code-important: {ERR};
  --code-operator: {SECONDARY};
  --code-property: {SECONDARY};
  --code-punctuation: {SECONDARY};
  --code-string: {OK};
  --code-tag: {ACCENT};
  --code-value: {WARN};
  --graph-node: {SECONDARY};
  --graph-node-focused: {ACCENT};
  --graph-node-tag: {OK};
  --graph-node-attachment: {WARN};
  --graph-node-unresolved: {MUTED};
  --graph-line: {HAIRLINE};
  --scrollbar-thumb-bg: rgba({rgb(ACCENT)}, 0.18);
  --scrollbar-active-thumb-bg: rgba({rgb(ACCENT)}, 0.35);
}}

/* HUD touch: a thin accent line under the active tab and the focused pane header. */
.theme-dark .workspace-tab-header.is-active {{ box-shadow: inset 0 -2px 0 {ACCENT}; }}
.theme-dark .workspace-leaf.mod-active .view-header {{ border-bottom: 1px solid {PANE}; }}
.theme-dark .markdown-rendered h1, .theme-dark .HyperMD-header-1 {{ letter-spacing: 0.02em; }}
"""
w('obsidian/HUDdy/theme.css', css)
w('obsidian/HUDdy/manifest.json', json.dumps({"name": "HUDdy", "version": "1.1.0", "minAppVersion": "1.0.0",
    "author": "David Rush", "authorUrl": "https://davidprush.com"}, indent=2) + '\n')

# ---------------- VS Code ----------------
A = lambda c, a: c + a  # hex alpha
wb = {
 "focusBorder": ACCENT, "foreground": FG, "disabledForeground": INACTIVE, "descriptionForeground": SECONDARY,
 "errorForeground": ERR, "icon.foreground": SECONDARY, "widget.shadow": "#00000080", "selection.background": A(ACCENT, "40"),
 "textLink.foreground": ACCENT, "textLink.activeForeground": NEON, "textPreformat.foreground": OK,
 "textBlockQuote.background": SURFACE, "textBlockQuote.border": ACCENT, "textCodeBlock.background": SURFACE,
 "textSeparator.foreground": HAIRLINE,
 "button.background": ACCENT, "button.foreground": ON_ACCENT, "button.hoverBackground": NEON,
 "button.secondaryBackground": PANEL, "button.secondaryForeground": FG, "button.secondaryHoverBackground": SEL,
 "button.border": "#00000000", "checkbox.background": SURFACE, "checkbox.border": PANE, "checkbox.foreground": ACCENT,
 "dropdown.background": SURFACE, "dropdown.border": HAIRLINE, "dropdown.foreground": FG, "dropdown.listBackground": SURFACE,
 "input.background": SURFACE, "input.border": HAIRLINE, "input.foreground": FG, "input.placeholderForeground": MUTED,
 "inputOption.activeBackground": A(ACCENT, "33"), "inputOption.activeBorder": ACCENT, "inputOption.activeForeground": INK_HIGH,
 "inputValidation.errorBackground": SURFACE, "inputValidation.errorBorder": ERR,
 "inputValidation.warningBackground": SURFACE, "inputValidation.warningBorder": WARN,
 "inputValidation.infoBackground": SURFACE, "inputValidation.infoBorder": ACCENT,
 "scrollbar.shadow": "#00000000", "scrollbarSlider.background": A(ACCENT, "22"),
 "scrollbarSlider.hoverBackground": A(ACCENT, "44"), "scrollbarSlider.activeBackground": A(ACCENT, "66"),
 "badge.background": ACCENT, "badge.foreground": ON_ACCENT, "progressBar.background": ACCENT,
 "list.activeSelectionBackground": SEL, "list.activeSelectionForeground": INK_HIGH, "list.activeSelectionIconForeground": ACCENT,
 "list.inactiveSelectionBackground": PANEL, "list.inactiveSelectionForeground": FG, "list.hoverBackground": A(ACCENT, "12"),
 "list.hoverForeground": FG, "list.focusOutline": ACCENT, "list.focusBackground": SEL, "list.highlightForeground": ACCENT,
 "list.errorForeground": ERR, "list.warningForeground": WARN, "list.dropBackground": A(ACCENT, "22"),
 "tree.indentGuidesStroke": HAIRLINE, "tree.inactiveIndentGuidesStroke": HAIRLINE,
 "activityBar.background": BG, "activityBar.foreground": ACCENT, "activityBar.inactiveForeground": MUTED,
 "activityBar.border": HAIRLINE, "activityBar.activeBorder": ACCENT, "activityBar.activeBackground": SURFACE,
 "activityBarBadge.background": ACCENT, "activityBarBadge.foreground": ON_ACCENT,
 "sideBar.background": SURFACE, "sideBar.foreground": FG, "sideBar.border": HAIRLINE,
 "sideBarTitle.foreground": ACCENT, "sideBarSectionHeader.background": SURFACE, "sideBarSectionHeader.foreground": SECONDARY,
 "sideBarSectionHeader.border": HAIRLINE,
 "minimap.background": BG, "minimap.selectionHighlight": A(ACCENT, "66"), "minimap.findMatchHighlight": A(WARN, "99"),
 "minimap.errorHighlight": ERR, "minimap.warningHighlight": WARN, "minimapSlider.background": A(ACCENT, "18"),
 "minimapSlider.hoverBackground": A(ACCENT, "30"), "minimapSlider.activeBackground": A(ACCENT, "44"),
 "editorGroup.border": HAIRLINE, "editorGroup.dropBackground": A(ACCENT, "18"),
 "editorGroupHeader.tabsBackground": SURFACE, "editorGroupHeader.tabsBorder": HAIRLINE, "editorGroupHeader.noTabsBackground": BG,
 "tab.activeBackground": BG, "tab.activeForeground": INK_HIGH, "tab.activeBorderTop": ACCENT, "tab.activeBorder": BG,
 "tab.inactiveBackground": SURFACE, "tab.inactiveForeground": MUTED, "tab.border": HAIRLINE,
 "tab.hoverBackground": PANEL, "tab.hoverForeground": FG, "tab.unfocusedActiveForeground": SECONDARY,
 "tab.unfocusedActiveBorderTop": PANE, "tab.activeModifiedBorder": WARN, "tab.inactiveModifiedBorder": A(WARN, "80"),
 "editor.background": BG, "editor.foreground": FG,
 "editorLineNumber.foreground": INACTIVE, "editorLineNumber.activeForeground": ACCENT,
 "editorCursor.foreground": ACCENT, "editorCursor.background": ON_ACCENT,
 "editor.selectionBackground": A(ACCENT, "40"), "editor.inactiveSelectionBackground": A(ACCENT, "22"),
 "editor.selectionHighlightBackground": A(ACCENT, "22"), "editor.wordHighlightBackground": A(ACCENT, "20"),
 "editor.wordHighlightStrongBackground": A(OK, "22"), "editor.findMatchBackground": A(WARN, "55"),
 "editor.findMatchBorder": WARN, "editor.findMatchHighlightBackground": A(WARN, "30"),
 "editor.lineHighlightBackground": SURFACE, "editor.lineHighlightBorder": "#00000000",
 "editor.rangeHighlightBackground": A(ACCENT, "12"), "editorLink.activeForeground": NEON,
 "editorWhitespace.foreground": HAIRLINE, "editorIndentGuide.background1": HAIRLINE, "editorIndentGuide.activeBackground1": PANE,
 "editorRuler.foreground": HAIRLINE, "editorCodeLens.foreground": MUTED,
 "editorBracketMatch.background": A(ACCENT, "22"), "editorBracketMatch.border": ACCENT,
 "editorBracketHighlight.foreground1": ACCENT, "editorBracketHighlight.foreground2": WARN,
 "editorBracketHighlight.foreground3": OK, "editorBracketHighlight.foreground4": MIDNIGHT,
 "editorBracketHighlight.foreground5": MAGENTA, "editorBracketHighlight.foreground6": SECONDARY,
 "editorBracketHighlight.unexpectedBracket.foreground": ERR,
 "editorError.foreground": ERR, "editorWarning.foreground": WARN, "editorInfo.foreground": ACCENT, "editorHint.foreground": OK,
 "editorGutter.background": BG, "editorGutter.addedBackground": OK, "editorGutter.modifiedBackground": WARN,
 "editorGutter.deletedBackground": ERR,
 "editorOverviewRuler.border": HAIRLINE, "editorOverviewRuler.errorForeground": ERR,
 "editorOverviewRuler.warningForeground": WARN, "editorOverviewRuler.infoForeground": ACCENT,
 "editorOverviewRuler.addedForeground": OK, "editorOverviewRuler.modifiedForeground": WARN, "editorOverviewRuler.deletedForeground": ERR,
 "editorWidget.background": SURFACE, "editorWidget.foreground": FG, "editorWidget.border": PANE,
 "editorSuggestWidget.background": SURFACE, "editorSuggestWidget.border": PANE, "editorSuggestWidget.foreground": FG,
 "editorSuggestWidget.selectedBackground": SEL, "editorSuggestWidget.highlightForeground": ACCENT,
 "editorHoverWidget.background": SURFACE, "editorHoverWidget.border": PANE,
 "editorStickyScroll.background": BG, "editorStickyScrollHover.background": SURFACE,
 "peekView.border": ACCENT, "peekViewEditor.background": SURFACE, "peekViewResult.background": BG,
 "peekViewTitle.background": PANEL, "peekViewTitleLabel.foreground": INK_HIGH, "peekViewTitleDescription.foreground": SECONDARY,
 "peekViewEditor.matchHighlightBackground": A(WARN, "40"), "peekViewResult.matchHighlightBackground": A(WARN, "40"),
 "peekViewResult.selectionBackground": SEL,
 "diffEditor.insertedTextBackground": A(OK, "1f"), "diffEditor.removedTextBackground": A(ERR, "1f"),
 "diffEditor.insertedLineBackground": A(OK, "12"), "diffEditor.removedLineBackground": A(ERR, "12"),
 "merge.currentHeaderBackground": A(OK, "40"), "merge.incomingHeaderBackground": A(ACCENT, "40"),
 "panel.background": BG, "panel.border": HAIRLINE, "panelTitle.activeForeground": ACCENT,
 "panelTitle.activeBorder": ACCENT, "panelTitle.inactiveForeground": MUTED, "panelInput.border": HAIRLINE,
 "statusBar.background": PANEL, "statusBar.foreground": FG, "statusBar.border": HAIRLINE,
 "statusBar.debuggingBackground": WARN, "statusBar.debuggingForeground": ON_ACCENT,
 "statusBar.noFolderBackground": PANEL, "statusBarItem.hoverBackground": SEL,
 "statusBarItem.remoteBackground": ACCENT, "statusBarItem.remoteForeground": ON_ACCENT,
 "statusBarItem.prominentBackground": SEL, "statusBarItem.errorBackground": ERR, "statusBarItem.errorForeground": ON_ACCENT,
 "statusBarItem.warningBackground": WARN, "statusBarItem.warningForeground": ON_ACCENT,
 "titleBar.activeBackground": BG, "titleBar.activeForeground": FG, "titleBar.inactiveBackground": BG,
 "titleBar.inactiveForeground": MUTED, "titleBar.border": HAIRLINE,
 "menubar.selectionBackground": SEL, "menu.background": SURFACE, "menu.foreground": FG, "menu.border": PANE,
 "menu.selectionBackground": SEL, "menu.selectionForeground": INK_HIGH, "menu.separatorBackground": HAIRLINE,
 "commandCenter.background": SURFACE, "commandCenter.foreground": FG, "commandCenter.border": HAIRLINE,
 "commandCenter.activeBackground": PANEL,
 "quickInput.background": SURFACE, "quickInput.foreground": FG, "quickInputTitle.background": PANEL,
 "quickInputList.focusBackground": SEL, "quickInputList.focusForeground": INK_HIGH, "pickerGroup.foreground": ACCENT,
 "pickerGroup.border": HAIRLINE, "keybindingLabel.background": PANEL, "keybindingLabel.foreground": FG,
 "keybindingLabel.border": PANE, "keybindingLabel.bottomBorder": PANE,
 "notifications.background": SURFACE, "notifications.foreground": FG, "notifications.border": PANE,
 "notificationCenterHeader.background": PANEL, "notificationsErrorIcon.foreground": ERR,
 "notificationsWarningIcon.foreground": WARN, "notificationsInfoIcon.foreground": ACCENT,
 "notificationLink.foreground": ACCENT,
 "breadcrumb.foreground": MUTED, "breadcrumb.focusForeground": FG, "breadcrumb.activeSelectionForeground": ACCENT,
 "breadcrumbPicker.background": SURFACE,
 "gitDecoration.addedResourceForeground": OK, "gitDecoration.modifiedResourceForeground": WARN,
 "gitDecoration.deletedResourceForeground": ERR, "gitDecoration.untrackedResourceForeground": OK,
 "gitDecoration.ignoredResourceForeground": INACTIVE, "gitDecoration.conflictingResourceForeground": MAGENTA,
 "gitDecoration.renamedResourceForeground": MIDNIGHT, "gitDecoration.submoduleResourceForeground": SECONDARY,
 "terminal.background": BG, "terminal.foreground": FG, "terminalCursor.foreground": ACCENT, "terminalCursor.background": ON_ACCENT,
 "terminal.selectionBackground": SEL, "terminal.selectionForeground": INK_HIGH, "terminal.border": HAIRLINE,
 "welcomePage.tileBackground": SURFACE, "welcomePage.tileHoverBackground": PANEL, "welcomePage.tileBorder": HAIRLINE,
 "walkThrough.embeddedEditorBackground": SURFACE,
 "settings.headerForeground": ACCENT, "settings.modifiedItemIndicator": WARN,
 "debugToolBar.background": SURFACE, "debugIcon.breakpointForeground": ERR,
 "charts.foreground": FG, "charts.lines": MUTED, "charts.red": ERR, "charts.blue": MIDNIGHT, "charts.yellow": WARN,
 "charts.orange": WARN, "charts.green": OK, "charts.purple": MAGENTA,
}
names = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
for i, n in enumerate(names):
    wb[f"terminal.ansi{n.capitalize()}"] = ANSI[i]
    wb[f"terminal.ansiBright{n.capitalize()}"] = ANSI[i + 8]
def t(name, scope, fg=None, style=None):
    s = {}
    if fg: s["foreground"] = fg
    if style is not None: s["fontStyle"] = style
    return {"name": name, "scope": scope, "settings": s}
tokens = [
 t("Comment", ["comment", "punctuation.definition.comment"], MUTED, "italic"),
 t("Keyword", ["keyword", "keyword.control", "storage", "storage.type", "storage.modifier"], ACCENT),
 t("Operator", ["keyword.operator", "punctuation.separator", "punctuation.terminator", "punctuation.accessor"], SECONDARY),
 t("Punctuation", ["punctuation", "meta.brace", "punctuation.definition.tag"], SECONDARY),
 t("String", ["string", "punctuation.definition.string", "string.quoted", "string.template"], OK),
 t("String escape", ["constant.character.escape", "string.regexp", "constant.other.character-class.regexp"], NEON),
 t("Number", ["constant.numeric", "constant.other.color", "keyword.other.unit"], WARN),
 t("Language constant", ["constant.language", "support.constant"], WARN),
 t("Constant", ["constant", "variable.other.constant", "variable.other.enummember"], WARN),
 t("Function", ["entity.name.function", "support.function", "meta.function-call entity.name.function", "variable.function"], MIDNIGHT),
 t("Type / class", ["entity.name.type", "entity.name.class", "support.type", "support.class", "entity.other.inherited-class",
                     "storage.type.class", "entity.name.namespace"], MAGENTA),
 t("Variable", ["variable", "variable.other.readwrite", "meta.definition.variable"], FG),
 t("Parameter", ["variable.parameter", "meta.parameter"], SECONDARY, "italic"),
 t("Property", ["variable.other.property", "variable.other.object.property", "support.variable.property",
                "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name"], SECONDARY),
 t("this / self", ["variable.language", "variable.language.this", "variable.language.self"], ERR, "italic"),
 t("Decorator", ["meta.decorator", "entity.name.function.decorator", "punctuation.decorator"], MAGENTA),
 t("Tag", ["entity.name.tag", "meta.tag.sgml"], ACCENT),
 t("Attribute", ["entity.other.attribute-name"], WARN, "italic"),
 t("CSS selector", ["entity.other.attribute-name.class.css", "entity.other.attribute-name.id.css",
                    "entity.name.tag.css"], MIDNIGHT),
 t("Invalid", ["invalid", "invalid.illegal"], ERR),
 t("Deprecated", ["invalid.deprecated"], WARN, "strikethrough"),
 t("Markdown heading", ["markup.heading", "markup.heading entity.name", "punctuation.definition.heading.markdown"], ACCENT, "bold"),
 t("Markdown bold", ["markup.bold"], INK_HIGH, "bold"),
 t("Markdown italic", ["markup.italic"], FG, "italic"),
 t("Markdown link", ["markup.underline.link", "string.other.link"], MIDNIGHT),
 t("Markdown code", ["markup.inline.raw", "markup.fenced_code", "markup.raw"], OK),
 t("Markdown quote", ["markup.quote"], SECONDARY, "italic"),
 t("Markdown list", ["punctuation.definition.list.begin.markdown", "beginning.punctuation.definition.list.markdown"], WARN),
 t("Diff inserted", ["markup.inserted"], OK), t("Diff deleted", ["markup.deleted"], ERR),
 t("Diff changed", ["markup.changed"], WARN), t("Diff header", ["meta.diff.header", "meta.diff.range"], ACCENT),
 t("JSON key", ["source.json meta.structure.dictionary.json support.type.property-name.json"], ACCENT),
 t("Shell variable", ["variable.other.normal.shell", "punctuation.definition.variable.shell"], WARN),
]
sem = {
 "namespace": MAGENTA, "type": MAGENTA, "class": MAGENTA, "enum": MAGENTA, "interface": MAGENTA, "struct": MAGENTA,
 "typeParameter": {"foreground": MAGENTA, "italic": True}, "parameter": {"foreground": SECONDARY, "italic": True},
 "variable": FG, "variable.readonly": WARN, "variable.defaultLibrary": WARN, "property": SECONDARY,
 "property.readonly": SECONDARY, "enumMember": WARN, "function": MIDNIGHT, "method": MIDNIGHT,
 "function.defaultLibrary": MIDNIGHT, "macro": NEON, "keyword": ACCENT, "comment": {"foreground": MUTED, "italic": True},
 "string": OK, "number": WARN, "regexp": NEON, "operator": SECONDARY, "decorator": MAGENTA, "label": WARN,
 "selfParameter": {"foreground": ERR, "italic": True}, "*.deprecated": {"strikethrough": True},
}
theme = {"$schema": "vscode://schemas/color-theme", "name": "HUDdy", "type": "dark", "semanticHighlighting": True,
         "colors": wb, "tokenColors": tokens, "semanticTokenColors": sem}
V = 'vscode/huddy-theme/'
w(V + 'themes/HUDdy-color-theme.json', json.dumps(theme, indent=2) + '\n')
pkg = {
 "name": "huddy-theme", "publisher": "davidprush", "displayName": "HUDdy",
 "description": "HUDdy: the dark heads-up-display theme from NuzeHub, Dirlume and SSHush",
 "version": "1.0.1", "license": "MIT", "author": {"name": "David Rush"},
 "homepage": "https://davidprush.com", "icon": "icon-huddy.png",
 "galleryBanner": {"color": BG, "theme": "dark"}, "engines": {"vscode": "^1.103.0"},
 "categories": ["Themes"], "keywords": ["theme", "dark theme", "hud", "huddy", "cyan", "terminal", "nuzehub", "color theme"],
 "contributes": {"themes": [{"label": "HUDdy", "uiTheme": "vs-dark", "path": "./themes/HUDdy-color-theme.json"}]},
}
w(V + 'package.json', json.dumps(pkg, indent=2) + '\n')
print('ok', len(wb), 'workbench colours,', len(tokens), 'token rules,', len(sem), 'semantic')
