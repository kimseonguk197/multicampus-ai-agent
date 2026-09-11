
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#  SQL 조회없는 일반대화 응답 생성 LLM
#  temperature=0.5: 더 높은 자유도 부여
llm_chat = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.5,
    max_tokens=500,
)

# SQL 조회가 필요 없는 일반 대화에 응답 LLM
def format_general_response(user_message: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "데이터베이스 조회가 필요하지 않은 일반적인 대화에 자연스럽게 응답하세요.\n"
            "답변은 간결하게 1-3문장 이내로 유지하세요.",
        ),
        ("user", "{user_message}"),
    ])
    chain = prompt | llm_chat | StrOutputParser()
    return chain.invoke({"user_message": user_message})
