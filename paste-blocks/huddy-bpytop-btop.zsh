# ---- HUDdy for bpytop (and btop) 1.1 (any Mac; safe to paste again) ----
( set -e -o pipefail
echo "== HUDdy for bpytop / btop · pre-check (report only)"
TB=$( { /sbin/ifconfig bridge0 2>/dev/null || true; } | /usr/bin/awk '/status:/ {print $2}')
if [ "$TB" = "active" ]; then echo "docked: yes (Thunderbolt Bridge up)"; else echo "docked: no (Thunderbolt Bridge ${TB:-absent})"; fi
OLL=$( /usr/bin/curl -s -m 3 -o /dev/null -w '%{http_code}' http://127.0.0.1:11434/api/version || true )
if [ "$OLL" = "200" ]; then echo "Ollama: answering (not used by this theme)"; else echo "Ollama: not answering here (${OLL:-no reply}; not used by this theme)"; fi
echo "swap: $(/usr/sbin/sysctl -n vm.swapusage)"
WORK="${TMPDIR:-/tmp}"; WORK="${WORK%/}/huddy-themes-1.1"; /bin/mkdir -p "$WORK"
echo "working folder: $WORK"
cd "$WORK"
echo "== unpack and check"
/usr/bin/base64 -D <<'B64' | /usr/bin/gunzip -c > bpytop-huddy.theme
H4sIAAAAAAAC/5VUy47aMBTd8xUWbFoJ0SSERxddtIOqmcVUozKsqgo59jWxJokjx2GGXT+iX9gv
qe04xJmwgAVIvuccn2ufG0/udxt6QiqFHBATEiXlSYkShbMQ/fvzFzXwVjCF7kShJK4U2pZANCGY
oceH5yna4COn6GddpbPRaPKIeYESTF4OUtQFHdmdf+W6uk8Ov7+MJ8E6gPDzuKUqeFM+iVkSiQij
xJC+iTekuMqgciy7MJwFQMiY4dzzQ5rpnwKKXuCEMlAKZCtIuduUsWQRr4xgCxkQwy6lIFBVSIpX
x64c5LoN44jM6UWN1/lZ1Bh1nT0UmCh+BPQJ1UVdafVB4jL1tdxRnDYOYrKwJ39yPom+gZwXHJGy
buRTva6I05t29mZt1HPKGF4b9d3TzipFrTJegCPrLfa6ao1WGJPI5gC5kKcL7BzyIfsHqAvUAtSQ
6p+gT7dND/gma8r1NHXh6eXe6AwxWi1gabN4hrwEiVUtwV2o/qccCoU+VApLZW6IThEU9GM7Nlqy
t5jZahnTyCTkYVrgD4mH6F0aRANBe7d1hQ9Xm5trP3u3GXXQRWsDDJy/SwCUN3ld6c20pDMP8RLH
eOxjjXuv5Hy9acIk1cN7mzOxos47wou1ya+H9t1d0fm3KY0mX4+YZzjJbj08bnVe9OuYRPPxgNBv
pKufM2gfj111802YL9/vIFrMzx1YrG9uS4PsN+K1yASm15pSx/cCcB/QO9yNX/tqvUNdHxhY0GSx
K2/poi77PfQH0KGug/6X4TDnv1oxZl6J/x3ueBixBgAA
B64
print -r -- "ac75c676351ee526121491cc0aa425ebc4afbb6d0cbef16160c222d10acd99f8  bpytop-huddy.theme" | /usr/bin/shasum -a 256 -c -
/usr/bin/base64 -D <<'B64' | /usr/bin/gunzip -c > btop-huddy.theme
H4sIAAAAAAAC/5VVTY/aMBC98yssuLQSoiSEjz300C5qdw9Uq7Kcqgo59phYmy8lDrvc+iP6C/eX
1OM4xAEqwQEk+703bzwzdgYPmyU/EBVBAkRkBQlVlhNv5JH3P39JDa4zoch9lqqCloqsc2CaMB6R
1ePzkCzpXnLysyqjUa83WFGZkpCyl12RVSnvmbi/Er27DXe/P/cH48UYvLt+Q1XwplySMCTmM8EZ
kr5mb0RJFUNpWWaBnCmAJwRyHuQuivVPAScvcCAxKAVFI4ikDSpEOA3mKFhDDAzZeZExKEtSZK+W
XVrIZusFPpvwixon86OoNmoze0wpU3IP5BOp0qrU6l1B88jVSkux2mAcsKk5+XfDjGkIcUloygmX
SaIjoJZ8wC59tCFMzC3uY4Q5v5tQk/IKdBmcZnRVCaLNMUMfAg81T/Z0oa57IlNJWF7VSQ/1umRW
jEXY4hrVEy4EXaD6/mljlFmlYpmCJesQW71rjjenlPl1cklWHC6wE0jO2T9AXaCmoM6p7gm6dJP0
GR8njEs9w+3I6OUWdUj051OYmXI+Q5JDQVVVgG2j/ucSUt2OUtFCYYX4kEDKmxorLdkaDEPNAu7j
XDiYFrij6SA6So1oYNzUtirp7mpzLPvRu+lRC120RuDM+VsBQJK6X1d6Cy1pzT06owHtu1jt3tmy
vs40URbpgb/NmRlR6+3T6QL710G77nbT+jdd6g2+7KnU9y++9fC00TmtXwTMn/TPCN1E2v1jD5on
a1PeXAl8b9wM/OnkmIHBuuZm66z3y+w1jTPKrzXllu80wF6gE9yOX/NWnqA2DwpiXPdik9+SRZV3
c+gOoEVtBt2bYTHrP58L0X1V8Dm86Rbaz8X/bmIDX7yNDXjSlX8pRVMvswcAAA==
B64
print -r -- "26701c17af27655f91a0bb1fe88b2fe829cb5ef419b252bb567613bdf380ddb4  btop-huddy.theme" | /usr/bin/shasum -a 256 -c -
upd() {
  if [ -f "$1" ] && /usr/bin/cmp -s "$1" "$2"; then echo "$3: already set, nothing changed"; return 0; fi
  if [ -f "$1" ]; then BK="$1.huddy-backup.$(/bin/date +%Y%m%d-%H%M%S)"; /bin/cp -p "$1" "$BK"; echo "$3: backup $BK"; fi
  /bin/cat "$2" > "$1"; echo "$3: updated $1"
}
echo "== bpytop"
BD="$HOME/.config/bpytop"; /bin/mkdir -p "$BD/themes"
/usr/bin/install -m 644 bpytop-huddy.theme "$BD/themes/huddy.theme"; echo "theme file: $BD/themes/huddy.theme"
if [ -x /opt/homebrew/bin/bpytop ] || command -v bpytop >/dev/null; then echo "bpytop: installed"; else echo "bpytop: not installed (brew install bpytop); the theme is ready for it"; fi
if /usr/bin/pgrep -qf '[b]in/bpytop'; then
  echo "bpytop is running: quit it (press q), then paste this block again to set color_theme"
else
  if [ -f "$BD/bpytop.conf" ]; then
    if /usr/bin/grep -q '^color_theme=' "$BD/bpytop.conf"; then /usr/bin/sed 's/^color_theme=.*/color_theme="+huddy"/' "$BD/bpytop.conf" > bpytop.conf.new
    else { /bin/cat "$BD/bpytop.conf"; echo 'color_theme="+huddy"'; } > bpytop.conf.new; fi
  else printf '%s\n' '#? Config file for bpytop (started by HUDdy Themes 1.1; bpytop fills in the rest)' 'color_theme="+huddy"' > bpytop.conf.new; fi
  upd "$BD/bpytop.conf" bpytop.conf.new "bpytop.conf"
fi
echo "== btop (only if btop is installed or configured)"
TD="${XDG_CONFIG_HOME:-$HOME/.config}/btop"
if [ -x /opt/homebrew/bin/btop ] || command -v btop >/dev/null || [ -d "$TD" ]; then
  /bin/mkdir -p "$TD/themes"; /usr/bin/install -m 644 btop-huddy.theme "$TD/themes/huddy.theme"; echo "theme file: $TD/themes/huddy.theme"
  if /usr/bin/pgrep -qx btop; then echo "btop is running: quit it (press q), then paste this block again to set color_theme"
  else
    if [ -f "$TD/btop.conf" ]; then
      if /usr/bin/grep -Eq '^color_theme[[:space:]]*=' "$TD/btop.conf"; then /usr/bin/sed -E 's/^color_theme[[:space:]]*=.*/color_theme = "huddy"/' "$TD/btop.conf" > btop.conf.new
      else { /bin/cat "$TD/btop.conf"; echo 'color_theme = "huddy"'; } > btop.conf.new; fi
    else printf '%s\n' 'color_theme = "huddy"' > btop.conf.new; fi
    upd "$TD/btop.conf" btop.conf.new "btop.conf"
  fi
else echo "btop: not installed, skipped (brew install btop, then paste again)"; fi
echo "Done. Start bpytop (or btop); the HUDdy colours show at once. Menu (m) > Options > color_theme lists it as +huddy."
)
