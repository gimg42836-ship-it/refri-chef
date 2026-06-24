import streamlit as st
import logic  # 2단계에서 만든 logic.py 파일을 가져와 연결합니다!

# 1. UI 타이틀 및 한 줄 목표 확정 (수업 가이드라인 반영)
st.title("🍳 자취방 냉장고 파먹기")
st.subheader("남은 재료만 적으세요. 완벽한 레시피를 드립니다.")

# 2. 사용자 입력창 배치 (초기 예시값 설정)
user_ingredients = st.text_input(
    "냉장고에 남은 재료를 쉼표(,)로 구분해서 적어주세요.", 
    value="김치, 계란, 스팸"
)

# 3. 추천 버튼 배치 및 API 연동 처리
if st.button("오늘의 추천 요리 보기"):
    if user_ingredients:
        # 로딩 애니메이션 표시
        with st.spinner("냉장고 탈탈 털어 레시피 짜는 중..."):
            # logic.py의 함수를 실행하여 결과 가져오기
            recipe_result = logic.get_refrigerator_recipe(user_ingredients)
            
            st.success("오늘의 추천 요리 완성!")
            st.markdown(recipe_result)  # 제미나이가 준 답변 출력
    else:
        st.warning("재료를 최소 한 개 이상 입력해주세요!")
