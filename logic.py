import streamlit as st
import google.generativeai as genai

# Streamlit Cloud의 Secrets에서 API 키를 안전하게 가져옵니다.
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 최신 인공지능 모델인 gemini-1.5-flash를 설정합니다.
model = genai.GenerativeModel('gemini-1.5-flash')

def get_refrigerator_recipe(ingredients):
    """
    사용자가 입력한 재료를 바탕으로 Gemini API를 사용해 레시피를 생성합니다.
    """
    # 인공지능에게 줄 명령어(프롬프트)를 조립합니다.
    prompt = f"""
    당신은 자취생들을 위한 최고의 가성비 요리사입니다.
    현재 냉장고에 남은 재료는 다음과 같습니다: {ingredients}
    
    위 재료들을 활용해서 만들 수 있는 맛있는 요리 1가지를 추천해 주세요.
    반드시 다음 양식을 엄격하게 지켜서 답변해 주세요:
    
    1. 요리 이름: (추천 요리명)
    2. 필요한 기본 양념: (집에 있을법한 소금, 간장 등의 양념 목록)
    3. 초간단 3단계 레시피:
       - 1단계: ...
       - 2단계: ...
       - 3단계: ...
    """
    
    # 제미나이에게 질문을 던지고 답변을 받습니다.
    response = model.generate_content(prompt)
    return response.text