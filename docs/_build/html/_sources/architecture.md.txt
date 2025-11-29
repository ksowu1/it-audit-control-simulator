# System Architecture

──────────────────────────────┐
│ main.py │
│ Runs all control tests │
└──────────────┬───────────────┘
│
▼
┌──────────────────────────────┐
│ controls/ │
│ access_control.py │
│ sod.py │
│ change_management.py │
│ backup_recovery.py │
└──────────────┬───────────────┘
│
▼
┌──────────────────────────────┐
│ utils/ │
│ loader.py │
│ export.py │
└──────────────────────────────┘


- Fully modular test files  
- Easily extendable  
- Supports CSV exports  
- Ready for CI/CD  
