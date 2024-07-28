# A classe MainWindow tem o objetivo de configurar e gerenciar a interface gráfica principal da aplicação. 
# Aqui está um resumo das suas responsabilidades:

#   Criação e Configuração da Janela Principal:
#       Define o título e o tamanho inicial da janela principal.

#   Criação e Configuração das Ações:
#       Cria as ações que serão usadas em barras de ferramentas e menus, como criar blocos funcionais e modos de interação.

#   Criação e Configuração das Barras de Ferramentas:
#       Cria e organiza as barras de ferramentas para ações como adicionar blocos funcionais e selecionar modos de interação.

#   Criação e Configuração do Widget Central:
#       Cria o widget central da janela e adiciona o Viewer, que é onde o diagrama de blocos é exibido e interage com o usuário.

#   Conexão de Sinais e Slots:
#       Conecta as ações das barras de ferramentas e botões aos slots apropriados no Viewer, como adicionar blocos, mudar modos 
#       de interação e executar ações.

from PyQt5.QtWidgets import QMainWindow, QAction, QActionGroup, QHBoxLayout, QWidget, QToolBar, QStatusBar, QMenuBar
from PyQt5.QtGui import QIcon
from workspace.viewer import Viewer

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('BlockVision')
        self.resize(938, 598)
        self.createActions()
        self.createActionGroup()
        self.createToolBars()
        self.createCentralWidget()
        # Barra de status e menu bar podem ser adicionados mais tarde, conforme necessário
        # self.createStatusBar()
        # self.createMenuBar()
        self.connectSignals()

    def createActions(self):
        """
        Cria as ações utilizadas nas barras de ferramentas e menus.
        Estas ações representam operações como criar blocos funcionais e modos de interação.
        """
        self.createLoadImageNode = QAction(QIcon('icons/nodes/load_image.svg'), 'Load Image', self)
        self.createDisplayImageNode = QAction(QIcon('icons/nodes/display_image.svg'), 'Display Image', self)
        self.createConvolutionKernelNode = QAction(QIcon('icons/nodes/convolution_kernel.svg'), 'Convolution Kernel', self)
        self.createConvolutionNode = QAction(QIcon('icons/nodes/convolution.svg'), 'Convolution', self)

        self.selectMoveMode = QAction(QIcon('icons/interaction_modes/point.svg'), 'Select/Move', self)
        self.connectMode = QAction(QIcon('icons/interaction_modes/line.svg'), 'Connect', self)
        self.selectMoveMode.setCheckable(True)
        self.connectMode.setCheckable(True)
        self.selectMoveMode.setChecked(True)

        self.actionRun = QAction(QIcon('icons/actions/run.svg'), 'Run', self)
        self.actionOptions = QAction(QIcon('icons/actions/options.svg'), 'Options', self)

    def createActionGroup(self):
        """
        Cria um grupo de ações exclusivas para modos de interação.
        Apenas um modo de interação pode ser selecionado por vez.
        """
        self.exclusiveSelectionGroup = QActionGroup(self)
        self.exclusiveSelectionGroup.addAction(self.selectMoveMode)
        self.exclusiveSelectionGroup.addAction(self.connectMode)

    def createToolBars(self):
        """
        Cria e configura as barras de ferramentas da aplicação.
        Adiciona ações para blocos funcionais e modos de interação.
        """
        self.nodesToolBar = QToolBar('Nodes ToolBar', self)
        self.nodesToolBar.addAction(self.createLoadImageNode)
        self.nodesToolBar.addAction(self.createDisplayImageNode)
        self.nodesToolBar.addAction(self.createConvolutionKernelNode)
        self.nodesToolBar.addAction(self.createConvolutionNode)
        self.addToolBar(self.nodesToolBar)

        self.pointerToolbar = QToolBar('Interaction Modes and Actions', self)
        self.pointerToolbar.addAction(self.selectMoveMode)
        self.pointerToolbar.addAction(self.connectMode)
        self.pointerToolbar.addAction(self.actionRun)
        self.pointerToolbar.addAction(self.actionOptions)
        self.addToolBar(self.pointerToolbar)

    def createCentralWidget(self):
        """
        Cria o widget central da janela e adiciona o Viewer para exibir e interagir com o diagrama de blocos.
        """
        self.centralWidget = QWidget(self)
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.viewer = Viewer(self.centralWidget)
        self.horizontalLayout.addWidget(self.viewer)
        self.setCentralWidget(self.centralWidget)

    def createStatusBar(self):
        """
        Cria a barra de status da aplicação. 
        Pode ser utilizada para exibir informações ou mensagens ao usuário.
        """
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def createMenuBar(self):
        """
        Cria a barra de menu da aplicação.
        Pode ser utilizada para adicionar menus e itens de menu.
        """
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)

    def connectSignals(self):
        """
        Conecta as ações às funções correspondentes para manipulação dos blocos e modos de interação.
        """
        self.createLoadImageNode.triggered.connect(lambda: self.viewer.addItem(self.createLoadImageNode, 'icons/nodes/load_image.svg'))
        self.createDisplayImageNode.triggered.connect(lambda: self.viewer.addItem(self.createDisplayImageNode, 'icons/nodes/display_image.svg'))
        self.createConvolutionKernelNode.triggered.connect(lambda: self.viewer.addItem(self.createConvolutionKernelNode, 'icons/nodes/convolution_kernel.svg'))
        self.createConvolutionNode.triggered.connect(lambda: self.viewer.addItem(self.createConvolutionNode, 'icons/nodes/convolution.svg'))

        self.selectMoveMode.triggered.connect(lambda: self.viewer.scene.setMode("POINTER"))
        self.connectMode.triggered.connect(lambda: self.viewer.scene.setMode("LINE"))

        self.actionRun.triggered.connect(lambda: self.viewer.play())
        self.actionOptions.triggered.connect(lambda: self.viewer.openOptionsWindow())
