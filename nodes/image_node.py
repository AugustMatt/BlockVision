# Classe para especificar que determinados blocos funcionais terão uma variavel "image" representando uma imagem que podera ser operada por outros blocos
# Util para verificar se determinadas classes são validas como entrada para outros blocos, evitando verificações hard coded

class ImageNode:
    """
    Base class for nodes that handle images.
    Provides a common interface for nodes that have an image attribute,
    allowing them to be used interchangeably in operations that require image input.
    """

    def __init__(self):
        """
        Initializes the ImageNode.
        Sets the initial value of the image attribute to None.
        """
        self.image = None

    def getImage(self):
        """
        Returns the image associated with this node.
        :return: The image (or None if no image is set).
        """
        return self.image