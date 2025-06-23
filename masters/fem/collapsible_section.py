from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolButton, QSizePolicy, QFrame
from PyQt5.QtCore import Qt

class CollapsibleSection(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)

        # Обгортка рамки
        self.frame = QFrame()
        self.frame.setObjectName("CollapsibleFrame")
        self.frame.setStyleSheet("""
            QFrame#CollapsibleFrame {
                border: 1px solid #aaa;
                border-radius: 8px;
                background-color: transparent;
            }
        """)

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        # Заголовок
        self.toggle_button = QToolButton(text=title, checkable=True, checked=True)
        self.toggle_button.setObjectName("CollapseButton")
        self.toggle_button.setStyleSheet("""
            QToolButton#CollapseButton {
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 6px;
                font-weight: bold;
            }
        """)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.DownArrow)
        self.toggle_button.clicked.connect(self.on_toggle)

        # Контент
        self.content_area = QWidget()
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.content_area.setObjectName("CollapsibleContentArea")
        self.content_area.setStyleSheet("""
            QWidget#CollapsibleContentArea {
                background-color: white;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """)
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(8, 6, 8, 8)
        self.content_layout.setSpacing(6)
        self.content_area.setLayout(self.content_layout)

        # Компонування в рамці
        frame_layout.addWidget(self.toggle_button)
        frame_layout.addWidget(self.content_area)
        self.frame.setLayout(frame_layout)

        # Головне компонування віджета
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.frame)

    def on_toggle(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setArrowType(Qt.DownArrow)
            self.content_area.show()
        else:
            self.toggle_button.setArrowType(Qt.RightArrow)
            self.content_area.hide()

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

    def add_layout(self, layout):
        self.content_layout.addLayout(layout)
