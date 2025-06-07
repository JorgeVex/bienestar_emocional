from pymongo import MongoClient
from datetime import datetime
import os

class MongoService:
    """
    Clase responsable de gestionar la conexión y operaciones con la base de datos MongoDB.
    """

    def __init__(self):
        """
        Inicializa la conexión a MongoDB Atlas usando la URI proporcionada desde variables de entorno.
        """
        uri = os.getenv("MONGO_ATLAS_URI")
        self.client = MongoClient(uri)
        self.db = self.client['cuestionario_bienestar']

    def insertar_por_categoria(self, data, asignacion_colecciones):
        """
        Inserta las respuestas en colecciones separadas según la categoría.
        
        Parámetros:
        - data (dict): Diccionario con las respuestas del usuario.
        - asignacion_colecciones (dict): Mapeo de categorías a números de preguntas.
        """
        for nombre_coleccion, preguntas in asignacion_colecciones.items():
            doc = {"fecha": datetime.now()}  # Agrega la fecha actual
            for numero in preguntas:
                clave = f'pregunta{numero}'
                doc[clave] = data.get(clave)
            self.db[nombre_coleccion].insert_one(doc)

    def insertar_resumen_completo(self, data):
        """
        Inserta todas las respuestas en una colección resumen, junto con la fecha.
        
        Parámetros:
        - data (dict): Diccionario con las respuestas del usuario.
        """
        data_completa = dict(data)
        data_completa["fecha"] = datetime.now()
        self.db["Resumen_Completo"].insert_one(data_completa)
