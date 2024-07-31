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
        # Status bar and menu bar can be added later as needed
        # self.createStatusBar()
        # self.createMenuBar()
        self.connectSignals()

    def createActions(self):
        """
        Creates actions used in toolbars and menus.
        These actions represent operations such as creating functional blocks and interaction modes.
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
        Creates a group of actions exclusive to interaction modes.
        Only one interaction mode can be selected at a time.
        """
        self.exclusiveSelectionGroup = QActionGroup(self)
        self.exclusiveSelectionGroup.addAction(self.selectMoveMode)
        self.exclusiveSelectionGroup.addAction(self.connectMode)

    def createToolBars(self):
        """
        Creates and configures the application's toolbars.
        Adds actions for functional blocks and interaction modes.
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
        Creates the central widget of the window and adds the Viewer to display and interact with the block diagram.
        """
        self.centralWidget = QWidget(self)
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.viewer = Viewer(self.centralWidget)
        self.horizontalLayout.addWidget(self.viewer)
        self.setCentralWidget(self.centralWidget)

    def createStatusBar(self):
        """
        Creates the application's status bar.
        Can be used to display information or messages to the user.
        """
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def createMenuBar(self):
        """
        Creates the application's menu bar.
        Can be used to add menus and menu items.
        """
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)

    def connectSignals(self):
        """
        Connects actions to their corresponding functions for handling blocks and interaction modes.
        """
        self.createLoadImageNode.triggered.connect(lambda: self.viewer.addItem(self.createLoadImageNode, 'icons/nodes/load_image.svg'))
        self.createDisplayImageNode.triggered.connect(lambda: self.viewer.addItem(self.createDisplayImageNode, 'icons/nodes/display_image.svg'))
        self.createConvolutionKernelNode.triggered.connect(lambda: self.viewer.addItem(self.createConvolutionKernelNode, 'icons/nodes/convolution_kernel.svg'))
        self.createConvolutionNode.triggered.connect(lambda: self.viewer.addItem(self.createConvolutionNode, 'icons/nodes/convolution.svg'))

        self.selectMoveMode.triggered.connect(lambda: self.viewer.scene.setMode("POINTER"))
        self.connectMode.triggered.connect(lambda: self.viewer.scene.setMode("LINE"))

        self.actionRun.triggered.connect(lambda: self.viewer.run())
        self.actionOptions.triggered.connect(lambda: self.viewer.openOptionsWindow())
