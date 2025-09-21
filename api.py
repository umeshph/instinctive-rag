from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sqlite3

# Import your search functions from search.py
import search

# Create the FastAPI application
app = FastAPI()

# Define the request body model
class AskRequest(BaseModel):
    q: str
    k: int = 5
    mode: str = "rerank"  # Can be 'baseline' or 'rerank'

# Define the API endpoint
@app.post("/ask")
def ask_question(request: AskRequest):
    reranker_used = False
    contexts = []

    if request.mode == "rerank":
        reranker_used = True
        search_results = search.hybrid_search(query=request.q, k=request.k)
        
        score_threshold = 100 
        if not search_results or search_results[0]['final_score'] < score_threshold:
            return {
                "answer": "Could not find a confident answer.",
                "contexts": [],
                "reranker_used": reranker_used
            }
        
        answer = search_results[0]['content']
        contexts = search_results

    else: # Baseline mode
        reranker_used = False
        ids, scores = search.vector_search(query=request.q, k=request.k)
        
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        for chunk_id, score in zip(ids, scores):
            cursor.execute("SELECT content, source FROM chunks WHERE rowid = ?", (chunk_id,))
            row = cursor.fetchone()
            if row:
                contexts.append({
                    "content": row[0],
                    "source": row[1],
                    "score": float(1 - score) # Convert to standard float
                })
        conn.close()

        score_threshold = 0.6
        if not contexts or contexts[0]['score'] < score_threshold:
             return {
                "answer": "Could not find a confident answer.",
                "contexts": [],
                "reranker_used": reranker_used
            }
        answer = contexts[0]['content']

    return {
        "answer": answer,
        "contexts": contexts,
        "reranker_used": reranker_used
    }

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)