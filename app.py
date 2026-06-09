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

# 2. 개인 포트폴리오 웹사이트 감성 (Minimal Black & White) CSS 주입
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Noto+Sans+KR:wght@300;400;700&display=swap');
        
        /* 전체 배경 및 기본 폰트 세팅 */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            font-family: 'Noto Sans KR', sans-serif;
            color: #111111;
        }
        
        /* 사이드바 미니멀리즘 디자인 */
        [data-testid="stSidebar"] {
            background-color: #F9F9F9 !important;
            border-right: 1px solid #EAEAEA;
        }
        
        /* 세련된 웹진 스타일 타이틀 & 텍스트 */
        .web-sub {
            font-family: 'Playfair Display', serif;
            font-size: 16px;
            font-style: italic;
            letter-spacing: 1px;
            color: #666666;
            margin-bottom: 5px;
        }
        .web-title {
            font-family: 'Playfair Display', serif;
            font-size: 46px;
            font-weight: 700;
            letter-spacing: -1px;
            line-height: 1.1;
            margin-bottom: 10px;
        }
        .web-caption {
            font-size: 15px;
            color: #555555;
            font-weight: 300;
            margin-bottom: 30px;
        }
        
        /* 섹션 구분선 */
        .section-line {
            border-top: 1px solid #111111;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        .section-sub-line {
            border-top: 1px solid #EAEAEA;
            margin-top: 30px;
            margin-bottom: 30px;
        }
        
        /* 미니멀 메트릭 카드 블록 */
        .metric-wrapper {
            border-left: 1px solid #111111;
            padding-left: 15px;
            margin-bottom: 20px;
        }
        .metric-label {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #888888;
        }
        .metric-value {
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            font-weight: 700;
            color: #111111;
            margin-top: 5px;
        }
        
        /* 섹션 헤더 */
        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .section-desc {
            font-size: 13px;
            color: #777777;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 후 정제
@st.cache_data
def load_data():
    data = {
        "brand": (
            ["무신사 스탠다드"] * 25 + ["스파오"] * 25 + 
            ["마르디 메크르디"] * 20 + ["인사일런스"] * 15 + ["헌치"] * 15
        ),
        "brand_type": (
            ["SPA"] * 50 + ["Designer"] * 50
        ),
        "product_name": [
            "쿨탠다드 베이직 티셔츠", "에센셜 라운드 넥 반팔티", "릴렉스핏 크루넥 티셔츠", "데일리 코튼 반팔 셔츠", "린넨 블렌드 릴렉스 셔츠",
            "쿨 오버핏 레이어드 티셔츠", "베이직 무지 반팔티 팩", "피케 카라 반팔 셔츠", "기능성 쿨링 드라이 티셔츠", "스탠다드 피트 카라티",
            "스트레치 베이직 셔츠", "데일리 레이어드 나시 티셔츠", "쿨 베이직 옥스포드 셔츠", "에센셜 브이넥 반팔", "헤비웨이트 라운드 티셔츠",
            "와이드 오픈카라 셔츠", "베이직 가디건 레이어드 셔츠", "쿨탠다드 리브드 티셔츠", "워크웨어 가먼트다잉 셔츠", "릴렉스 다잉 반팔티",
            "스탠다드 워시드 코튼 셔츠", "에센셜 투팩 반팔 레이어드", "컴포트 핏 옥스포드 반팔", "데일리 미니멀 반팔 셔츠", "린넨 베이직 반팔 셔츠",
            "루즈핏 코튼 그래픽 티셔츠", "편안한 린넨 블렌드 셔츠", "캐주얼 카라 반팔 셔츠", "쿨테크 오버핏 반팔티", "데일리 스트라이프 셔츠",
            "베이직 옥스포드 반팔 셔츠", "그래픽 프린팅 나염 티셔츠", "소프트 터치 크루넥 반팔", "루즈핏 카라 피케티", "이지케어 오픈카라 셔츠",
            "쿨링 에센셜 레이어드 티", "캐주얼 워시드 데님 셔츠", "오버핏 무지 카라 셔츠", "컴포트핏 베이직 티셔츠", "린넨 라이크 루즈핏 가디건 셔츠",
            "데일리 스웨트 반팔 셔츠", "어반 베이직 포켓 티셔츠", "소프트 코튼 반팔 셔츠", "스트릿 루즈핏 나염 반팔", "이지 드라이 쿨 반팔티",
            "컴포트 베이직 스트라이프 셔츠", "루즈핏 미니멀 포켓 티셔츠", "이지 쿨링 라운드 넥", "어반 캐주얼 오픈카라", "스파오 에센셜 코튼 셔츠",
            "TSHIRT FLOWER MARDI CLASSIC", "TSHIRT LES BLOSSOM SIGNATURE", "SWEATSHIRT ECLORE ESSENTIAL", "MARDI LOGO EMBLEM SHIRT", "TSHIRT UNIVERSE FLOWER",
            "프렌치 로고 자수 반팔 티셔츠", "시그니처 플라워 프린팅 티셔츠", "블라썸 아카이브 오버핏 반팔", "CLASSIC MARDI EMBROIDERY SHIRT", "프렌치 가든 그래픽 티셔츠",
            "TSHIRT FLOWER MARDI BLOSSOM", "LEES SIGNATURE LOGO TEE", "프렌치 무드 셔링 카라 블라우스", "MARDI ARCHIVE PREMIUM SHIRT", "엠블럼 자수 크롭 반팔티",
            "TSHIRT FLOWER MARDI VINTAGE", "프렌치 리본 그래픽 티셔츠", "CLASSIC LOGO OVERSIZED SHIRT", "시그니처 플라워 레터링 반팔티", "MARDI PIQUE 블라썸 셔츠",
            "미니멀 아키텍처 오버핏 셔츠", "드레이프 실루엣 반팔 티셔츠", "익스클루시브 디테일 크루넥", "모던 미니멀리즘 반팔 셔츠", "아카이브 스트럭처 반팔티",
            "구조적 실루엣 레이어드 셔츠", "테일러드 디테일 카라 셔츠", "미니멀리즘 링클 프리 셔츠", "오버사이즈 실루엣 가먼트 셔츠", "익스클루시브 원단 워시드 셔츠",
            "모던 아카이브 포켓 반팔티", "비대칭 디테일 미니멀 셔츠", "드레이프 코튼 레이어드 티셔츠", "아키텍처 레이아웃 그래픽 티", "인사일런스 익스클루시브 셔츠",
            "타임리스 프렌치 클래식 셔츠", "소프트 클래식 무드 반팔티", "로맨틱 시어 레이어드 블라우스", "프렌치 시그니처 로고 티셔츠", "타임리스 미니멀 원피스 셔츠",
            "소프트 코튼 링클 셔츠", "내추럴 클래식 옥스포드 셔츠", "프렌치 가든 소프트 가디건 셔츠", "타임리스 아카이브 리넨 셔츠", "앤티크 로맨틱 자수 셔츠",
            "프렌치 클래식 스트라이프 반팔", "소프트 실루엣 카라 셔츠", "타임리스 베이직 포켓 셔츠", "내추럴 무드 레이어드 티셔츠", "헌치 클래식 에센셜 셔츠"
        ],
        "category": ["상의"] * 100,
        "price": [
            19900, 15900, 19900, 29900, 35900, 19900, 25900, 29900, 17900, 27900, 29900, 12900, 29900, 15900, 21900, 31900, 29900, 17900, 39900, 19900, 32900, 23900, 29900, 29900, 35900,
            25900, 39900, 29900, 19900, 35900, 29900, 25900, 19900, 29900, 32900, 21900, 39900, 29900, 23900, 39900, 35900, 19900, 23900, 25900, 19900, 32900, 29900, 19900, 29900, 29900,
            42000, 42000, 68000, 75000, 45000, 42000, 42000, 45000, 75000, 42000, 42000, 39000, 68000, 89000, 48000, 42000, 42000, 78000, 42000, 52000,
            79000, 59000, 55000, 74000, 59000, 84000, 79000, 74000, 89000, 84000, 55000, 79000, 59000, 64000, 89000,
            68000, 48000, 78000, 45000, 82000, 72000, 68000, 75000, 88000, 72000, 65000, 58000, 58000, 52000, 68000
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# 뻔한 카테고리 단어 필터링 세팅
STOPWORDS = {
    "셔츠", "티셔츠", "반팔티", "반팔", "블라우스", "카라티", "나시", "원피스", "팩", "투팩", "원단",
    "SHIRT", "TSHIRT", "TEE", "SWEATSHIRT", "MARDI", "LEES", "인사일런스", "스파오", "넥", "라운드", "크루넥"
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

df['lang_type'] = df['product_name'].apply(get_language_type)

# 4. 헤더 레이아웃 (개인 포트폴리오 웹사이트 디자인 복제)
st.markdown('<div class="web-sub">Portfolio Project — 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="web-title">Jiyoon Lee × The Language of Fashion</div>', unsafe_allow_html=True)
st.markdown('<div class="web-caption">Fashion Design · SKKU · Brand Marketing Focus</div>', unsafe_allow_html=True)
st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

# 5. 내비게이션 / 사이드바 멀티 필터링
st.sidebar.markdown("<h3 style='font-family:\"Playfair Display\", serif;'>01 — Filter</h3>", unsafe_allow_html=True)
selected_types = st.sidebar.multiselect("COLLECTION TYPE", options=["SPA", "Designer"], default=["SPA", "Designer"])

available_brands = df[df['brand_type'].isin(selected_types)]['brand'].unique()
selected_brands = st.sidebar.multiselect("BRANDS SELECTION", options=list(available_brands), default=list(available_brands))

filtered_df = df[(df['brand_type'].isin(selected_types)) & (df['brand'].isin(selected_brands))]

# 6. 미니멀 스코어 카드 레이아웃
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.markdown('<div class="metric-wrapper"><div class="metric-label">Total Selected Items</div><div class="metric-value">' + f"{len(filtered_df)}" + '</div></div>', unsafe_allow_html=True)
with m_col2:
    st.markdown('<div class="metric-wrapper"><div class="metric-label">Average Base Price</div><div class="metric-value">₩' + f"{int(filtered_df['price'].mean()):,}" + '</div></div>', unsafe_allow_html=True)
with m_col3:
    st.markdown('<div class="metric-wrapper"><div class="metric-label">Active Brands Count</div><div class="metric-value">' + f"{filtered_df['brand'].nunique()}" + '</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-sub-line"></div>', unsafe_allow_html=True)

# 7. 메인 시각화 (차트 색상을 완벽한 무채색 모노톤으로 제어)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown('<div class="section-title">02 — Concept Adjectives</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">카테고리 명칭을 정제하고 추출한 고유 스타일 수식어 리스트</div>', unsafe_allow_html=True)
    
    all_words = extract_fashion_keywords(filtered_df['product_name'])
    if all_words:
        word_counts = Counter(all_words).most_common(10)
        word_df = pd.DataFrame(word_counts, columns=['Keyword', 'Count'])
        
        # 시크한 딥 차콜-블랙 단색 바 차트
        fig_bar = px.bar(word_df, x='Count', y='Keyword', orientation='h',
                         color_discrete_sequence=['#111111'])
        fig_bar.update_layout(
            yaxis={'categoryorder':'total ascending'}, 
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0, r=20, t=0, b=0),
            xaxis_title=None, yaxis_title=None
        )
        fig_bar.update_xaxes(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111')
        fig_bar.update_yaxes(linecolor='#111111')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.write("선택된 조건에 해당하는 키워드가 없습니다.")

with chart_col2:
    st.markdown('<div class="section-title">03 — Linguistic Typology</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">상품 네이밍에 투영된 언어 혼용 구조 및 영문 텍스트 비율</div>', unsafe_allow_html=True)
    
    if not filtered_df.empty:
        lang_counts = filtered_df['lang_type'].value_counts().reset_index()
        lang_counts.columns = ['Language Type', 'Count']
        
        # 완벽한 톤온톤 블랙-그레이-라이트그레이 파이 조각 매핑
        fig_pie = px.pie(lang_counts, values='Count', names='Language Type',
                         color_discrete_sequence=['#111111', '#666666', '#CCCCCC'])
        fig_pie.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', 
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.write("데이터가 없습니다.")

st.markdown('<div class="section-sub-line"></div>', unsafe_allow_html=True)

# 8. 브랜드 포지셔닝 스캐터 차트
st.markdown('<div class="section-title">04 — Brand Market Positioning</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">브랜드별 가격대 스펙트럼과 상품명의 언어적 포지셔닝 매트릭스</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    fig_scatter = px.scatter(filtered_df, x='brand', y='price', color='brand_type',
                             hover_data=['product_name'], size=[9]*len(filtered_df),
                             color_discrete_map={'SPA': '#666666', 'Designer': '#111111'})
    fig_scatter.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis_title=None, yaxis_title=None
    )
    fig_scatter.update_xaxes(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111')
    fig_scatter.update_yaxes(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111')
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown('<div class="section-sub-line"></div>', unsafe_allow_html=True)

# 9. 데이터 아카이브 및 실시간 쿼리 검색창
st.markdown('<div class="section-title">05 — Archive & Data Collection</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">전체 브랜드 수집 말뭉치 로우 데이터 및 필터 검색 아카이브</div>', unsafe_allow_html=True)

search_query = st.text_input("🔍 Search Concept Word (e.g. 베이직, 에센셜, CLASSIC, 실루엣)")

if search_query:
    display_df = filtered_df[filtered_df['product_name'].str.contains(search_query, case=False)]
else:
    display_df = filtered_df

st.dataframe(display_df[['brand', 'brand_type', 'product_name', 'price', 'lang_type']], use_container_width=True)

# 10. 미니멀 푸터 디자인
st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 11px; color: #888888; font-family:\'Playfair Display\', serif;">© 2026 Jiyoon Lee · Fashion Design, SKKU · All rights reserved.</p>', unsafe_allow_html=True)
