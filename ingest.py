import sqlite3
import pypdf
from pathlib import Path

import sqlite3

# Connect to the database file
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# CORRECTED: Removed the 'TEXT' data types from the column definitions
sql_command = """
CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(
    content,
    source
);
"""

# Execute the command
cursor.execute(sql_command)

# Commit (save) the changes and close the connection
conn.commit()
conn.close()

print("Database and FTS5 table created successfully.")

import pypdf
from pathlib import Path
import sqlite3

def populate_database():
    print("Starting to populate the database...")
    pdf_directory = Path('./industrial-safety-pdfs')
    
    # Connect to the database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Loop through all PDF files in the directory
    for pdf_path in pdf_directory.glob("*.pdf"):
        print(f"Processing {pdf_path.name}...")
        
        # 1. Read the PDF
        reader = pypdf.PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
            
        # 2. Chunk the text (simple paragraph-based chunking)
        chunks = full_text.split('\n\n')
        
        # 3. Insert chunks into the database
        for chunk in chunks:
            # Clean up whitespace and skip empty chunks
            clean_chunk = chunk.strip()
            if len(clean_chunk) > 20: # Only insert meaningful chunks
                # Use parameterized query to prevent SQL injection
                cursor.execute("INSERT INTO chunks (content, source) VALUES (?, ?)", 
                               (clean_chunk, pdf_path.name))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    
    print("Database population complete.")

# --- Main execution ---
# (You might already have the table creation code here)
# Now, call the function to populate it.
populate_database()

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import sqlite3
import json

def create_embeddings_and_index():
    print("Starting embedding and indexing process...")
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # 1. Fetch all chunks from the database
    cursor.execute("SELECT rowid, content FROM chunks")
    rows = cursor.fetchall()
    # Keep track of the database ID for each chunk
    chunk_ids = [row[0] for row in rows] 
    contents = [row[1] for row in rows]
    
    conn.close()

    # 2. Load the embedding model
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 3. Generate embeddings for all chunks
    print("Generating embeddings... (This may take a few minutes)")
    embeddings = model.encode(contents, show_progress_bar=True)

    # 4. Create a FAISS index
    print("Creating FAISS index...")
    embedding_dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dimension)
    # Add the embeddings to the index
    index.add(np.array(embeddings))

    # 5. Save the index and the ID mapping
    faiss.write_index(index, 'chunks.index')
    with open('chunk_ids.json', 'w') as f:
        json.dump(chunk_ids, f)
    
    print("Embedding and indexing complete.")

# --- Main execution ---
# (You should have your table creation and populate_database() calls here)
# Now, call the new function.
create_embeddings_and_index()