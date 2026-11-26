# ---- HUDdy for Obsidian 1.1 (any Mac; asks which vault; safe to paste again) ----
( set -e -o pipefail
echo "== HUDdy for Obsidian · pre-check (report only)"
TB=$( { /sbin/ifconfig bridge0 2>/dev/null || true; } | /usr/bin/awk '/status:/ {print $2}')
if [ "$TB" = "active" ]; then echo "docked: yes (Thunderbolt Bridge up)"; else echo "docked: no (Thunderbolt Bridge ${TB:-absent})"; fi
OLL=$( /usr/bin/curl -s -m 3 -o /dev/null -w '%{http_code}' http://127.0.0.1:11434/api/version || true )
if [ "$OLL" = "200" ]; then echo "Ollama: answering (not used by this theme)"; else echo "Ollama: not answering here (${OLL:-no reply}; not used by this theme)"; fi
echo "swap: $(/usr/sbin/sysctl -n vm.swapusage)"
WORK="${TMPDIR:-/tmp}"; WORK="${WORK%/}/huddy-themes-1.1"; /bin/mkdir -p "$WORK"
echo "working folder: $WORK"
cd "$WORK"
echo "== unpack and check"
/usr/bin/base64 -D <<'B64' | /usr/bin/gunzip -c > obsidian-manifest.json
H4sIAAAAAAAC/6vmUlBQykvMTVWyUlDyCHVJqVTSAQmVpRYVZ+bngUQN9Qz1DCCiuZl5jgUFYchy
BjC5xNKSjPwikKBLYllmikJQaXEGskxoUQ5IMqOkpKDYSl8/BaSooAioSC85P1eJq5YLADr/PQ2L
AAAA
B64
print -r -- "7209eaaaa547d143020d2a731e19251fdc991be1f6cb6cd60b067638a749e8bd  obsidian-manifest.json" | /usr/bin/shasum -a 256 -c -
/usr/bin/base64 -D <<'B64' | /usr/bin/gunzip -c > obsidian-theme.css
H4sIAAAAAAAC/4VXS47jNhDd9ykIBIOkB5ZbkiV/epbpxWQxCJBJDkBRJYuwTDoU5W5jMEAOkRPm
JClStEyJcs+mjeZ7r1isH6mnj+TzXy/lhVRSkd+LlpecCpIsk2VM/vvnXwd+lZUmv0qhFW01+XoC
hpR4Sb789ueCvNAzL8kfXVsvHwjBf9WBSNFcnp24pi0RkjR8X2tyog1oDQvSymG7n1siX4UjMNnI
TrWEKiBdCyXhFbnIjrSvXLOa6KuhoyxhST4+PTwsdQ1HiEqz7zf0wFhQUcvM6jMxy59wNYr69YK2
EMXxM/kp3saQ7EIsNxhNsjQNsMTqymSXsgBLDZYkabLahpixiRbZqgywldUVKWRJiBlduslhHeoy
o8vijOWhL7nBctjE2yzA1gbblLsVDW1uDIbItqhmzm5AlrKqxA09VEEZqX3xTNI8X5BttiAYhU9j
AiqrKs82sb8uFRV78LTJNlmQTRJyrLxAvQ9doGnkqydP4xXaSNchyepZsQEf2isA0cvXuG/vwXob
UFC8KquKjhB2oU67wwOnaW4NTBk2C5BU42g2nTs0hhRlSRxoDQW166xMx9pTp07NVb3bocPZOlD3
JJOszW6q5+LgB3xl/kzUSLHx2m52hUs0ZQyEjmqzqUuPW2rtKT6M1hoM6PaDb7MHZqPhNIkpyjWk
FZsBU5MCqOKrUsObjqS4mfVbeQxGXJxBaVuBPosLDYoyzc8w711IiGqJpjxXLK+g7LBXshNldFL8
SNVlslNIiGijJ3PEI7XApCidnR9QnCV/6ng0HJG84oDlJFVpPffHzH3icFB/8rxDryTr2kn45ujO
LJYf/cXvmgWJl/H28b7QpeE9fZK9owelpJqMoDle22Gi23bS8JrrBgqqPMm05EJGH5S+7Lwkalpg
aQtNuYB3DCpeFFjCd/GS45WLBmyXeHm9NYCQ6kgbb2APyLHru8Ef8xao0Ck9uRssMNsfHhI0xoDP
Bd4CdyJtoFeqBBf7ycjvVdAAloIUd4ogTR89do3vBPtWiIq9E/i3jBGs4nsCV3N3dFn+6IJdJ0MS
/OjU6bDsD/F6NSz7566zYdk/c50Py36y6vWw7KeqkE05AOUasspdwlzThrMB8guiMdfBnP83YDa5
FsaQgRK0mT2pZXRCQSubM5Sz59N0P7u5WfdLf77hh9QZdj+InLFZ/iq/DohGssPfndQwkY0TGDaX
vZZqYIdCvs1qBhCH/MGzO35oljDp69FzEtHZ1rUIk8cjBD1qoaoTrjMmrwbEDnB5xZMG1y9C/HiS
SlNrc/xAQ1Ce8AbUQf1Z7KQMqi+zmPGlo86dAG616vt7/KpCBFM55+SZ9s8hv3b2ip5qDFUJky1u
gDeCfZMeod/Pd8MDqdaU1S7e81t7BT7JSc/BJoBJAbVMyaYxd4Wuu2NxG01BfV8vxJvCXYM/ENpC
//7w8GS/7PCDqWP4bqNE11yQfmAT4xjB8gOFy0B6wwQvJ0JFaZdc7PB7DZk1UKTary3/Y2uJVXVo
T5SBvdcci7fOUfKNmGZoa1qaFzgXLWgSkyg9veHPNSfk+z2bDdBqiXfz1dzyzOHV7WJt2+YtpNby
iK9QtIqpwC/R67Nlatl0JXqCz3YwJ8fD1TjMR5TPFyzqLy9ukyjBbeznKj4N0CVbtfhUSeFojP8P
YJRvETsPAAA=
B64
print -r -- "59778a9aa93efca4b138f5934758f8288c5c018691dc4ff8890d7708222ad9ef  obsidian-theme.css" | /usr/bin/shasum -a 256 -c -
upd() {
  if [ -f "$1" ] && /usr/bin/cmp -s "$1" "$2"; then echo "$3: already set, nothing changed"; return 0; fi
  if [ -f "$1" ]; then BK="$1.huddy-backup.$(/bin/date +%Y%m%d-%H%M%S)"; /bin/cp -p "$1" "$BK"; echo "$3: backup $BK"; fi
  /bin/cat "$2" > "$1"; echo "$3: updated $1"
}
echo "== which vault?"
VAULTS=$(/usr/bin/osascript -l JavaScript -e 'function run() { ObjC.import("Foundation");
  const h = $.NSProcessInfo.processInfo.environment.objectForKey("HOME").js;
  const s = $.NSString.stringWithContentsOfFileEncodingError(h + "/Library/Application Support/obsidian/obsidian.json", 4, null);
  if (s.isNil()) return ""; return Object.values(JSON.parse(s.js).vaults || {}).map(v => v.path).join("\n"); }' 2>/dev/null || true)
LIST=("${(@f)VAULTS}"); [ -n "$VAULTS" ] || LIST=()
ANS="${HUDDY_VAULT:-}"
if [ -z "$ANS" ]; then
  if [ ${#LIST} -gt 0 ]; then echo "Vaults Obsidian knows on this Mac:"; i=1; for v in "${LIST[@]}"; do echo "  $i) $v"; i=$((i+1)); done
    PROMPT="Vault number(s), 'all', or a vault folder path [1]: "
  else echo "No vault list found."; PROMPT="Full path of your vault folder: "; fi
  [ -r /dev/tty ] || { echo "No terminal to ask on; run again with HUDDY_VAULT=/path/to/vault"; exit 1; }
  read -r "ANS?$PROMPT" < /dev/tty
  [ -n "$ANS" ] || ANS=1
fi
TARGETS=()
if [ "$ANS" = "all" ]; then TARGETS=("${LIST[@]}")
elif [[ "$ANS" =~ '^[0-9]+( [0-9]+)*$' ]]; then for n in ${=ANS}; do [ "$n" -ge 1 ] && [ "$n" -le ${#LIST} ] || { echo "no vault number $n"; exit 1; }; TARGETS+=("${LIST[$n]}"); done
else TARGETS=("${ANS/#\~/$HOME}"); fi
RUN=0; /usr/bin/pgrep -qx Obsidian && RUN=1
for V in "${TARGETS[@]}"; do
  echo "== vault: $V"
  [ -d "$V/.obsidian" ] || { echo "not an Obsidian vault (no .obsidian folder): $V"; exit 1; }
  T="$V/.obsidian/themes/HUDdy"; /bin/mkdir -p "$T"
  /usr/bin/install -m 644 obsidian-manifest.json "$T/manifest.json"; /usr/bin/install -m 644 obsidian-theme.css "$T/theme.css"
  echo "theme files: $T"
  if [ $RUN -eq 1 ]; then echo "Obsidian is open: choose it in Settings > Appearance > Themes > HUDdy"
  else
    /usr/bin/osascript -l JavaScript -e 'function run(a) { ObjC.import("Foundation");
      const s = $.NSString.stringWithContentsOfFileEncodingError(a[0], 4, null);
      const j = s.isNil() ? {} : JSON.parse(s.js); j.cssTheme = "HUDdy"; if (!j.theme) j.theme = "obsidian";
      $(JSON.stringify(j, null, 2)).writeToFileAtomicallyEncodingError(a[1], true, 4, null);
      return j.theme; }' "$V/.obsidian/appearance.json" "$WORK/appearance.new" > appearance.base
    upd "$V/.obsidian/appearance.json" "$WORK/appearance.new" "appearance.json"
    case "$(/bin/cat appearance.base)" in obsidian) ;; *) echo "note: Base color scheme is not Dark; HUDdy is dark only, so set Settings > Appearance > Base color scheme > Dark";; esac
  fi
done
echo "Done. Open the vault; HUDdy is under Settings > Appearance > Themes."
)
