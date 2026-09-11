from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


llm_response = ChatOllama(
    model="llama3.2:3b",
    temperature=0.3
)


def generate_response_sllm(user_message: str, data: str) -> str:

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "사용자의 질문에 대해 아래 참고 데이터를 바탕으로 사용자의 질문에 답변해. "
            "만약 참고데이터에 적절한 내용이 없으면 응답불가합니다 라고 답변해.\n\n"
            "[참고 데이터]\n{data}"
        ),
        ("user", "{user_message}"),
    ])

    chain = prompt | llm_response | StrOutputParser()

    response = chain.invoke({
        "data": data,
        "user_message": user_message
    })

    return response