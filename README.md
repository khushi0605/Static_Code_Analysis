# Lab 5: Static Code Analysis Report

This repository contains the work for Lab 5, demonstrating the use of Pylint, Bandit, and Flake8 to analyze and improve a Python application.

## Deliverables

* **Original Code:** `inventory_system.py`
* **Cleaned Code:** `fixed_inventory_system.py`
* **Analysis Reports:** (The updated reports after running the tools on the *fixed* file)
    * `pylint_report.txt`
    * `bandit_report.txt`
    * `flake8_report.txt`

---

## Issue Identification Table

[cite_start]Here is a summary of the major issues identified and fixed, as required by the lab[cite: 35].

| Issue | Tool(s) | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| [cite_start]**Mutable Default Argument** [cite: 13] | Pylint | `12` | The `logs=[]` argument is mutable and shared across all function calls, causing logs to merge. | Changed default to `logs=None` and initialized a new list `[]` inside the function if `logs` is `None`. |
| [cite_start]**Use of `eval`** [cite: 27] | Bandit | `62` | `eval()` is a high-risk security vulnerability (B307) that allows arbitrary code execution. | Replaced the `eval()` call with a standard `print()` function to achieve the same output safely. |
| [cite_start]**Broad Exception Clause** [cite: 13, 75] | Pylint | `21` | `except:` catches all errors, hiding bugs and preventing clean exits. | Replaced the bare `except:` with `except KeyError:` to specifically handle cases where a non-existent item is removed. |
| **Missing Context Manager** | Pylint | `28, 33` | Files were opened with `open()` but not `close()`. Using `with open(...)` ensures files are closed automatically. | Refactored `loadData` and `saveData` to use the `with open(...) as f:` syntax. |
| [cite_start]**Multiple Imports on One Line** [cite: 25] | Flake8 | `1` | `import json, logging, datetime` violates PEP 8 (E401). | Split each import onto its own line. |
| **Missing `if __name__ == "__main__"`** | Pylint | `64` | The script executes `main()` when imported as a module. | Wrapped the `main()` call in an `if __name__ == "__main__":` block. |

---

## Reflection Questions

[cite_start]Here are the answers to the reflection questions as required by the lab[cite: 36, 83].

**1. Which issues were the easiest to fix, and which were the hardest? [cite_start]Why?** [cite: 85]

* [cite_start]**Easiest:** The easiest issues to fix were the **Flake8 style violations**[cite: 25]. For example, splitting `import json, logging, datetime` onto separate lines was straightforward. These issues are easy because the tool tells you *exactly* what's wrong and the fix is purely mechanical, requiring no deep understanding of the program's logic.

* [cite_start]**Hardest:** The hardest issue to fix was the **`dangerous-default-value` (mutable default argument)** identified by Pylint[cite: 23]. This was difficult because it's a *logical bug*, not a simple syntax error. I had to understand *why* using `logs=[]` as a default was a problem (i.e., the list is created only once and then shared by all calls). The fix required changing the function's signature and adding logic inside it (`if logs is None:`), which changes how the function behaves.

**2. Did the static analysis tools report any false positives? [cite_start]If so, describe one example.** [cite: 86]

Yes, Pylint in particular reported a few issues that could be considered "false positives" or at least "low-priority noise" in this context.

A common example was the `invalid-name` warning for the global variable `stock_data`. Pylint prefers global constants to be in `UPPER_CASE`. However, `stock_data` is not a constant; it's a global *state* variable that is intentionally modified. Renaming it to `STOCK_DATA` would be misleading, as it implies it's a fixed value. In a real project, I would likely disable this specific warning for that line with a comment (e.g., `# pylint: disable=invalid-name`).

**3. [cite_start]How would you integrate static analysis tools into your actual software development workflow?** [cite: 87]

[cite_start]I would integrate these tools at two key stages, as suggested by the lab handout[cite: 88]:

1.  **Local Development:** I would use **pre-commit hooks**. This is a Git feature that lets you run scripts *before* a commit is finalized. I would set up a hook to automatically run `flake8` and `bandit` on any changed Python files. This provides immediate feedback and prevents simple style errors or new security issues from ever entering the repository.

2.  **Continuous Integration (CI):** I would add a step in a CI pipeline (like GitHub Actions) to run all three tools (`pylint`, `bandit`, `flake8`) every time new code is pushed. This acts as a centralized gatekeeper. The CI job would be configured to **fail the build** if any high-severity security issues (from Bandit) or critical code-quality errors (from Pylint) are found, preventing the broken code from being merged.

**4. [cite_start]What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?** [cite: 89]

The improvements were significant and tangible across the board:

* **Robustness:** The code is much more robust. [cite_start]By replacing the bare `except:` [cite: 75] with `except KeyError:`, the program no longer silently hides *all* errors. Using `with open()` for file handling means the program won't accidentally leave files open if an error occurs.
* **Security:** The most critical improvement was **removing the `eval()` call**. [cite_start]This single change, prompted by Bandit[cite: 27], eliminated a massive security hole that could have allowed an attacker to run any code on the machine.
* **Correctness:** The original code was functionally *broken*. [cite_start]Fixing the mutable default argument (`logs=[]`) [cite: 13] was a critical bug fix that made the `addItem` function actually work as intended.
* **Readability & Maintainability:** The code is now much cleaner. [cite_start]Using f-strings [cite: 76][cite_start], organizing imports, and following PEP 8 guidelines [cite: 25] makes the code easier for another developer (or me, six months from now) to read, understand, and safely modify.
