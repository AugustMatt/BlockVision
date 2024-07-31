# Bloco funcional para exibir imagem
# Ao executar exibe o conteudo de um atributo "image" do bloco funcional que esta conectado como entrada
# A exibição ocorre em uma janela redimensionavel

from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QSizeF
import cv2
from .node import Node

class DisplayImage(Node):
    """
    Node that displays an image from a connected input node.
    The image is shown in a resizable window using OpenCV.
    """

    def __init__(self, image_path):
        """
        Initializes the DisplayImage node.
        :param image_path: Path to the SVG image representing the node.
        """
        super().__init__("Display Image")
        self.svg_renderer = QSvgRenderer(image_path)
        self.image_path = image_path

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

    def run(self):
        """
        Retrieves the image from the connected input node and displays it in a resizable window.
        """
        # Retrieves the connections of the functional block (Display Image)
        connections = self.getInputConnectors()

        # If the functional block has connections
        if connections:
            # Gets the image stored in the output block of the current connector
            src_image = connections[0].getSrc().image

            # Displays the image if it exists
            if src_image is not None:
                # Window name is unique using the memory address of this instance
                window_name = f"Image_{id(self)}"

                # Makes the window resizable
                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                cv2.imshow(window_name, src_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("No image to display")
        else:
            print("The block has no connections")
