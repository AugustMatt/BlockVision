# Classe que representa o bloco funcional da convoluçao
# Recebe 2 blocos como entrada. Um deles deve ser uma fonte de imagem (carregar Imagem ou outro bloco de convolução por exemplo)
# O outro um bloco do tipo kernel de convolução
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QSizeF
import numpy as np
import cv2
from .node import Node
from .image_node import ImageNode
from .convolution_kernel import ConvolutionKernel

class Convolution(Node, ImageNode):
    """
    Node that performs convolution on an input image using a specified kernel.
    """

    def __init__(self, image_path):
        """
        Initializes the Convolution node.
        :param image_path: Path to the SVG image representing the node.
        """
        super().__init__("Convolution")
        self.svg_renderer = QSvgRenderer(image_path)
        self.image_path = image_path

    def paint(self, painter, option, widget):
        """
        Paints the SVG image for the node.
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
        Executes the convolution operation using the connected image and kernel nodes.
        """
        input_connectors = self.getInputConnectors()

        # Verifica se há dois conectores de entrada
        if len(input_connectors) == 2:
            try:
                load_image_node, convolution_kernel_node = self._get_items_from_connectors(input_connectors)
                
                if load_image_node and convolution_kernel_node:
                    image = load_image_node.image
                    convolution_kernel = convolution_kernel_node.getConvolutionKernel()

                    # Verifica se a imagem e o kernel são válidos
                    if self._validate_inputs(image, convolution_kernel):
                        self._apply_convolution(image, convolution_kernel, convolution_kernel_node.getDivisibilityFactor())
                    else:
                        print("Erro ao aplicar convolução. Imagem ou núcleo de convolução inválido.")
                else:
                    print("Erro ao aplicar convolução. Verificar blocos de entrada.")
            except Exception as e:
                print(f"Erro inesperado ao aplicar convolução: {e}")
        else:
            print("Erro ao aplicar convolução. Espera-se 2 conexões no bloco.")

    def _get_items_from_connectors(self, connectors):
        """
        Retrieves the connected image and kernel nodes.
        """
        load_image_node = connectors[0].getSrc()
        convolution_kernel_node = connectors[1].getSrc()

        # Verifica se os tipos dos blocos estão trocados (dependendo da ordem de conexão que foi feita)
        if isinstance(load_image_node, ConvolutionKernel) and isinstance(convolution_kernel_node, ImageNode):
            load_image_node, convolution_kernel_node = convolution_kernel_node, load_image_node

        # Verifica se os tipos dos blocos são validos para realizar a convolução
        if isinstance(load_image_node, ImageNode) and isinstance(convolution_kernel_node, ConvolutionKernel):
            return load_image_node, convolution_kernel_node
        else:
            print("Blocos de entrada inválidos para convolução")
            return None, None

    def _validate_inputs(self, image, kernel):
        """
        Validates the input image and kernel.
        """
        return image is not None and image.size != 0 and kernel is not None

    def _apply_convolution(self, image, kernel, divisibility_factor):
        """
        Applies convolution to the input image using the specified kernel and divisibility factor.
        """
        kernel_mat = np.array(kernel, dtype=np.float32)
        kernel_mat /= divisibility_factor

        self.image = cv2.filter2D(image, -1, kernel_mat)
        print("Convolução realizada com sucesso!")
