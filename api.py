import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# 1. Initialize the FastAPI app
app = FastAPI(
    title="Instinctive RAG Q&A Service",
    description="A simple service to ask questions over a set of documents."
)

# 2. Create the security object for HTTP Basic Auth
security = HTTPBasic()

# 3. Define a function to check user credentials
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Checks the provided username and password against hardcoded values.
    In a real-world application, you would check against a database.
    """
    # Use secrets.compare_digest to prevent timing attacks
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- Your Project's Core Logic ---
# You can import your search function from search.py or define it here.
def perform_search(query: str) -> dict:
    """
    A placeholder for your actual search logic.
    This function should take a query and return the search results.
    """
    # Replace this with a call to your actual search function
    print(f"Performing search for: {query}")
    return {
        "query": query,
        "results": [
            {
                "text": "This is a sample result from your documents.",
                "source": "document1.pdf",
                "score": 0.95
            }
        ]
    }
# ------------------------------------

# 4. Define the main API endpoint and protect it
@app.post("/search")
def search_documents(query: str, username: str = Depends(get_current_username)):
    """
    Performs a Q&A search on the indexed documents.

    This endpoint is protected and requires a valid username and password.
    - **query**: The question you want to ask.
    """
    # The code below will only run if authentication is successful.
    results = perform_search(query)
    return results

# 5. (Optional) A root endpoint for basic health checks
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the Instinctive RAG API!"}