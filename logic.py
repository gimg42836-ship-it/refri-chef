import streamlit as st
import requests

def get_refrigerator_recipe(ingredients):
    """
    구글 라이브러리 버그를 우회하여 API로 직접 레시피를 안전하게 요청합니다.
    """
    # 1. Streamlit Secrets에서 API 키를 안전하게 가져옵니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # 2. 구글 제미나이 최신 엔드포인트 주소 설정
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # 3. 인공지능에게 줄 명령어(프롬프트) 조립
    prompt_text = f"""
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
    
    # 4. 구글 서버가 이해할 수 있는 규격 데이터 만들기
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        # 5. 구글 AI 서버에 직접 전송
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        
        # 6. 답변 텍스트만 쏙 골라내서 반환
        return response_json['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"레시피를 가져오는 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요! (에러 상세: {str(e)})"