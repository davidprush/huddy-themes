import hashlib, os, re
P='/workspace/huddy-1.1-src/pack'; t=open('/workspace/huddy-1.1-src/template.md').read()
def blk(m):
    s=open(f'{P}/paste-blocks/{m.group(1)}').read()
    sha=hashlib.sha256(s.encode()).hexdigest()
    return f"*Block file: `paste-blocks/{m.group(1)}` (sha256 `{sha}`).*\n\n```zsh\n{s}```"
t=re.sub(r'@@BLOCK (\S+)@@', blk, t)
sha=lambda p: hashlib.sha256(open(f'{P}/{p}','rb').read()).hexdigest()
t=t.replace('@@VSIX_SHA@@', sha('vscode/huddy-theme-1.0.1.vsix'))
files=['ghostty/HUDdy','bpytop/huddy.theme','btop/huddy.theme','obsidian/HUDdy/manifest.json','obsidian/HUDdy/theme.css',
 'vscode/huddy-theme-1.0.1.vsix','vscode/huddy-theme/package.json','vscode/huddy-theme/themes/HUDdy-color-theme.json','vscode/huddy-theme/icon-huddy.png',
 'paste-blocks/huddy-ghostty.zsh','paste-blocks/huddy-bpytop-btop.zsh','paste-blocks/huddy-vscode.zsh','paste-blocks/huddy-obsidian.zsh']
t=t.replace('@@SHA_TABLE@@', '| File | sha256 |\n|---|---|\n'+'\n'.join(f'| `{f}` | `{sha(f)}` |' for f in files))
open(f'{P}/HUDdy-Themes-Install-Guide.md','w').write(t)
# self-check: blocks in guide are byte-identical to files
for f in os.listdir(f'{P}/paste-blocks'):
    if f.endswith('.zsh') and f!='test-blocks.zsh': assert '```zsh\n'+open(f'{P}/paste-blocks/{f}').read()+'```' in t, f
print('guide ok', len(t.splitlines()), 'lines')
