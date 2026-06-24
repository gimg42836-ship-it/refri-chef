import streamlit as st
import requests

def get_refrigerator_recipe(ingredients):
    """
    구글 서버의 일시적 오류나 빈 응답(candidates 에러)을 완벽하게 방어합니다.
    """
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
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
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        
        # [⭐ 에러 방어 핵심] 구글 서버가 정상적인 답변(candidates)을 주었는지 먼저 확인합니다.
        if 'candidates' in response_json and response_json['candidates']:
            first_candidate = response_json['candidates'][0]
            if 'content' in first_candidate and 'parts' in first_candidate['content']:
                return first_candidate['content']['parts'][0]['text']
        
        # 만약 구글 서버에서 에러 메세지를 보냈다면 무슨 내용인지 친절하게 알려줍니다.
        if 'error' in response_json:
            return f"구글 API 오류 발생: {response_json['error'].get('message', '알 수 없는 오류')}"
            
        return "구글 AI 서버가 순간적으로 응답을 생성하지 못했습니다. 재료를 조금 더 자세히 적고 다시 버튼을 눌러주세요!"
        
    except Exception as e:
        return f"통신 중 오류가 발생했습니다: {str(e)}"