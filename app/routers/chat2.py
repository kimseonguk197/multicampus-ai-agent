from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db, get_current_member
from app.text_to_sql.chat_classify import classify_intent
from app.text_to_sql.sql.sql_pipeline import call_sql_pipeline
from app.text_to_sql.action.action_pipeline import call_action_pipeline
from app.text_to_sql.general_response import format_general_response


router_v2 = APIRouter(prefix="/chats/v2")
@router_v2.post("",response_model=schemas.ChatResponse,status_code=status.HTTP_201_CREATED,)
def create_chat_v2(
    body: schemas.ChatRequest,
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_member),
):
    print("text-to-sql")

    result = process_text_to_sql(body.message, db, current_member.id)

    # 대화 이력 저장
    chat_record = models.Chat(
        member_id=current_member.id,
        request=body.message,
        response=result,
    )
    db.add(chat_record)
    db.commit()
    db.refresh(chat_record)

    return chat_record


# 의도 분류 후 QUERY/ACTION/GENERAL 파이프라인으로 라우팅 (chat.py의 get_api 분기에서도 재사용)
def process_text_to_sql(message: str, db: Session, member_id: int) -> str:
    intent = classify_intent(message)
    print(f"[파이프라인] 의도 분류 결과: {intent}")

    # 1)질의를 SQL로 변환(TEXT-TO-SQL)
    if intent == "QUERY":
        return call_sql_pipeline(message, db, member_id)
    # 2)기존API활용 작업(insert, update 등)
    elif intent == "ACTION":
        return call_action_pipeline(message, db, member_id)
    # 3)DB 작업 없는 일반 LLM응답
    else:
        return format_general_response(message)
