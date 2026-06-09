import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# 1. 페이지 기본 설정 및 와이드 모드
st.set_page_config(
    layout="wide", 
    page_title="The Language of Fashion — Dashboard",
    initial_sidebar_state="expanded"
)

# 2. 깔끔한 고딕체 중심의 가독성 극대화 CSS (이모티콘 매칭 반영)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
        
        /* 전체 배경 및 깔끔한 폰트 세팅 */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            font-family: 'Noto Sans KR', sans-serif !important;
            color: #111111;
        }
        
        /* 사이드바 미니멀 디자인 */
        [data-testid="stSidebar"] {
            background-color: #F9F9F9 !important;
            border-right: 1px solid #EAEAEA;
        }
        
        /* 가독성을 높인 타이틀 & 텍스트 */
        .web-sub {
            font-size: 14px;
            letter-spacing: 2px;
            color: #777777;
            font-weight: 500;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        .web-title {
            font-size: 40px;
            font-weight: 900;
            letter-spacing: -1px;
            line-height: 1.2;
            color: #111111 !important;
            margin-bottom: 10px;
        }
        .web-caption {
            font-size: 15px;
            color: #555555;
            font-weight: 400;
            margin-bottom: 30px;
        }
        
        /* 구분선 */
        .section-line {
            border-top: 2px solid #111111;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        .section-sub-line {
            border-top: 1px solid #EAEAEA;
            margin-top: 30px;
            margin-bottom: 30px;
        }
        
        /* 지표 카드 블록 */
        .metric-wrapper {
            border-left: 3px solid #111111;
            padding-left: 15px;
            margin-bottom: 20px;
        }
        .metric-label {
            font-size: 13px;
            font-weight: 500;
            letter-spacing: 0.5px;
            color: #666666;
        }
        .metric-value {
            font-size: 30px;
            font-weight: 700;
            color: #111111;
            margin-top: 5px;
        }
        
        /* 섹션 타이틀 */
        .section-title {
            font-size: 20px;
            font-weight: 700;
            color: #111111 !important;
            margin-bottom: 5px;
        }
        .section-desc {
            font-size: 13px;
            color: #666666;
            margin-bottom: 25px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터셋 로드 (200개 코퍼스)
@st.cache_data
def load_large_data():
    brands = (
        ["무신사 스탠다드"] * 50 + ["스파오"] * 50 + 
        ["마르디 메크르디"] * 40 + ["인사일런스"] * 30 + ["헌치"] * 30
    )
    brand_types = ["SPA"] * 100 + ["Designer"] * 100
    
    product_names = [
        # --- 무신사 스탠다드 (50개) ---
        "쿨탠다드 베이직 티셔츠", "에센셜 라운드 넥 반팔티", "릴렉스핏 크루넥 티셔츠", "데일리 코튼 반팔 셔츠", "린넨 블렌드 릴렉스 셔츠",
        "쿨 오버핏 레이어드 티셔츠", "베이직 무지 반팔티 팩", "피케 카라 반팔 셔츠", "기능성 쿨링 드라이 티셔츠", "스탠다드 피트 카라티",
        "스트레치 베이직 셔츠", "데일리 레이어드 나시 티셔츠", "쿨 베이직 옥스포드 셔츠", "에센셜 브이넥 반팔", "헤비웨이트 라운드 티셔츠",
        "와이드 오픈카라 셔츠", "베이직 가디건 레이어드 셔츠", "쿨탠다드 리브드 티셔츠", "워크웨어 가먼트다잉 셔츠", "릴렉스 다잉 반팔티",
        "스탠다드 워시드 코튼 셔츠", "에센셜 투팩 반팔 레이어드", "컴포트 핏 옥스포드 반팔", "데일리 미니멀 반팔 셔츠", "린넨 베이직 반팔 셔츠",
        "라이트웨이트 베이직 윈드브레이커", "미니멀 카고 스트레치 팬츠", "에센셜 테이퍼드 치노 팬츠", "데일리 슬림핏 데님 스커트", "스탠다드 컴포트 셋업 자켓",
        "쿨 베이직 슬랙스", "릴렉스 실루엣 와이드 슬랙스", "에센셜 리넨 라이크 자켓", "데일리 옥스포드 롱 셔츠", "미니멀 라운드 가디건",
        "쿨탠다드 기능성 드라이 패키지", "베이직 드로스트링 조거 팬츠", "컴포트 핏 피케 셔츠", "스트레치 릴렉스드 팬츠", "에센셜 코튼 카고 스커트",
        "데일리 윈터 써모 가디건", "헤비웨이트 미니멀 후드집업", "스탠다드 워시드 데님 자켓", "릴렉스핏 카라 스웨터", "쿨 베이직 스트라이프 티셔츠",
        "에센셜 드레스 소포트 셔츠", "미니멀리즘 컴포트 슬랙스", "데일리 에어 가디건", "린넨 블렌드 데일리 원피스", "스탠다드 언더웨어 코튼 팩",
        # --- 스파오 (50개) ---
        "루즈핏 코튼 그래픽 티셔츠", "편안한 린넨 블렌드 셔츠", "캐주얼 카라 반팔 셔츠", "쿨테크 오버핏 반팔티", "데일리 스트라이프 셔츠",
        "베이직 옥스포드 반팔 셔츠", "그래픽 프린팅 나염 티셔츠", "소프트 터치 크루넥 반팔", "루즈핏 카라 피케티", "이지케어 오픈카라 셔츠",
        "쿨링 에센셜 레이어드 티", "캐주얼 워시드 데님 셔츠", "오버핏 무지 카라 셔츠", "컴포트핏 베이직 티셔츠", "린넨 라이크 루즈핏 가디건 셔츠",
        "데일리 스웨트 반팔 셔츠", "어반 베이직 포켓 티셔츠", "소프트 코튼 반팔 셔츠", "스트릿 루즈핏 나염 반팔", "이지 드라이 쿨 반팔티",
        "컴포트 베이직 스트라이프 셔츠", "루즈핏 미니멀 포켓 티셔츠", "이지 쿨링 라운드 넥", "어반 캐주얼 오픈카라", "스파오 에센셜 코튼 셔츠",
        "웜테크 데일리 발열 내의", "캐주얼 코듀로이 와이드 팬츠", "이지 밴딩 데님 스커트", "루즈핏 그래픽 후드 스웨트", "스트릿 아웃포켓 카고 팬츠",
        "편안한 이지 가디건", "어반 스트라이프 롱 셔츠", "쿨테크 드라이 포켓 카라티", "소프트 플리스 캐주얼 집업", "루즈핏 베이직 패딩 조끼",
        "데일리 코튼 카고 반바지", "어반 스타일리시 셋업 자켓", "이지케어 링클프리 데일리 셔츠", "스트릿 나염 프린팅 롱 슬리브", "캐주얼 데님 오버롤 스커트",
        "소프트 터치 캐주얼 니트 가디건", "루즈핏 쿨링 린넨 자켓", "스파오 캐릭터 콜라보 그래픽 티", "데일리 이지 밴딩 슬랙스", "어반 라이프 옥스포드 셔츠",
        "웜테크 하이넥 소프트 스웨터", "캐주얼 가먼트다잉 스웨트 팬츠", "루즈핏 후드 레이어드 셔츠", "이지 스트레치 캐주얼 면바지", "스파오 베이직 스니커즈 슬립온",
        # --- 마르디 메크르디 (40개) ---
        "TSHIRT FLOWER MARDI CLASSIC", "TSHIRT LES BLOSSOM SIGNATURE", "SWEATSHIRT ECLORE ESSENTIAL", "MARDI LOGO EMBLEM SHIRT", "TSHIRT UNIVERSE FLOWER",
        "프렌치 로고 자수 반팔 티셔츠", "시그니처 플라워 프린팅 티셔츠", "블라썸 아카이브 오버핏 반팔", "CLASSIC MARDI EMBROIDERY SHIRT", "프렌치 가든 그래픽 티셔츠",
        "TSHIRT FLOWER MARDI BLOSSOM", "LEES SIGNATURE LOGO TEE", "프렌치 무드 셔링 카라 블라우스", "MARDI ARCHIVE PREMIUM SHIRT", "엠블럼 자수 크롭 반팔티",
        "TSHIRT FLOWER MARDI VINTAGE", "프렌치 리본 그래픽 티셔츠", "CLASSIC LOGO OVERSIZED SHIRT", "시그니처 플라워 레터링 반팔티", "MARDI PIQUE 블라썸 셔츠",
        "SWEATSHIRT FLOWER MARDI NEEDLEWORK", "CARDIGAN LA BLOSSOM V-NECK", "HOODIE MARDI EMBLEM OVERSIZED", "MARDI SIGNATURE BOUCLE SWEATER", "프렌치 자수 니트 스커트",
        "FLOWER MARDI JACQUARD PANTS", "시그니처 로고 프렌치 베레모", "블라썸 아카이브 가죽 숄더백", "MARDI LOGO JACQUARD MINI SKIRT", "프렌치 로맨틱 레이스 가디건",
        "TSHIRT MARDI EMBLEM CROPPED", "SWEATSHIRT LES FLOWER SIGNATURE", "MARDI LOGO SILK SCARF", "프렌치 아카이브 코튼 원피스", "시그니처 리본 트위드 자켓",
        "MARDI ECO LEATHER JACKET MINI", "CLASSIC MARDI KNIT VEST", "프렌치 가든 패턴 롱 스커트", "TSHIRT FLOWER MARDI WHITE", "MARDI EMBLEM PREMIUM CARDIGAN",
        # --- 인사일런스 (30개) ---
        "미니멀 아키텍처 오버핏 셔츠", "드레이프 실루엣 반팔 티셔츠", "익스클루시브 디테일 크루넥", "모던 미니멀리즘 반팔 셔츠", "아카이브 스트럭처 반팔티",
        "구조적 실루엣 레이어드 셔츠", "테일러드 디테일 카라 셔츠", "미니멀리즘 링클 프리 셔츠", "오버사이즈 실루엣 가먼트 셔츠", "익스클루시브 원단 워시드 셔츠",
        "모던 아카이브 포켓 반팔티", "비대칭 디테일 미니멀 셔츠", "드레이프 코튼 레이어드 티셔츠", "아키텍처 레이아웃 그래픽 티", "인사일런스 익스클루시브 셔츠",
        "모던 아키텍처 발마칸 코트", "드레이프 실루엣 울 슬랙스", "익스클루시브 가죽 트렌치 자켓", "미니멀 스트럭처 패딩 자켓", "테일러드 아카이브 블레이저",
        "구조적 디자인 해링턴 자켓", "비대칭 디테일 와이드 팬츠", "미니멀리즘 크롭 블루종 자켓", "드레이프 링클 프리 모던 셔츠", "인사일런스 시그니처 레더 셔츠",
        "오버사이즈 스트럭처 모던 코트", "아키텍처 레이아웃 가디건", "테일러드 실루엣 데님 팬츠", "모던 미니멀 싱글 자켓", "익스클루시브 텍스처 울 스웨터",
        # --- 헌치 (30개) ---
        "타임리스 프렌치 클래식 셔츠", "소프트 클래식 무드 반팔티", "로맨틱 시어 레이어드 블라우스", "프렌치 시그니처 로고 티셔츠", "타임리스 미니멀 원피스 셔츠",
        "소프트 코튼 링클 셔츠", "내추럴 클래식 옥스포드 셔츠", "프렌치 가든 소프트 가디건 셔츠", "타임리스 아카이브 리넨 셔츠", "앤티크 로맨틱 자수 셔츠",
        "프렌치 클래식 스트라이프 반팔", "소프트 실루엣 카라 셔츠", "타임리스 베이직 포켓 셔츠", "내추럴 무드 레이어드 티셔츠", "헌치 클래식 에센셜 셔츠",
        "로맨틱 트위드 타임리스 자켓", "앤티크 무드 레이스 블라우스", "소프트 클래식 플리츠 스커트", "프렌치 헌치 에센셜 원피스", "타임리스 숄더 리본 블라우스",
        "내추럴 시어 레이어드 가디건", "로맨틱 아카이브 트렌치 코트", "소프트 실루엣 플레어 스커트", "프렌치 가든 자수 자켓", "타임리스 미니멀 슬랙스 패키지",
        "앤티크 플라워 로맨틱 원피스", "내추럴 코튼 소프트 자켓", "헌치 프렌치 시그니처 스카프", "소프트 클래식 롱 가디건", "로맨틱 빈티지 레이어드 스커트"
    ]
    
    categories = (
        ["상의"] * 25 + ["하의"] * 10 + ["아우터"] * 10 + ["잡화"] * 5 +
        ["상의"] * 25 + ["하의"] * 10 + ["아우터"] * 10 + ["잡화"] * 5 +
        ["상의"] * 20 + ["하의"] * 5 + ["아우터"] * 10 + ["잡화"] * 5 +
        ["상의"] * 15 + ["하의"] * 5 + ["아우터"] * 10 +
        ["상의"] * 15 + ["하의"] * 5 + ["아우터"] * 5 + ["잡화"] * 5
    )
    
    seasons = (
        ["SS"] * 35 + ["FW"] * 15 + ["SS"] * 35 + ["FW"] * 15 +
        ["SS"] * 25 + ["FW"] * 15 + ["SS"] * 15 + ["FW"] * 15 + ["SS"] * 20 + ["FW"] * 10
    )
    
    prices = (
        [19900, 25900, 29900, 39900, 49000] * 10 + [25900, 39900, 49900, 59900, 79000] * 10 +
        [42000, 45000, 68000, 75000, 89000, 128000, 159000, 189000] * 5 +
        [59000, 79000, 89000, 149000, 219000, 289000] * 5 +
        [48000, 68000, 78000, 88000, 128000, 168000] * 5
    )
    
    df = pd.DataFrame({
        "brand": brands,
        "brand_type": brand_types,
        "product_name": product_names,
        "category": categories,
        "season": seasons,
        "price": prices
    })
    return df

df = load_large_data()

# 뻔한 카테고리 단어 필터링 세팅
STOPWORDS = {
    "셔츠", "티셔츠", "반팔티", "반팔", "블라우스", "카라티", "나시", "원피스", "팩", "투팩", "원단", "팬츠", "슬랙스", 
    "스커트", "자켓", "가디건", "코트", "패딩", "스웨터", "니트", "집업", "바지", "면바지", "원피스", "후드집업",
    "SHIRT", "TSHIRT", "TEE", "SWEATSHIRT", "MARDI", "LEES", "인사일런스", "스파오", "넥", "라운드", "크루넥", "HOODIE", "CARDIGAN"
}

def extract_fashion_keywords(text_series):
    words = []
    for text in text_series:
        cleaned = re.sub(r'[^\w\s]', ' ', text)
        for w in cleaned.split():
            w_upper = w.upper()
            if len(w_upper) > 1 and w_upper not in STOPWORDS:
                words.append(w_upper)
    return words

def get_language_type(text):
    has_ko = bool(re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', text))
    has_en = bool(re.search(r'[a-zA-Z]', text))
    if has_ko and has_en: return "Mixed (한글+영어)"
    elif has_en: return "English (영어)"
    else: return "Korean (한글)"

def analyze_mood_category(text):
    text_upper = text.upper()
    if any(k in text_upper for k in ["미니멀", "MINIMAL", "에센셜", "ESSENTIAL", "베이직", "BASIC", "스탠다드", "STANDARD"]):
        return "Minimal & Essential"
    elif any(k in text_upper for k in ["클래식", "CLASSIC", "타임리스", "TIMELESS", "테일러드", "TAILORED"]):
        return "Classic & Timeless"
    elif any(k in text_upper for k in ["프렌치", "FRENCH", "로맨틱", "ROMANTIC", "앤티크", "ANTIQUE", "블라썸", "BLOSSOM"]):
        return "French & Romantic"
    elif any(k in text_upper for k in ["데일리", "DAILY", "캐주얼", "CASUAL", "루즈핏", "오버핏", "스트릿", "STREET"]):
        return "Daily & Casual"
    else:
        return "Modern Unique"

df['lang_type'] = df['product_name'].apply(get_language_type)
df['mood_type'] = df['product_name'].apply(analyze_mood_category)
df['name_length'] = df['product_name'].apply(len)

# 4. 상단 헤더 레이아웃 (이모티콘 매칭)
st.markdown('<div class="web-sub">🗂️ Portfolio Project — 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="web-title">👔 The Language of Fashion Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="web-caption">Fashion Design · SKKU · Brand Marketing Focus</div>', unsafe_allow_html=True)
st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

# 5. 내비게이션 / 사이드바 멀티 필터링
st.sidebar.markdown("### 🎛️ 01 — Filter Collection", unsafe_allow_html=True)
selected_types = st.sidebar.multiselect("🏷️ COLLECTION TYPE", options=["SPA", "Designer"], default=["SPA", "Designer"])

available_brands = df[df['brand_type'].isin(selected_types)]['brand'].unique()
selected_brands = st.sidebar.multiselect("🏢 BRANDS SELECTION", options=list(available_brands), default=list(available_brands))

selected_categories = st.sidebar.multiselect("🧥 PRODUCT CATEGORY", options=list(df['category'].unique()), default=list(df['category'].unique()))
selected_seasons = st.sidebar.select_slider("☀️ SEASON SPECTRIC", options=["ALL", "SS", "FW"], value="ALL")

# 필터 바인딩
filtered_df = df[(df['brand_type'].isin(selected_types)) & (df['brand'].isin(selected_brands)) & (df['category'].isin(selected_categories))]
if selected_seasons != "ALL":
    filtered_df = filtered_df[filtered_df['season'] == selected_seasons]

# 6. 미니멀 지표 스코어보드 (이모티콘 적용)
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.markdown('<div class="metric-wrapper"><div class="metric-label">📦 Total Corpus Items</div><div class="metric-value">' + f"{len(filtered_df)}" + ' items</div></div>', unsafe_allow_html=True)
with m_col2:
    st.markdown('<div class="metric-wrapper"><div class="metric-label">💰 Average Base Price</div><div class="metric-value">₩' + f"{int(filtered_df['price'].mean()):,}" + '</div></div>', unsafe_allow_html=True)
with m_col3:
    st.markdown('<div class="metric-wrapper"><div class="metric-label">✨ Active Brands</div><div class="metric-value">' + f"{filtered_df['brand'].nunique()}" + ' brands</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-sub-line"></div>', unsafe_allow_html=True)

# 7. 시각화 섹션 1 & 2
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown('<div class="section-title">📊 02 — Style Descriptors & Adjectives</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">상품 복종 명칭을 정제하고 남은 핵심 스타일 브랜드 수식어 빈도</div>', unsafe_allow_html=True)
    
    all_words = extract_fashion_keywords(filtered_df['product_name'])
    if all_words:
        word_counts = Counter(all_words).most_common(10)
        word_df = pd.DataFrame(word_counts, columns=['Keyword', 'Count'])
        fig_bar = px.bar(word_df, x='Count', y='Keyword', orientation='h', color_discrete_sequence=['#111111'])
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=0, r=20, t=0, b=0), xaxis_title=None, yaxis_title=None)
        fig_bar.update_xaxes(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111')
        fig_bar.update_yaxes(linecolor='#111111')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.write("선택된 조건에 수식어가 없습니다.")

with chart_col2:
    st.markdown('<div class="section-title">🌐 03 — Linguistic Typology</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">네이밍 시 투영된 한글, 영어, 혼용(Mixed) 등 언어 유형별 쉐어</div>', unsafe_allow_html=True)
    if not filtered_df.empty:
        lang_counts = filtered_df['lang_type'].value_counts().reset_index()
        lang_counts.columns = ['Language Type', 'Count']
        fig_pie = px.pie(lang_counts, values='Count', names='Language Type', color_discrete_sequence=['#111111', '#666666', '#CCCCCC'])
        fig_pie.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

st.markdown('<div class="section-sub-line"></div>', unsafe_allow_html=True)

# 8. 시각화 섹션 3 & 4 (신규 차트)
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.markdown('<div class="section-title">🖤 04 — Brand Emotional Mood Segment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">어감 형태소 분류를 통해 추출한 브랜드별 감성 타겟 포지션</div>', unsafe_allow_html=True)
    if not filtered_df.empty:
        mood_df = filtered_df.groupby(['brand', 'mood_type']).size().reset_index(name='Count')
        fig_mood = px.bar(mood_df, x='brand', y='Count', color='mood_type', 
                          color_discrete_sequence=['#111111', '#444444', '#888888', '#CCCCCC', '#EAEAEA'])
        fig_mood.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=0, r=0, t=10, b=0), xaxis_title=None, yaxis_title=None, legend_title=None)
        fig_mood.update_xaxes(linecolor='#111111')
        fig_mood.update_yaxes(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111')
        st.plotly_chart(fig_mood, use_container_width=True)

with chart_col4:
    st.markdown('<div class="section-title">✏️ 05 — Product Name Length Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">브랜드 타입별 상품명 글자 수 스펙트럼 (정보 위주 vs 감성 서술형)</div>', unsafe_allow_html=True)
    if not filtered_df.empty:
        fig_box = px.box(filtered_df, x='brand_type', y='name_length', color='brand_type',
                         color_discrete_map={'SPA': '#888888', 'Designer': '#111111'})
        fig_box.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=0, r=0, t=10, b=0), xaxis_title=None, yaxis_title="Character Length", showlegend=False)
        fig_box.update_xaxes(linecolor='#111111')
        fig_box.update_yaxes(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111')
        st.plotly_chart(fig_box, use_container_width=True)

st.markdown('<div class="section-sub-line"></div>', unsafe_allow_html=True)

# 9. 마켓 포지셔닝 스캐터 매트릭스
st.markdown('<div class="section-title">🎯 06 — Brand Market Positioning Map</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">시즌별 브랜드 가격 스펙트럼 및 복합 포지셔닝</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    fig_scatter = px.scatter(filtered_df, x='brand', y='price', color='brand_type', symbol='season',
                             hover_data=['product_name'], size=[10]*len(filtered_df),
                             color_discrete_map={'SPA': '#777777', 'Designer': '#111111'})
    fig_scatter.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=0, r=0, t=20, b=0), xaxis_title=None, yaxis_title=None)
    fig_scatter.update_xaxes(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111')
    fig_scatter.update_yaxes(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111')
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown('<div class="section-sub-line"></div>', unsafe_allow_html=True)

# 10. 로우 데이터 아카이브
st.markdown('<div class="section-title">🔍 07 — Archive & Data Collection Search</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">분석에 사용된 전체 패션 브랜드 말뭉치 로우 데이터 검색</div>', unsafe_allow_html=True)

search_query = st.text_input("⌨️ Search Concept Word (e.g. 베이직, 에센셜, CLASSIC, 실루엣)")

if search_query:
    display_df = filtered_df[filtered_df['product_name'].str.contains(search_query, case=False)]
else:
    display_df = filtered_df

st.dataframe(display_df[['brand', 'brand_type', 'product_name', 'category', 'season', 'price', 'lang_type', 'mood_type']], use_container_width=True)

# 11. 웹진형 푸터
st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 11px; color: #888888;">© 2026 Jiyoon Lee · Fashion Design, SKKU · All rights reserved.</p>', unsafe_allow_html=True)
