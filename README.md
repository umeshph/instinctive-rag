Build a small Q&A service over a tiny set of documents

## Setup ⚙️

Instructions on how to set up the project environment.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/umeshph/instinctive-rag.git)
    cd your-repository-name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

# Instinctive RAG Project

This project is a small Question & Answer (Q&A) service built over a tiny set of documents, powered by a FastAPI backend.

---

## Setup ⚙️

Follow these steps to set up the project environment on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/umeshph/instinctive-rag.git](https://github.com/umeshph/instinctive-rag.git)
    cd instinctive-rag
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## How to Run Locally ▶️

Once the setup is complete, you can run the web server on your local machine.

1.  **Navigate to the project directory** (if you're not already there):
    ```powershell
    cd D:\instinctive_rag
    ```

2.  **Activate the virtual environment**:
    ```powershell
    .\venv\Scripts\activate
    ```

3.  **Start the web server**:
    ```bash
    uvicorn api:app --reload
    ```

4.  **Access the API documentation**:
    Open your web browser and navigate to the interactive API documentation at:
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Learnings 🧠

-   **Technical Skill:** I learned how to implement data aggregation and transformation using the pandas library. For example, I used the `requests` library to efficiently handle API calls.
-   **Challenge:** One major challenge was handling missing values and inconsistent data types within the dataset, which I solved by implementing a pre-processing function that cleans the data by filling null values with the column's median and standardizing data formats.
-   **Key Takeaway:** My main takeaway is the importance of version control using Git for building robust applications.
## Results Table 📊

Present your key findings or results in a table.

| Metric        | Score | Notes                               |
|---------------|-------|-------------------------------------|
| Accuracy      | 95%   | Achieved on the validation dataset. |
| Speed (s)     | 2.5   | Average processing time per query.  |
| Model Used    | GPT-3 | Or specify your model/algorithm.    |

---

## Learnings 🧠



-   Technical Skill: I learned how to implement data aggregation and transformation using the pandas library. For example, I used the requests library to efficiently handle API calls.

Challenge: One major challenge was handling missing values and inconsistent data types within the dataset, which I solved by implementing a pre-processing function that cleans the data by filling null values with the column's median and standardizing data formats.

Key Takeaway: My main takeaway is the importance of version control using Git for building robust applications.
