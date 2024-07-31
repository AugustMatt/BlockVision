from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QSizeF
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QGridLayout, QPushButton
import numpy as np
from .node import Node

class ConvolutionKernel(Node):
    """
    Node that represents a convolution kernel.
    This class allows the user to configure a convolution matrix and its divisibility factor.
    """

    def __init__(self, image_path):
        """
        Initializes the ConvolutionKernel node.
        :param image_path: Path to the SVG image representing the node.
        """
        super().__init__("Conv. Kernel")
        self.svg_renderer = QSvgRenderer(image_path)
        self.image_path = image_path

        # Initial convolution kernel: 3x3 matrix of zeros
        self.convolution_kernel = np.zeros((3, 3), dtype=np.float32)

        # Divisibility factor (divides all values in the matrix)
        self.divisibility_factor = 1.0

        # Attributes used to manage matrix fields
        self.matrix_layout = None
        self.matrix_fields = []
        self.sizeSelector = None
        self.divisibilityLineEdit = None

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
        Opens a dialog to configure the convolution kernel and divisibility factor.
        Updates the kernel matrix and divisibility factor based on user input.
        """
        dialog = QDialog()
        dialog.setWindowTitle("Set Kernel")

        layout = QVBoxLayout(dialog)
        self.addMatrixSizeSelector(layout)
        self.addDivisibilityFactorField(layout)
        self.matrix_layout, self.matrix_fields = self.addMatrixFields(layout)

        self.fillMatrixFields(self.matrix_layout, self.matrix_fields, self.convolution_kernel.tolist())
        self.updateSizeSelector()

        okButton = QPushButton("OK")
        layout.addWidget(okButton)
        okButton.clicked.connect(dialog.accept)

        if dialog.exec() == QDialog.Accepted:
            self.updateKernelConfiguration(self.matrix_fields, dialog)

    def addMatrixSizeSelector(self, layout):
        """
        Adds a matrix size selector to the dialog.
        :param layout: Layout to which the selector will be added.
        """
        sizeLabel = QLabel("Matrix Size:")
        layout.addWidget(sizeLabel)

        self.sizeSelector = QComboBox()
        self.sizeSelector.addItems(["3x3", "5x5"])
        layout.addWidget(self.sizeSelector)
        self.sizeSelector.activated.connect(self.updateMatrixFields)

    def addDivisibilityFactorField(self, layout):
        """
        Adds a divisibility factor field to the dialog.
        :param layout: Layout to which the field will be added.
        """
        divisibilityLabel = QLabel("Divisibility Factor:")
        layout.addWidget(divisibilityLabel)

        self.divisibilityLineEdit = QLineEdit(str(self.divisibility_factor))
        layout.addWidget(self.divisibilityLineEdit)

    def addMatrixFields(self, layout):
        """
        Adds fields for the matrix values to the dialog.
        :param layout: Layout to which the fields will be added.
        :return: Tuple containing the matrix layout and matrix fields.
        """
        matrixValuesLabel = QLabel("Matrix Values:")
        layout.addWidget(matrixValuesLabel)

        matrix_layout = QGridLayout()
        layout.addLayout(matrix_layout)
        matrix_fields = []
        return matrix_layout, matrix_fields

    def fillMatrixFields(self, matrix_layout, matrix_fields, convolution_kernel):
        """
        Fills the matrix fields with the given convolution kernel values.
        :param matrix_layout: Layout for the matrix fields.
        :param matrix_fields: List to hold the matrix field widgets.
        :param convolution_kernel: List of lists representing the kernel matrix values.
        """
        matrix_size = len(convolution_kernel)

        # Clear existing fields
        for row in matrix_fields:
            for line_edit in row:
                matrix_layout.removeWidget(line_edit)
                line_edit.deleteLater()
        matrix_fields.clear()

        # Create new fields
        for i in range(matrix_size):
            row_fields = []
            for j in range(matrix_size):
                line_edit = QLineEdit(str(convolution_kernel[i][j]))
                line_edit.setMaximumWidth(50)
                row_fields.append(line_edit)
                matrix_layout.addWidget(line_edit, i, j)
            matrix_fields.append(row_fields)

    def updateMatrixFields(self):
        """
        Updates the matrix fields based on the selected matrix size.
        """
        size = 3 if self.sizeSelector.currentIndex() == 0 else 5
        default_matrix = [[0.0]*size for _ in range(size)]
        self.fillMatrixFields(self.matrix_layout, self.matrix_fields, default_matrix)

    def updateSizeSelector(self):
        """
        Updates the matrix size selector based on the current size of the kernel.
        """
        matrix_size = len(self.convolution_kernel)
        index = 0 if matrix_size == 3 else 1
        self.sizeSelector.setCurrentIndex(index)

    def updateKernelConfiguration(self, matrix_fields, dialog):
        """
        Updates the kernel matrix and divisibility factor based on user input.
        :param matrix_fields: List of matrix field widgets.
        :param dialog: The dialog that contains the input fields.
        """
        updated_kernel_matrix = []

        try:
            for row_fields in matrix_fields:
                row_values = [float(field.text()) for field in row_fields]
                updated_kernel_matrix.append(row_values)
        except ValueError:
            print("Valores da matriz inválidos!")
            return

        try:
            divisibility = float(self.divisibilityLineEdit.text())
        except ValueError:
            print("Valor de divisibilidade inválido!")
            return

        self.convolution_kernel = np.array(updated_kernel_matrix, dtype=np.float32)
        self.divisibility_factor = divisibility
        print("Configurações do Kernel atualizadas!")

    def getDivisibilityFactor(self):
        """
        Returns the divisibility factor for the kernel.
        :return: Divisibility factor.
        """
        return self.divisibility_factor
    
    def getConvolutionKernel(self):
        """
        Returns the convolution kernel matrix.
        :return: Convolution kernel matrix.
        """
        return self.convolution_kernel
