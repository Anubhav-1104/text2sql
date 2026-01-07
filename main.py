from langgraph.graph import StateGraph , START , END
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser , PydanticOutputParser
from typing import TypedDict , Literal
from database import check_against_db , get_schema , format_schema
from pydantic import BaseModel

llm = ChatOllama(model='gpt-oss:120b-cloud')

class SQL(TypedDict):
    user_query:str
    response:str
    validator:str
    syntax_error:str
    corrector:str
    executor:str

# class StructuredResponse(BaseModel):
#     exccution:Literal['Success' , 'Runrtime Error']

# parser = PydanticOutputParser(pydantic_object=StructuredResponse)

# structured_llm = llm | parser


def user_query(state: SQL):
    schema = get_schema()
    schema_text = format_schema(schema)

    prompt = f"""
You are a SQL expert.

Use ONLY the following database schema.
DO NOT invent tables or columns.
If the question cannot be answered using this schema, say "Cannot answer".

{schema_text}

User Question:
{state['user_query']}

Return ONLY raw SQL. No markdown.
"""

    response = llm.invoke(prompt)
    return {"response": response.content.strip()}



def syntax_validation_node(state: SQL):
    prompt = f"""
Validate SQL syntax.

SQL:
{state['response']}

Reply only with:
Valid or Invalid
"""
    response = llm.invoke(prompt)
    return {"validator": response.content.strip()}


def check_validator(state: SQL):
    value = state["validator"].strip().lower()

    if value == "valid":
        return "query_execution_node"
    else:
        return "syntax_error_analyzer"


    
def syntax_error_analyzer(state: SQL):
    prompt = f"""
Find syntax errors in this SQL.

SQL:
{state['response']}

Return ONLY error message.
"""
    response = llm.invoke(prompt)
    return {"syntax_error": response.content.strip()}


def correction_node(state: SQL):
    prompt = f"""
Correct the SQL using the error.

SQL:
{state['response']}

Error:
{state['syntax_error']}

Return ONLY corrected SQL.
"""
    response = llm.invoke(prompt)
    return {"corrector": response.content.strip()}

def validate_sql_against_schema(sql: str, schema: dict):
    sql_lower = sql.lower()

    allowed_tables = {table.lower() for table in schema.keys()}

    words = sql_lower.replace(",", " ").split()

    used_tables = []

    for i, word in enumerate(words):
        if word in ("from", "join") and i + 1 < len(words):
            table = words[i + 1]
            used_tables.append(table)

    for table in used_tables:
        if table not in allowed_tables:
            return False

    return True




def query_execution_node(state: SQL):
    try:
        sql = state.get("corrector") or state["response"]

        schema = get_schema()
        is_safe = validate_sql_against_schema(sql, schema)

        if not is_safe:
            return {"executor": "Blocked: Query uses invalid schema"}

        result = check_against_db(sql)
        return {"executor": f"Success: {result}"}

    except Exception as e:
        return {"executor": f"Runtime Error: {str(e)}"}


graph = StateGraph(SQL)

graph.add_node("user_query", user_query)
graph.add_node("syntax_validation_node", syntax_validation_node)
graph.add_node("syntax_error_analyzer", syntax_error_analyzer)
graph.add_node("correction_node", correction_node)
graph.add_node("query_execution_node", query_execution_node)

graph.add_edge(START, "user_query")
graph.add_edge("user_query", "syntax_validation_node")
graph.add_conditional_edges("syntax_validation_node", check_validator)
graph.add_edge("syntax_error_analyzer", "correction_node")
graph.add_edge("correction_node", "query_execution_node")
graph.add_edge("query_execution_node", END)

workflow = graph.compile()


initial_state = {
    "user_query": "List the top 5 artists whose albums have generated the highest total sales revenue. For each artist, show the artist name, total revenue, and total number of tracks sold. Sort the result by total revenue in descending order."
}

print(workflow.invoke(initial_state))
