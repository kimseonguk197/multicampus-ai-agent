from langchain_ollama import ChatOllama
from app.ai.classification.classification_list import TOOLS

llm_classify = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

llm_with_tools = llm_classify.bind_tools(TOOLS)

def classify_message_sllm(message: str) -> str:
    response = llm_with_tools.invoke(message)

    if not response.tool_calls:
        return "응답불가합니다"

    return response.tool_calls[0]["name"]