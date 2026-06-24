import streamlit as st
import requests

def get_refrigerator_recipe(ingredients):
    """
    구글 API 정식 규격(models/gemini-1.5-flash)에 맞춰 직접 레시피를 요청합니다.
    """
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # [⭐ 핵심 수정] 주소 뒤쪽에 gemini-1.5-flash 대신 models/gemini-1.5-flash 가 정확히 들어가야 합니다!
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
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
        
        # 구글 서버가 정상적인 답변(candidates)을 주었는지 확인
        if 'candidates' in response_json and response_json['candidates']:
            first_candidate = response_json['candidates'][0]
            if 'content' in first_candidate and 'parts' in first_candidate['content']:
                return first_candidate['content']['parts'][0]['text']
        
        # 오류 발생 시 메시지 출력
        if 'error' in response_json:
            return f"구글 API 오류 발생: {response_json['error'].get('message', '알 수 없는 오류')}"
            
        return "구글 AI 서버가 응답을 생성하지 못했습니다. 다시 시도해 주세요."
        
    except Exception as e:
        return f"통신 중 오류가 발생했습니다: {str(e)}"