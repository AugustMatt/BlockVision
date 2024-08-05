from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QSizeF
import numpy as np
import cv2
from .node import Node
from .image_node import ImageNode

class Add(Node, ImageNode):
    """
    Node that performs sum on input images.
    """

    def __init__(self, image_path):
        """
        Initializes the sum node.
        :param image_path: Path to the SVG image representing the node.
        """
        super().__init__("Add")
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
        Executes the sum operation using the connected images.
        """
        input_connectors = self.getInputConnectors()

        # Verifica se há dois conectores de entrada
        if len(input_connectors) == 2:
            try:
                image_node1, image_node2 = self._get_items_from_connectors(input_connectors)
                
                if image_node1 and image_node2:
                    image1 = image_node1.image
                    image2 = image_node2.image

                    # Verifica se as imagens são validas. Se sim, realiza a soma das imagens
                    if self._validate_inputs(image1, image2):
                        self._apply_sum(image1, image2)
                    else:
                        print("Erro ao aplicar a soma. Imagens inválidas.")
                else:
                    print("Erro ao aplicar a soma. Verificar blocos de entrada.")
            except Exception as e:
                print(f"Erro inesperado ao aplicar a soma: {e}")
        else:
            print("Erro ao aplicar a soma. Espera-se 2 conexões no bloco.")

    def _get_items_from_connectors(self, connectors):
        """
        Retrieves the connected images nodes.
        """
        image_node1 = connectors[0].getSrc()
        image_node2 = connectors[1].getSrc()

        # Verifica se os tipos dos blocos são validos para realizar a soma
        if isinstance(image_node1, ImageNode) and isinstance(image_node2, ImageNode):
            return image_node1, image_node2
        else:
            print("Blocos de entrada inválidos para soma")
            return None, None

    def _validate_inputs(self, image1, image2):
        """
        Validates the input images.
        """

        # Garantir que as imagens tenham o mesmo padrão de cor (color channel size)
        # Garantir que as imagens tenham o mesmo tamanho
        channels1 = image1.shape[2] if len(image1.shape) == 3 else 1
        channels2 = image2.shape[2] if len(image2.shape) == 3 else 1

        height1, width1 = image1.shape[:2]
        height2, width2 = image2.shape[:2]
        print(height1, width1)
        print(height2, width2)


        # Verificar se o número de canais é o mesmo
        if channels1 == channels2:
            if (height1, width1) != (height2, width2):
                print("As imagens precisam ter o mesmo tamanho.")
                return False    
            else:
                return (image1 is not None) and (image1.size != 0) and (image2 is not None) and (image2.size != 0)
        else:
            print("As imagens possuem diferentes números de canais de cor.")
            return False
        
    def _apply_sum(self, image1, image2):
        """
        Applies the sum of input images.
        """
        self.image = cv2.add(image1, image2)
        print("Soma realizada com sucesso!")

