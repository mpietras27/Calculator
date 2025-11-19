from PySide6.QtCore import (
    Qt, QRectF, QPointF, QPropertyAnimation, QEasingCurve, Signal, Property
)
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QBrush


class ToggleSwitch(QWidget):
    toggled = Signal(bool)   # ⭐ REAL SIGNAL

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(52, 28)
        self.setFocusPolicy(Qt.NoFocus)    # ⭐ Prevent stealing focus

        # Internal state
        self._checked = False
        self._thumb_pos = 2

        # Animation
        self._animation = QPropertyAnimation(self, b"thumb_pos")
        self._animation.setDuration(180)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)

    # --------------------------------------------------------------
    # Property so the animation can manipulate `thumb_pos`
    # --------------------------------------------------------------
    def get_thumb_pos(self):
        return self._thumb_pos

    def set_thumb_pos(self, pos):
        self._thumb_pos = pos
        self.update()

    thumb_pos = Property(int, get_thumb_pos, set_thumb_pos)

    # --------------------------------------------------------------
    # Painting
    # --------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Track color
        track_color = QColor("#4CAF50") if self._checked else QColor("#888888")
        painter.setBrush(QBrush(track_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(0, 0, 52, 28), 14, 14)

        # Thumb color
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawEllipse(QPointF(self._thumb_pos + 12, 14), 10, 10)

    # --------------------------------------------------------------
    # Mouse Interaction
    # --------------------------------------------------------------
    def mouseReleaseEvent(self, event):
        self._checked = not self._checked
        self.toggled.emit(self._checked)     # ⭐ Emit real signal
        self._start_animation()
        event.accept()

    def _start_animation(self):
        end_pos = 52 - 28 if self._checked else 2
        self._animation.stop()
        self._animation.setStartValue(self._thumb_pos)
        self._animation.setEndValue(end_pos)
        self._animation.start()