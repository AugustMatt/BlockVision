# Classe que representa uma conexão entre dois blocos funcionais da aplicação
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt, QSizeF

class Connector(QGraphicsLineItem):

    # Construtor da classe
    # src -> circuit item de origem da conexão
    # dst -> circuit item de destino da conexão
    def __init__(self, src, dst, parent=None, scene=None):

        # Chama o construtor da classe base
        super().__init__(parent)

        # Armazena o item de origem
        self.src = src

        # Armazena o item de destino
        self.dst = dst 

        # Calcula metade da largura e altura do item de destino para ajustes de posição
        self.dst_width = 0.5 * dst.boundingRect().bottomRight().x()
        self.dst_height = 0.5 * dst.boundingRect().bottomRight().y()
       
        # Raio do círculo desenhado no final da linha
        self.radius = 10
        
        # Cor da linha do conector
        self.line_color = QColor(Qt.black)

        # Cor do círculo no final da linha
        self.circle_color = QColor(Qt.red)

        # Define a profundidade do item no stack de desenho
        self.setZValue(0)

         # Permite que o item seja selecionado
        self.setFlags(QGraphicsLineItem.ItemIsSelectable)

        # Atualiza a posição do conector
        self.updatePosition()

    # Método para desenhar o conector
    def paint(self, painter, option, widget):
        
        # Certifica-se de que a posição está atualizada
        self.updatePosition()

        # Configura a caneta para desenhar a linha
        my_pen = QPen(self.line_color)

        # Define a largura da linha
        my_pen.setWidth(3)

        # Altera a cor da linha se o conector estiver selecionado
        if self.isSelected():
            my_pen.setColor(Qt.blue)

        # Define a caneta no pintor
        painter.setPen(my_pen)

        # Define o pincel no pintor para desenhar o círculo
        painter.setBrush(self.circle_color)

        # Desenha a linha central
        painter.drawLine(self.center_line)

         # Desenha o círculo no ponto de borda
        painter.drawEllipse(self.border_point, self.radius, self.radius)

    # Retorna a caixa delimitadora da linha que representa uma conexão
    def boundingRect(self):

        # Margem extra para a caixa delimitadora
        extra = (self.pen().width() + 20) / 2.0 + self.radius

        # Cria e ajusta a caixa delimitadora
        return QRectF(self.line().p1(),
                      QSizeF(self.line().p2().x() - self.line().p1().x(),
                             self.line().p2().y() - self.line().p1().y())
                      ).normalized().adjusted(-extra, -extra, extra, extra)

    # Atualiza a posição do conector
    def updatePosition(self):

        # Obtém o centro do item de origem (source) e do item de destino (destination)
        src_center = self.src.center()
        dst_center = self.dst.center()

        # Cria uma linha (QLineF) que vai do centro do item de origem ao centro do item de destino
        line = QLineF(src_center, dst_center)

        # Define a linha do QGraphicsLineItem (superclasse do Connector) com a linha criada
        self.setLine(line)

        # Armazena a linha central entre os dois centros
        self.center_line = QLineF(src_center, dst_center)

        # Calcula o vetor unitário da linha central (um vetor com magnitude 1 na direção da linha)
        self.border_vector = self.center_line.unitVector()

        # Calcula o ponto na borda do item de destino onde a linha termina, levando em conta a largura e a altura do destino
        self.border_point = QPointF(
            -self.dst_width * self.border_vector.dx() + dst_center.x(),
            -self.dst_height * self.border_vector.dy() + dst_center.y()
        )

        # Ajusta o ponto final da linha central para ser o ponto de borda calculado
        self.center_line.setP2(self.border_point)

    # Retorna o objeto (circuit item) de origem da conexão
    def getSrc(self):
        return self.src

    # Retorna o objeto (circuit item) de destino da conexão
    def getDst(self):
        return self.dst

    # Adicione métodos para remover o conector
    def remove(self):

        # Remover o conector das listas de conectores dos itens
        if self in self.src.output_connectors:
            self.src.output_connectors.remove(self)
        if self in self.dst.input_connectors:
            self.dst.input_connectors.remove(self)
        
        # Remover referências aos itens conectados
        self.src = None
        self.dst = None
        # Remover o conector da cena
        self.scene().removeItem(self)
