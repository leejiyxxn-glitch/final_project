# final_project
# 📌 The Language of Fashion Dashboard
> **Analyzing How Korean Fashion Brands Construct Trendiness Through Words**

본 프로젝트는 한국 패션 브랜드(SPA 및 디자이너 브랜드)들이 상품명과 상품 설명에서 사용하는 언어적 패턴과 키워드를 분석하고 시각화하는 인터랙티브 웹 대시보드입니다.

---

## 📖 Project Overview (프로젝트 개요)
패션은 의류 디자인을 통해 시각적으로 표현될 뿐만 아니라, 상품명에 사용되는 정교한 단어 선택을 통해 언어적으로도 소비자와 소통합니다. 본 대시보드는 상품 카테고리나 가격에만 집중하던 기존 방식에서 벗어나, 브랜드들이 어떤 언어적 전략을 통해 스타일, 아이덴티티, 그리고 구매 욕구를 자극하는지 탐색합니다.

## 🎯 Project Goals (프로젝트 목표)
* **키워드 빈도 분석:** 한국 패션 상품 명명법에서 가장 빈번하게 사용되는 핵심 키워드 추출
* **브랜드 다각도 비교:** 대중성을 지닌 SPA 브랜드와 독창성을 지닌 K-디자이너 브랜드 간의 언어 패턴 차이 분석
* **언어 형태 분포 파악:** 브랜드별 한글, 영어, 혹은 혼용(Mixed) 단어 사용 비중 시각화
* **인터랙티브 대시보드 구현:** Streamlit을 활용하여 사용자가 직접 키워드를 검색하고 데이터를 필터링할 수 있는 UI 디자인

## 📊 Data Source & Scope (데이터 소스 및 범위)
* **대상 플랫폼:** 무신사(Musinsa), 29CM에 입점한 대표 브랜드 데이터 기반
* **비교 군:**
  * **SPA 브랜드:** 무신사 스탠다드, 스파오 (실용성, 기능성, 베이직 중심 단어 사용)
  * **Designer 브랜드:** 마르디 메크르디, 인사일런스, 헌치 (감성, 시그니처, 무드 중심 단어 사용)
* **수집 항목:** 브랜드명, 브랜드 유형, 상품명, 가격, 언어 유형

## 🛠️ Tools & Technologies (사용 기술)
* **Language:** Python 3.x
* **Framework:** Streamlit (Web Dashboard)
* **Data Processing:** Pandas, Regular Expressions (re), Collections (Counter)
* **Visualization:** Plotly Express
