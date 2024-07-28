import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

def main():
    """
    Função principal para iniciar a aplicação PyQt5.
    """
    # Cria uma instância da classe QApplication, que é necessária para qualquer aplicação Qt
    app = QApplication(sys.argv)

    # Cria e exibe a janela principal
    main_window = MainWindow()
    main_window.show()

    # Inicia o loop de eventos da aplicação e aguarda até que seja encerrada
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
