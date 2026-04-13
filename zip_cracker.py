# ============================================================
#   BRUTE FORCE ZIP CRACKER  (Educational)
#   Author  : Your Name
#   GitHub  : github.com/yourusername
#   Purpose : Attempts to crack a password-protected ZIP file
#             using two methods:
#               1. Dictionary Attack  — tries passwords from a wordlist
#               2. Brute Force Attack — generates all combinations
#             Teaches why weak passwords are dangerous.
#
#   ⚠  LEGAL NOTICE: Only use this on ZIP files YOU created
#      or have explicit permission to test. Cracking files
#      you do not own is illegal.
#
#   Dependencies: None — uses Python's built-in zipfile module
# ============================================================

import zipfile          # Built-in module for working with ZIP files
import itertools        # For generating character combinations
import string           # Provides sets of characters (letters, digits etc.)
import time
import os
import sys
from datetime import datetime

# ── ANSI colour codes ──
RED     = "\033[91m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
CYAN    = "\033[96m"
MAGENTA = "\033[95m"
RESET   = "\033[0m"
BOLD    = "\033[1m"


# ══════════════════════════════════════════════
#  CORE — TRY A SINGLE PASSWORD
#  zipfile raises BadZipFile or RuntimeError
#  if the password is wrong. We catch those errors
#  to know whether a password worked or not.
# ══════════════════════════════════════════════

def try_password(zip_ref: zipfile.ZipFile, password: str) -> bool:
    """
    Tries one password against a ZIP file.
    Returns True if the password is correct, False otherwise.

    zipfile.extractall() requires the password as bytes,
    so we encode the string: "hello" → b"hello"
    """
    try:
        # Try to extract using this password (into memory only, not disk)
        zip_ref.extractall(pwd=password.encode("utf-8"), path=None)
        return True     # No error = correct password!
    except (RuntimeError, zipfile.BadZipFile, Exception):
        return False    # Wrong password — keep trying


# ══════════════════════════════════════════════
#  METHOD 1 — DICTIONARY ATTACK
#  Tries every password from a wordlist file.
#  Most real-world passwords are common words —
#  dictionary attacks crack them in seconds.
# ══════════════════════════════════════════════

def dictionary_attack(zip_path: str, wordlist_path: str) -> str | None:
    """
    Reads passwords from a wordlist file (one per line)
    and tries each against the ZIP file.

    Returns the correct password if found, None otherwise.
    """
    if not os.path.exists(wordlist_path):
        print(f"\n  {RED}Wordlist not found: {wordlist_path}{RESET}")
        return None

    if not os.path.exists(zip_path):
        print(f"\n  {RED}ZIP file not found: {zip_path}{RESET}")
        return None

    print(f"\n  {CYAN}Opening ZIP file: {zip_path}{RESET}")

    try:
        zip_ref = zipfile.ZipFile(zip_path, 'r')
    except zipfile.BadZipFile:
        print(f"  {RED}Error: '{zip_path}' is not a valid ZIP file.{RESET}")
        return None

    # Count total passwords in wordlist for progress display
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        total = sum(1 for _ in f)

    print(f"  {YELLOW}Wordlist  : {wordlist_path}  ({total:,} passwords){RESET}")
    print(f"  {YELLOW}Method    : Dictionary Attack{RESET}")
    print(f"  {YELLOW}Starting attack — press Ctrl+C to stop...\n{RESET}")

    start_time = time.time()
    attempted  = 0

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
            for line in wordlist:
                password  = line.strip()    # Remove newline characters
                attempted += 1

                # ── Live progress every 500 attempts ──
                if attempted % 500 == 0 or attempted == 1:
                    elapsed = time.time() - start_time
                    rate    = attempted / elapsed if elapsed > 0 else 0
                    pct     = (attempted / total * 100) if total > 0 else 0
                    print(
                        f"  Tried: {attempted:>7,} / {total:,}  "
                        f"({pct:.1f}%)  |  "
                        f"Speed: {rate:,.0f} pwd/s  |  "
                        f"Current: {password[:20]:<20}",
                        end="\r"
                    )

                if try_password(zip_ref, password):
                    elapsed = time.time() - start_time
                    print()  # New line after progress
                    print(f"\n  {GREEN}{BOLD}🔓 PASSWORD FOUND!{RESET}")
                    print(f"  {GREEN}Password  : {BOLD}{password}{RESET}")
                    print(f"  Attempts  : {attempted:,}")
                    print(f"  Time      : {elapsed:.2f} seconds")
                    print(f"  Speed     : {attempted/elapsed:,.0f} passwords/second")
                    zip_ref.close()
                    return password

    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Attack stopped by user.{RESET}")
        zip_ref.close()
        return None

    elapsed = time.time() - start_time
    print()
    print(f"\n  {RED}Password not found in wordlist.{RESET}")
    print(f"  Tried {attempted:,} passwords in {elapsed:.2f}s")
    zip_ref.close()
    return None


# ══════════════════════════════════════════════
#  METHOD 2 — BRUTE FORCE ATTACK
#  Generates EVERY possible combination of characters
#  up to a given length. Guaranteed to find the password
#  eventually — but gets exponentially slower with length.
#
#  Example: 4-char lowercase = 26^4 = 456,976 combos
#           6-char lowercase = 26^6 = 308,915,776 combos
# ══════════════════════════════════════════════

def brute_force_attack(zip_path: str, charset: str, max_length: int) -> str | None:
    """
    Generates every combination of characters from charset
    up to max_length characters and tries each as a password.

    Uses itertools.product() which is very memory-efficient —
    it generates combinations one at a time without storing all of them.
    """
    if not os.path.exists(zip_path):
        print(f"\n  {RED}ZIP file not found: {zip_path}{RESET}")
        return None

    try:
        zip_ref = zipfile.ZipFile(zip_path, 'r')
    except zipfile.BadZipFile:
        print(f"  {RED}Error: '{zip_path}' is not a valid ZIP file.{RESET}")
        return None

    # ── Calculate total combinations to show scale ──
    total_combos = sum(len(charset) ** l for l in range(1, max_length + 1))

    print(f"\n  {YELLOW}Charset       : {charset}")
    print(f"  Charset size  : {len(charset)} characters")
    print(f"  Max length    : {max_length}")
    print(f"  Total combos  : {total_combos:,}")
    print(f"  Method        : Brute Force{RESET}")
    print(f"  {YELLOW}Starting attack — press Ctrl+C to stop...\n{RESET}")

    start_time = time.time()
    attempted  = 0

    try:
        # Try lengths 1, 2, 3, ... up to max_length
        for length in range(1, max_length + 1):
            print(f"  {CYAN}Trying length {length}...{RESET}")

            # itertools.product generates all combinations with repetition
            # e.g. product('ab', repeat=2) → aa, ab, ba, bb
            for combo in itertools.product(charset, repeat=length):
                password  = "".join(combo)   # Convert tuple ('a','b') → "ab"
                attempted += 1

                # ── Live progress every 1000 attempts ──
                if attempted % 1000 == 0:
                    elapsed = time.time() - start_time
                    rate    = attempted / elapsed if elapsed > 0 else 0
                    print(
                        f"  Tried: {attempted:>10,}  |  "
                        f"Speed: {rate:,.0f} pwd/s  |  "
                        f"Current: {password:<15}",
                        end="\r"
                    )

                if try_password(zip_ref, password):
                    elapsed = time.time() - start_time
                    print()
                    print(f"\n  {GREEN}{BOLD}🔓 PASSWORD FOUND!{RESET}")
                    print(f"  {GREEN}Password  : {BOLD}{password}{RESET}")
                    print(f"  Length    : {len(password)} characters")
                    print(f"  Attempts  : {attempted:,}")
                    print(f"  Time      : {elapsed:.2f} seconds")
                    print(f"  Speed     : {attempted/elapsed:,.0f} passwords/second")
                    zip_ref.close()
                    return password

    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Attack stopped by user.{RESET}")
        zip_ref.close()
        return None

    elapsed = time.time() - start_time
    print()
    print(f"\n  {RED}Password not found in brute force range.{RESET}")
    print(f"  Tried {attempted:,} combinations in {elapsed:.2f}s")
    zip_ref.close()
    return None


# ══════════════════════════════════════════════
#  BUILT-IN DEMO WORDLIST
#  Creates a small sample wordlist so the user
#  can test without downloading anything.
# ══════════════════════════════════════════════

def create_demo_wordlist(path: str = "demo_wordlist.txt") -> str:
    """Creates a small demo wordlist with common passwords for testing."""
    passwords = [
        "123456", "password", "123456789", "qwerty", "abc123",
        "111111", "iloveyou", "admin", "welcome", "monkey",
        "dragon", "master", "sunshine", "princess", "letmein",
        "football", "shadow", "superman", "michael", "password1",
        "test123", "hello", "secret", "hunter2", "trustno1",
        "zippass", "mypassword", "securezip", "zip1234", "archive",
    ]
    with open(path, 'w') as f:
        f.write("\n".join(passwords))
    print(f"  {GREEN}Demo wordlist created: {path}  ({len(passwords)} passwords){RESET}")
    return path


# ══════════════════════════════════════════════
#  EDUCATIONAL: WHY THIS MATTERS
# ══════════════════════════════════════════════

def show_why_it_matters():
    print(f"""
{BOLD}{CYAN}  ╔══════════════════════════════════════════════════════╗
  ║        WHY WEAK PASSWORDS ARE DANGEROUS             ║
  ╚══════════════════════════════════════════════════════╝{RESET}

  {YELLOW}Dictionary Attack:{RESET}
    → Uses a list of common passwords (rockyou.txt has 14M!)
    → Cracks "password", "123456", "qwerty" in milliseconds
    → Over 80% of hacking breaches involve weak/stolen passwords
      (Source: Verizon Data Breach Investigations Report)

  {YELLOW}Brute Force Attack:{RESET}
    → Tries EVERY possible combination
    → Guaranteed to work — only question is time

  {GREEN}How long to brute-force a password? (modern GPU){RESET}

    Length  Lowercase only    + Numbers       + Symbols
    ──────  ──────────────    ─────────────   ─────────────
    4 chars  Instantly         Instantly       2 seconds
    6 chars  2 seconds         1 minute        3 hours
    8 chars  22 minutes        5 hours         8 years
    10 chars 4 months          8 years         Centuries
    12 chars 350 years         200,000 years   Never

  {GREEN}The fix — use a strong password:{RESET}
    ✅ At least 12 characters
    ✅ Mix of uppercase, lowercase, digits, symbols
    ✅ Use a password manager (Bitwarden, 1Password)
    ✅ Never reuse passwords across sites
    ✅ Enable MFA (Multi-Factor Authentication)
    """)


# ══════════════════════════════════════════════
#  CHARSET PRESETS
# ══════════════════════════════════════════════

CHARSETS = {
    "1": ("Digits only (0-9)",            string.digits),
    "2": ("Lowercase letters (a-z)",       string.ascii_lowercase),
    "3": ("Lowercase + digits",            string.ascii_lowercase + string.digits),
    "4": ("Upper + Lower + digits",        string.ascii_letters + string.digits),
    "5": ("Full charset (all printable)",  string.printable.strip()),
}


# ══════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════

def print_banner():
    print(f"\n{BOLD}{CYAN}╔══════════════════════════════════════════╗")
    print(f"║     🗝️  BRUTE FORCE ZIP CRACKER         ║")
    print(f"║     Dictionary & Brute Force Attacks    ║")
    print(f"╚══════════════════════════════════════════╝{RESET}")
    print(f"  {RED}⚠  For educational use only. Only crack ZIPs you own!{RESET}\n")


def main():
    print_banner()

    while True:
        print(f"  {BOLD}Choose an option:\n{RESET}")
        print(f"  {CYAN}[1]{RESET} Dictionary attack   (use a wordlist file)")
        print(f"  {CYAN}[2]{RESET} Brute force attack  (try all combinations)")
        print(f"  {CYAN}[3]{RESET} Create demo wordlist (for testing)")
        print(f"  {CYAN}[4]{RESET} Why weak passwords are dangerous")
        print(f"  {CYAN}[0]{RESET} Exit\n")

        choice = input("  Choice: ").strip()

        # ── Dictionary Attack ──
        if choice == '1':
            zip_path      = input("\n  ZIP file path  : ").strip()
            wordlist_path = input("  Wordlist path  : ").strip() or "demo_wordlist.txt"
            result        = dictionary_attack(zip_path, wordlist_path)

            if result:
                print(f"\n  {GREEN}💡 Tip: This password was weak enough to appear in a wordlist.")
                print(f"     Always use randomly generated passwords for sensitive files!{RESET}\n")
            else:
                print(f"\n  {YELLOW}💡 The password wasn't in the wordlist — it may be stronger,")
                print(f"     or try a larger wordlist like 'rockyou.txt'.{RESET}\n")

        # ── Brute Force Attack ──
        elif choice == '2':
            zip_path = input("\n  ZIP file path : ").strip()

            print(f"\n  {BOLD}Choose character set:{RESET}")
            for key, (label, _) in CHARSETS.items():
                print(f"  {CYAN}[{key}]{RESET} {label}")

            cs_choice  = input("\n  Charset choice (default 2): ").strip() or "2"
            label, charset = CHARSETS.get(cs_choice, CHARSETS["2"])

            try:
                max_len = int(input("  Max password length (default 4): ").strip() or "4")
                max_len = min(max_len, 6)  # Cap at 6 to prevent infinite runs
            except ValueError:
                max_len = 4

            print(f"\n  {YELLOW}Warning: Brute force gets exponentially slower with length.")
            print(f"  Recommended: max length 4–5 for testing.{RESET}")

            result = brute_force_attack(zip_path, charset, max_len)

            if result:
                print(f"\n  {GREEN}💡 This password was short/simple enough to brute-force.")
                print(f"     A 12+ character random password would take centuries!{RESET}\n")

        # ── Create Demo Wordlist ──
        elif choice == '3':
            path = input("\n  Save wordlist as (default: demo_wordlist.txt): ").strip() \
                   or "demo_wordlist.txt"
            create_demo_wordlist(path)
            print(f"  {YELLOW}💡 To test: create a ZIP with password 'secret' or 'admin',")
            print(f"     then run a dictionary attack with this wordlist.{RESET}\n")

        # ── Educational Info ──
        elif choice == '4':
            show_why_it_matters()

        # ── Exit ──
        elif choice == '0':
            print(f"\n  {CYAN}Use strong passwords. Stay secure. 🔐{RESET}\n")
            break

        else:
            print(f"  {RED}Invalid choice.{RESET}\n")


if __name__ == "__main__":
    main()
