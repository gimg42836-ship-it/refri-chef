import google.generativeai as genai

# 발급받은 제미나이 API 키를 여기에 입력하세요
genai.configure(api_key="AQ.Ab8RN6IzSDg9wDSsbT-dw9KAFSDKWJYZJ4SdGyeaLVQPB3C4Sw") 

def get_refrigerator_recipe(ingredients):
    """사용자가 입력한 재료로 레시피를 생성하는 함수"""
    model = genai.GenerativeModel('gemini-pro')
    
    # 4대 요소를 반영한 프롬프트 설계 [cite: 18]
    prompt = f"""
    너는 제한된 재료로 최고의 가성비 요리를 만드는 자취 요리 전문 유튜버야.
    사용자가 냉장고에 남은 재료들을 입력하면, 그 재료들을 활용한 초간단 요리를 추천해야 해.
    
    [입력된 재료]: {ingredients}
    
    [출력 형식]:
    1. 요리 이름: (재치 있는 이름으로 지어줘)
    2. 필요한 추가 기본 양념: (자취방에 흔히 있는 간장, 설탕, 소금 등만 허용)
    3. 조리 단계: (대학생 자취생이 이해하기 쉽게 딱 3단계로 요약)
    """
    
    response = model.generate_content(prompt)
    return response.text
