# text2sql

# Text-to-SQL with Schema Validation (Chinook SQLite)

This project converts **natural language questions into SQL queries** using a Large Language Model (LLM) and safely executes them on a database.

The system is designed to **prevent schema hallucination and accidental data access**, which are common and dangerous problems in AI-based Text-to-SQL systems.

---

## 🚀 What This Project Does

- Takes a **natural language question** from the user
- Converts it into **SQL using an LLM**
- **Validates SQL syntax**
- **Validates database schema usage**
- Executes the query **only if it is safe**
- Returns results from the database

The project uses **Chinook_Sqlite.sqlite** as the sample database.

---

## 🧠 Why This Project Is Important

LLMs are good at generating SQL, but they can:
- Invent table names
- Guess column names
- Accidentally access unintended or sensitive tables

In real systems, this can lead to **data leaks or security risks**.

This project prevents those issues by adding **schema-aware validation and controlled execution** before any query reaches the database.

---

## 🏗️ Architecture (High Level)

User Question
↓
LLM (Text → SQL)
↓
SQL Syntax Validation
↓
Schema Validation (Safety Gate)
↓
Read-only Query Execution
↓
Database Result



---

## 🔐 Key Safety Features

### 1. Schema Validation
Before executing SQL, the system checks:
- Which tables are used in the query
- Whether those tables actually exist in the allowed database schema

If a query references an unknown or unauthorized table, it is **blocked before execution**.

---

### 2. Read-Only Enforcement
Only `SELECT` queries are allowed.

Queries attempting:
- `INSERT`
- `UPDATE`
- `DELETE`
- `DROP`
- `ALTER`

are automatically rejected.

---

### 3. Separation of Responsibilities
- **LLM** only generates SQL
- **Validators** enforce safety rules
- **Database** executes only safe, verified queries

This separation is critical for production-grade systems.

---

## 📂 Project Structure

Text2SQL/
│
├── main.py # LangGraph workflow
├── database.py # Safe SQL execution logic
├── Dockerfile
├── Chinook_Sqlite.sqlite # Sample database
├── .dockerignore
├── uv.lock # Dependency lock file
└── README.md


---

## 🧪 Example Query

**Input (Natural Language):**


**Output (Example):**
- Artist Name
- Total Revenue
- Total Tracks Sold

(The actual values depend on the database content.)

---

## ⚠️ Limitations

- Supports **read-only analytical queries only**
- Designed for learning and demonstration purposes
- Does not include query cost estimation or rate limiting (yet)

---

## 🎯 Learning Outcomes

Through this project, you learn:
- Text-to-SQL using LLMs
- Schema hallucination prevention
- Safe query execution patterns
- LangGraph-based control flow
- Production-aware AI system design

---

## 📌 Future Improvements

- Query cost estimation
- Auto-retry with schema hints
- SQL explanation agent
- Multi-database support
- Role-based table access

---

## 👤 Author

Built as a learning project to understand **real-world risks and safeguards** in AI-powered database systems.
