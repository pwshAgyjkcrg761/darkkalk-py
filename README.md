# <img src="darkkalk+_internal/icons/darkkalk+_icon.svg" width="32" height="32"> Darkkalk+™ <img src="darkkalk+_internal/icons/darkkalk+_icon.svg" width="32" height="32">
**A modern algebraic scientific expression calculator with arbitrary-precision integers, execution safety limits, rich history logging, and multi-format export.**

---

![Darkkalk+ Dark Mode Main Interface](images/darkkalk-py_dark_mode_main.png)

## Overview
Darkkalk+™ is an algebraic scientific expression calculator written in Python and PyQt6.

**Primary Environment:** Developed and tested on **Python 3.14.5** using the **PyQt6** GUI framework. It is engineered for engineers, scientists, developers, students, and power users who require reliable calculation workflows, runaway calculation safety controls, and clean export to HTML, Markdown, and Plain Text.

### The Calculation & Logging Engine
The utility couples a safe, sandboxed expression evaluator with an interactive 5×7 scientific keypad, rich HTML-rendered audit logging, and configurable safety limits.

Key operational features include:
1. **Natural Algebraic Evaluation:** Type complex equations naturally (e.g., `5 + sin(30) * 2^3`) respecting standard mathematical operator precedence.
2. **Implicit Multiplication & Auto-Parentheses:** Automatically infers multiplication where appropriate (`2pi`, `5sin(45)`, `10(2+3)`, `(4)(5)`, `50%200`) and inserts auto-closing parentheses pairs with cursor auto-positioning.
3. **Full Scientific & Trigonometric Suite:** Built-in keypad and typeable functions for `sin`, `cos`, `tan`, `log` (base 10), `ln` (natural log), `sqrt`, `abs`, and constants `pi` (π) and `e` (Euler's number).
4. **Trigonometric Angle Modes:** Seamlessly switch between **Degrees** (default) and **Radians** via the Preferences dialog.
5. **Arbitrary-Precision Integer Arithmetic:** Whole-number arithmetic (such as `2^10000`, large factorials, and multiplications) has no fixed 64-bit integer ceiling. Massive numbers (≥ 10¹²) are automatically rendered in compact scientific notation without integer overflow.
6. **Execution Safety Limits & Timeouts:** Background thread evaluation (`ThreadPoolExecutor`) enforces configurable execution timeouts (1s to 10s, or Unlimited) and maximum integer digit limits (10,000 to 500,000, or Unlimited) to eliminate UI freezes on runaway exponential calculations.
7. **Interactive Memory Registers:** Full Memory Store (`MS`), Memory Recall (`MR`), Memory Addition (`M+`), Memory Subtraction (`M-`), and Memory Clear (`MC`) suite featuring dynamic color-coded visual indicator badges when active values are stored.
8. **Previous Result Chaining (`Ans`):** Easily insert or chain calculations using `Ans`. Typing an arithmetic operator (`+`, `-`, `*`, `/`, `^`, `%`) into an empty input line automatically prepends `Ans`.
9. **Continuous Timestamped Calculation Log:** Left pane maintains a running history of equations and color-coded results with configurable timestamp headers (Logical `YYYY-MM-DD`, System Locale, or Disabled).
10. **Past Inputs Dropdown:** Click the dropdown button (**▼**) next to the input field to review and instantly reload up to 30 past expressions.
11. **Multi-Format Export (Save Output):** Export calculation logs to **HTML** (with full responsive styling and color scheme preservation), **Markdown (`.md`)**, or universal **Plain Text (`.txt`)** via `File > Save Output` (`Ctrl+S`), remembering the last used folder across sessions.
12. **High-DPI Printing & PDF Export:** Print high-contrast vector logs or export directly to PDF via `File > Print Output` (`Ctrl+P`) with automated 3x print scaling and running page headers.
13. **Adjustable Window Opacity:** Built-in opacity slider under Preferences allows seamless transparency adjustments from 20% to 100%, syncing across all menus and popup lists.
14. **Theme Engine & Windows Title Bar Integration:** Full support for Dark, Light, and System-synced palettes with native Windows DWM dark title bar syncing.
15. **Audio Suppression & Status Badges:** Option to disable system notification sounds while maintaining crisp, vector-rendered success and error badges.
16. **Persistent State Management:** Automatically remembers window geometry, last used directory, theme preferences, calculation limits, and complete session history in `darkkalk+_internal/` config files.

---

## Feature Reference

| Option / Feature | Description |
| :--- | :--- |
| **Algebraic Parsing Engine** | Evaluates equations following strict mathematical precedence with implicit multiplication support. |
| **Scientific Functions** | Keypad access to `sin`, `cos`, `tan`, `log`, `ln`, `sqrt`, `pi`, and `e` with degree and radian support. |
| **Arbitrary Precision** | Evaluates arbitrarily large integer arithmetic with automatic scientific notation formatting for numbers ≥ 10¹². |
| **Safety Limits & Timeout** | Background worker thread with user-defined digit caps (10,000–500,000) and timeouts (1s–10s) to prevent lockups. |
| **Memory System (MC/MR/M+/M-/MS)** | Dedicated memory registers with real-time visual button illumination when holding stored values. |
| **Continuous Audit Log** | Persistent calculation pane tracking timestamped equations, outputs, and syntax error alerts. |
| **Past Inputs Menu (▼)** | Interactive dropdown menu to quickly review and reload recent equations into the input line. |
| **Multi-Format Log Export** | Save logs to **HTML**, **Markdown (`.md`)**, or **Plain Text (`.txt`)** with persistent folder recall (`Ctrl+S`). |
| **High-DPI Print & PDF** | Vector document rendering with 3x print scaling and page headers for physical printing or PDF generation (`Ctrl+P`). |
| **Window Transparency** | Real-time slider-based opacity adjustment (20%–100%) applied across main windows, dialogs, and menus. |
| **Theme Engine** | Custom `QPalette` implementation supporting Dark, Light, and System themes with Windows DWM title bar styling. |
| **Date & Time Formatting** | Configurable history timestamps supporting Logical (`YYYY-MM-DD`), System Locale, or Disabled modes. |
| **Notification Sound Toggle** | Option to mute all audio alerts while preserving visual dialog badges. |
| **Factory Reset Button** | Instant one-click restoration of default calculation, display, and safety limit settings in Preferences. |

---

## Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Enter` / `Return` / `=` | Calculate and evaluate active expression. |
| `Escape` | Clear current input line. |
| `Backspace` | Delete last character (or automatically delete empty `()` parenthesis pairs). |
| `Ctrl+S` | Save calculation output log to file (HTML, Markdown, or Plain Text). |
| `Ctrl+P` | Open the Print / PDF export dialog. |
| `Ctrl+Delete` | Clear output calculation history. |
| `Ctrl+X` / `Ctrl+C` / `Ctrl+V` | Standard Cut, Copy, and Paste operations. |

---


## Assets & Licensing
This software is released under the **GNU General Public License v3**.

### Icon Credits
* **File:** `darkkalk+_icon.svg`
    * **Asset:** Calculator SVG Vector
    * **Source:** <a href="https://www.svgrepo.com/svg/253926/calculator" target="_blank">https://www.svgrepo.com/svg/253926/calculator</a>
    * **License:** <a href="https://creativecommons.org/publicdomain/zero/1.0/" target="_blank">CC0 License</a>
    * **Modifications:** Modified by pwshAgyjkcrg761.

---

## Dependencies
* **OS:** Microsoft Windows 10 / 11 (64-bit).
* **Python:** 3.14.5+ (Recommended).
* **PyQt6:** Required for the Graphical User Interface framework (`pip install PyQt6`).

## Support & Maintenance
**This repository is provided "as-is" for archival purposes.** The author is not actively looking for feedback, feature requests, or bug reports. The issue tracker is disabled.

## Disclaimer
*Darkkalk+ is an algebraic scientific calculator provided without warranty of any kind. While arbitrary precision and safety limit safeguards are implemented, users are responsible for verifying critical mathematical calculations independently. The author is not liable for any calculation errors or omissions.*

---
> **Document Control**<br>
> *This document is up-to-date with the following version of Darkkalk+™.*<br>
> *2026.09.18__12.26.32*