#!/bin/zsh
# Tests the HUDdy paste blocks with scratch HOMEs (never the real ~). Each block runs twice (idempotency).
# Interactive zsh (-i, history expansion on) reads each block from stdin, as a paste would.
setopt pipefail
B=${0:A:h}; T=$HOME/huddy-work/blocktest; rm -rf $T; mkdir -p $T
VSC="$HOME/huddy-work/apps/Visual Studio Code.app/Contents/Resources/app/bin/code"
G=/Applications/Ghostty.app/Contents/MacOS/ghostty
pass=0; fail=0
ok() { if eval "$2"; then echo "PASS $1"; pass=$((pass+1)); else echo "FAIL $1  [$2]"; fail=$((fail+1)); fi }
paste() { local h=$1 blk=$2; shift 2; env -i HOME=$h TMPDIR=$h/tmp/ PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin USER=$USER LOGNAME=$USER "$@" /bin/zsh -f -i -o interactivecomments < $B/$blk 2>&1; }
newhome() { mkdir -p $T/$1/tmp; echo $T/$1; }

echo "### Ghostty: fresh home"
H=$(newhome g1); paste $H huddy-ghostty.zsh > $T/g1-run1.log; paste $H huddy-ghostty.zsh > $T/g1-run2.log
ok "g1 theme file" "cmp -s $B/../ghostty/HUDdy $H/.config/ghostty/themes/HUDdy"
ok "g1 one theme line" "[ \$(grep -c '^theme = HUDdy' $H/.config/ghostty/config) = 1 ]"
ok "g1 run2 unchanged" "grep -q 'already set, nothing changed' $T/g1-run2.log && grep -q 'theme file: already current' $T/g1-run2.log"
ok "g1 no backups on fresh" "[ \$(ls $H/.config/ghostty | grep -c huddy-backup) = 0 ]"
ok "g1 ghostty resolves HUDdy" "grep -q 'Ghostty resolves: theme = HUDdy background = #080e19' $T/g1-run2.log"
ok "g1 validate OK" "grep -q 'validate-config: OK' $T/g1-run1.log"
echo "### Ghostty: existing terminal-setup config (GitHub Dark, no trailing newline)"
H=$(newhome g2); mkdir -p $H/.config/ghostty; printf '# >>> terminal-setup:ghostty >>>\ntheme = GitHub Dark\nfont-size = 14\n# <<< terminal-setup:ghostty <<<\nmacos-option-as-alt = left' > $H/.config/ghostty/config
paste $H huddy-ghostty.zsh > $T/g2-run1.log; paste $H huddy-ghostty.zsh > $T/g2-run2.log; paste $H huddy-ghostty.zsh > $T/g2-run3.log
ok "g2 one backup only" "[ \$(ls $H/.config/ghostty | grep -c huddy-backup) = 1 ]"
ok "g2 last line kept intact" "grep -qx 'macos-option-as-alt = left' $H/.config/ghostty/config"
ok "g2 one HUDdy line" "[ \$(grep -c '^theme = HUDdy' $H/.config/ghostty/config) = 1 ]"
ok "g2 managed block untouched" "grep -qx 'theme = GitHub Dark' $H/.config/ghostty/config"
ok "g2 resolves HUDdy over GitHub Dark" "grep -q 'Ghostty resolves: theme = HUDdy' $T/g2-run3.log"
ok "g2 setup-terminal note" "grep -q 'keep-ghostty-overrides' $T/g2-run1.log"
echo "### Ghostty: config.ghostty preferred, App Support warning"
H=$(newhome g3); mkdir -p $H/.config/ghostty "$H/Library/Application Support/com.mitchellh.ghostty"; echo 'font-size = 13' > $H/.config/ghostty/config.ghostty; echo 'theme = Dracula' > "$H/Library/Application Support/com.mitchellh.ghostty/config"
paste $H huddy-ghostty.zsh > $T/g3-run1.log
ok "g3 wrote config.ghostty" "grep -q '^theme = HUDdy' $H/.config/ghostty/config.ghostty && [ ! -f $H/.config/ghostty/config ]"
ok "g3 warns about App Support theme" "grep -q 'loads later and sets a theme: theme = Dracula' $T/g3-run1.log"

echo "### bpytop/btop: fresh home"
H=$(newhome b1); paste $H huddy-bpytop-btop.zsh > $T/b1-run1.log; paste $H huddy-bpytop-btop.zsh > $T/b1-run2.log
ok "b1 bpytop theme" "cmp -s $B/../bpytop/huddy.theme $H/.config/bpytop/themes/huddy.theme"
ok "b1 btop theme" "cmp -s $B/../btop/huddy.theme $H/.config/btop/themes/huddy.theme"
ok "b1 bpytop.conf" "grep -qx 'color_theme=\"+huddy\"' $H/.config/bpytop/bpytop.conf"
ok "b1 btop.conf" "grep -qx 'color_theme = \"huddy\"' $H/.config/btop/btop.conf"
ok "b1 run2 unchanged x2" "[ \$(grep -c 'already set, nothing changed' $T/b1-run2.log) = 2 ]"
echo "### bpytop/btop: existing confs"
H=$(newhome b2); mkdir -p $H/.config/bpytop $H/.config/btop; printf '#? Config file for bpytop v. 1.0.68\ncolor_theme="Default"\ntheme_background=True\n' > $H/.config/bpytop/bpytop.conf; printf 'color_theme = "Default"\ntheme_background = true\n' > $H/.config/btop/btop.conf
paste $H huddy-bpytop-btop.zsh > $T/b2-run1.log; paste $H huddy-bpytop-btop.zsh > $T/b2-run2.log
ok "b2 bpytop replaced in place" "[ \$(grep -c '^color_theme=' $H/.config/bpytop/bpytop.conf) = 1 ] && grep -qx 'color_theme=\"+huddy\"' $H/.config/bpytop/bpytop.conf && grep -qx 'theme_background=True' $H/.config/bpytop/bpytop.conf"
ok "b2 btop replaced in place" "[ \$(grep -c '^color_theme' $H/.config/btop/btop.conf) = 1 ] && grep -qx 'color_theme = \"huddy\"' $H/.config/btop/btop.conf"
ok "b2 one backup each" "[ \$(ls $H/.config/bpytop | grep -c huddy-backup) = 1 ] && [ \$(ls $H/.config/btop | grep -c huddy-backup) = 1 ]"
echo "### bpytop really loads it from the written conf (HOME=b1, 3 s run in a pty)"
H=$T/b1; ( cd $H && HOME=$H script -q /dev/null /usr/bin/perl -e 'alarm 4; exec @ARGV' /opt/homebrew/bin/bpytop >/dev/null 2>&1 || true )
ok "b1 bpytop no theme error" "! grep -qi 'theme' $H/.config/bpytop/error.log 2>/dev/null"

echo "### Obsidian: two known vaults, answer 2 at the prompt (pty), then HUDDY_VAULT=all"
H=$(newhome o1); mkdir -p "$H/Library/Application Support/obsidian" $H/Notes/A/.obsidian "$H/Notes/B Vault/.obsidian"
printf '{"vaults":{"aaa":{"path":"%s","ts":1,"open":true},"bbb":{"path":"%s","ts":2}}}' "$H/Notes/A" "$H/Notes/B Vault" > "$H/Library/Application Support/obsidian/obsidian.json"
echo '{"theme":"moonstone","baseFontSize":15}' > "$H/Notes/B Vault/.obsidian/appearance.json"
(sleep 3; printf '2\n'; sleep 4) | env -i HOME=$H TMPDIR=$H/tmp/ PATH=/usr/bin:/bin:/usr/sbin:/sbin script -q /dev/null /bin/zsh -f -o interactivecomments $B/huddy-obsidian.zsh > $T/o1-run1.log 2>&1
ok "o1 prompt listed vaults" "grep -q '2) $H/Notes/B Vault' $T/o1-run1.log"
ok "o1 only vault 2 got it" "[ -f '$H/Notes/B Vault/.obsidian/themes/HUDdy/theme.css' ] && [ ! -d $H/Notes/A/.obsidian/themes ]"
ok "o1 css identical" "cmp -s $B/../obsidian/HUDdy/theme.css '$H/Notes/B Vault/.obsidian/themes/HUDdy/theme.css'"
ok "o1 appearance kept font, set cssTheme" "grep -q '\"cssTheme\": \"HUDdy\"' '$H/Notes/B Vault/.obsidian/appearance.json' && grep -q '\"baseFontSize\": 15' '$H/Notes/B Vault/.obsidian/appearance.json'"
ok "o1 light-mode note" "grep -q 'Base color scheme is not Dark' $T/o1-run1.log"
paste $H huddy-obsidian.zsh HUDDY_VAULT=all > $T/o1-run2.log; paste $H huddy-obsidian.zsh HUDDY_VAULT=all > $T/o1-run3.log
ok "o1 all: vault A done" "grep -q '\"cssTheme\": \"HUDdy\"' $H/Notes/A/.obsidian/appearance.json && grep -q '\"theme\": \"obsidian\"' $H/Notes/A/.obsidian/appearance.json"
ok "o1 run3 unchanged x2" "[ \$(grep -c 'already set, nothing changed' $T/o1-run3.log) = 2 ]"
ok "o1 bad path stops" "! paste $H huddy-obsidian.zsh HUDDY_VAULT=$H/nowhere > $T/o1-bad.log || true; grep -q 'not an Obsidian vault' $T/o1-bad.log"

echo "### VS Code (scratch VS Code app via CODE_BIN; HOME scratch, so ~/.vscode is scratch)"
H=$(newhome v1); paste $H huddy-vscode.zsh CODE_BIN="$VSC" > $T/v1-run1.log; paste $H huddy-vscode.zsh CODE_BIN="$VSC" > $T/v1-run2.log
ok "v1 installed" "grep -qx 'davidprush.huddy-theme@1.0.1' $T/v1-run1.log && grep -qx 'davidprush.huddy-theme@1.0.1' $T/v1-run2.log"
ok "v1 extension dir" "[ -f $H/.vscode/extensions/davidprush.huddy-theme-1.0.1/themes/HUDdy-color-theme.json ]"
ok "v1 vsix sha checked" "grep -q 'huddy-theme-1.0.1.vsix: OK' $T/v1-run1.log"
H=$(newhome v2); paste $H huddy-vscode.zsh CODE_BIN= > $T/v2-run1.log || true
ok "v2 no VS Code: clear message" "grep -q 'VS Code not found' $T/v2-run1.log"

echo "### every log: pre-check lines, no errors from zsh"
ok "pre-check in all logs" "for f in $T/[gbov]*-run1.log; do grep -q '^docked: ' \$f && grep -q '^swap: ' \$f && grep -q '^Ollama: ' \$f || exit 1; done"
ok "no zsh errors" "! grep -h -E 'zsh: |command not found|parse error|bad pattern|event not found' $T/*.log"
ok "nothing outside scratch" "[ ! -e $HOME/.config/bpytop ] && [ ! -e $HOME/.config/btop ] && ! grep -q huddy $HOME/.config/ghostty/config"
echo "RESULT: $pass passed, $fail failed"; sysctl vm.swapusage
