"""Build the HUDdy paste blocks: each embeds its files as gzip+base64 (decoded with macOS `base64 -D`)."""
import base64, gzip, hashlib, os, textwrap
P = '/workspace/huddy-1.1-src/pack'; OUT = os.path.join(P, 'paste-blocks'); os.makedirs(OUT, exist_ok=True)
def emb(path, dest):
    raw = open(path, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    b = base64.b64encode(gzip.compress(raw, 9, mtime=0)).decode()
    lines = '\n'.join(textwrap.wrap(b, 76))
    return (f"/usr/bin/base64 -D <<'B64' | /usr/bin/gunzip -c > {dest}\n{lines}\nB64\n"
            f"print -r -- \"{sha}  {dest}\" | /usr/bin/shasum -a 256 -c -\n"), sha

PRE = r'''echo "== HUDdy for @APP@ · pre-check (report only)"
TB=$( { /sbin/ifconfig bridge0 2>/dev/null || true; } | /usr/bin/awk '/status:/ {print $2}')
if [ "$TB" = "active" ]; then echo "docked: yes (Thunderbolt Bridge up)"; else echo "docked: no (Thunderbolt Bridge ${TB:-absent})"; fi
OLL=$( /usr/bin/curl -s -m 3 -o /dev/null -w '%{http_code}' http://127.0.0.1:11434/api/version || true )
if [ "$OLL" = "200" ]; then echo "Ollama: answering (not used by this theme)"; else echo "Ollama: not answering here (${OLL:-no reply}; not used by this theme)"; fi
echo "swap: $(/usr/sbin/sysctl -n vm.swapusage)"
WORK="${TMPDIR:-/tmp}"; WORK="${WORK%/}/huddy-themes-1.1"; /bin/mkdir -p "$WORK"
echo "working folder: $WORK"
cd "$WORK"
'''
# shared helper: write $2 over $1 only if different, backing $1 up first. Keeps symlinks and permissions (cat >).
UPD = r'''upd() {
  if [ -f "$1" ] && /usr/bin/cmp -s "$1" "$2"; then echo "$3: already set, nothing changed"; return 0; fi
  if [ -f "$1" ]; then BK="$1.huddy-backup.$(/bin/date +%Y%m%d-%H%M%S)"; /bin/cp -p "$1" "$BK"; echo "$3: backup $BK"; fi
  /bin/cat "$2" > "$1"; echo "$3: updated $1"
}
'''

def ghostty():
    e, sha = emb(f'{P}/ghostty/HUDdy', 'HUDdy.ghostty')
    return f'''# ---- HUDdy for Ghostty 1.1 (any Mac; safe to paste again) ----
( set -e -o pipefail
{PRE.replace('@APP@','Ghostty')}echo "== unpack and check"
{e}{UPD}echo "== install the theme"
XDG="${{XDG_CONFIG_HOME:-$HOME/.config}}"
/bin/mkdir -p "$XDG/ghostty/themes"
if /usr/bin/cmp -s HUDdy.ghostty "$XDG/ghostty/themes/HUDdy"; then echo "theme file: already current"; else /usr/bin/install -m 644 HUDdy.ghostty "$XDG/ghostty/themes/HUDdy"; echo "theme file: $XDG/ghostty/themes/HUDdy"; fi
echo "== select it (one managed block at the end of your config; replaced, never duplicated)"
if [ -f "$XDG/ghostty/config.ghostty" ]; then CFG="$XDG/ghostty/config.ghostty"; else CFG="$XDG/ghostty/config"; fi
if [ -f "$CFG" ]; then /usr/bin/awk '/^# >>> huddy-theme >>>/ {{s=1; next}} /^# <<< huddy-theme <<</ {{s=0; next}} !s' "$CFG" > config.new; else : > config.new; fi
printf '%s\\n' '# >>> huddy-theme >>> (HUDdy Themes 1.1; pasting the block again replaces this)' 'theme = HUDdy' '# <<< huddy-theme <<<' >> config.new
upd "$CFG" config.new "Ghostty config"
if /usr/bin/grep -q '^# >>> terminal-setup:ghostty >>>' "$CFG"; then
  echo "note: setup-terminal.sh comments out theme lines outside its block; if you re-run it, add --keep-ghostty-overrides (or paste this block again)"
fi
AS="$HOME/Library/Application Support/com.mitchellh.ghostty"
for f in "$AS/config.ghostty" "$AS/config"; do
  if [ -f "$f" ] && /usr/bin/grep -Eq '^[[:space:]]*theme[[:space:]]*=' "$f"; then echo "warning: $f loads later and sets a theme: $(/usr/bin/grep -E '^[[:space:]]*theme[[:space:]]*=' "$f" | /usr/bin/tail -1)"; fi
done
echo "== check with Ghostty itself"
GB=""; for g in "$(command -v ghostty || true)" /Applications/Ghostty.app/Contents/MacOS/ghostty "$HOME/Applications/Ghostty.app/Contents/MacOS/ghostty"; do [ -n "$g" ] && [ -x "$g" ] && {{ GB="$g"; break; }}; done
if [ -n "$GB" ]; then
  if "$GB" +validate-config >/dev/null 2>&1; then echo "validate-config: OK"; else echo "validate-config reported (from your config, shown as is):"; "$GB" +validate-config || true; fi
  echo "Ghostty resolves: $("$GB" +show-config 2>/dev/null | /usr/bin/grep -E '^(theme|background) = ' | /usr/bin/tr '\\n' ' ')"
else echo "Ghostty app not found; the theme is installed for when it is"; fi
echo "Done. In Ghostty press Cmd+Shift+, (Reload Configuration) or open a new window."
)
''', sha

def tops():
    e1, s1 = emb(f'{P}/bpytop/huddy.theme', 'bpytop-huddy.theme')
    e2, s2 = emb(f'{P}/btop/huddy.theme', 'btop-huddy.theme')
    return f'''# ---- HUDdy for bpytop (and btop) 1.1 (any Mac; safe to paste again) ----
( set -e -o pipefail
{PRE.replace('@APP@','bpytop / btop')}echo "== unpack and check"
{e1}{e2}{UPD}echo "== bpytop"
BD="$HOME/.config/bpytop"; /bin/mkdir -p "$BD/themes"
/usr/bin/install -m 644 bpytop-huddy.theme "$BD/themes/huddy.theme"; echo "theme file: $BD/themes/huddy.theme"
if [ -x /opt/homebrew/bin/bpytop ] || command -v bpytop >/dev/null; then echo "bpytop: installed"; else echo "bpytop: not installed (brew install bpytop); the theme is ready for it"; fi
if /usr/bin/pgrep -qf '[b]in/bpytop'; then
  echo "bpytop is running: quit it (press q), then paste this block again to set color_theme"
else
  if [ -f "$BD/bpytop.conf" ]; then
    if /usr/bin/grep -q '^color_theme=' "$BD/bpytop.conf"; then /usr/bin/sed 's/^color_theme=.*/color_theme="+huddy"/' "$BD/bpytop.conf" > bpytop.conf.new
    else {{ /bin/cat "$BD/bpytop.conf"; echo 'color_theme="+huddy"'; }} > bpytop.conf.new; fi
  else printf '%s\\n' '#? Config file for bpytop (started by HUDdy Themes 1.1; bpytop fills in the rest)' 'color_theme="+huddy"' > bpytop.conf.new; fi
  upd "$BD/bpytop.conf" bpytop.conf.new "bpytop.conf"
fi
echo "== btop (only if btop is installed or configured)"
TD="${{XDG_CONFIG_HOME:-$HOME/.config}}/btop"
if [ -x /opt/homebrew/bin/btop ] || command -v btop >/dev/null || [ -d "$TD" ]; then
  /bin/mkdir -p "$TD/themes"; /usr/bin/install -m 644 btop-huddy.theme "$TD/themes/huddy.theme"; echo "theme file: $TD/themes/huddy.theme"
  if /usr/bin/pgrep -qx btop; then echo "btop is running: quit it (press q), then paste this block again to set color_theme"
  else
    if [ -f "$TD/btop.conf" ]; then
      if /usr/bin/grep -Eq '^color_theme[[:space:]]*=' "$TD/btop.conf"; then /usr/bin/sed -E 's/^color_theme[[:space:]]*=.*/color_theme = "huddy"/' "$TD/btop.conf" > btop.conf.new
      else {{ /bin/cat "$TD/btop.conf"; echo 'color_theme = "huddy"'; }} > btop.conf.new; fi
    else printf '%s\\n' 'color_theme = "huddy"' > btop.conf.new; fi
    upd "$TD/btop.conf" btop.conf.new "btop.conf"
  fi
else echo "btop: not installed, skipped (brew install btop, then paste again)"; fi
echo "Done. Start bpytop (or btop); the HUDdy colours show at once. Menu (m) > Options > color_theme lists it as +huddy."
)
''', (s1, s2)

def obsidian():
    e1, s1 = emb(f'{P}/obsidian/HUDdy/manifest.json', 'obsidian-manifest.json')
    e2, s2 = emb(f'{P}/obsidian/HUDdy/theme.css', 'obsidian-theme.css')
    return f'''# ---- HUDdy for Obsidian 1.1 (any Mac; asks which vault; safe to paste again) ----
( set -e -o pipefail
{PRE.replace('@APP@','Obsidian')}echo "== unpack and check"
{e1}{e2}{UPD}echo "== which vault?"
VAULTS=$(/usr/bin/osascript -l JavaScript -e 'function run() {{ ObjC.import("Foundation");
  const h = $.NSProcessInfo.processInfo.environment.objectForKey("HOME").js;
  const s = $.NSString.stringWithContentsOfFileEncodingError(h + "/Library/Application Support/obsidian/obsidian.json", 4, null);
  if (s.isNil()) return ""; return Object.values(JSON.parse(s.js).vaults || {{}}).map(v => v.path).join("\\n"); }}' 2>/dev/null || true)
LIST=("${{(@f)VAULTS}}"); [ -n "$VAULTS" ] || LIST=()
ANS="${{HUDDY_VAULT:-}}"
if [ -z "$ANS" ]; then
  if [ ${{#LIST}} -gt 0 ]; then echo "Vaults Obsidian knows on this Mac:"; i=1; for v in "${{LIST[@]}}"; do echo "  $i) $v"; i=$((i+1)); done
    PROMPT="Vault number(s), 'all', or a vault folder path [1]: "
  else echo "No vault list found."; PROMPT="Full path of your vault folder: "; fi
  [ -r /dev/tty ] || {{ echo "No terminal to ask on; run again with HUDDY_VAULT=/path/to/vault"; exit 1; }}
  read -r "ANS?$PROMPT" < /dev/tty
  [ -n "$ANS" ] || ANS=1
fi
TARGETS=()
if [ "$ANS" = "all" ]; then TARGETS=("${{LIST[@]}}")
elif [[ "$ANS" =~ '^[0-9]+( [0-9]+)*$' ]]; then for n in ${{=ANS}}; do [ "$n" -ge 1 ] && [ "$n" -le ${{#LIST}} ] || {{ echo "no vault number $n"; exit 1; }}; TARGETS+=("${{LIST[$n]}}"); done
else TARGETS=("${{ANS/#\\~/$HOME}}"); fi
RUN=0; /usr/bin/pgrep -qx Obsidian && RUN=1
for V in "${{TARGETS[@]}}"; do
  echo "== vault: $V"
  [ -d "$V/.obsidian" ] || {{ echo "not an Obsidian vault (no .obsidian folder): $V"; exit 1; }}
  T="$V/.obsidian/themes/HUDdy"; /bin/mkdir -p "$T"
  /usr/bin/install -m 644 obsidian-manifest.json "$T/manifest.json"; /usr/bin/install -m 644 obsidian-theme.css "$T/theme.css"
  echo "theme files: $T"
  if [ $RUN -eq 1 ]; then echo "Obsidian is open: choose it in Settings > Appearance > Themes > HUDdy"
  else
    /usr/bin/osascript -l JavaScript -e 'function run(a) {{ ObjC.import("Foundation");
      const s = $.NSString.stringWithContentsOfFileEncodingError(a[0], 4, null);
      const j = s.isNil() ? {{}} : JSON.parse(s.js); j.cssTheme = "HUDdy"; if (!j.theme) j.theme = "obsidian";
      $(JSON.stringify(j, null, 2)).writeToFileAtomicallyEncodingError(a[1], true, 4, null);
      return j.theme; }}' "$V/.obsidian/appearance.json" "$WORK/appearance.new" > appearance.base
    upd "$V/.obsidian/appearance.json" "$WORK/appearance.new" "appearance.json"
    case "$(/bin/cat appearance.base)" in obsidian) ;; *) echo "note: Base color scheme is not Dark; HUDdy is dark only, so set Settings > Appearance > Base color scheme > Dark";; esac
  fi
done
echo "Done. Open the vault; HUDdy is under Settings > Appearance > Themes."
)
''', (s1, s2)

def vscode():
    e, sha = emb(f'{P}/vscode/huddy-theme-1.0.1.vsix', 'huddy-theme-1.0.1.vsix')
    return f'''# ---- HUDdy for VS Code 1.0.1 (any Mac; installs the .vsix locally; safe to paste again) ----
( set -e -o pipefail
{PRE.replace('@APP@','VS Code')}echo "== unpack and check"
{e}echo "== find VS Code's code command"
CODE="${{CODE_BIN:-}}"
if [ -z "$CODE" ]; then for c in "$(command -v code || true)" "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" "$HOME/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"; do [ -n "$c" ] && [ -x "$c" ] && {{ CODE="$c"; break; }}; done; fi
if [ -z "$CODE" ]; then
  echo "VS Code not found. Install it, or in VS Code use Extensions > ... > Install from VSIX... and pick:"
  echo "  $WORK/huddy-theme-1.0.1.vsix"; exit 1
fi
echo "code: $CODE"
echo "== install"
"$CODE" --install-extension "$WORK/huddy-theme-1.0.1.vsix" --force 2>/dev/null
"$CODE" --list-extensions --show-versions 2>/dev/null | /usr/bin/grep -x 'davidprush.huddy-theme@1.0.1'
echo "Done. In VS Code: Cmd+K Cmd+T, pick HUDdy."
echo "The same .vsix is what you upload to the Marketplace (update the existing 1.0.0 listing): $WORK/huddy-theme-1.0.1.vsix"
echo "(show it in Finder: open -R \\"$WORK/huddy-theme-1.0.1.vsix\\")"
)
''', sha

shas = {}
for name, fn in [('ghostty', ghostty), ('bpytop-btop', tops), ('obsidian', obsidian), ('vscode', vscode)]:
    text, s = fn(); shas[name] = s
    open(os.path.join(OUT, f'huddy-{name}.zsh'), 'w').write(text)
print(shas)
