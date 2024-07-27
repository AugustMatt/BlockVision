import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

if __name__ == '__main__':

    # Cria uma instância da classe QApplication para gerenciar a aplicação
    app = QApplication(sys.argv)

    # Cria uma instância da classe MainWindow, que é a janela principal da aplicação
    window = MainWindow()

    # Exibe a janela principal na tela
    window.show()

    # Inicia o loop de eventos da aplicação Qt e gerencia a execução da aplicação até que seja encerrada
    sys.exit(app.exec_())