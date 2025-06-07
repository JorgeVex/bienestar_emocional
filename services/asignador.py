class AsignadorColecciones:
    """
    Clase que contiene la lógica para asignar las preguntas a sus respectivas categorías.
    """

    def __init__(self):
        """
        Inicializa el diccionario que mapea categorías con los números de las preguntas.
        """
        self.asignacion = {
            'Estado_Emocional': [1, 2, 3, 4],
            'Condiciones_de_Entorno': [5, 6, 7, 8],
            'Apoyo_Social': [9, 10, 11],
            'Balance_Vida_y_Trabajo': [12, 13],
            'Evaluacion_General': [14, 15, 16]
        }

    def obtener_asignacion(self):
        """
        Devuelve el diccionario de asignación de preguntas.
        
        Retorna:
        - dict: Mapeo de categorías a números de preguntas.
        """
        return self.asignacion
