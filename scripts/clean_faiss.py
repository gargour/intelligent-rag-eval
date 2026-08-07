"""Nettoie l'index FAISS des vecteurs dont le document_id n'existe plus en base."""
from app.vectorstore.faiss_store import get_vectorstore
from app.db.session import SessionLocal
from app.db.models import Document

def clean_orphan_vectors():
    db = SessionLocal()
    valid_ids = {d.id for d in db.query(Document.id).all()}
    db.close()

    store = get_vectorstore()
    if store.store is None:
        print("Index FAISS vide, rien à nettoyer.")
        return

    orphan_ids = [
        doc_id for doc_id, doc in store.store.docstore._dict.items()
        if doc.metadata.get("document_id") not in valid_ids
    ]

    print(f"Documents valides en base: {len(valid_ids)}")
    print(f"Vecteurs FAISS totaux: {len(store.store.docstore._dict)}")
    print(f"Vecteurs orphelins trouvés: {len(orphan_ids)}")

    if orphan_ids:
        store.store.delete(orphan_ids)
        store._persist()
        print(f"✅ {len(orphan_ids)} vecteurs orphelins supprimés.")
    else:
        print("✅ Aucun nettoyage nécessaire.")

if __name__ == "__main__":
    clean_orphan_vectors()