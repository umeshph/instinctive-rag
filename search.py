import sqlite3
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import re

# --- LOAD ASSETS ---
print("Loading search assets...")
# Load the embedding model
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
# Load the FAISS index
INDEX = faiss.read_index('chunks.index')
# Load the mapping from index position to chunk ID
with open('chunk_ids.json', 'r') as f:
    CHUNK_IDS = json.load(f)
print("Assets loaded successfully.")

def vector_search(query: str, k: int = 10):
    """Performs a pure vector similarity search."""
    query_embedding = MODEL.encode([query])
    D, I = INDEX.search(np.array(query_embedding), k)
    retrieved_chunk_ids = [CHUNK_IDS[i] for i in I[0]]
    scores = D[0]
    return retrieved_chunk_ids, scores

def hybrid_search(query: str, k: int = 5):
    """Performs a hybrid search combining vector search with FTS keyword search."""
    initial_k = k * 5
    retrieved_chunk_ids, vector_scores = vector_search(query, k=initial_k)
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    results = []
    
    clean_query = re.sub(r'[^\w\s]', '', query)
    fts_query = " OR ".join(clean_query.split())

    for chunk_id, vec_score in zip(retrieved_chunk_ids, vector_scores):
        sql = f"SELECT rank, content, source FROM chunks WHERE rowid = ? AND chunks MATCH '{fts_query}'"
        cursor.execute(sql, (chunk_id,))
        
        row = cursor.fetchone()
        if row:
            fts_score = 1.0 / (row[0] * -1) if row[0] != 0 else 0
            results.append({
                "id": chunk_id,
                "content": row[1],
                "source": row[2],
                "vector_score": float(1 - vec_score), # Convert to standard float
                "fts_score": float(fts_score)        # Convert to standard float
            })
    conn.close()
    
    for item in results:
        item['final_score'] = (0.6 * item['vector_score']) + (0.4 * item['fts_score'])
        
    results.sort(key=lambda x: x['final_score'], reverse=True)
    
    return results[:k]

if __name__ == '__main__':
    print("\n--- Testing Vector Search ---")
    ids, scores = vector_search("What is a safety relay?")
    print(f"Retrieved chunk IDs: {ids}")
    
    print("\n--- Testing Hybrid Search ---")
    final_results = hybrid_search("What is a safety relay?", k=3)
    if final_results:
        for res in final_results:
            print(f"Source: {res['source']}, Score: {res['final_score']:.4f}")
            print(f"Content: {res['content'][:200]}...\n")