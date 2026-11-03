"""
Setup script — called by CI to finalize directory structure and verify imports.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

dirs = [
    'pages', 'tests', 'data', 'utils', 'config', 'drivers', 'scripts',
    'reports/HTML', 'reports/Excel', 'reports/JSON',
    'reports/Screenshots', 'reports/Logs', 'reports/Summary',
    'screenshots/failures', 'screenshots/passed',
    'logs', 'history',
]
for d in dirs:
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)

# Create __init__.py files
for pkg in ['pages', 'tests', 'utils', 'config', 'data', 'scripts']:
    init = os.path.join(ROOT, pkg, '__init__.py')
    if not os.path.exists(init):
        open(init, 'w').close()

print('✅ Directory structure verified')
print(f'   ROOT = {ROOT}')
