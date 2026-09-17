# ==============================================================================
# SCRIPT: dk+.py (Darkkalk+)
# VERSION: 2026.09.16__20.39.18
# TARGET: Python 3.14.5
#
# Copyright (C) 2026 pwshAgyjkcrg761
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
# ==============================================================================
# <PROTECTED>
# ==============================================================================
# AI INSTRUCTIONS
# Copyright (c) 2026 pwshAgyjkcrg761
# License: MIT
# Source: https://git.disroot.org/pwshAgyjkcrg761/AI_Instructions
#
# AI INSTRUCTIONS v2026.09.01__04.25.09 : 
#
# 1. MESSAGE STAMP: 
#    - Every response containing code MUST begin with a standalone version stamp.
#    - Use CHICAGO TIME (Central Time), 24-hour clock.
#    - Format: YYYY.MM.DD__HH.MM.SS.
#    - CRITICAL: Use the time provided in the prompt or at 
#      https://www.timeanddate.com/worldclock/usa/chicago. Ensure minutes are exact.
#
# 2. VERSION SNIPPET PROHIBITION:
#    - DO NOT provide code snippets, anchors, or steps to update the script's 
#      internal VERSION comment or $scriptVersion variable. 
#    - The user handles internal file versioning manually based on the Message Stamp.
#
# 3. SCRIPT OUTPUT (SURGICAL FIXES ONLY):
#    - Provide minimal, highly targeted, surgical edits. Do not rewrite large blocks or 
#      entire functions.
#    - Always use a codebox with a copy button.
#    - Multiple modifications MUST be presented strictly ONE step at a time. Wait for 
#      user confirmation before proceeding to the next step. 
#    - DO NOT modify or refactor any code inside <PROTECTED> tags.
#
# 4. VERBATIM ANCHOR PROTOCOL (FOR NOTEPAD++):
#    - To facilitate "Find" in Notepad++, always structure edits with:
#      - "Verbatim Anchor (Before)" - The exact lines of existing code immediately before 
#         the change.
#      - "Verbatim Anchor (After)" - The exact lines of existing code immediately after 
#         the change.
#      - "Snippet to REPLACE" - The exact code block to be deleted.
#      - "What to PASTE in its place" - The new code block to be inserted.
#    - Do not summarize, truncate, or refactor the existing code used as an anchor.
#    - Match spaces, comments, and symbols exactly as they appear in the file.
#
# 5. CONTENT PRESERVATION:
#    - Do not remove, modify, or strip out telemetry data or DevDebug information from any 
#      provided code.
# ==============================================================================
# </PROTECTED>

import sys
import os
import json
import re
import ctypes

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

APP_VERSION = "2026.09.16__20.39.18"

DEV_DEBUG = any(arg.lower() in ("-devdebug", "--devdebug", "/devdebug") for arg in sys.argv)

import math

def calc_sin(x, use_degrees=True):
    rad = math.radians(x) if use_degrees else x
    res = math.sin(rad)
    return 0.0 if abs(res) < 1e-15 else res

def calc_cos(x, use_degrees=True):
    rad = math.radians(x) if use_degrees else x
    res = math.cos(rad)
    return 0.0 if abs(res) < 1e-15 else res

def calc_tan(x, use_degrees=True):
    rad = math.radians(x) if use_degrees else x
    if abs(math.cos(rad)) < 1e-15:
        raise ValueError("Undefined (tangent vertical asymptote)")
    res = math.tan(rad)
    return 0.0 if abs(res) < 1e-15 else res

def evaluate_math_expression(expr_str, ans_val=0.0, use_degrees=True):
    """Safely evaluates mathematical expressions with trig, logarithms, and powers."""
    if not expr_str or not expr_str.strip():
        return ""
    
    clean_expr = expr_str.strip()
    clean_expr = clean_expr.replace('×', '*').replace('÷', '/').replace('^', '**')

    # Auto-close unclosed parentheses
    open_count = clean_expr.count('(')
    close_count = clean_expr.count(')')
    if open_count > close_count:
        clean_expr += ')' * (open_count - close_count)

    # Substitute Ans safely before implicit multiplication
    ans_repr = str(ans_val).strip() if str(ans_val).strip() else "0"
    clean_expr = re.sub(r'\bAns\b', f"({ans_repr})", clean_expr, flags=re.IGNORECASE)

    # Implicit multiplication where constants precede numbers, parentheses, or functions (e.g., pi2 -> pi*2, pi(2) -> pi*(2))
    clean_expr = re.sub(r'\b(pi|e)\s*(\d+(\.\d+)?)', r'\1*\2', clean_expr)
    clean_expr = re.sub(r'\b(pi|e)\s*\(', r'\1*(', clean_expr)
    clean_expr = re.sub(r'\b(pi|e)\s*(sin|cos|tan|log|ln|sqrt|pi|e|abs)\b', r'\1*\2', clean_expr)

    # Implicit multiplication where numbers or ')' precede constants or functions (excluding scientific notation 1e5)
    clean_expr = re.sub(r'(\d+(\.\d+)?|\))\s*(sin|cos|tan|log|ln|sqrt|pi|abs)\b', r'\1*\3', clean_expr)
    clean_expr = re.sub(r'(\))\s*e\b', r'\1*e', clean_expr)

    # Implicit multiplication with parentheses (e.g., 10(5+5) -> 10*(5+5), (2)(3) -> (2)*(3), (5)2 -> (5)*2)
    clean_expr = re.sub(r'(\d+(\.\d+)?)\s*\(', r'\1*(', clean_expr)
    clean_expr = re.sub(r'\)\s*\(', r')*(', clean_expr)
    clean_expr = re.sub(r'\)\s*(\d+(\.\d+)?)', r')*\1', clean_expr)

    clean_expr = re.sub(r'\bpi\b', str(math.pi), clean_expr)
    clean_expr = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100.0)', clean_expr)

    allowed_names = {
        "sin": lambda x: calc_sin(x, use_degrees),
        "cos": lambda x: calc_cos(x, use_degrees),
        "tan": lambda x: calc_tan(x, use_degrees),
        "log": lambda x: math.log10(x),
        "ln": lambda x: math.log(x),
        "sqrt": lambda x: math.sqrt(x),
        "abs": abs,
        "pi": math.pi,
        "e": math.e,
        "inf": float("inf"),
        "nan": float("nan")
    }

    try:
        compiled_code = compile(clean_expr, "<string>", "eval")
        for name in compiled_code.co_names:
            if name not in allowed_names:
                raise NameError(f"Function or identifier '{name}' is not allowed.")

        result = eval(compiled_code, {"__builtins__": {}}, allowed_names)
        
        if isinstance(result, complex):
            if abs(result.imag) < 1e-15:
                result = result.real
            else:
                return "Error: Non-real result"

        if isinstance(result, (int, float)):
            if result == 0:
                return "0"

            # Format large integers in scientific notation
            if isinstance(result, int) and abs(result) >= 10**12:
                try:
                    f_val = float(result)
                    if not math.isinf(f_val):
                        return f"{f_val:.10g}"
                except OverflowError:
                    pass

                s = str(abs(result))
                exp = len(s) - 1
                mantissa = s[0] + ('.' + s[1:11].rstrip('0') if len(s) > 1 else '')
                mantissa = mantissa.rstrip('.')
                sign = "-" if result < 0 else ""
                return f"{sign}{mantissa}e+{exp}"

            if isinstance(result, float):
                if math.isinf(result):
                    return "Error: Overflow (Infinity)"
                if math.isnan(result):
                    return "Error: Undefined (NaN)"
                if result.is_integer() and abs(result) < 10**12:
                    return str(int(result))
                return f"{result:.10g}"

            return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except OverflowError:
        return "Error: Number overflow (exceeds float limit ~10^308)"
    except ValueError as ve:
        return f"Error: {ve}"
    except (SyntaxError, NameError, TypeError):
        return "Error: Invalid syntax"
    except Exception as e:
        return f"Error: {e}"

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QDir, QTimer, QLocale, QDate
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QFileDialog, QLabel, QMessageBox, 
                             QDialog, QCheckBox, QTextBrowser, QDialogButtonBox,
                             QComboBox, QProgressBar, QHBoxLayout, QListWidget,
                             QTabWidget, QLineEdit, QFormLayout, QTreeWidget,
                             QTreeWidgetItem, QSplitter, QHeaderView, QMenu,
                             QInputDialog, QTreeView, QAbstractItemView,
                             QStackedWidget, QRadioButton, QButtonGroup)
from PyQt6.QtGui import (QActionGroup, QPalette, QColor, QIcon, QPixmap, QPainter, 
                         QPen, QFileSystemModel)


def get_status_pixmap(status="success", size=48):
    """Draws a crisp green checkmark or red X badge for dialog message boxes."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    if status == "success":
        painter.setBrush(QColor("#28a745"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(2, 2, size - 4, size - 4)

        pen = QPen(QColor("#ffffff"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawLine(int(size * 0.28), int(size * 0.52), int(size * 0.44), int(size * 0.68))
        painter.drawLine(int(size * 0.44), int(size * 0.68), int(size * 0.72), int(size * 0.34))
    else:
        painter.setBrush(QColor("#dc3545"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(2, 2, size - 4, size - 4)

        pen = QPen(QColor("#ffffff"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        margin = int(size * 0.30)
        painter.drawLine(margin, margin, size - margin, size - margin)
        painter.drawLine(size - margin, margin, margin, size - margin)

    painter.end()
    return pixmap


class SettingsWrapper:
    def __init__(self, config_path):
        self.path = config_path
        self.data = {}
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception:
                pass

    def value(self, key, default):
        return self.data.get(key, default)

    def setValue(self, key, value):
        self.data[key] = value
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        except Exception:
            pass


class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setWindowTitle("Preferences")
        self.resize(440, 320)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(script_dir, "darkkalk+_internal", "icons", "darkkalk+_icon.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        main_layout = QVBoxLayout(self)

        self.tabs = QTabWidget(self)

        # Tab 1: Calculation Options
        tab_calc = QWidget()
        calc_layout = QFormLayout(tab_calc)
        calc_layout.setContentsMargins(15, 15, 15, 15)
        calc_layout.setSpacing(12)

        self.combo_angle = QComboBox()
        self.combo_angle.addItems(["Degrees", "Radians"])
        calc_layout.addRow("Trigonometry Angle Mode:", self.combo_angle)

        curr_date = QDate.currentDate()
        logical_example = curr_date.toString("yyyy-MM-dd")
        system_example = QLocale.system().toString(curr_date, QLocale.FormatType.ShortFormat)

        dt_group_widget = QWidget()
        dt_group_layout = QVBoxLayout(dt_group_widget)
        dt_group_layout.setContentsMargins(0, 0, 0, 0)
        dt_group_layout.setSpacing(6)

        self.rb_datetime_logical = QRadioButton(f"Logical ({logical_example})")
        self.rb_datetime_system = QRadioButton(f"System ({system_example})")
        self.rb_datetime_disabled = QRadioButton("Disabled")

        self.btn_group_datetime = QButtonGroup(self)
        self.btn_group_datetime.addButton(self.rb_datetime_logical)
        self.btn_group_datetime.addButton(self.rb_datetime_system)
        self.btn_group_datetime.addButton(self.rb_datetime_disabled)

        dt_group_layout.addWidget(self.rb_datetime_logical)
        dt_group_layout.addWidget(self.rb_datetime_system)
        dt_group_layout.addWidget(self.rb_datetime_disabled)

        calc_layout.addRow("Date && Time Settings:", dt_group_widget)

        self.chk_disable_sound = QCheckBox("Disable Notification Sounds")
        self.chk_disable_sound.setToolTip("Mutes all audio chimes and notification sounds.")
        calc_layout.addRow("", self.chk_disable_sound)

        self.tabs.addTab(tab_calc, "General")
        main_layout.addWidget(self.tabs)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.save_and_close)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

        self.load_values()

    def load_values(self):
        if self.parent_app and hasattr(self.parent_app, 'settings'):
            s = self.parent_app.settings
            self.chk_disable_sound.setChecked(s.value("disable_notification_sounds", False))
            angle_mode = s.value("angle_mode", "Degrees")
            idx = self.combo_angle.findText(angle_mode)
            if idx >= 0:
                self.combo_angle.setCurrentIndex(idx)

            dt_setting = s.value("datetime_format", "Logical")
            if dt_setting == "System":
                self.rb_datetime_system.setChecked(True)
            elif dt_setting == "Disabled":
                self.rb_datetime_disabled.setChecked(True)
            else:
                self.rb_datetime_logical.setChecked(True)

    def save_and_close(self):
        if self.parent_app and hasattr(self.parent_app, 'settings'):
            s = self.parent_app.settings
            s.setValue("disable_notification_sounds", self.chk_disable_sound.isChecked())
            s.setValue("angle_mode", self.combo_angle.currentText())

            if self.rb_datetime_system.isChecked():
                s.setValue("datetime_format", "System")
            elif self.rb_datetime_disabled.isChecked():
                s.setValue("datetime_format", "Disabled")
            else:
                s.setValue("datetime_format", "Logical")
        self.accept()





from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtGui import QFont, QKeySequence, QShortcut


class DarkkalkPlus(QMainWindow):
    def __init__(self):
        super().__init__()
        QApplication.setCursorFlashTime(0)
        self.setWindowTitle(f"Darkkalk+ v{APP_VERSION}")

        script_dir = os.path.dirname(os.path.realpath(__file__))
        internal_dir = os.path.join(script_dir, "darkkalk+_internal")
        os.makedirs(internal_dir, exist_ok=True)
        self.config_file = os.path.join(internal_dir, "darkkalk+.config.json")

        icon_path = os.path.join(internal_dir, "icons", "darkkalk+_icon.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        if sys.platform == "win32":
            myappid = f"pwshAgyjkcrg761.darkkalkplus.{APP_VERSION}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.default_size = (800, 580)
        self.setMinimumSize(750, 560)
        self.settings = SettingsWrapper(self.config_file)
        self.load_geometry()

        self.history_file = os.path.join(internal_dir, "darkkalk+.history.json")
        self.history_data = {"input_history": [], "calculation_history": []}

        self.memory_val = 0.0
        self.has_memory = False
        self.last_ans = 0.0

        self.current_theme = self.settings.value("theme", "Dark")

        self.init_ui()
        self.load_history()
        self.apply_theme(self.current_theme)
        self.setup_shortcuts()

    def init_ui(self):
        self.create_menu()

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # ----------------- Left Pane: History -----------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        self.lbl_title = QLabel("Darkkalk+")
        self.lbl_title.setFont(QFont("Verdana", 14, QFont.Weight.Bold))
        left_layout.addWidget(self.lbl_title)

        self.txt_history = QTextBrowser()
        self.txt_history.document().setDocumentMargin(8)
        self.txt_history.setStyleSheet("""
            QTextBrowser {
                font-family: 'Consolas', 'Segoe UI', monospace;
                font-size: 14px;
                border: 2px solid #3c3c3c;
                border-radius: 4px;
                padding: 0px;
            }
        """)
        left_layout.addWidget(self.txt_history, 1)

        self.btn_clear_history = QPushButton("Clear History")
        self.btn_clear_history.setMinimumHeight(42)
        self.btn_clear_history.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_clear_history.setStyleSheet("font-family: 'Verdana', 'Segoe UI', sans-serif; font-size: 13px; font-weight: bold;")
        self.btn_clear_history.clicked.connect(self.clear_history)
        left_layout.addWidget(self.btn_clear_history)

        main_layout.addWidget(left_widget, 5)

        # ----------------- Right Pane: Calculator & Grid -----------------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(6)

        self.txt_display = QLineEdit()
        self.txt_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_display.setMinimumHeight(52)
        self.txt_display.setStyleSheet("""
            QLineEdit {
                font-family: 'Verdana', 'Segoe UI', sans-serif;
                font-size: 24px;
                font-weight: bold;
                color: #4a90e2;
                border: 2px solid #4e5058;
                border-radius: 4px;
                padding: 4px 12px;
            }
        """)
        self.txt_display.returnPressed.connect(self.calculate_result)
        self.txt_display.installEventFilter(self)
        input_layout.addWidget(self.txt_display, 1)

        self.btn_history_dropdown = QPushButton("▼")
        self.btn_history_dropdown.setFixedSize(52, 52)
        self.btn_history_dropdown.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_history_dropdown.setToolTip("Past Inputs")
        self.btn_history_dropdown.clicked.connect(self.show_input_history_menu)
        input_layout.addWidget(self.btn_history_dropdown)

        right_layout.addWidget(input_container)

        # 5 Columns x 7 Rows Button Grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)

        buttons = [
            # Row 0
            ("MC", 0, 0), ("MR", 0, 1), ("M+", 0, 2), ("M-", 0, 3), ("MS", 0, 4),
            # Row 1
            ("sin", 1, 0), ("cos", 1, 1), ("tan", 1, 2), ("log", 1, 3), ("pi", 1, 4),
            # Row 2
            ("(", 2, 0), (")", 2, 1), ("%", 2, 2), ("", 2, 3), ("C", 2, 4),
            # Row 3
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("/", 3, 3), ("sqrt", 3, 4),
            # Row 4
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("*", 4, 3), ("^", 4, 4),
            # Row 5
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("-", 5, 3), ("DEL", 5, 4),
            # Row 6
            ("0", 6, 0), (".", 6, 1), ("=", 6, 2), ("+", 6, 3), ("Ans", 6, 4)
        ]

        self.grid_buttons = {}
        for text, r, c in buttons:
            if not text:
                continue
            btn = QPushButton(text)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setMinimumHeight(55)
            btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            self.grid_buttons[text] = btn
            grid_layout.addWidget(btn, r, c)

        right_layout.addLayout(grid_layout, 1)
        main_layout.addWidget(right_widget, 5)

        self.setCentralWidget(main_widget)
        self.txt_display.setFocus()

    def setup_shortcuts(self):
        sc_esc = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        sc_esc.activated.connect(self.clear_display)

    def flash_button(self, key_text):
        btn = self.grid_buttons.get(key_text)
        if btn:
            btn.setDown(True)
            QTimer.singleShot(120, lambda: btn.setDown(False))

    def insert_with_auto_close(self, prefix):
        pos = self.txt_display.cursorPosition()
        if self.txt_display.hasSelectedText():
            sel = self.txt_display.selectedText()
            self.txt_display.insert(f"{prefix}{sel})")
            self.txt_display.setCursorPosition(pos + len(prefix) + len(sel) + 1)
        else:
            self.txt_display.insert(f"{prefix})")
            self.txt_display.setCursorPosition(pos + len(prefix))
        self.txt_display.setFocus()

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj == self.txt_display and event.type() == QEvent.Type.KeyPress:
            k = event.key()
            t = event.text()

            if not self.txt_display.text().strip() and t in ("+", "-", "*", "/", "^", "%"):
                if t in self.grid_buttons:
                    self.flash_button(t)
                self.txt_display.setText(f"Ans{t}")
                return True

            if t == "(":
                self.flash_button("(")
                self.insert_with_auto_close("(")
                return True
            elif t == ")":
                pos = self.txt_display.cursorPosition()
                cur_text = self.txt_display.text()
                if pos < len(cur_text) and cur_text[pos] == ")":
                    self.flash_button(")")
                    self.txt_display.setCursorPosition(pos + 1)
                    return True
            elif k == Qt.Key.Key_Backspace and not self.txt_display.hasSelectedText():
                pos = self.txt_display.cursorPosition()
                cur_text = self.txt_display.text()
                if 0 < pos < len(cur_text) and cur_text[pos - 1] == "(" and cur_text[pos] == ")":
                    self.flash_button("DEL")
                    self.txt_display.setText(cur_text[:pos - 1] + cur_text[pos + 1:])
                    self.txt_display.setCursorPosition(pos - 1)
                    return True

            if k in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Equal) and not t == "+":
                self.flash_button("=")
            elif k == Qt.Key.Key_Backspace:
                self.flash_button("DEL")
            elif k == Qt.Key.Key_Escape:
                self.flash_button("C")
            elif t in self.grid_buttons:
                self.flash_button(t)

        return super().eventFilter(obj, event)

    def update_memory_indicator(self):
        btn_ms = self.grid_buttons.get("MS")
        btn_mc = self.grid_buttons.get("MC")
        btn_mr = self.grid_buttons.get("MR")

        if self.has_memory:
            if btn_ms:
                btn_ms.setStyleSheet("QPushButton { background-color: #28a745; color: #ffffff; border: 2px solid #218838; font-weight: bold; } QPushButton:hover { background-color: #218838; } QPushButton:pressed { background-color: #007acc; border: 2px solid #388bfd; color: #ffffff; }")
            if btn_mc:
                btn_mc.setStyleSheet("QPushButton { background-color: #dc3545; color: #ffffff; border: 2px solid #c82333; font-weight: bold; } QPushButton:hover { background-color: #c82333; } QPushButton:pressed { background-color: #007acc; border: 2px solid #388bfd; color: #ffffff; }")
            if btn_mr:
                btn_mr.setStyleSheet("QPushButton { background-color: #c68a00; color: #ffffff; border: 2px solid #9e6e00; font-weight: bold; } QPushButton:hover { background-color: #a87500; } QPushButton:pressed { background-color: #007acc; border: 2px solid #388bfd; color: #ffffff; }")
        else:
            if btn_ms:
                btn_ms.setStyleSheet("")
            if btn_mc:
                btn_mc.setStyleSheet("")
            if btn_mr:
                btn_mr.setStyleSheet("")

    def on_button_click(self, text):
        if text == "=":
            self.calculate_result()
        elif text == "C":
            self.clear_display()
        elif text == "DEL":
            self.delete_last_char()
        elif text in ("sin", "cos", "tan", "log", "sqrt"):
            self.insert_with_auto_close(f"{text}(")
        elif text == "(":
            self.insert_with_auto_close("(")
        elif text == ")":
            pos = self.txt_display.cursorPosition()
            cur_text = self.txt_display.text()
            if pos < len(cur_text) and cur_text[pos] == ")":
                self.txt_display.setCursorPosition(pos + 1)
            else:
                self.txt_display.insert(")")
            self.txt_display.setFocus()
        elif text == "pi":
            self.txt_display.insert("pi")
            self.txt_display.setFocus()
        elif text == "Ans":
            self.txt_display.insert("Ans")
            self.txt_display.setFocus()
        elif text == "MC":
            self.memory_val = 0.0
            self.has_memory = False
            self.update_memory_indicator()
            self.txt_display.setFocus()
        elif text == "MR":
            self.txt_display.insert(str(int(self.memory_val) if self.memory_val.is_integer() else self.memory_val))
            self.txt_display.setFocus()
        elif text == "MS":
            try:
                curr = float(self.txt_display.text().strip() or "0")
                self.memory_val = curr
                self.has_memory = True
                self.update_memory_indicator()
            except Exception:
                pass
            self.txt_display.setFocus()
        elif text == "M+":
            try:
                curr = float(self.txt_display.text().strip() or "0")
                self.memory_val += curr
                self.has_memory = True
                self.update_memory_indicator()
            except Exception:
                pass
            self.txt_display.setFocus()
        elif text == "M-":
            try:
                curr = float(self.txt_display.text().strip() or "0")
                self.memory_val -= curr
                self.has_memory = True
                self.update_memory_indicator()
            except Exception:
                pass
            self.txt_display.setFocus()
        elif text in ("+", "-", "*", "/", "^", "%"):
            if not self.txt_display.text().strip():
                self.txt_display.setText(f"Ans{text}")
            else:
                self.txt_display.insert(text)
            self.txt_display.setFocus()
        else:
            self.txt_display.insert(text)
            self.txt_display.setFocus()

    def format_history_entry_html(self, date_str, time_str, expr, res):
        is_err = res.startswith("Error")
        res_color = "#f04747" if is_err else "#4a90e2"
        res_size = "16px" if is_err else "18px"

        dt_format = self.settings.value("datetime_format", "Logical")
        header_html = ""
        if dt_format != "Disabled":
            display_dt = f"{date_str}<br>{time_str}"
            if dt_format == "System":
                try:
                    from datetime import datetime
                    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                    q_d = QDate(dt.year, dt.month, dt.day)
                    sys_date = QLocale.system().toString(q_d, QLocale.FormatType.ShortFormat)
                    sys_time = dt.strftime("%I:%M:%S %p").lstrip("0") if sys.platform == "win32" else dt.strftime("%-I:%M:%S %p")
                    display_dt = f"{sys_date}<br>{sys_time}"
                except Exception:
                    display_dt = f"{date_str}<br>{time_str}"
            header_html = f'<tr>\n                <td align="left" style="color: #8e9297; font-size: 11px; line-height: 1.2;">{display_dt}</td>\n            </tr>'

        return f"""
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 22px; font-family: 'Verdana', 'Segoe UI', sans-serif;">
            {header_html}
            <tr>
                <td align="left" style="color: #dcddde; font-size: 14px; padding-top: 4px;">{expr}</td>
            </tr>
            <tr>
                <td align="right" style="color: {res_color}; font-size: {res_size}; font-weight: bold; padding-top: 2px;">{res}</td>
            </tr>
        </table>
        """

    def calculate_result(self):
        from datetime import datetime
        expr = self.txt_display.text().strip()
        if not expr:
            return

        angle_mode = self.settings.value("angle_mode", "Degrees")
        res = evaluate_math_expression(expr, ans_val=self.last_ans, use_degrees=(angle_mode == "Degrees"))

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        # Save to in-memory history data
        inputs = self.history_data.setdefault("input_history", [])
        if expr in inputs:
            inputs.remove(expr)
        inputs.append(expr)

        calc_list = self.history_data.setdefault("calculation_history", [])
        calc_list.append({
            "date": date_str,
            "time": time_str,
            "expression": expr,
            "result": res
        })
        self.save_history()

        is_err = res.startswith("Error")
        if not is_err:
            self.last_ans = res

        entry_html = self.format_history_entry_html(date_str, time_str, expr, res)
        self.txt_history.append(entry_html)
        if not is_err:
            self.txt_display.clear()

        sb = self.txt_history.verticalScrollBar()
        if sb:
            sb.setValue(sb.maximum())

    def clear_display(self):
        self.txt_display.clear()
        self.txt_display.setFocus()

    def delete_last_char(self):
        t = self.txt_display.text()
        if t:
            self.txt_display.setText(t[:-1])
        self.txt_display.setFocus()

    def clear_input_history(self):
        self.history_data["input_history"] = []
        self.save_history()
        self.txt_display.setFocus()

    def clear_output(self):
        self.txt_history.clear()
        self.history_data["calculation_history"] = []
        self.save_history()
        self.txt_display.setFocus()

    def clear_history(self):
        self.clear_output()

    def clear_all(self):
        self.txt_display.clear()
        self.txt_history.clear()
        self.history_data = {"input_history": [], "calculation_history": []}
        self.save_history()
        self.txt_display.setFocus()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history_data = json.load(f)
            except Exception:
                self.history_data = {"input_history": [], "calculation_history": []}

        if not isinstance(self.history_data, dict):
            self.history_data = intelligence_data = {"input_history": [], "calculation_history": []}
        self.history_data.setdefault("input_history", [])
        self.history_data.setdefault("calculation_history", [])

        self.txt_history.clear()
        for item in self.history_data.get("calculation_history", []):
            date_str = item.get("date", "")
            time_str = item.get("time", "")
            expr = item.get("expression", "")
            res = item.get("result", "")
            entry_html = self.format_history_entry_html(date_str, time_str, expr, res)
            self.txt_history.append(entry_html)

        sb = self.txt_history.verticalScrollBar()
        if sb:
            sb.setValue(sb.maximum())

    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history_data, f, indent=4)
        except Exception:
            pass

    def show_input_history_menu(self):
        import time
        now = time.time()
        if now - getattr(self, '_history_menu_closed_time', 0) < 0.25:
            self.txt_display.setFocus()
            return

        menu = QMenu(self)
        menu.aboutToHide.connect(lambda: setattr(self, '_history_menu_closed_time', time.time()))

        inputs = self.history_data.get("input_history", [])
        if not inputs:
            for _ in range(6):
                act = menu.addAction(" ")
                act.setEnabled(False)
        else:
            for item_text in reversed(inputs[-30:]):
                act = menu.addAction(item_text)
                act.triggered.connect(lambda checked, t=item_text: self.set_input_from_history(t))

        pos = self.txt_display.mapToGlobal(self.txt_display.rect().bottomLeft())
        total_width = self.txt_display.width() + self.btn_history_dropdown.width() + 6
        menu.setMinimumWidth(total_width)
        menu.exec(pos)
        self.txt_display.setFocus()

    def set_input_from_history(self, text):
        self.txt_display.setText(text)
        self.txt_display.setFocus()

    def load_geometry(self):
        self.resize(*self.default_size)
        if os.path.exists(self.config_file):
            try:
                if "x" in self.settings.data and "y" in self.settings.data:
                    self.move(self.settings.value("x", 100), self.settings.value("y", 100))
                else:
                    self.center_window()
                self.resize(self.settings.value("width", self.default_size[0]),
                            self.settings.value("height", self.default_size[1]))
            except Exception as e:
                print(f"Error loading geometry: {e}")
                self.center_window()
        else:
            self.center_window()

    def center_window(self):
        frame_geo = self.frameGeometry()
        screen = QApplication.primaryScreen().availableGeometry().center()
        frame_geo.moveCenter(screen)
        self.move(frame_geo.topLeft())

    def closeEvent(self, event):
        pos = self.pos()
        self.settings.setValue("x", pos.x())
        self.settings.setValue("y", pos.y())
        self.settings.setValue("width", self.width())
        self.settings.setValue("height", self.height())
        self.settings.setValue("theme", self.current_theme)
        event.accept()

    def print_output(self):
        try:
            from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
            from PyQt6.QtGui import QTextDocument, QPainter, QFont, QPen, QColor
            from PyQt6.QtCore import QRectF, QSizeF, Qt

            printer = QPrinter()
            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle("Print Calculation Output")
            # Enabling PrintToFile unlocks 'Microsoft Print to PDF' and other virtual port-prompt printers in Windows
            dialog.setOption(QPrintDialog.PrintDialogOption.PrintToFile, True)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                doc = QTextDocument()
                raw_html = self.txt_history.toHtml()
                # Scale font sizes, margins, and line spacing by 300% (3x) for high-DPI print output
                scaled_html = re.sub(r'(\d+)px', lambda m: f"{int(m.group(1)) * 3}px", raw_html)
                # Ensure light theme text prints as high-contrast dark text on white pages
                scaled_html = scaled_html.replace('#dcddde', '#111111').replace('#ffffff', '#000000')
                doc.setHtml(scaled_html)

                page_rect = printer.pageLayout().paintRectPixels(printer.resolution())
                page_width = float(page_rect.width())
                page_height = float(page_rect.height())

                # Compact running header height (~0.28 inches)
                header_height = max(30.0, float(int(20 * printer.resolution() / 72)))
                content_height = page_height - header_height

                doc.setPageSize(QSizeF(page_width, content_height))
                page_count = max(1, doc.pageCount())

                painter = QPainter(printer)
                for page_idx in range(page_count):
                    if page_idx > 0:
                        printer.newPage()

                    # Draw small, unobtrusive running header
                    painter.setFont(QFont("Segoe UI", 8))
                    painter.setPen(QColor("#777777"))
                    header_rect = QRectF(0, 0, page_width, header_height * 0.7)
                    painter.drawText(header_rect, int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter), f"Darkkalk+ v{APP_VERSION}")
                    painter.drawText(header_rect, int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter), f"Page {page_idx + 1} of {page_count}")

                    # Thin subtle divider rule
                    painter.setPen(QPen(QColor("#d0d0d0"), 1))
                    line_y = header_height * 0.85
                    painter.drawLine(0, int(line_y), int(page_width), int(line_y))

                    # Render document content slice for this page
                    painter.save()
                    painter.translate(0, header_height)
                    painter.setClipRect(QRectF(0, 0, page_width, content_height))
                    painter.translate(0, -page_idx * content_height)
                    doc.drawContents(painter, QRectF(0, page_idx * content_height, page_width, content_height))
                    painter.restore()

                painter.end()
        except Exception as e:
            self.show_alert("Print Error", f"Could not print output:\n{e}", icon_type="error")

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        print_action = file_menu.addAction("Print Output")
        print_action.setShortcut(QKeySequence("Ctrl+P"))
        print_action.triggered.connect(self.print_output)

        file_menu.addSeparator()

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        edit_menu = menu_bar.addMenu("&Edit")
        cut_action = edit_menu.addAction("Cut")
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(lambda: self.txt_display.cut() if self.txt_display.hasSelectedText() else (QApplication.clipboard().setText(self.txt_display.text()), self.txt_display.clear()))

        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(lambda: self.txt_display.copy() if self.txt_display.hasSelectedText() else QApplication.clipboard().setText(self.txt_display.text()))

        paste_action = edit_menu.addAction("Paste")
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(lambda: self.txt_display.paste())

        edit_menu.addSeparator()

        clear_menu = edit_menu.addMenu("Clear")
        clear_input_action = clear_menu.addAction("Input")
        clear_input_action.triggered.connect(lambda: self.clear_input_history())

        clear_output_action = clear_menu.addAction("Output")
        clear_output_action.setShortcut(QKeySequence("Ctrl+Del"))
        clear_output_action.triggered.connect(lambda: self.clear_output())

        clear_menu.addSeparator()

        clear_all_action = clear_menu.addAction("All")
        clear_all_action.triggered.connect(lambda: self.clear_all())

        options_menu = menu_bar.addMenu("&Options")
        themes_menu = options_menu.addMenu("&Themes")

        self.theme_group = QActionGroup(self)
        self.theme_group.setExclusive(True)

        for theme in ["Dark", "Light", "System"]:
            action = themes_menu.addAction(theme)
            action.setCheckable(True)
            self.theme_group.addAction(action)
            action.triggered.connect(lambda checked, t=theme: self.change_theme(t))

        saved_theme = self.settings.value("theme", "Dark")
        for action in self.theme_group.actions():
            if action.text() == saved_theme:
                action.setChecked(True)

        options_menu.addSeparator()
        pref_action = options_menu.addAction("&Preferences")
        pref_action.triggered.connect(self.show_preferences)

        help_menu = menu_bar.addMenu("&Help")
        manual_action = help_menu.addAction("Manual")
        manual_action.triggered.connect(self.show_manual)
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

    def show_preferences(self):
        dialog = PreferencesDialog(self)
        if dialog.exec():
            self.load_history()

    def apply_theme(self, theme_name):
        app = QApplication.instance()
        app.setStyle("Fusion")

        if theme_name == "System":
            is_dark = app.style().standardPalette().color(QPalette.ColorRole.Window).lightness() < 128
            effective_theme = "Dark" if is_dark else "Light"
        else:
            effective_theme = theme_name

        if sys.platform == "win32":
            try:
                hwnd = int(self.winId())
                val = ctypes.c_int(1 if effective_theme == "Dark" else 0)
                for attr in (20, 19):
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd, attr, ctypes.byref(val), ctypes.sizeof(val)
                    )
            except Exception:
                pass

        palette = QPalette(app.style().standardPalette())

        if effective_theme == "Dark":
            palette.setColor(QPalette.ColorRole.Window, QColor("#202225"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#2b2d31"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#202225"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#202225"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#2b2d31"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#aaaaaa"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#007acc"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))

            app.setStyleSheet("""
                QMenuBar {
                    background-color: #202225;
                    color: #ffffff;
                }
                QMenuBar::item {
                    background-color: transparent;
                    color: #ffffff;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background-color: #3b3e45;
                }
                QMenu {
                    background-color: #202225;
                    color: #ffffff;
                    border: 1px solid #4e5058;
                }
                QMenu::item {
                    color: #ffffff;
                    padding: 4px 20px 4px 20px;
                }
                QMenu::item:selected {
                    background-color: #007acc;
                    color: #ffffff;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #4e5058;
                    margin: 4px 8px;
                }
                QLabel {
                    color: #ffffff;
                }
                QPushButton {
                    font-family: 'Verdana', 'Segoe UI', sans-serif;
                    background-color: #2b2d31;
                    color: #ffffff;
                    border: 2px solid #4e5058;
                    border-radius: 4px;
                    font-size: 13px;
                    font-weight: bold;
                    padding: 4px;
                }
                QPushButton:hover {
                    background-color: #3b3e45;
                    border: 2px solid #949ba4;
                    color: #ffffff;
                }
                QPushButton:pressed {
                    background-color: #007acc;
                    border: 2px solid #388bfd;
                    color: #ffffff;
                }
                QLineEdit, QTextBrowser {
                    background-color: #2b2d31;
                    color: #ffffff;
                    border: 2px solid #4e5058;
                    border-radius: 4px;
                }
            """)
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#fcfcfc"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#e1e1e1"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#777777"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#0078d7"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))

            app.setStyleSheet("""
                QMenuBar {
                    background-color: #f0f0f0;
                    color: #000000;
                }
                QMenuBar::item {
                    background-color: transparent;
                    color: #000000;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background-color: #e5f1fb;
                }
                QMenu {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #b0b0b0;
                }
                QMenu::item {
                    color: #000000;
                    padding: 4px 20px 4px 20px;
                }
                QMenu::item:selected {
                    background-color: #0078d7;
                    color: #ffffff;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #b0b0b0;
                    margin: 4px 8px;
                }
                QLabel {
                    color: #000000;
                }
                QPushButton {
                    font-family: 'Verdana', 'Segoe UI', sans-serif;
                    background-color: #f2f2f2;
                    color: #000000;
                    border: 2px solid #b0b0b0;
                    border-radius: 4px;
                    font-size: 13px;
                    font-weight: bold;
                    padding: 4px;
                }
                QPushButton:hover {
                    background-color: #e5f1fb;
                    border: 2px solid #0078d7;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #0078d7;
                    border: 2px solid #005499;
                    color: #ffffff;
                }
                QLineEdit, QTextBrowser {
                    background-color: #ffffff;
                    color: #000000;
                    border: 2px solid #b0b0b0;
                    border-radius: 4px;
                }
            """)

        app.setPalette(palette)
        self.update_memory_indicator()

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme(theme_name)

    def show_manual(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Manual")
        dialog.resize(600, 420)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(script_dir, "darkkalk+_internal", "icons", "darkkalk+_icon.svg")
        if os.path.exists(icon_path):
            dialog.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout(dialog)

        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setStyleSheet("""
            QTextBrowser {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                line-height: 1.6;
                color: palette(text);
                background-color: palette(base);
                border: none;
                padding: 15px;
            }
            h1 { color: #007acc; font-size: 20px; }
            h2 { color: #007acc; font-size: 16px; border-bottom: 1px solid #444; padding-bottom: 4px; margin-top: 15px; }
            b { color: #007acc; }
        """)

        manual_text = (
            f"<h1>Darkkalk+ v{APP_VERSION}</h1>"
            f"<p>A scientific and arithmetic expression calculator written in Python and PyQt6 under GPLv3.</p>"
            f"<h2>KEYPAD &amp; FUNCTIONS</h2>"
            f"<ul>"
            f"<li><b>Basic Operations:</b> <code>+</code>, <code>-</code>, <code>*</code>, <code>/</code>, <code>^</code> (exponent), <code>%</code> (percentage).</li>"
            f"<li><b>Scientific Functions:</b> <code>sin</code>, <code>cos</code>, <code>tan</code>, <code>log</code> (log10), <code>sqrt</code>, <code>pi</code>.</li>"
            f"<li><b>Memory Keys:</b> <code>MC</code> (Clear), <code>MR</code> (Recall), <code>MS</code> (Store), <code>M+</code> (Add), <code>M-</code> (Subtract).</li>"
            f"<li><b>Ans Key:</b> Inserts the previous calculation's result into the current formula.</li>"
            f"</ul>"
            f"<h2>SHORTCUTS</h2>"
            f"<ul>"
            f"<li><b>Enter / Return:</b> Evaluate expression.</li>"
            f"<li><b>Escape:</b> Clear expression.</li>"
            f"<li><b>Ctrl+C / Ctrl+V:</b> Copy result and paste into expression.</li>"
            f"</ul>"
        )

        text_browser.setHtml(manual_text)
        layout.addWidget(text_browser)

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)

        dialog.exec()

    def show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About")
        dialog.resize(480, 320)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(script_dir, "darkkalk+_internal", "icons", "darkkalk+_icon.svg")
        if os.path.exists(icon_path):
            dialog.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout(dialog)
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setStyleSheet("""
            QTextBrowser {
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                color: palette(text);
                background-color: palette(base);
                border: none;
                padding: 10px;
            }
            h1 { color: #007acc; font-size: 18px; }
            b { color: #007acc; }
        """)

        about_text = (
            f"<h1>Darkkalk+ v{APP_VERSION}</h1>"
            "<p>Copyright (C) 2026 <b>pwshAgyjkcrg761</b><br>"
            "Licensed under <b>GPLv3</b></p>"
            "<p>Official License: <a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">gnu.org/licenses/gpl-3.0.html</a></p>"
            "<hr>"
            "<p><b>Icon Credits:</b><br>"
            "'<a href=\"https://www.svgrepo.com/svg/253926/calculator\">Calculator SVG Vector</a>' by <a href=\"https://www.svgrepo.com/\">SVGRepo</a>.<br>"
            "Used under <a href=\"https://creativecommons.org/publicdomain/zero/1.0/\">CC0 License</a>. Modified by pwshAgyjkcrg761.</p>"
        )
        text_browser.setHtml(about_text)
        layout.addWidget(text_browser)

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(dialog.accept)
        layout.addWidget(btn_ok, alignment=Qt.AlignmentFlag.AlignRight)

        dialog.exec()

    def show_alert(self, title, text, icon_type="info", buttons=QMessageBox.StandardButton.Ok, default_button=None):
        sound_disabled = False
        if hasattr(self, 'settings'):
            sound_disabled = self.settings.value("disable_notification_sounds", False)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(script_dir, "darkkalk+_internal", "icons", "darkkalk+_icon.svg")

        msg_box = QMessageBox(self if self.isVisible() else None)
        msg_box.setWindowTitle(f"Darkkalk+ - {title}")
        msg_box.setText(text)
        msg_box.setStandardButtons(buttons)
        if default_button:
            msg_box.setDefaultButton(default_button)

        if os.path.exists(icon_path):
            msg_box.setWindowIcon(QIcon(icon_path))

        if icon_type == "success":
            msg_box.setIconPixmap(get_status_pixmap("success"))
        elif icon_type == "error":
            msg_box.setIconPixmap(get_status_pixmap("error"))
        elif icon_type == "warning":
            if not sound_disabled:
                msg_box.setIcon(QMessageBox.Icon.Warning)
            else:
                std_icon = self.style().standardIcon(self.style().StandardPixmap.SP_MessageBoxWarning)
                msg_box.setIconPixmap(std_icon.pixmap(48, 48))
        elif icon_type == "question":
            if not sound_disabled:
                msg_box.setIcon(QMessageBox.Icon.Question)
            else:
                std_icon = self.style().standardIcon(self.style().StandardPixmap.SP_MessageBoxQuestion)
                msg_box.setIconPixmap(std_icon.pixmap(48, 48))
        elif icon_type == "info":
            if not sound_disabled:
                msg_box.setIcon(QMessageBox.Icon.Information)
            else:
                std_icon = self.style().standardIcon(self.style().StandardPixmap.SP_MessageBoxInformation)
                msg_box.setIconPixmap(std_icon.pixmap(48, 48))

        return msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = DarkkalkPlus()
    window.show()
    sys.exit(app.exec())