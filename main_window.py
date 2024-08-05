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
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLineEdit, QSizePolicy, QStyle
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from workspace.viewer import Viewer
import os
from functools import partial


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('BlockVision')
        self.resize(938, 598)

        self.get_nodes_icons_infos()
        self.get_interaction_modes_icons_infos()
        self.get_actions_icons_infos()

        self.create_actions()
        self.create_action_group()
        self.create_toolbars()
        self.create_central_widget()
        self.createStatusBar()
        self.createMenuBar()
        self.connect_signals()

    def get_nodes_icons_infos(self):

        # Caminho para a pasta de icones dos blocos funcionais
        self.nodes_icons_dir = os.path.join(os.getcwd(), 'icons', 'nodes')

        # Obtem a lista com o nome dos arquivos dos icones dos blocos funcionais (sem extensão)
        self.nodes_filenames = self.list_files_in_dir(self.nodes_icons_dir)

        # Lista com o nomes capitalizados
        self.nodes_names = [self.format_string(filename) for filename in self.nodes_filenames]

        # Lista com as ações dos blocos funcionais
        self.nodes_actions_list = []

    def get_interaction_modes_icons_infos(self):

        # Caminho para a pasta de icones dos blocos funcionais
        self.interaction_modes_icons_dir = os.path.join(os.getcwd(), 'icons', 'interaction_modes')

        # Obtem a lista com o nome dos arquivos dos icones dos blocos funcionais (sem extensão)
        self.interaction_modes_filenames = self.list_files_in_dir(self.interaction_modes_icons_dir)

        # Lista com o nomes capitalizados
        self.interaction_modes_names = [self.format_string(filename) for filename in self.interaction_modes_filenames]

        # Lista com as ações dos blocos funcionais
        self.interaction_modes_actions_list = []

    def get_actions_icons_infos(self):

        # Caminho para a pasta de icones dos blocos funcionais
        self.actions_icons_dir = os.path.join(os.getcwd(), 'icons', 'actions')

        # Obtem a lista com o nome dos arquivos dos icones dos blocos funcionais (sem extensão)
        self.actions_filenames = self.list_files_in_dir(self.actions_icons_dir)

        # Lista com o nomes capitalizados
        self.actions_names = [self.format_string(filename) for filename in self.actions_filenames]

        # Lista com as ações dos blocos funcionais
        self.actions_actions_list = []

    def list_files_in_dir(self, directory):
        try:
            # Obtém a lista de arquivos e diretórios no diretório especificado
            files = os.listdir(directory)
            
            # Filtra apenas os arquivos, ignorando subdiretórios
            file_names_with_ext = [file for file in files if os.path.isfile(os.path.join(directory, file))]
            
            # Remove a extensão de cada arquivo
            file_names_without_ext = [os.path.splitext(file)[0] for file in file_names_with_ext]
            
            return file_names_without_ext
        except FileNotFoundError:
            print(f"Directory not found: {directory}")
            return []
        except PermissionError:
            print(f"Permission denied: {directory}")
            return []

    def format_string(self, input_string):
        # Substitui ocorrências de "_" por espaços
        spaced_string = input_string.replace('_', ' ')
        
        # Coloca a primeira letra de cada palavra em maiúsculo
        capitalized_string = spaced_string.title()
        
        return capitalized_string

    def create_actions(self):
        """
        Creates actions used in toolbars and menus.
        These actions represent operations such as creating functional blocks and interaction modes.
        """
        
        # Para cada arquivo, cria uma ação com o icone associado ao arquivo e com o nome capitalizado
        for node_filename, node_name in zip(self.nodes_filenames, self.nodes_names):
            full_icon_path = f'{self.nodes_icons_dir}\\{node_filename}.svg'
            action = QAction(QIcon(full_icon_path), node_name, self)
            self.nodes_actions_list.append(action)

        for interaction_mode_filename, interaction_mode_name in zip(self.interaction_modes_filenames, self.interaction_modes_names):
            full_icon_path = f'{self.interaction_modes_icons_dir}\\{interaction_mode_filename}.svg'
            action = QAction(QIcon(full_icon_path), interaction_mode_name, self)
            action.setCheckable(True)
            self.interaction_modes_actions_list.append(action)
            if(interaction_mode_name == "Point"):
                action.setChecked(True)

        for action_filename, action_name in zip(self.actions_filenames, self.actions_names):
            full_icon_path = f'{self.actions_icons_dir}\\{action_filename}.svg'
            action = QAction(QIcon(full_icon_path), action_name, self)
            self.actions_actions_list.append(action)

    def create_action_group(self):
        """
        Creates a group of actions exclusive to interaction modes.
        Only one interaction mode can be selected at a time.
        """
        self.exclusiveSelectionGroup = QActionGroup(self)
        for action in self.interaction_modes_actions_list:
            self.exclusiveSelectionGroup.addAction(action)

    def create_toolbars(self):
        """
        Creates and configures the application's toolbars.
        Adds actions for functional blocks and interaction modes.
        """
        self.nodes_toolbar = QToolBar('Nodes ToolBar', self)
        
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Search Blocks...")
        self.line_edit.setFixedWidth(150)  # Define a largura fixa para 200 pixels
        self.line_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Permite a expansão vertical
        self.nodes_toolbar.addWidget(self.line_edit)

        for action in self.nodes_actions_list:
            self.nodes_toolbar.addAction(action)


        self.addToolBar(self.nodes_toolbar)

        self.addToolBarBreak()

        self.interaction_modes_toolbar = QToolBar('Interaction Modes ToolBar', self)
        for action in self.interaction_modes_actions_list:
            self.interaction_modes_toolbar.addAction(action)
        self.addToolBar(self.interaction_modes_toolbar)

        self.actions_toolbar = QToolBar('Actions ToolBar', self)
        for action in self.actions_actions_list:
            self.actions_toolbar.addAction(action)

        self.addToolBar(self.actions_toolbar)

    def create_central_widget(self):
        """
        Creates the central widget of the window and adds the Viewer to display and interact with the block diagram.
        """
        self.central_widget = QWidget(self)
        
        # Layout vertical para o widget central
        self.central_widget_vertical_layout = QVBoxLayout(self.central_widget)
                    
        # Criação e adição do Viewer
        self.viewer = Viewer()
        self.central_widget_vertical_layout.addWidget(self.viewer)
        
        # Configura o layout do widget central
        self.central_widget.setLayout(self.central_widget_vertical_layout)
        
        # Define o widget central
        self.setCentralWidget(self.central_widget)

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

    def connect_signals(self):
        """
        Connects actions to their corresponding functions for handling blocks and interaction modes.
        """

        # Aqui o partial foi necessario para poder invocar os metodos com argumentos
        for node, node_filename in zip(self.nodes_actions_list, self.nodes_filenames):
            icon_path = os.path.join(self.nodes_icons_dir, f'{self.nodes_icons_dir}\\{node_filename}.svg')
            node.triggered.connect(partial(self.viewer.addItem, node, icon_path))

        for interaction_mode, interaction_mode_name in zip(self.interaction_modes_actions_list, self.interaction_modes_names):
            interaction_mode.triggered.connect(partial(self.viewer.scene.setMode, interaction_mode_name))

        for action, action_name in zip(self.actions_actions_list, self.actions_names):
            if action_name == "Run":
                action.triggered.connect(lambda: self.viewer.run())
            elif action_name == "Options":
                action.triggered.connect(lambda: self.viewer.openOptionsWindow())

        self.line_edit.textChanged.connect(self.filter_actions)

    def filter_actions(self):
        
        filter_text = self.line_edit.text().lower()
        for node_name, node in zip(self.nodes_names, self.nodes_actions_list):
            node.setVisible(filter_text in node_name.lower())