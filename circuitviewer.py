from PyQt5.QtWidgets import QGraphicsView, QFileDialog, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QGridLayout
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from circuitscene import CircuitScene
from circuititem import CircuitItem

class CircuitViewer(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = CircuitScene(self)
        self.setScene(self.scene)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.scene.setBackgroundBrush(QBrush(QColor(200, 200, 200), Qt.SolidPattern))
        self.setRenderHint(QPainter.Antialiasing)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Adicione lógica adicional se necessário

    # Adiciona o bloco funcional a cena utilizando o metodo add da classe circuitscene
    def addItem(self, action):
        self.scene.add(action.text())

    # Ajusta o modo conforme necessário para definir o modo
    def setMode(self, action):
        self.scene.setMode(action.text())

    # Grava o arquivo da cena
    def record(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File")
        print(f"record: {file_name}")
        self.scene.record(file_name)

    # Executa a funcionalidade do bloco selecionado
    def play(self):

        # Lista dos elementos selecionados
        # Espera-se ter somente um (indice 0)
        selected_items_list = self.scene.selectedItems()
        
        # Se existe ao menos um item selecionado
        if selected_items_list:

            # Adquire esse item
            selected_item = selected_items_list[0]

            # Verifica se é do tipo circuit item, caso contrario o substitui por None
            circuit_item = selected_item if isinstance(selected_item, CircuitItem) else None

            # Caso exista
            if circuit_item:
                
                # Adquire o tipo do bloco funcional
                item_type = circuit_item.getType()

                # Se for o bloco de carregar imagem
                if item_type == "load_image":
                    self.seletorDeImagem(circuit_item)

                # Se for o bloco de exibir imagem
                elif item_type == "show_image":
                    self.exibirImagem(circuit_item)

                # Se for o bloco de convolução
                elif item_type == "convolution":
                    self.aplicarConvolucao(circuit_item)

                else:
                    print("Funcionalidade não implementada para esse bloco")

            else:
                print("Elemento selecionado não é um circuit item")

        else:
            print("Sem elementos selecionados")

    # Janela de carregamento de imagem
    def seletorDeImagem(self, circuit_item):

        # Abre um seletor de arquivos com tipos especificos de imagem filtrados
        # Armazenando o caminho do arquivo selecionado
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar imagem", "", "Imagens (*.png *.jpg *.bmp)")

        # Se o caminho existe
        if file_path:

            # Adquire o padrão de cor do bloco para leitura
            color_pattern = circuit_item.getColorPattern()

            # Carrega a imagem com OpenCV
            image = self.carregarImagem(file_path, color_pattern)
            
            # Armazena a imagem lida no bloco funcional
            if image is not None:
                circuit_item.setImage(image)
                print(f"Imagem lida no formato {color_pattern}")
            else:
                print("Erro ao ler a imagem")
            
        else:
            print("Nenhum arquivo foi selecionado")

    # Método auxiliar para carregar a imagem
    def carregarImagem(self, file_path, color_pattern):
        if color_pattern == "RGB":
            image = cv2.imread(file_path)
        elif color_pattern == "Grayscale":
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        else:
            print('Padrão de cor não suportado para leitura')
            return None
        return image

    # Exibe a imagem na janela
    def exibirImagem(self, circuit_item):

        # Adquire as conexões do bloco funcional (Exibir imagem)
        connections = circuit_item.getInputConnectors()

        # Se o bloco funcional tiver conexões
        if connections:

            # Adquire a imagem armazenada no bloco de saida do connector corrente
            src_image = connections[0].getSrc().image

            # Exibe a imagem caso exista
            if src_image is not None:
                window_name = f"Image_{id(circuit_item)}"
                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL) # faz com que a janela com esse nome seja redimensionavel
                cv2.imshow(window_name, src_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("Não existe imagem para exibir")
        else:
            print('O bloco não tem conexões')

    # Aplica a convolução na imagem
    def aplicarConvolucao(self, circuit_item):
        input_connectors = circuit_item.getInputConnectors()
        
        # Verifica se há dois conectores de entrada
        if len(input_connectors) == 2:

            # Adquire os itens de imagem e kernel dos conectores
            load_item_image = input_connectors[0].getSrc()
            kernel_item = input_connectors[1].getSrc()

            # Verifica se os itens estão invertidos e os corrige
            if load_item_image.getType() == "convolution_kernel":
                load_item_image, kernel_item = kernel_item, load_item_image

            # Se os itens forem válidos
            if load_item_image and kernel_item:
                image = load_item_image.image
                convolution_kernel = kernel_item.getMatrix()

                # Verifica se a imagem e o kernel são válidos
                if image is not None and image.size != 0 and convolution_kernel:

                    # Converte o kernel para matriz numpy e normaliza
                    kernel_mat = np.array(convolution_kernel, dtype=np.float32)
                    kernel_mat /= kernel_item.getDivisibility()

                    # Aplica a convolução
                    result_image = cv2.filter2D(image, -1, kernel_mat)
                    circuit_item.image = result_image
                    print("Convolução realizada com sucesso!")
                else:
                    print("Erro ao aplicar convolução. Imagem ou nucleo de convolução invalido")
            else:
                print("Erro ao aplicar convolução. Verificar conectores")
        else:
            print("Erro ao aplicar convolução. Espera-se 2 conexões no bloco")

    # Abre a janela de ajustes do bloco funcional selecionado (Se houver)
    def openOptionsWindow(self):
        
        # Lista dos elementos selecionados
        # Espera-se ter somente um (indice 0)
        selected_items_list = self.scene.selectedItems()

        # Se existe ao menos um item selecionado
        if selected_items_list:

            # Adquire esse item
            selected_item = selected_items_list[0]

            # Verifica se é do tipo circuit item, caso contrario o substitui por None
            circuit_item = selected_item if isinstance(selected_item, CircuitItem) else None

            # Caso exista
            if circuit_item:
                
                # Adquire o tipo do bloco funcional
                item_type = circuit_item.getType()

                # Se for o bloco de carregar imagem
                if item_type == "load_image":
                    self.createCollorPatternSelectionWindow(selected_item)

                # Se for o bloco de kernel de convolução
                elif item_type == "convolution_kernel":
                    self.createConvolutionMatrixWindow(selected_item)

                else:
                    print("Ajustes não implementado para esse bloco")

            else:
                print("Elemento selecionado não é um circuit item")

        else:
            print("Sem elementos selecionados")

    # Metodo que cria a janela de seleção do padrão de cor de leitura da imagem do bloco carregar imagem
    # selectedItem é a instancia do bloco funcional carregar imagem corrente
    def createCollorPatternSelectionWindow(self, selectedItem):

        # Janela do tipo QDialog
        dialog = QDialog()

        dialog.resize(300, 50)

        # Titulo da janela
        dialog.setWindowTitle("Configurações do Load Image")

        # Layout vertical para posicionar os eementos
        layout = QVBoxLayout(dialog)

        # Label informativa do padrão de cor
        colorLabel = QLabel("Padrão de Cor:")

        # Adicionando a label ao layout
        layout.addWidget(colorLabel)

        # Seletor do padrão de cor
        colorSelector = QComboBox()

        # Opções do seletor
        colorSelector.addItems(["RGB", "Grayscale"])

        # Adicionando o seletor ao layout
        layout.addWidget(colorSelector)

        # Botão "ok" para confirmar alterações
        okButton = QPushButton("OK")

        # Adicionando o botão ao layout
        layout.addWidget(okButton)

        # Função do botão "ok"
        okButton.clicked.connect(dialog.accept)

        # Quando o botão de "ok" for clicado, muda a variavel referente ao padrão de cor do bloco funcional
        if dialog.exec() == QDialog.Accepted:
            selectedPattern = colorSelector.currentText()
            selectedItem.setColorPattern(selectedPattern)
            print(f"Padrão de cor alterado para {selectedPattern}! Por favor, execute o bloco novamente para aplicá-las")

    # Metodo que cria a janela de definição da matriz de convolução do bloco de criar matriz de convolução
    def createConvolutionMatrixWindow(self, selectedItem):

        # Janela do tipo QDialog
        dialog = QDialog()

        # Titulo da janela
        dialog.setWindowTitle("Configurações do Kernel")

        # Layout vertical que armazenará os elementos da janela
        layout = QVBoxLayout(dialog)

        # Label que informa o tamanho da matriz de kernal
        sizeLabel = QLabel("Tamanho da Matriz:")
        layout.addWidget(sizeLabel)

        # Seletor do tamanho da matriz de kernel
        sizeSelector = QComboBox()
        sizeSelector.addItems(["3x3", "5x5"])
        layout.addWidget(sizeSelector)

        # Label que informa o fator de divisibilidade
        divisibilityLabel = QLabel("Fator de Divisibilidade:")
        layout.addWidget(divisibilityLabel)

        # Caixa de texto para inserir o fator de divisibilidade
        # Por padrão vai iniciar com a string 1.0
        # Talvez esse padrão seja redundante visto que mais para frente no codigo eu adquiro o fator armazenado...mas tenho que ver
        divisibilityLineEdit = QLineEdit("1.0")
        layout.addWidget(divisibilityLineEdit)

        # Label que informa os campos do kernel de convolução
        matrixValuesLabel = QLabel("Valores da Matriz:")
        layout.addWidget(matrixValuesLabel)

        # Layout do tipo grid que armazenara os campos para inserir os valores do kernel de convolução
        matrixLayout = QGridLayout()

        # Lista que armazenará elementos do tipo QLineEdits que representam os campos da matriz do kernel de convolução
        matrixFields = []

        # Adquirimos a matriz de convolução armazenada no bloco do kernel corrente
        convolutionKernel = selectedItem.getMatrix()

        # Se existir, preenchemos os campos da matriz com os valores armazenados
        if convolutionKernel:

            # Preenchimento dos campos com os valores armazenados
            self.fillMatrixFields(matrixLayout, matrixFields, convolutionKernel)

            # Tamanho do kernel armazenado
            matrixSize = len(convolutionKernel)

            # Pre-seleciona o campo do tamanho da matriz baseado no tamanho do kernel armazenado
            sizeSelector.setCurrentIndex(0 if matrixSize == 3 else 1)
        
        # Caso não existe matriz armazenada previamente, cria uma matriz de zeros
        else:
            self.fillMatrixFields(matrixLayout, matrixFields, [[0.0]*5]*5)

        # Adquire o fator de divisibilidade e o preenche no campo
        divisibilityLineEdit.setText(str(selectedItem.getDivisibility()))

        # Insere os elementos no layout
        layout.addLayout(matrixLayout)

        # Executa a função updateMatrixFields quando um elemento do seletor de tamanho mudar
        sizeSelector.activated.connect(lambda index: self.updateMatrixFields(index, matrixLayout, matrixFields))

        # Botão de "OK" para confirmação das alterações/definições
        okButton = QPushButton("OK")

        # Adiciona o botão ao layout
        layout.addWidget(okButton)

        okButton.clicked.connect(dialog.accept)

        if dialog.exec() == QDialog.Accepted:

            updatedKernelMatrix = []
            
            try:
                for rowFields in matrixFields:
                    rowValues = [float(field.text()) for field in rowFields]
                    updatedKernelMatrix.append(rowValues)
            except ValueError:
                print("Valores da matriz invalidos!")
                return

            divisibilityStr = divisibilityLineEdit.text()

            try:
                divisibility = float(divisibilityStr)
            except ValueError:
                print("Valor de divisibilidade inválido!")
                return

            selectedItem.setMatrix(updatedKernelMatrix)
            selectedItem.setDivisibility(divisibility)
            print("Configurações do Kernel atualizadas!")

    # Metodo que preenche os campos da matriz do kernel de convolução
    def fillMatrixFields(self, matrix_layout, matrix_fields, convolution_kernel):

        # Tamanho do kernel de convolução
        matrix_size = len(convolution_kernel)

        # Limpa os campos antigos
        for row in matrix_fields:
            for line_edit in row:
                matrix_layout.removeWidget(line_edit)
                line_edit.deleteLater()
        matrix_fields.clear()

        # Adiciona novos campos com os valores da convolution_kernel
        for i in range(matrix_size):
            row_fields = []
            for j in range(matrix_size):
                line_edit = QLineEdit(str(convolution_kernel[i][j]))
                line_edit.setMaximumWidth(50)  # Define a largura máxima do campo de entrada
                row_fields.append(line_edit)
                matrix_layout.addWidget(line_edit, i, j)
            matrix_fields.append(row_fields)

    # Preenche os campos visuais da matriz com zeros quando o tamanho da matriz muda
    def updateMatrixFields(self, index, matrixLayout, matrixFields):
        size = 3 if index == 0 else 5
        defaultMatrix = [[0.0]*size for _ in range(size)]
        self.fillMatrixFields(matrixLayout, matrixFields, defaultMatrix)
