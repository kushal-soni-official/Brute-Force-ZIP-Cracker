# 🗝️ Brute Force ZIP Cracker

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Category](https://img.shields.io/badge/Category-Password%20Security-red)

An educational ZIP password cracker demonstrating **dictionary** and **brute force** attacks —
built with zero dependencies using Python's built-in `zipfile` module.
Teaches why weak passwords are catastrophically easy to crack.

---

## 📸 Preview

```
╔══════════════════════════════════════════╗
║     🗝️  BRUTE FORCE ZIP CRACKER         ║
║     Dictionary & Brute Force Attacks    ║
╚══════════════════════════════════════════╝

  Wordlist  : demo_wordlist.txt  (30 passwords)
  Method    : Dictionary Attack
  Starting attack...

  Tried:       1 / 30  (3.3%)  |  Speed: 312 pwd/s  |  Current: 123456

  🔓 PASSWORD FOUND!
  Password  : secret
  Attempts  : 27
  Time      : 0.09 seconds
  Speed     : 300 passwords/second
```

---

## 🚀 Features

- ✅ **Dictionary attack** — tries passwords from any wordlist file
- ✅ **Brute force attack** — generates every possible character combination
- ✅ **5 charset presets** — digits / lowercase / alphanumeric / full printable
- ✅ **Live progress bar** — speed, attempts, current password
- ✅ **Built-in demo wordlist generator** — test without downloading anything
- ✅ **Educational mode** — password cracking time table + security advice
- ✅ **Zero dependencies** — uses only Python's built-in `zipfile` module

---

## ⚙️ Installation & Usage

### Requirements
- Python 3.8+
- No pip installs needed

### Run it

```bash
git clone https://github.com/yourusername/zip-cracker.git
cd zip-cracker
python zip_cracker.py
```

### Quick Test (step by step)

**Step 1** — Create a test ZIP with a weak password (Windows):
```
Right-click a file → Send to → Compressed folder
Open the ZIP → File → Add a password → type: secret
```
Or using Python:
```python
import pyminizip
pyminizip.compress("test.txt", None, "test_protected.zip", "secret", 0)
```

**Step 2** — Run the cracker, choose `[3]` to create demo wordlist

**Step 3** — Choose `[1]` dictionary attack, point it at your ZIP + wordlist

---

## 🔍 How Each Attack Works

### Dictionary Attack
```
Read wordlist line by line
  ↓
Try each password against ZIP
  ↓
zipfile raises no error? → PASSWORD FOUND ✅
zipfile raises RuntimeError? → Wrong, try next ❌
```

### Brute Force Attack
```
For length = 1, 2, 3, ... max_length:
  Generate every combination from charset
    e.g. charset='abc', length=2 → aa, ab, ac, ba, bb ...
  Try each combination against ZIP
  Found? → Stop and report ✅
```

---

## 📊 Why This Demonstrates Password Security

### Brute Force Time Estimates (modern GPU ~1 billion attempts/sec)

| Length | Digits only | Lowercase | Alphanumeric | Full charset |
|--------|------------|-----------|--------------|-------------|
| 4 chars | < 1 sec | 2 seconds | 15 seconds | 2 minutes |
| 6 chars | < 1 sec | 19 minutes | 9 hours | 26 days |
| 8 chars | < 1 sec | 9 days | 100 years | 8,000 years |
| 10 chars | < 1 sec | 6,000 years | Millions yrs | Never |
| 12 chars | 1 minute | Centuries | Never | Never |

> This is why **length + complexity** are the two most critical factors in password strength.

---

## 📁 Project Structure

```
zip-cracker/
│
├── zip_cracker.py       # Main script
├── demo_wordlist.txt    # Auto-generated demo wordlist
└── README.md            # This file
```

---

## 🧠 What I Learned

- How dictionary and brute force attacks work at the code level
- Python's `zipfile` module and password-protected archives
- How `itertools.product()` generates combinations memory-efficiently
- Why password length and charset size have an **exponential** effect on security
- The difference between dictionary attacks (fast) vs brute force (guaranteed but slow)
- Why the rockyou.txt wordlist (14 million passwords) cracks most weak passwords instantly

---

## ⚠️ Legal Disclaimer

This tool is strictly for **educational purposes**.
**Only use it on ZIP files you created yourself or have explicit permission to test.**
Unauthorised access to password-protected files is illegal in most jurisdictions.

---

## 📄 License

MIT — free to use, modify, and distribute.
