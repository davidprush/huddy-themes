# ---- HUDdy for Ghostty 1.1 (any Mac; safe to paste again) ----
( set -e -o pipefail
echo "== HUDdy for Ghostty · pre-check (report only)"
TB=$( { /sbin/ifconfig bridge0 2>/dev/null || true; } | /usr/bin/awk '/status:/ {print $2}')
if [ "$TB" = "active" ]; then echo "docked: yes (Thunderbolt Bridge up)"; else echo "docked: no (Thunderbolt Bridge ${TB:-absent})"; fi
OLL=$( /usr/bin/curl -s -m 3 -o /dev/null -w '%{http_code}' http://127.0.0.1:11434/api/version || true )
if [ "$OLL" = "200" ]; then echo "Ollama: answering (not used by this theme)"; else echo "Ollama: not answering here (${OLL:-no reply}; not used by this theme)"; fi
echo "swap: $(/usr/sbin/sysctl -n vm.swapusage)"
WORK="${TMPDIR:-/tmp}"; WORK="${WORK%/}/huddy-themes-1.1"; /bin/mkdir -p "$WORK"
echo "working folder: $WORK"
cd "$WORK"
echo "== unpack and check"
/usr/bin/base64 -D <<'B64' | /usr/bin/gunzip -c > HUDdy.ghostty
H4sIAAAAAAAC/12STU7DMBCF9znFSN62+XF+nCB5RSXogg2FfRN7nEaEuIodRDeIQ3BCToLbRqrD
0t88vTdPHgKPrxt5AqVHeDhoY+0JkjCB3++febLTysK9HuxYGwu7IwoniEN42r6sYFN/dBKeJ3MI
AwLbwdi67+/gKwqFHlTXRu3VM7IHfEcTXSxX4F4D7C8M+DVnD90AJz3d1rg6hMGx7tHaszDmhGLK
ssxjCSdK5RmLPUY5SaVSdemx9KxrnNBjGSdFJqlSHss5EaxasoKTHDFZMMZJldZl47OSEyYdlR6r
zrklqxp/Z1eEMaUE9eGliWgY+tBVqSjGi+jEdZFlky6hK5Oi+qd0bWSBmaJBU4u3dtTTIB0ncRlj
UgXu1/EGBRVKikBMo9HjWuje3YTDc/UZW/y0noPBHoXt9LBeBiQZFan0xsuoeSlz7Du7lp07IvQS
KcuxkMEfi2YTIJwCAAA=
B64
print -r -- "30ce70c6eb8a918abfb3412e382b0b501d24db41db1bfd3b107dc76121f9aa06  HUDdy.ghostty" | /usr/bin/shasum -a 256 -c -
upd() {
  if [ -f "$1" ] && /usr/bin/cmp -s "$1" "$2"; then echo "$3: already set, nothing changed"; return 0; fi
  if [ -f "$1" ]; then BK="$1.huddy-backup.$(/bin/date +%Y%m%d-%H%M%S)"; /bin/cp -p "$1" "$BK"; echo "$3: backup $BK"; fi
  /bin/cat "$2" > "$1"; echo "$3: updated $1"
}
echo "== install the theme"
XDG="${XDG_CONFIG_HOME:-$HOME/.config}"
/bin/mkdir -p "$XDG/ghostty/themes"
if /usr/bin/cmp -s HUDdy.ghostty "$XDG/ghostty/themes/HUDdy"; then echo "theme file: already current"; else /usr/bin/install -m 644 HUDdy.ghostty "$XDG/ghostty/themes/HUDdy"; echo "theme file: $XDG/ghostty/themes/HUDdy"; fi
echo "== select it (one managed block at the end of your config; replaced, never duplicated)"
if [ -f "$XDG/ghostty/config.ghostty" ]; then CFG="$XDG/ghostty/config.ghostty"; else CFG="$XDG/ghostty/config"; fi
if [ -f "$CFG" ]; then /usr/bin/awk '/^# >>> huddy-theme >>>/ {s=1; next} /^# <<< huddy-theme <<</ {s=0; next} !s' "$CFG" > config.new; else : > config.new; fi
printf '%s\n' '# >>> huddy-theme >>> (HUDdy Themes 1.1; pasting the block again replaces this)' 'theme = HUDdy' '# <<< huddy-theme <<<' >> config.new
upd "$CFG" config.new "Ghostty config"
if /usr/bin/grep -q '^# >>> terminal-setup:ghostty >>>' "$CFG"; then
  echo "note: setup-terminal.sh comments out theme lines outside its block; if you re-run it, add --keep-ghostty-overrides (or paste this block again)"
fi
AS="$HOME/Library/Application Support/com.mitchellh.ghostty"
for f in "$AS/config.ghostty" "$AS/config"; do
  if [ -f "$f" ] && /usr/bin/grep -Eq '^[[:space:]]*theme[[:space:]]*=' "$f"; then echo "warning: $f loads later and sets a theme: $(/usr/bin/grep -E '^[[:space:]]*theme[[:space:]]*=' "$f" | /usr/bin/tail -1)"; fi
done
echo "== check with Ghostty itself"
GB=""; for g in "$(command -v ghostty || true)" /Applications/Ghostty.app/Contents/MacOS/ghostty "$HOME/Applications/Ghostty.app/Contents/MacOS/ghostty"; do [ -n "$g" ] && [ -x "$g" ] && { GB="$g"; break; }; done
if [ -n "$GB" ]; then
  if "$GB" +validate-config >/dev/null 2>&1; then echo "validate-config: OK"; else echo "validate-config reported (from your config, shown as is):"; "$GB" +validate-config || true; fi
  echo "Ghostty resolves: $("$GB" +show-config 2>/dev/null | /usr/bin/grep -E '^(theme|background) = ' | /usr/bin/tr '\n' ' ')"
else echo "Ghostty app not found; the theme is installed for when it is"; fi
echo "Done. In Ghostty press Cmd+Shift+, (Reload Configuration) or open a new window."
)
