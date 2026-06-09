import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# 1. 패션 브랜드 가상 데이터셋 (SPA 50개 vs 디자이너 50개)
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
            # --- 무신사 스탠다드 (25개) ---
            "쿨탠다드 베이직 티셔츠", "에센셜 라운드 넥 반팔티", "릴렉스핏 크루넥 티셔츠", "데일리 코튼 반팔 셔츠", "린넨 블렌드 릴렉스 셔츠",
            "쿨 오버핏 레이어드 티셔츠", "베이직 무지 반팔티 팩", "피케 카라 반팔 셔츠", "기능성 쿨링 드라이 티셔츠", "스탠다드 피트 카라티",
            "스트레치 베이직 셔츠", "데일리 레이어드 나시 티셔츠", "쿨 베이직 옥스포드 셔츠", "에센셜 브이넥 반팔", "헤비웨이트 라운드 티셔츠",
            "와이드 오픈카라 셔츠", "베이직 가디건 레이어드 셔츠", "쿨탠다드 리브드 티셔츠", "워크웨어 가먼트다잉 셔츠", "릴렉스 다잉 반팔티",
            "스탠다드 워시드 코튼 셔츠", "에센셜 투팩 반팔 레이어드", "컴포트 핏 옥스포드 반팔", "데일리 미니멀 반팔 셔츠", "린넨 베이직 반팔 셔츠",
            # --- 스파오 (25개) ---
            "루즈핏 코튼 그래픽 티셔츠", "편안한 린넨 블렌드 셔츠", "캐주얼 카라 반팔 셔츠", "쿨테크 오버핏 반팔티", "데일리 스트라이프 셔츠",
            "베이직 옥스포드 반팔 셔츠", "그래픽 프린팅 나염 티셔츠", "소프트 터치 크루넥 반팔", "루즈핏 카라 피케티", "이지케어 오픈카라 셔츠",
            "쿨링 에센셜 레이어드 티", "캐주얼 워시드 데님 셔츠", "오버핏 무지 카라 셔츠", "컴포트핏 베이직 티셔츠", "린넨 라이크 루즈핏 가디건 셔츠",
            "데일리 스웨트 반팔 셔츠", "어반 베이직 포켓 티셔츠", "소프트 코튼 반팔 셔츠", "스트릿 루즈핏 나염 반팔", "이지 드라이 쿨 반팔티",
            "컴포트 베이직 스트라이프 셔츠", "루즈핏 미니멀 포켓 티셔츠", "이지 쿨링 라운드 넥", "어반 캐주얼 오픈카라", "스파오 에센셜 코튼 셔츠",
            # --- 마르디 메크르디 (20개) ---
            "TSHIRT FLOWER MARDI CLASSIC", "TSHIRT LES BLOSSOM SIGNATURE", "SWEATSHIRT ECLORE ESSENTIAL", "MARDI LOGO EMBLEM SHIRT", "TSHIRT UNIVERSE FLOWER",
            "프렌치 로고 자수 반팔 티셔츠", "시그니처 플라워 프린팅 티셔츠", "블라썸 아카이브 오버핏 반팔", "CLASSIC MARDI EMBROIDERY SHIRT", "프렌치 가든 그래픽 티셔츠",
            "TSHIRT FLOWER MARDI BLOSSOM", "LEES SIGNATURE LOGO TEE", "프렌치 무드 셔링 카라 블라우스", "MARDI ARCHIVE PREMIUM SHIRT", "엠블럼 자수 크롭 반팔티",
            "TSHIRT FLOWER MARDI VINTAGE", "프렌치 리본 그래픽 티셔츠", "CLASSIC LOGO OVERSIZED SHIRT", "시그니처 플라워 레터링 반팔티", "MARDI PIQUE 블라썸 셔츠",
            # --- 인사일런스 (15개) ---
            "미니멀 아키텍처 오버핏 셔츠", "드레이프 실루엣 반팔 티셔츠", "익스클루시브 디테일 크루넥", "모던 미니멀리즘 반팔 셔츠", "아카이브 스트럭처 반팔티",
            "구조적 실루엣 레이어드 셔츠", "테일러드 디테일 카라 셔츠", "미니멀리즘 링클 프리 셔츠", "오버사이즈 실루엣 가먼트 셔츠", "익스클루시브 원단 워시드 셔츠",
            "모던 아카이브 포켓 반팔티", "비대칭 디테일 미니멀 셔츠", "드레이프 코튼 레이어드 티셔츠", "아키텍처 레이아웃 그래픽 티", "인사일런스 익스클루시브 셔츠",
            # --- 헌치 (15개) ---
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

# 단순 카테고리 명칭 및 뻔한 단어 제외용 불용어 사전
STOPWORDS = {
    "셔츠", "티셔츠", "반팔티", "반팔", "셔츠", "블라우스", "카라티", "나시", "원피스", "팩", "투팩", "원단",
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

st.set_page_config(layout="wide", page_title="The Language of Fashion")

st.title("THE LANGUAGE OF FASHION")
st.caption("Analyzing How Korean Fashion Brands Construct Trendiness Through Words")
st.markdown("---")

# 브랜드별 멀티 필터링 시스템
st.sidebar.header("FILTER COLLECTION")
selected_types = st.sidebar.multiselect("BRAND TYPE", options=["SPA", "Designer"], default=["SPA", "Designer"])

available_brands = df[df['brand_type'].isin(selected_types)]['brand'].unique()
selected_brands = st.sidebar.multiselect("SELECT BRANDS", options=list(available_brands), default=list(available_brands))

filtered_df = df[(df['brand_type'].isin(selected_types)) & (df['brand'].isin(selected_brands))]

# 상단 대시보드 스코어 보드
col1, col2, col3 = st.columns(3)
col1.metric("TOTAL ITEMS", f"{len(filtered_df)} items")
col2.metric("AVG PRICE", f"₩{int(filtered_df['price'].mean()):,}")
col3.metric("BRANDS COUNT", f"{filtered_df['brand'].nunique()} brands")
st.markdown("<br/>", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("CONCEPT KEYWORDS (TOP 10)")
    st.caption("카테고리명(셔츠 등)을 제외한 브랜드 고유의 스타일 서술어/형용사 빈도 분석")
    
    all_words = extract_fashion_keywords(filtered_df['product_name'])
    if all_words:
        word_counts = Counter(all_words).most_common(10)
        word_df = pd.DataFrame(word_counts, columns=['Keyword', 'Count'])
        
        # 모노톤 그라데이션 적용
        fig_bar = px.bar(word_df, x='Count', y='Keyword', orientation='h',
                         color='Count', color_continuous_scale=['#CCCCCC', '#555555', '#111111'])
        fig_bar.update_layout(
            yaxis={'categoryorder':'total ascending'}, 
            plot_bgcolor='white', paper_bgcolor='white',
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_bar.update_xaxes(showgrid=True, gridcolor='#F0F0F0', linecolor='#111111')
        fig_bar.update_yaxes(linecolor='#111111')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.write("선택된 조건에 해당하는 키워드가 없습니다.")

with chart_col2:
    st.subheader("LANGUAGE DISTRIBUTION")
    st.caption("상품 네이밍 시 사용된 언어 체계의 비율")
    
    if not filtered_df.empty:
        lang_counts = filtered_df['lang_type'].value_counts().reset_index()
        lang_counts.columns = ['Language Type', 'Count']
        
        # 차콜, 그레이, 연그레이 모노톤 파이 차트
        fig_pie = px.pie(lang_counts, values='Count', names='Language Type',
                         color_discrete_sequence=['#222222', '#777777', '#DDDDDD'])
        fig_pie.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.write("데이터가 없습니다.")

st.markdown("---")

st.subheader("BRAND PRICE POSITIONING")
if not filtered_df.empty:
    fig_scatter = px.scatter(filtered_df, x='brand', y='price', color='brand_type',
                             hover_data=['product_name'], size=[10]*len(filtered_df),
                             color_discrete_map={'SPA': '#888888', 'Designer': '#222222'})
    fig_scatter.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig_scatter.update_xaxes(showgrid=True, gridcolor='#F0F0F0', linecolor='#111111')
    fig_scatter.update_yaxes(showgrid=True, gridcolor='#F0F0F0', linecolor='#111111')
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

st.subheader("ARCHIVE COLLECTION DATA")
search_query = st.text_input("🔍 Search Concept Word (e.g. 베이직, 에센셜, CLASSIC, 실루엣)")

if search_query:
    display_df = filtered_df[filtered_df['product_name'].str.contains(search_query, case=False)]
else:
    display_df = filtered_df

st.dataframe(display_df[['brand', 'brand_type', 'product_name', 'price', 'lang_type']], use_container_width=True) 
