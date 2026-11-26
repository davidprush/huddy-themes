# HUDdy Themes 1.1: Install and Publish Guide

*Palette: HUDdy Soft Contrast Spec 1.0, background `#080e19`. This is a colour update of HUDdy Themes 1.0; hues and accents are unchanged.*

This pack brings HUDdy to four apps. Each one has a single paste block that works on any of your Macs and is safe to paste again.

| App | What you get | Paste block installs to | How I checked it |
|---|---|---|---|
| **Ghostty** | `HUDdy` theme: 16-colour palette, background, text, cursor, selection, split lines | `~/.config/ghostty/themes/HUDdy` plus one managed `theme = HUDdy` block in your config | Ghostty 1.4.0 `+validate-config` OK, `+list-themes` shows `HUDdy (user)`, real Ghostty screenshot, background pixel exact |
| **bpytop** (and **btop**) | `huddy.theme` with every `theme[...]` key and all 8 graph gradients (btop adds `graph_text`, `meter_bg`, `process_*`) | `~/.config/bpytop/themes/huddy.theme`, `color_theme="+huddy"`; btop: `~/.config/btop/themes/huddy.theme`, `color_theme = "huddy"` | bpytop 1.0.68 and btop 1.4.8 running in Ghostty, real screenshots, box colour and background exact |
| **VS Code** | `davidprush.huddy-theme` 1.0.1: 283 workbench colours, terminal ANSI, 34 TextMate rules, 28 semantic token rules | installed from the `.vsix` with `code --install-extension` | Packaged with `@vscode/vsce` 4.1.1, installed into VS Code 1.147.0, real screenshot (TypeScript file, semantic highlighting on) |
| **Obsidian** | `HUDdy` community-format theme (`manifest.json` + `theme.css`), dark mode | `<vault>/.obsidian/themes/HUDdy/`, selected in `appearance.json` | Loaded in Obsidian 1.15.1 with a test vault, real screenshot (headings, tags, callout, checkboxes, code) |

Screenshots are in `screenshots/`. Paste each block twice into an interactive zsh with a scratch home folder to confirm it is safe to run again.

---

## Before you paste

- **Any Mac, any order.** None of these blocks changes the others. For quick wins, I'd go Ghostty, then bpytop, then VS Code, then Obsidian.
- **Each block starts with a pre-check that only reports.** It shows whether you're docked (Thunderbolt Bridge), whether Ollama answers, and your swap. None of it stops the block, and the themes don't use the network or Ollama.
- **Everything is inside the block.** Each one carries its files as gzip+base64 and decodes them with `base64 -D`. Each file is checked with `shasum -a 256 -c` before it's used. Nothing is downloaded, and the working files go in `${TMPDIR:-/tmp}/huddy-themes-1.1`.
- **Safe to paste again.** A file is only rewritten when its content would change. It's backed up first as `<file>.huddy-backup.<time>`, so a second paste prints `already set, nothing changed`.
- Paste each block whole into zsh in Ghostty. It runs in a subshell, stops at the first error and leaves your shell as it was.

---

## Step 1 · Ghostty

The block does four things:

1. Installs the theme to `~/.config/ghostty/themes/HUDdy`.
2. Adds one managed block at the end of your Ghostty config: `config.ghostty` if you have one, otherwise `config`. Later lines win, so it overrides the `theme = GitHub Dark` inside your terminal-setup block without editing that block.
3. Warns if a config in `~/Library/Application Support/com.mitchellh.ghostty/` sets its own theme, because that file loads later.
4. Asks Ghostty itself to validate the config and print the theme it resolves.

@@BLOCK huddy-ghostty.zsh@@

Afterwards, press **Cmd+Shift+,** in Ghostty (Reload Configuration) or open a new window.

> **setup-terminal.sh:** if you run `setup-terminal.sh` again, it comments out `theme` lines outside its own block. Run it with `--keep-ghostty-overrides`, or paste this block again afterwards.

**Undo:** removes the managed block and the theme file, so your earlier theme takes over again.

```zsh
( set -e; XDG="${XDG_CONFIG_HOME:-$HOME/.config}"; for CFG in "$XDG/ghostty/config.ghostty" "$XDG/ghostty/config"; do [ -f "$CFG" ] || continue; /usr/bin/awk '/^# >>> huddy-theme >>>/ {s=1; next} /^# <<< huddy-theme <<</ {s=0; next} !s' "$CFG" > "${TMPDIR:-/tmp}/ghostty-config.undo"; /bin/cat "${TMPDIR:-/tmp}/ghostty-config.undo" > "$CFG"; done; /bin/rm -f "$XDG/ghostty/themes/HUDdy"; echo "HUDdy removed from Ghostty; reload with Cmd+Shift+," )
```

---

## Step 2 · bpytop (and btop)

The block always installs the bpytop theme and sets `color_theme="+huddy"` in `~/.config/bpytop/bpytop.conf`. The `+` means the theme is in your own themes folder. It changes that one line and keeps the rest of the file. If you have no config yet, it starts one, and bpytop fills in the rest when it next saves.

btop is bpytop's successor, and its theme files use the same format with a few extra keys. If btop is installed, the block also installs `huddy.theme` for btop and sets `color_theme = "huddy"`. If bpytop or btop is open, quit it with **q** first, or the block skips that app's config and tells you so.

@@BLOCK huddy-bpytop-btop.zsh@@

You can also pick the theme by hand. In bpytop, open the **Menu (m)**, go to **Options**, then **color_theme**, and choose **+huddy**. In btop, press **Esc**, open **Options**, then **Color theme**, and choose **huddy**.

**Undo:**

```zsh
[ -f ~/.config/bpytop/bpytop.conf ] && /usr/bin/sed -i '' 's/^color_theme=.*/color_theme="Default"/' ~/.config/bpytop/bpytop.conf; [ -f ~/.config/btop/btop.conf ] && /usr/bin/sed -i '' -E 's/^color_theme[[:space:]]*=.*/color_theme = "Default"/' ~/.config/btop/btop.conf; echo "bpytop/btop back to Default"
```

---

## Step 3 · VS Code (install on your Macs)

The block decodes `huddy-theme-1.0.1.vsix` and checks its sha256. It then finds VS Code's `code` command, either on your PATH or inside `/Applications/Visual Studio Code.app`, runs `code --install-extension … --force`, and confirms `davidprush.huddy-theme@1.0.1` is listed.

@@BLOCK huddy-vscode.zsh@@

Then in VS Code press **Cmd+K Cmd+T** and pick **HUDdy**. You can also click the gear in the bottom left and go to **Themes**, then **Color Theme**. The ID is the same as the Marketplace one (Step 5), so once you publish a newer version there, VS Code updates this copy like any other Marketplace extension.

**Undo:** `code --uninstall-extension davidprush.huddy-theme`

---

## Step 4 · Obsidian

The block asks which vault to use. It lists the vaults Obsidian knows on that Mac (from `~/Library/Application Support/obsidian/obsidian.json`) and accepts four kinds of answer:

- a number, or several numbers separated by spaces
- `all`
- a full folder path
- nothing, which picks vault 1

It copies `manifest.json` and `theme.css` into `<vault>/.obsidian/themes/HUDdy/`.

If Obsidian is closed, it also sets `"cssTheme": "HUDdy"` in that vault's `appearance.json`. Your other settings there are kept, and the file is backed up first. If Obsidian is open, it tells you where to choose the theme instead. HUDdy is dark only, so the block warns you if the vault's base colour scheme isn't Dark.

To skip the question, paste `export HUDDY_VAULT=all` (or a vault path) on its own line first.

@@BLOCK huddy-obsidian.zsh@@

If Obsidian was open, choose the theme yourself in **Settings**, then **Appearance**, then **Themes**, and pick **HUDdy**.

**Undo:** pick another theme in **Settings**, then **Appearance**, then **Themes**, and delete `<vault>/.obsidian/themes/HUDdy`.

---

## Step 5 · Publish HUDdy to the VS Code Marketplace

The extension matches your KDE Plasma Breeze listing:

- publisher `davidprush`
- category `Themes`
- a PNG icon named `icon-huddy.png`
- a dark `galleryBanner`, here `#080e19`
- `engines.vscode` `^1.103.0`
- a README in the same layout, with "☞ How to install" and "Activation"

Its ID is `davidprush.huddy-theme` (the same as 1.0.0, already on the Marketplace) and its display name is **HUDdy**. This pack is version **1.0.1**, a colour-only update. Upload it as an update to the existing listing; do not create a second extension.

> **⚠ Change since your last upload: global PATs end on Dec 1, 2026 (one week from today).**
>
> Microsoft's publishing page (code.visualstudio.com/api/working-with-extensions/publishing-extension, checked today) says Azure DevOps **global Personal Access Tokens are retired on December 1, 2026**. A token set to *All accessible organizations*, which is the kind `vsce publish` has always needed, is a global PAT.
>
> - **Until Mon Nov 30** you can still publish with a PAT (Route B).
> - **From Dec 1**, the PAT route stops working. Use the web upload (Route A), which needs no token, or Microsoft's new Trusted Publishing from GitHub Actions (Route C).

### Route A · Upload the .vsix on the website (recommended; no token, keeps working after Dec 1)

1. Run the Step 3 block on the Mac you'll upload from. The last lines print where the `.vsix` is, and `open -R "…/huddy-theme-1.0.1.vsix"` shows it in Finder. The file is also in this pack at `vscode/huddy-theme-1.0.1.vsix`, sha256 `@@VSIX_SHA@@`.
2. Open **https://marketplace.visualstudio.com/manage/publishers/davidprush** and sign in with the Microsoft account that owns the `davidprush` publisher, the one you used for KDE Plasma Breeze.
3. Find the existing **HUDdy** row (`davidprush.huddy-theme`). Click **⋯**, then **Update**.
4. Drag in `huddy-theme-1.0.1.vsix`, or click to choose it, and click **Upload**. Do not click **+ New extension**.
5. The Marketplace checks the package. The row shows a spinner or "Verifying" for a few minutes, then version **1.0.1**.

### Route B · `vsce` with a Personal Access Token (only until Nov 30, 2026)

1. **Create the token.** Go to https://dev.azure.com, open any organization (create one if asked), and click the user-settings icon next to your picture. Choose **Personal access tokens**, then **+ New Token**, and fill in:
   - **Name:** anything, for example `vsce HUDdy`
   - **Organization:** **All accessible organizations** (this matters; a single organization gives 401/403 errors)
   - **Expiration:** any date. After Dec 1 the token won't work anyway.
   - **Scopes:** **Custom defined**, then **Show all scopes**, then **Marketplace**, then tick **Manage**

   Click **Create** and copy the token. Don't save it in a file or paste it into chat.
2. **Log in once.** Run `npx --yes @vscode/vsce@latest login davidprush` and paste the token when it asks. You should see "The Personal Access Token verification succeeded for the publisher 'davidprush'."
3. **Publish the exact .vsix you tested.** Run `npx --yes @vscode/vsce@latest publish --packagePath "${TMPDIR:-/tmp}/huddy-themes-1.1/huddy-theme-1.0.1.vsix"`. (`vsce publish` run in the project folder also works. It rebuilds the package first.)
4. Optionally, sign out afterwards: `npx --yes @vscode/vsce@latest logout davidprush`.

### Route C · Trusted Publishing (after Dec 1, if you want command-line publishing)

Microsoft's replacement for PATs publishes from a **GitHub Actions** workflow with no stored secret. It needs a GitHub repo that **you** create and push; I don't push to GitHub.

1. In the publisher page, open **Trusted Publishing**, then **Create**. Enter the repository owner `davidprush`, your repo name, and a workflow file such as `publish.yml`.
2. In that workflow, the job needs `permissions: id-token: write` and runs `npx @vscode/vsce publish --oidc`.
3. For a private repo, run the workflow within 48 hours of creating the policy. The first successful run activates it.

For a theme you update rarely, Route A is simpler.

### Releasing a new version later

The project is in this pack at `vscode/huddy-theme/`. Unzip the pack into a folder you keep (not `~/Desktop`), for example `~/Projects/huddy-themes`.

1. Edit `themes/HUDdy-color-theme.json`, raise `"version"` in `package.json` (for example `1.0.2`), and add a line to `CHANGELOG.md`.
2. Build the package: `cd …/vscode/huddy-theme && npx --yes @vscode/vsce@latest package --allow-missing-repository`. This creates `huddy-theme-1.0.2.vsix`.
3. Try it locally: `code --install-extension huddy-theme-1.0.2.vsix --force`.
4. Upload it:
   - **Route A:** open the publisher page, click **⋯** on the HUDdy row, choose **Update**, and upload the new `.vsix`.
   - **Route B (before Dec 1):** run `npx @vscode/vsce publish patch`. This bumps the version and publishes in one step. In a git repo it also commits and tags the version.
5. A version number can never be reused, even if you delete that version.

`--allow-missing-repository` is there because `package.json` has no `repository` field yet, since there's no public repo. If you create one, for example `davidprush/huddy-vscode-theme` like your Breeze repo, add `"repository": "https://github.com/davidprush/<repo>"` and drop the flag. You can then also add a screenshot to the README. The Marketplace needs README images to be `https` URLs or images in a linked repo.

### Checking the listing

- Open https://marketplace.visualstudio.com/items?itemName=davidprush.huddy-theme. It shows the icon, "HUDdy", "davidprush.com", version 1.0.1 and the README.
- Run `npx --yes @vscode/vsce@latest show davidprush.huddy-theme`. It prints the published version and the date.
- In VS Code, search Extensions for `HUDdy`. It can take a few minutes after "Verifying" ends before it appears in search.
- On the publisher page, **⋯**, then **Reports**, shows installs over time.

---

## Step 6 · Share the Obsidian theme in the Community directory (optional)

The pack's `obsidian/HUDdy/` folder already has everything a submission needs:

- `manifest.json`: name `HUDdy`, version `1.1.0`, `minAppVersion` `1.0.0`, author David Rush
- `versions.json`: maps `1.0.0` and `1.1.0` to `minAppVersion` `1.0.0`
- `theme.css`
- `README.md`
- `LICENSE` (MIT)
- `screenshot.png` at the recommended 512×288

> **Changed since the old process:** Obsidian's current docs (checked today) say themes are now submitted through **community.obsidian.md**, not by a pull request to `community-css-themes.json` in `obsidianmd/obsidian-releases`.

1. **You** create a public GitHub repo, for example `davidprush/obsidian-huddy`, and push `manifest.json`, `theme.css`, `versions.json`, `README.md`, `LICENSE` and `screenshot.png` to its root. I don't push to GitHub. The theme's name in `manifest.json` can't contain "Obsidian" or "Theme" (`HUDdy` is fine), and it can't be changed after submission.
2. Create a **GitHub release** whose tag is exactly `1.1.0`, matching `manifest.json`. Attach `manifest.json` and `theme.css` to it as files. If you already published 1.0.0, keep that release and add a new `1.1.0` release (never reuse a tag).
3. Sign in at **https://community.obsidian.md** with your Obsidian account, link your GitHub account, and **Add** your theme from the repo.
4. An automatic review shows anything to fix. Fix it in the repo and make a new release with a higher version. Once it's published, people can install HUDdy from inside Obsidian and get updates from your releases.

---

## Step 7 · Sharing the Ghostty and bpytop themes (optional)

- **Ghostty** takes its built-in themes from the iTerm2-Color-Schemes project. To get HUDdy listed there, you would open a pull request with the palette. It's not needed for your own Macs, where the user theme file works.
- **btop** ships themes in `aristocratos/btop` under `themes/`, and a pull request with `btop/huddy.theme` is how others would get it. bpytop is no longer developed, so local install is the way.

---

## Files and checksums

@@SHA_TABLE@@

The full list for the whole pack is in `SHA256SUMS.txt`. Check it with `shasum -a 256 -c SHA256SUMS.txt` inside the unzipped folder.

## Palette

See `PALETTE.md` and `CHANGES.md`. Every colour comes from HUDdy Soft Contrast Spec 1.0 (the 1.0 palette with lifted backgrounds and capped whites). Accents, status colours and derived decorative tokens are unchanged. A few colours have no HUDdy source and are marked **derived** there:

- **magenta `#c792ff`**, because HUDdy has no purple
- **the bright ANSI variants**, each 30% toward white
- **two text greys and the dim graph starts**, mixed toward the background

## Caveats

- **HUDdy is dark only.** No light variant is included, for Obsidian or VS Code.
- **The Ghostty block overrides your terminal-setup theme from below the managed block.** If you re-run `setup-terminal.sh`, use `--keep-ghostty-overrides` or paste the block again.
- **bpytop and btop must be closed while the block sets `color_theme`.** If one is open, the block skips that config and tells you.
- **The `.vsix` from Step 3 is in `${TMPDIR}`,** which macOS clears after a reboot. Paste the block again to recreate it, or use the copy in this pack.
- **There's no `repository` in `package.json` yet,** so the README has no screenshot. Add both if you create a repo.
- **ANSI black is the HUDdy disabled grey `#2e3744`,** not the background, so text printed in "black" stays faintly visible.
