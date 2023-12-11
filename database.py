from pymongo import MongoClient

def connect_to_mongodb(uri):
    try:
        client = MongoClient(uri)
        print("Conexión exitosa!")
        return client, client.get_database()
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def insert_data_to_mongodb(db, collection_name, data):
    try:
        collection = db[collection_name]
        collection.insert_many(data)
        print(f"Datos insertados en la colección '{collection_name}' con éxito.")
    except Exception as e:
        print(f"Error al insertar datos en MongoDB: {e}")