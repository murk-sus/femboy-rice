#!/usr/bin/env python3
"""Темы райса — окно переключения тем (обои, цвета, терминал, GRUB, Plymouth, SDDM, rEFInd)."""
import os, sys, json
from PyQt6.QtCore import Qt, QProcess, QSize
from PyQt6.QtGui import QPixmap, QIcon, QFont, QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox,
                             QPlainTextEdit, QScrollArea, QGridLayout, QFrame, QSizePolicy)

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
import rice  # noqa: E402


def rounded(pix, r):
    out = QPixmap(pix.size()); out.fill(Qt.GlobalColor.transparent)
    p = QPainter(out); p.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath(); path.addRoundedRect(0, 0, pix.width(), pix.height(), r, r)
    p.setClipPath(path); p.drawPixmap(0, 0, pix); p.end(); return out


class Card(QFrame):
    def __init__(self, t, on_pick):
        super().__init__()
        self.t = t; self.on_pick = on_pick; self.sel = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("card")
        lay = QVBoxLayout(self); lay.setContentsMargins(10, 10, 10, 12); lay.setSpacing(6)
        img = QLabel(); pv = os.path.join(t["_dir"], t.get("preview", "preview.png"))
        if os.path.exists(pv):
            img.setPixmap(rounded(QPixmap(pv).scaled(QSize(400, 225), Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                                     Qt.TransformationMode.SmoothTransformation).copy(0, 0, 400, 225), 12))
        img.setFixedSize(400, 225); lay.addWidget(img)
        self.title = QLabel(t["name"]); f = QFont(); f.setPointSize(13); f.setBold(True); self.title.setFont(f)
        lay.addWidget(self.title)
        d = QLabel(t.get("description", "")); d.setWordWrap(True); d.setMaximumWidth(400); d.setStyleSheet("opacity: .8")
        lay.addWidget(d)
        self.badge = QLabel(""); lay.addWidget(self.badge)
        self.setFixedWidth(424)
        self.restyle(False)

    def restyle(self, sel, active=False):
        self.sel = sel; acc = self.t.get("accent", "#888")
        self.setStyleSheet(f"#card {{ border: 3px solid {acc if sel else 'transparent'}; border-radius: 16px;"
                           f" background: {self.t.get('bg', '#111')}; }} QLabel {{ color: #eee; background: transparent; }}")
        self.title.setStyleSheet(f"color: {acc}")
        self.badge.setText("● активна" if active else "")
        self.badge.setStyleSheet(f"color: {self.t.get('accent2', acc)}")

    def mousePressEvent(self, e): self.on_pick(self)


class Win(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Темы райса"); self.setWindowIcon(QIcon.fromTheme("preferences-desktop-theme-global"))
        self.resize(1360, 860)
        v = QVBoxLayout(self)
        h = QLabel("Тема оформления целиком: обои на оба монитора, цвета, курсор, звуки, сплэш, Konsole/kitty, "
                   "bash/fish, fastfetch, подсветка клавиатуры, а также GRUB, rEFInd, Plymouth и SDDM.")
        h.setWordWrap(True); v.addWidget(h)
        sa = QScrollArea(); sa.setWidgetResizable(True); inner = QWidget(); self.grid = QGridLayout(inner)
        self.grid.setSpacing(18); sa.setWidget(inner); v.addWidget(sa, 1)
        self.cards = []; cur = rice.current()
        for i, t in enumerate(rice.themes()):
            c = Card(t, self.pick); self.cards.append(c); self.grid.addWidget(c, i // 3, i % 3, Qt.AlignmentFlag.AlignTop)
        self.chk_user = QCheckBox("Рабочий стол: обои, цвета, курсор, звуки, терминалы, клавиатура"); self.chk_user.setChecked(True)
        self.chk_sys = QCheckBox("Загрузка и вход: GRUB, rEFInd, Plymouth, SDDM, аватар  (спросит пароль, ~1 мин)")
        helper = os.path.exists(rice.HELPER)
        self.chk_sys.setChecked(helper); self.chk_sys.setEnabled(helper)
        if not helper: self.chk_sys.setText(self.chk_sys.text() + "  — сначала: sudo bash ~/rice-install-system.sh")
        v.addWidget(self.chk_user); v.addWidget(self.chk_sys)
        row = QHBoxLayout(); self.btn = QPushButton("Применить"); self.btn.setMinimumHeight(40)
        f = QFont(); f.setPointSize(12); f.setBold(True); self.btn.setFont(f); self.btn.clicked.connect(self.apply)
        row.addStretch(1); row.addWidget(self.btn); v.addLayout(row)
        self.log = QPlainTextEdit(); self.log.setReadOnly(True); self.log.setMaximumHeight(170)
        self.log.setFont(QFont("JetBrainsMono Nerd Font", 9)); v.addWidget(self.log)
        self.proc = None; self.picked = None
        for c in self.cards:
            if c.t["id"] == cur: self.pick(c)
        self.refresh_badges()

    def refresh_badges(self):
        cur = rice.current()
        for c in self.cards: c.restyle(c is self.picked, c.t["id"] == cur)

    def pick(self, card):
        self.picked = card; self.refresh_badges()

    def apply(self):
        if not self.picked or self.proc: return
        args = [os.path.join(HERE, "rice.py"), "apply", self.picked.t["id"]]
        if not self.chk_user.isChecked() and not self.chk_sys.isChecked(): return
        if self.chk_sys.isChecked(): args.append("--system" if self.chk_user.isChecked() else "--system-only")
        self.btn.setEnabled(False); self.log.clear()
        self.proc = QProcess(self); self.proc.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.proc.readyReadStandardOutput.connect(lambda: self.log.appendPlainText(
            bytes(self.proc.readAllStandardOutput()).decode(errors="replace").rstrip()))
        self.proc.finished.connect(self.done)
        self.proc.start(sys.executable, args)

    def done(self, code, _status):
        self.log.appendPlainText("— готово ✓" if code == 0 else f"— завершено с ошибкой (код {code}), подробности выше")
        self.proc = None; self.btn.setEnabled(True); self.refresh_badges()


if __name__ == "__main__":
    app = QApplication(sys.argv); app.setApplicationName("rice-themes"); app.setDesktopFileName("rice-themes")
    w = Win(); w.show(); sys.exit(app.exec())
