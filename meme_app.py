import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsTextItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QSpinBox,
    QLabel,
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PIL import Image, ImageFont, ImageDraw
import numpy as np


class MemeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meme Editor")
        self.initUI()

    def initUI(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Create a QGraphicsScene and QGraphicsView
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        main_layout.addWidget(self.view)

        # Load the full resolution image using QPixmap
        self.image_path = "imgs/meme.png"
        self.original_pixmap = QPixmap(self.image_path)
        self.full_width = self.original_pixmap.width()
        self.full_height = self.original_pixmap.height()

        # Downsample for display if the image is too big
        max_display_width = 800  # adjust as needed
        if self.full_width > max_display_width:
            self.scale_factor = self.full_width / max_display_width
            self.display_pixmap = self.original_pixmap.scaledToWidth(max_display_width, Qt.SmoothTransformation)
        else:
            self.scale_factor = 1.0
            self.display_pixmap = self.original_pixmap

        # Add the downsampled image to the scene
        self.pixmap_item = QGraphicsPixmapItem(self.display_pixmap)
        self.scene.addItem(self.pixmap_item)

        # Define positions for the text on the full-resolution image
        top_text_full_pos = (280, 30)
        bottom_text_full_pos = (170, self.full_height - 100)

        # Convert full resolution positions to display positions (divide by scale_factor)
        top_text_display_pos = (top_text_full_pos[0] / self.scale_factor, top_text_full_pos[1] / self.scale_factor)
        bottom_text_display_pos = (
            bottom_text_full_pos[0] / self.scale_factor,
            bottom_text_full_pos[1] / self.scale_factor,
        )

        # Create text items
        self.top_text_item = QGraphicsTextItem("ONE DOES NOT SIMPLY")
        self.bottom_text_item = QGraphicsTextItem("EXPLAIN MRI WITH NO FFT")

        # Set default font (using Impact if available)
        default_font = QFont("Impact", 40)
        self.top_text_item.setFont(default_font)
        self.bottom_text_item.setFont(default_font)

        self.top_text_item.setDefaultTextColor(Qt.white)
        self.bottom_text_item.setDefaultTextColor(Qt.white)

        # Make text items movable and selectable
        self.top_text_item.setFlags(QGraphicsTextItem.ItemIsMovable | QGraphicsTextItem.ItemIsSelectable)
        self.bottom_text_item.setFlags(QGraphicsTextItem.ItemIsMovable | QGraphicsTextItem.ItemIsSelectable)

        # Set initial positions based on the downsampled image
        self.top_text_item.setPos(*top_text_display_pos)
        self.bottom_text_item.setPos(*bottom_text_display_pos)
        self.scene.addItem(self.top_text_item)
        self.scene.addItem(self.bottom_text_item)

        # Create controls for editing text and font sizes
        controls_layout = QHBoxLayout()
        main_layout.addLayout(controls_layout)

        # Top text controls
        top_text_layout = QVBoxLayout()
        controls_layout.addLayout(top_text_layout)
        top_text_label = QLabel("Top Text:")
        self.top_text_edit = QLineEdit(self.top_text_item.toPlainText())
        self.top_font_size_spin = QSpinBox()
        self.top_font_size_spin.setRange(10, 200)
        self.top_font_size_spin.setValue(40)
        top_text_layout.addWidget(top_text_label)
        top_text_layout.addWidget(self.top_text_edit)
        top_text_layout.addWidget(QLabel("Font Size:"))
        top_text_layout.addWidget(self.top_font_size_spin)

        # Bottom text controls
        bottom_text_layout = QVBoxLayout()
        controls_layout.addLayout(bottom_text_layout)
        bottom_text_label = QLabel("Bottom Text:")
        self.bottom_text_edit = QLineEdit(self.bottom_text_item.toPlainText())
        self.bottom_font_size_spin = QSpinBox()
        self.bottom_font_size_spin.setRange(10, 200)
        self.bottom_font_size_spin.setValue(40)
        bottom_text_layout.addWidget(bottom_text_label)
        bottom_text_layout.addWidget(self.bottom_text_edit)
        bottom_text_layout.addWidget(QLabel("Font Size:"))
        bottom_text_layout.addWidget(self.bottom_font_size_spin)

        # Save button
        self.save_button = QPushButton("Save Meme")
        controls_layout.addWidget(self.save_button)

        # Connect signals to update text and font sizes
        self.top_text_edit.textChanged.connect(self.update_top_text)
        self.bottom_text_edit.textChanged.connect(self.update_bottom_text)
        self.top_font_size_spin.valueChanged.connect(self.update_top_font_size)
        self.bottom_font_size_spin.valueChanged.connect(self.update_bottom_font_size)
        self.save_button.clicked.connect(self.save_meme)

    def update_top_text(self, text):
        self.top_text_item.setPlainText(text)

    def update_bottom_text(self, text):
        self.bottom_text_item.setPlainText(text)

    def update_top_font_size(self, size):
        font = self.top_text_item.font()
        font.setPointSize(size)
        self.top_text_item.setFont(font)

    def update_bottom_font_size(self, size):
        font = self.bottom_text_item.font()
        font.setPointSize(size)
        self.bottom_text_item.setFont(font)

    def save_meme(self):
        # Open the full resolution image with Pillow
        base_image = Image.open(self.image_path)
        draw = ImageDraw.Draw(base_image)

        # Get positions from the displayed text items and convert them to full resolution
        top_pos_display = self.top_text_item.pos()
        bottom_pos_display = self.bottom_text_item.pos()
        top_pos_full = (top_pos_display.x() * self.scale_factor, top_pos_display.y() * self.scale_factor)
        bottom_pos_full = (bottom_pos_display.x() * self.scale_factor, bottom_pos_display.y() * self.scale_factor)

        # Calculate full resolution font sizes by multiplying the spin box values by the scale factor
        top_font_size_full = int(self.top_font_size_spin.value() * self.scale_factor * np.sqrt(2))
        bottom_font_size_full = int(self.bottom_font_size_spin.value() * self.scale_factor * np.sqrt(2))

        # Try to load Impact font for full resolution; fall back to default if not available
        try:
            font_top = ImageFont.truetype("impact.ttf", top_font_size_full)
            font_bottom = ImageFont.truetype("impact.ttf", bottom_font_size_full)
        except IOError:
            font_top = ImageFont.load_default()
            font_bottom = ImageFont.load_default()

        # Helper function to draw text with an outline for visibility
        def draw_text_with_outline(position, text, font, draw_obj):
            x, y = position
            outline_range = 2  # adjust to change the thickness of the outline
            # Draw outline by drawing the text multiple times in black
            for dx in range(-outline_range, outline_range + 1):
                for dy in range(-outline_range, outline_range + 1):
                    draw_obj.text((x + dx, y + dy), text, font=font, fill="black")
            # Draw the main text in white
            draw_obj.text((x, y), text, font=font, fill="white")

        # Draw the texts onto the full resolution image
        draw_text_with_outline(top_pos_full, self.top_text_item.toPlainText(), font_top, draw)
        draw_text_with_outline(bottom_pos_full, self.bottom_text_item.toPlainText(), font_bottom, draw)

        # Save the final meme in full resolution
        base_image.save("meme-out.jpg")
        print("Meme saved as meme-out.jpg")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = MemeEditor()
    editor.show()
    sys.exit(app.exec_())
