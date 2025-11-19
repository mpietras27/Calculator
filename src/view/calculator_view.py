from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QEvent
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout
)
from PySide6.QtGui import QFont, QColor, QPalette, QKeyEvent

from view.widgets.toggle_switch import ToggleSwitch


class CalculatorView(QWidget):

    def __init__(self):
        super().__init__()


        self.setWindowFlag(Qt.Window)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        self.setAttribute(Qt.WA_InputMethodEnabled, True)
        self.setAttribute(Qt.WA_KeyCompression, True)

        self.controller = None
        self._current_theme = "dark"

        self.setWindowTitle("Calculator")
        self.resize(360, 540)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        self.grabKeyboard()
        self.installEventFilter(self)


        # =============== MAIN LAYOUT ===============
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        # =============== HEADER BAR ===============
        header = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(16, 16, 16, 16)
        header.setLayout(header_layout)

        self.header_title = QLabel("Calculator")
        self.header_title.setFont(QFont("Segoe UI", 20, QFont.Bold))

        # Toggle switch
        self.theme_toggle = ToggleSwitch()
        self.theme_toggle.toggled.connect(self._toggle_theme_clicked)  # connect

        header_layout.addWidget(self.header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_toggle)

        # =============== DISPLAY (D3 TWO-LINE) ===============
        display_widget = QWidget()
        display_layout = QVBoxLayout(display_widget)
        display_layout.setContentsMargins(16, 16, 16, 16)

        self.history_label = QLabel("")
        self.history_label.setFont(QFont("Segoe UI", 16))
        self.history_label.setAlignment(Qt.AlignRight)
        self.history_label.setFocusPolicy(Qt.NoFocus)

        self.entry_label = QLabel("0")
        self.entry_label.setFont(QFont("Segoe UI", 42, QFont.Bold))
        self.entry_label.setAlignment(Qt.AlignRight)
        self.history_label.setFocusPolicy(Qt.NoFocus)

        display_layout.addWidget(self.history_label)
        display_layout.addWidget(self.entry_label)

        # =============== KEYPAD (K2) ===============
        keypad = QWidget()
        grid = QGridLayout(keypad)
        grid.setSpacing(10)
        grid.setContentsMargins(16, 0, 16, 16)

        buttons = [
            ["(", ")", "C", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "–"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", "±"]
        ]

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                btn = self._create_button(text)
                grid.addWidget(btn, r, c)

        # =============== ADD TO MAIN ===============
        main_layout.addWidget(header)
        main_layout.addWidget(display_widget)
        main_layout.addStretch()
        main_layout.addWidget(keypad)

        # =============== APPLY DEFAULT THEME ===============
        self._apply_theme("dark", animate=False)

    # --------------------------------------------------
    #   CONTROLLER CONNECTION
    # --------------------------------------------------
    def set_controller(self, controller):
        self.controller = controller

    # --------------------------------------------------
    #   BUTTON CREATION
    # --------------------------------------------------
    def _create_button(self, text):
        btn = QPushButton(text)
        btn.setMinimumHeight(60)
        btn.setFont(QFont("Segoe UI", 18))

        btn.setFocusPolicy(Qt.NoFocus)

        btn.clicked.connect(lambda: self._button_clicked(text))
        return btn

    def _button_clicked(self, text):
        if self.controller:
            self.controller.handle_button(text)

    # --------------------------------------------------
    #   THEME TOGGLE HANDLER
    # --------------------------------------------------
    def _toggle_theme_clicked(self, state):
        new_theme = "light" if state else "dark"
        self._apply_theme(new_theme, animate=True)

        # Force the view to retake keyboard focus
        self.setWindowFlag(Qt.Window, True)
        self.show()             # reassert window identity
        self.activateWindow()   # OS-level activation
        self.raise_()           # bring window to front
        self.setFocus(Qt.ActiveWindowFocusReason)


    # --------------------------------------------------
    #   THEME ENGINE
    # --------------------------------------------------
    def _apply_theme(self, theme_name, animate=True):

        THEME_LIGHT = {
            "bg": "#FFFFFF",
            "fg": "#222222",
            "button_bg": "#F5F5F5",
            "button_fg": "#000000",
            "header_bg": "#EFEFEF"
        }

        THEME_DARK = {
            "bg": "#1E1E1E",
            "fg": "#FFFFFF",
            "button_bg": "#2D2D2D",
            "button_fg": "#FFFFFF",
            "header_bg": "#2B2B2B"
        }

        theme = THEME_LIGHT if theme_name == "light" else THEME_DARK

        # 1) BACKGROUND
        if animate:
            self._animate_bg(theme["bg"])
        else:
            pal = self.palette()
            pal.setColor(QPalette.Window, QColor(theme["bg"]))
            self.setPalette(pal)
            self.setAutoFillBackground(True)

        # 2) BUTTON STYLE
        self._set_button_style(theme)

        # ============================================================
        # 3) LABEL COLORS — MUST OVERRIDE EVERYTHING ABOVE
        # ============================================================
        label_style = (
            "QLabel {"
            f" color: {theme['fg']};"
            " background: transparent;"
            "}"
        )

        self.history_label.setStyleSheet(label_style)
        self.entry_label.setStyleSheet(label_style)
        self.header_title.setStyleSheet(label_style)

        # Update theme tracking
        self._current_theme = theme_name


    # --- Animate background ---
    def _animate_bg(self, target_color):
        # Quick fade animation for smoother theme transitions
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(180)
        self.anim.setStartValue(0.6)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()

        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(target_color))
        self.setPalette(pal)
        self.setAutoFillBackground(True)

    def _set_button_style(self, theme):
        css = (
            f"QPushButton {{ "
            f"background-color: {theme['button_bg']}; "
            f"color: {theme['button_fg']}; "
            f"border-radius: 10px; "
            f"font-size: 18px; "
            f"padding: 10px; }}"
            f"QPushButton:pressed {{ opacity: 0.5; }}"
        )
        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet(css)

    # --------------------------------------------------
    #   KEYBOARD SUPPORT
    # --------------------------------------------------
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text()

        if not self.controller:
            return

        # Digits
        if text.isdigit():
            self.controller.handle_button(text)
            return

        # Operators from keyboard
        if text in "+-*/.":
            mapping = {"+": "+", "-": "–", "*": "×", "/": "÷", ".": "."}
            self.controller.handle_button(mapping[text])
            return

        # Parentheses
        if text in "()":
            self.controller.handle_button(text)
            return

        # Enter / Return → "="
        if key in (Qt.Key_Return, Qt.Key_Enter):
            self.controller.handle_button("=")
            return

        # Backspace → delete last char
        if key == Qt.Key_Backspace:
            self._backspace()
            return

        # ESC → Clear
        if key == Qt.Key_Escape:
            self.controller.handle_button("C")
            return

    # --------------------------------------------------
    #   BACKSPACE HELPER
    # --------------------------------------------------
    def _backspace(self):
        if not self.controller:
            return

        entry = self.controller.entry

        if entry and entry not in {"0", "-"}:
            entry = entry[:-1]

            if entry == "" or entry == "-":
                entry = "0"

            self.controller.entry = entry
            self.controller._update_view()

    def focusInEvent(self, event):
        """
        Ensures the main window always owns keyboard focus.
        This prevents the toggle and buttons from stealing focus.
        """
        self.grabKeyboard()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """
        If the window loses focus (rare), restore keyboard on return.
        """
        self.grabKeyboard()
        super().focusOutEvent(event)


    def eventFilter(self, watched, event):
        if event.type() == QEvent.KeyPress:
            self.keyPressEvent(event)
            return True

        return super().eventFilter(watched, event)