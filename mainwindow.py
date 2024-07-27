# Janela principal da aplicação
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QActionGroup, QHBoxLayout, QWidget, QToolBar, QStatusBar, QMenuBar
from PyQt5.QtGui import QIcon
from circuitviewer import CircuitViewer

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    # Método que define parametros iniciais da janela principal, alem dos elementos presentes
    # ao iniciar a aplicação
    def initUI(self):

        # Titulo da janela
        self.setWindowTitle('BlockVision')

        # Tamanho inicial da janela
        self.resize(938, 598)

        # Configuração da barra de ferramentas de blocos funcionais da aplicação (QToolBar)
        # Cada elemento (ação) da barra de ferramentas criará um bloco funcional no diagrama

        # Criando as ações dos blocos funcionais (QActions) da QToolBar
        # O segundo parametro é uma string que representa o tipo do QAction
        # Vou colocar o tipo como o nome do arquivo por comodidade
        self.actionLoadImage = QAction(QIcon('icons/load_image.svg'), 'load_image', self)
        self.actionShowImage = QAction(QIcon('icons/show_image.svg'), 'show_image', self)
        self.actionConvolutionKernel = QAction(QIcon('icons/convolution_kernel.svg'), 'convolution_kernel', self)
        self.actionConvolution = QAction(QIcon('icons/convolution.svg'), 'convolution', self)

        # Criando a barra de ferramentas principal (QToolBar)
        self.gatesToolbar = QToolBar('Blocos Funcionais', self)

        # Inserindo as ações (QActions) na barra de ferramentas (QToolBar)
        self.gatesToolbar.addAction(self.actionLoadImage)
        self.gatesToolbar.addAction(self.actionShowImage)
        self.gatesToolbar.addAction(self.actionConvolutionKernel)
        self.gatesToolbar.addAction(self.actionConvolution)

        # Adicionando a barra de ferramentas a janela da aplicação
        self.addToolBar(self.gatesToolbar)

        # Configuração do grupo de ações para os modos de operação (QActionGroup) da aplicação
        # Um QActionGroup é util para gerenciar varias ações contudo, com apenas uma dela ativa por vez

        # Criando ações de modos de operação
        self.actionPOINT = QAction(QIcon('icons/point.svg'), 'Selecionar/Mover', self)
        self.actionLINE = QAction(QIcon('icons/line.svg'), 'Criar Conexão', self)
        self.actionPLAY = QAction(QIcon('icons/play.svg'), 'Executar', self)
        self.actionOptions = QAction(QIcon('icons/options.svg'), 'Ajustes', self)

        # As ações POINT e LINE podem ser "checadas" ou seja estarem em um estado "ativo"
        # Ja a ação PLAY vai apenas ter sua funcionalidade quando clicada
        self.actionPOINT.setCheckable(True)
        self.actionLINE.setCheckable(True)

        # Faz com que a ação "POINT" seja seleciona automaticamente no inicio da aplicação
        self.actionPOINT.setChecked(True)

        # Cria um grupo de ações com as ações POINT e LINE, fazendo com que quando uma seja seleciona
        # a outra seja automaticamente "deseleciona" (seleção exclusiva entre essas duas)
        self.pointTypeGroup = QActionGroup(self)

        # Adiciona as ações ao grupo de ações
        self.pointTypeGroup.addAction(self.actionPOINT)
        self.pointTypeGroup.addAction(self.actionLINE)

        # Criação da Barra de ferramentas para os modos de operação do aplicativo
        self.pointerToolbar = QToolBar('Modos de Operação', self)

        # Adicionando ações de modo de operação
        self.pointerToolbar.addAction(self.actionPOINT)
        self.pointerToolbar.addAction(self.actionLINE)
        self.pointerToolbar.addAction(self.actionPLAY)
        self.pointerToolbar.addAction(self.actionOptions)

        # Adicionando barra de modos de operação a janela
        self.addToolBar(self.pointerToolbar)

        # Criação de um Widget central da janela
        self.centralWidget = QWidget(self)

        # Nesse caso seria o espaço onde sera criada o diagrama de blocos
        # Sera possivel fazer coisas como arrastar/soltar blocos, conecta-los, seleciona-los, abrir
        # configurações especificas de cada blocos, dentre outros

        # Atribuindo o widget central a janela
        self.setCentralWidget(self.centralWidget)

        # Cria um layout horizontal e o atribui ao widget central da janela
        self.horizontalLayout = QHBoxLayout(self.centralWidget)

        # Atribui uma instancia de CircuitViewer ao widget central da janela
        # Confira o arquivo que implementa a classe para verificar seus comportamentos e funcionalidades
        self.cv = CircuitViewer(self.centralWidget)
        self.horizontalLayout.addWidget(self.cv)

        # Me parece que status bar e menu bar nao estão sendo utilizados na aplicação, mas preciso checar
        # depois

        # Status bar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        # Menu bar
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)

        # Conectando as ações aos slots
        # Verificar posteriormente oque fazer com isso

        # Envia um sinal a função "addItem" da classe circuitviewer para iniciar o processo de renderização dos blocos funcionais quando clicados
        self.actionLoadImage.triggered.connect(lambda: self.cv.addItem(self.actionLoadImage))
        self.actionShowImage.triggered.connect(lambda: self.cv.addItem(self.actionShowImage))
        self.actionConvolutionKernel.triggered.connect(lambda: self.cv.addItem(self.actionConvolutionKernel))
        self.actionConvolution.triggered.connect(lambda: self.cv.addItem(self.actionConvolution))

        # Acessa o metodo setMode, da cena presente no circuitviewer e troca o modo de operação quando necessario
        self.actionPOINT.triggered.connect(lambda: self.cv.scene.setMode("POINTER"))
        self.actionLINE.triggered.connect(lambda: self.cv.scene.setMode("LINE"))

        # Acessa o metodo play
        self.actionPLAY.triggered.connect(lambda: self.cv.play())
        self.actionOptions.triggered.connect(lambda: self.cv.openOptionsWindow())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
