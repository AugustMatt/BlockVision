# Bloco funcional para carregar imagem
# Ao executar abre uma janela de seleção de arquivo de imagens
# Permite a alteração do padrão de cor da leitura atraves da janela de configurações

from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QSizeF
from PyQt5.QtWidgets import QFileDialog, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
import cv2
from .node import Node
from .image_node import ImageNode

class LoadImage(Node, ImageNode):
    """
    Node that loads an image from a file and supports different color patterns.
    Inherits from Node and ImageNode to manage image loading and color settings.
    """

    def __init__(self, image_path):
        """
        Initializes the LoadImage node.
        :param image_path: Path to the SVG image representing the node.
        """
        super().__init__("Load Image")
        self.svg_renderer = QSvgRenderer(image_path)
        self.image_path = image_path
        self.color_pattern = "RGB"  # Default color pattern

    def paint(self, painter, option, widget):
        """
        Paints the SVG image for the node.
        :param painter: QPainter used to render the SVG.
        :param option: Style option for the node.
        :param widget: Widget to paint on.
        """
        if self.svg_renderer and self.svg_renderer.isValid():
            image_rect = self.boundingRect()
            image_size = QSizeF(image_rect.size())
            size = self.svg_renderer.defaultSize()
            size = QSizeF(size)
            size.scale(image_size, Qt.KeepAspectRatio)
            image_rect.setSize(size)
            self.svg_renderer.render(painter, image_rect)
            super().paint(painter, option, widget)
        else:
            print('Error rendering Load Image block.')

    def run(self):
        """
        Opens a file dialog to select an image file and loads the image based on the selected color pattern.
        """
        # Open file dialog to select an image file
        file_path, _ = QFileDialog.getOpenFileName(None, "Select Image", "", "Images (*.png *.jpg *.bmp)")

        if file_path:
            # Load image based on the selected color pattern
            if self.color_pattern == "RGB":
                self.image = cv2.imread(file_path)
            elif self.color_pattern == "Grayscale":
                self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            else:
                print('Unsupported color pattern for image loading.')
                self.image = None
        else:
            print("No file selected.")

    def optionsWindow(self):
        """
        Creates and displays a dialog window to configure color pattern settings.
        """
        dialog = QDialog()
        dialog.resize(300, 100)
        dialog.setWindowTitle("Load Image Configurations")

        # Layout for the dialog
        layout = QVBoxLayout(dialog)

        # Color pattern label
        color_label = QLabel("Color Pattern:")
        layout.addWidget(color_label)

        # Color pattern selector
        color_selector = QComboBox()
        color_selector.addItems(["RGB", "Grayscale"])
        layout.addWidget(color_selector)

        # OK button
        ok_button = QPushButton("OK")
        layout.addWidget(ok_button)

        # Button click event
        ok_button.clicked.connect(dialog.accept)

        # Update color pattern if OK button is pressed
        if dialog.exec() == QDialog.Accepted:
            self.color_pattern = color_selector.currentText()
            print(f"Color pattern changed to {self.color_pattern}! Please run the block again to apply the changes.")