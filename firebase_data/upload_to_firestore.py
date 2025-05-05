
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Ruta del archivo de clave
cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
json_path = os.path.join(os.path.dirname(__file__), 'firebase_seed_data.json')

# Inicializar Firebase Admin
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Cargar el archivo JSON
with open(json_path, 'r') as f:
    data = json.load(f)

def upload_collection(collection_path, documents):
    for doc_id, fields in documents.items():
        doc_ref = db.document(f"{collection_path}/{doc_id}")
        doc_ref.set(fields)
        print(f"✔️ Subido: {collection_path}/{doc_id}")

for path, documents in data.items():
    if "/" in path:
        # Es subcolección (por ejemplo: community_posts/post_001/comments)
        parts = path.split("/")
        collection_path = "/".join(parts[:2])
        subcollection_path = "/".join(parts[2:])
        for doc_id, fields in documents.items():
            full_path = f"{collection_path}/{subcollection_path}/{doc_id}"
            db.document(full_path).set(fields)
            print(f"✔️ Subido subcolección: {full_path}")
    else:
        upload_collection(path, documents)

print("\n✅ Carga completada con éxito.")
