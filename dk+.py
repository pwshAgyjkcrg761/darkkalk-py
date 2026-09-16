# ==============================================================================
# SCRIPT: dk+.py (Darkkalk+)
# VERSION: 2026.09.16__10.04.15
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

APP_VERSION = "2026.09.16__10.04.15"

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
    clean_expr = re.sub(r'\bAns\b', f"({float(ans_val)})", clean_expr, flags=re.IGNORECASE)
    clean_expr = re.sub(r'\bpi\b', str(math.pi), clean_expr, flags=re.IGNORECASE)
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
        "e": math.e
    }

    try:
        compiled_code = compile(clean_expr, "<string>", "eval")
        for name in compiled_code.co_names:
            if name not in allowed_names:
                raise NameError(f"Function or identifier '{name}' is not allowed.")

        result = eval(compiled_code, {"__builtins__": {}}, allowed_names)
        
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            return f"{result:.10g}"
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except ValueError as ve:
        return f"Error: {ve}"
    except Exception:
        return "Error: Invalid syntax"

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QDir, QTimer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QFileDialog, QLabel, QMessageBox, 
                             QDialog, QCheckBox, QTextBrowser, QDialogButtonBox,
                             QComboBox, QProgressBar, QHBoxLayout, QListWidget,
                             QTabWidget, QLineEdit, QFormLayout, QTreeWidget,
                             QTreeWidgetItem, QSplitter, QHeaderView, QMenu,
                             QInputDialog, QTreeView, QAbstractItemView,
                             QStackedWidget)
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
        self.resize(440, 240)

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

    def save_and_close(self):
        if self.parent_app and hasattr(self.parent_app, 'settings'):
            s = self.parent_app.settings
            s.setValue("disable_notification_sounds", self.chk_disable_sound.isChecked())
            s.setValue("angle_mode", self.combo_angle.currentText())
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

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj == self.txt_display and event.type() == QEvent.Type.KeyPress:
            k = event.key()
            t = event.text()

            if k in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Equal) and not t == "+":
                self.flash_button("=")
            elif k == Qt.Key.Key_Backspace:
                self.flash_button("DEL")
            elif k == Qt.Key.Key_Escape:
                self.flash_button("C")
            elif t in self.grid_buttons:
                self.flash_button(t)

        return super().eventFilter(obj, event)

    def on_button_click(self, text):
        if text == "=":
            self.calculate_result()
        elif text == "C":
            self.clear_display()
        elif text == "DEL":
            self.delete_last_char()
        elif text in ("sin", "cos", "tan", "log", "sqrt"):
            self.txt_display.insert(f"{text}(")
            self.txt_display.setFocus()
        elif text == "pi":
            self.txt_display.insert("pi")
            self.txt_display.setFocus()
        elif text == "Ans":
            self.txt_display.insert("Ans")
            self.txt_display.setFocus()
        elif text == "MC":
            self.memory_val = 0.0
        elif text == "MR":
            self.txt_display.insert(str(int(self.memory_val) if self.memory_val.is_integer() else self.memory_val))
            self.txt_display.setFocus()
        elif text == "MS":
            try:
                curr = float(self.txt_display.text().strip() or "0")
                self.memory_val = curr
            except Exception:
                pass
        elif text == "M+":
            try:
                curr = float(self.txt_display.text().strip() or "0")
                self.memory_val += curr
            except Exception:
                pass
        elif text == "M-":
            try:
                curr = float(self.txt_display.text().strip() or "0")
                self.memory_val -= curr
            except Exception:
                pass
        else:
            self.txt_display.insert(text)
            self.txt_display.setFocus()

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
        res_color = "#f04747" if is_err else "#4a90e2"
        if not is_err:
            try:
                self.last_ans = float(res)
            except Exception:
                pass

        entry_html = f"""
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 22px; font-family: 'Verdana', 'Segoe UI', sans-serif;">
            <tr>
                <td align="left" style="color: #8e9297; font-size: 11px; line-height: 1.2;">{date_str}<br>{time_str}</td>
            </tr>
            <tr>
                <td align="left" style="color: #dcddde; font-size: 14px; padding-top: 4px;">{expr}</td>
            </tr>
            <tr>
                <td align="right" style="color: {res_color}; font-size: 18px; font-weight: bold; padding-top: 2px;">{res}</td>
            </tr>
        </table>
        """
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

    def clear_history(self):
        self.txt_history.clear()
        self.history_data = {"input_history": [], "calculation_history": []}
        self.save_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history_data = json.load(f)
            except Exception:
                self.history_data = {"input_history": [], "calculation_history": []}

        if not isinstance(self.history_data, dict):
            self.history_data = {"input_history": [], "calculation_history": []}
        self.history_data.setdefault("input_history", [])
        self.history_data.setdefault("calculation_history", [])

        self.txt_history.clear()
        for item in self.history_data.get("calculation_history", []):
            date_str = item.get("date", "")
            time_str = item.get("time", "")
            expr = item.get("expression", "")
            res = item.get("result", "")
            is_err = res.startswith("Error")
            res_color = "#f04747" if is_err else "#4a90e2"
            res_size = "16px" if is_err else "18px"

            entry_html = f"""
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 22px; font-family: 'Verdana', 'Segoe UI', sans-serif;">
                <tr>
                    <td align="left" style="color: #8e9297; font-size: 11px; line-height: 1.2;">{date_str}<br>{time_str}</td>
                </tr>
                <tr>
                    <td align="left" style="color: #dcddde; font-size: 14px; padding-top: 4px;">{expr}</td>
                </tr>
                <tr>
                    <td align="right" style="color: {res_color}; font-size: {res_size}; font-weight: bold; padding-top: 2px;">{res}</td>
                </tr>
            </table>
            """
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

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        edit_menu = menu_bar.addMenu("&Edit")
        copy_action = edit_menu.addAction("Copy Result")
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(lambda: QApplication.clipboard().setText(self.txt_display.text()))
        paste_action = edit_menu.addAction("Paste")
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(lambda: self.txt_display.insert(QApplication.clipboard().text()))

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
        dialog.exec()

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