#!/usr/bin/env python3
"""Mirror canonical skills/commands/agents into the Claude project folder and the plugin package.

Canonical: .agents/skills/*/SKILL.md, .claude/commands/*.md, .claude/agents/*.md
Mirrors:   .claude/skills/, plugins/ravan-hami/{skills,commands,agents}/
"""
from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[1]
plugin = root / 'plugins/ravan-hami'
pairs = [(p, [root / '.claude/skills' / p.parent.name / 'SKILL.md', plugin / 'skills' / p.parent.name / 'SKILL.md'])
         for p in (root / '.agents/skills').glob('*/SKILL.md')]
pairs += [(p, [plugin / kind / p.name]) for kind in ('commands', 'agents') for p in (root / '.claude' / kind).glob('*.md')]
for src, targets in pairs:
    for t in targets:
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, t)
for mirror in (root / '.claude/skills', plugin / 'skills'):
    for d in mirror.iterdir():
        if d.is_dir() and not (root / '.agents/skills' / d.name).exists():
            shutil.rmtree(d)
print(f'Synchronized {len(pairs)} canonical files')
