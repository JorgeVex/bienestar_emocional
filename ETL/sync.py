from pymongo import MongoClient
from dotenv import load_dotenv
import os

class SincronizadorMongo:
    """
    Clase encargada de sincronizar los datos entre MongoDB Atlas y CosmosDB (API MongoDB).
    """

    def __init__(self):
        """
        Constructor: carga las variables de entorno y establece conexiones a ambas bases de datos.
        """
        load_dotenv()

        # Leer URIs desde .env
        atlas_uri = os.getenv("MONGO_ATLAS_URI")
        cosmos_uri = os.getenv("COSMOSDB_URI")

        # Inicializar clientes y bases de datos
        self.atlas_client = MongoClient(atlas_uri)
        self.cosmos_client = MongoClient(cosmos_uri)

        self.atlas_db = self.atlas_client['cuestionario_bienestar']
        self.cosmos_db = self.cosmos_client['cuestionario_bienestar']

        # Colecciones a sincronizar
        self.colecciones = [
            "Estado_Emocional",
            "Condiciones_de_Entorno",
            "Apoyo_Social",
            "Balance_Vida_y_Trabajo",
            "Evaluacion_General",
            "Resumen_Completo"
        ]

    def sincronizar_coleccion(self, nombre_coleccion):
        """
        Sincroniza una sola colección entre Atlas y CosmosDB.
        """
        atlas_col = self.atlas_db[nombre_coleccion]
        cosmos_col = self.cosmos_db[nombre_coleccion]

        documentos = list(atlas_col.find())

        if documentos:
            print(f"🔄 Sincronizando {len(documentos)} documentos de '{nombre_coleccion}'...")

            # Remover _id para evitar conflicto en inserción
            for doc in documentos:
                doc.pop('_id', None)

            cosmos_col.insert_many(documentos)
            print(f"✅ '{nombre_coleccion}' sincronizada correctamente.")
        else:
            print(f"⚠️ No hay documentos para sincronizar en '{nombre_coleccion}'.")

    def sincronizar_todo(self):
        """
        Ejecuta la sincronización para todas las colecciones listadas.
        """
        print("🚀 Iniciando sincronización de todas las colecciones...")
        for nombre in self.colecciones:
            self.sincronizar_coleccion(nombre)
        print("🎉 Sincronización completa.")

# Si se ejecuta directamente
if __name__ == "__main__":
    sincronizador = SincronizadorMongo()
    sincronizador.sincronizar_todo()
