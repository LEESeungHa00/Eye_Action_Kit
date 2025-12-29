import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime

# 페이지 설정
st.set_page_config(
    page_title="Quick Start Tridge Eye",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 스타일링 (CSS) - 대시보드 스타일 강화
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #004e66;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #003344;
        color: white;
    }
    /* 결과 카드 스타일 */
    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 5px solid #004e66;
    }
    .verdict-header {
        font-size: 1.8em;
        font-weight: 800;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }
    .verdict-sub {
        font-size: 1.1em;
        color: #555;
        margin-bottom: 20px;
        line-height: 1.5;
    }
    .metric-label {
        font-size: 0.9em;
        color: #777;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.4em;
        font-weight: bold;
        color: #333;
    }
    /* 테이블 스타일 */
    .dataframe {
        font-size: 14px !important;
    }
    h1, h2, h3, h4 {
        color: #004e66;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# 사이드바 네비게이션
st.sidebar.title("🚀 Quick Start Tridge Eye")
st.sidebar.markdown("---")
page = st.sidebar.radio("도구 선택", ["Tool 1. 협상 & 타이밍 마스터", "Tool 2. 파트너 검증기", "📘 사용 가이드"])

# --- Tool 1: 협상 & 타이밍 마스터 ---
if page == "Tool 1. 협상 & 타이밍 마스터":
    st.title("🤝 Negotiation & Timing Master")
    st.markdown("##### 시장의 흐름(Trend)과 맥락(Context)을 읽어 협상의 주도권을 잡으세요.")
    
    # 2단 레이아웃: 입력(왼쪽) / 결과(오른쪽)
    input_col, output_col = st.columns([1, 1.4], gap="large")

    with input_col:
        st.info("### 1️⃣ 데이터 입력 (Input)")
        
        with st.expander("📝 Section 1. 미래 예측 (Eye Echo)", expanded=True):
            target_date = st.text_input("구매 예정 시점", "2025.12.W2")
            forecast_trend = st.selectbox("예측 방향성", ["↗️ 상승 (Rise)", "➡️ 보합 (Stable)", "↘️ 하락 (Fall)"])
            forecast_price = st.number_input("해당 시점 예상 단가 ($/kg)", min_value=0.0, format="%.2f")

        with st.expander("📝 Section 2. 현재 시장 추세 (Eye Shelf)", expanded=True):
            st.markdown("**산지 도매가 / 농가 출하가 추이**")
            market_trend = st.radio("최근 가격 추세", ["▲ 급등 (Surge)", "↗️ 상승 (Rise)", "➖ 보합 (Stable)", "▼ 하락 (Drop)"], horizontal=True)
            market_avg_price = st.number_input("현재 시장 평균가 (Wholesale/Export Avg) ($/kg)", min_value=0.0, value=0.50, format="%.2f")

        with st.expander("📝 Section 3. 공급사 제안 (Supplier)", expanded=True):
            offer_price = st.number_input("공급사 제안가 ($/kg)", min_value=0.0, value=0.58, format="%.2f")
            supplier_avg_margin = st.slider("공급사 인정 프리미엄 (%)", 0, 20, 5, help="시장가 대비 인정할 수 있는 품질/브랜드 가치")
            
        with st.expander("📝 Section 4. 뉴스 리스크 (Context)", expanded=True):
            risk_factors = st.multiselect("🚨 가격 인상/리스크 요인 (악재)", 
                                          ["작황 부진/기상 악화", "질병/해충", "물류 대란/항만 적체", "관세/규제", "원부자재 상승"])
            opp_factors = st.multiselect("✅ 가격 인하 요인 (호재)", 
                                         ["풍작 (Bumper Crop)", "수요 감소/재고 과잉", "환율 호재", "신규 공급처 진입"])

        analyze_btn = st.button("🚀 분석 실행 (Analyze)")

    with output_col:
        if analyze_btn:
            st.success("### 2️⃣ 분석 결과 (Verdict)")
            
            # --- 로직 엔진 (Logic Engine) ---
            # 1. 가격 계산
            fair_price = market_avg_price * (1 + supplier_avg_margin/100) # 적정가
            gap = offer_price - fair_price # 설명 안되는 마진
            gap_pct = (gap / fair_price) * 100 if fair_price > 0 else 0
            
            # 2. 케이스 분류 및 변수 설정
            case_id = ""
            verdict_icon = ""
            verdict_title = ""
            verdict_desc = ""
            verdict_color = ""
            timing = "검토 필요"
            leverage = "50 : 50"
            strategy_point = ""
            
            # 리스크 플래그
            has_supply_risk = any(r in ["작황 부진/기상 악화", "질병/해충", "관세/규제"] for r in risk_factors)
            has_logistics_risk = "물류 대란/항만 적체" in risk_factors
            has_bumper = "풍작 (Bumper Crop)" in opp_factors
            
            if has_supply_risk or "▲ 급등" in market_trend:
                # Case 3: 구조적 급등
                verdict_icon = "🔵"
                verdict_title = "물량 선확보 (Secure Volume)"
                verdict_desc = "가격 협상보다 물량 확보가 시급합니다. 지금 안 사면 나중에 못 살 수 있습니다."
                verdict_color = "#e3f2fd" # Light Blue
                target_price = offer_price
                timing = "즉시 (Now)"
                leverage = "20 : 80 (공급자 우위)"
                strategy_point = "단가 수용하되, 향후 3개월치 물량 Lock-in 제안 (재고 확보 우선)"
                
            elif has_logistics_risk:
                # Case 2: 리스크형 인상
                verdict_icon = "🟡"
                verdict_title = "조건부 협상 (Conditional)"
                verdict_desc = "가격 거품이 있으나 납기 리스크가 더 큽니다. 단가를 조금 양보하고 '선적 보장'을 받으세요."
                verdict_color = "#fff9db" # Light Yellow
                target_price = fair_price * 1.03
                timing = "계약 조건 확인 후"
                leverage = "40 : 60 (약간 불리)"
                strategy_point = "가격 인하 대신 '선적 우선순위(Priority Shipping)' 및 '지체상금' 조항 삽입"

            elif "▼ 하락" in market_trend and gap_pct > 10:
                # Case 1: 탐욕형 인상
                verdict_icon = "🔴"
                verdict_title = "강력 인하 요구 (Strong Push)"
                verdict_desc = "명분 없는 인상입니다. 시장 트렌드와 미래 전망 모두 귀하의 편입니다."
                verdict_color = "#ffe3e3" # Light Red
                target_price = market_avg_price
                timing = "협상 완료 시까지 보류"
                leverage = "90 : 10 (구매자 절대 우위)"
                strategy_point = "원가 하락 데이터 제시하며 프리미엄 제거 요구. 미수용 시 공급처 변경 압박."
                
            elif "▼ 하락" in market_trend and "↗️ 상승" in forecast_trend:
                # Case 4: 저점 매수
                verdict_icon = "🟢"
                verdict_title = "골든 타임 (Strike Price)"
                verdict_desc = "지금이 최저가일 확률이 높습니다. 스팟을 멈추고 장기 계약으로 전환하세요."
                verdict_color = "#d3f9d8" # Light Green
                target_price = offer_price
                timing = "즉시 (Best Timing)"
                leverage = "60 : 40 (구매자 우위)"
                strategy_point = "물량을 3배 늘리는 조건으로 대량 구매 할인(Volume Discount) 및 연간 계약 제안"

            elif "↘️ 하락" in forecast_trend or has_bumper:
                # Case 5: 하락장 진입
                verdict_icon = "⚪"
                verdict_title = "구매 보류 (Wait & See)"
                verdict_desc = "떨어지는 칼날입니다. 급한 물량이 아니라면 구매를 최대한 미루세요."
                verdict_color = "#f1f3f5" # Gray
                target_price = market_avg_price * 0.9
                timing = "2주 후 (대기)"
                leverage = "80 : 20 (구매자 우위)"
                strategy_point = "재고 소진하며 관망. 필요 시 스팟성으로만 최소량 구매."
                
            else:
                # Default
                verdict_icon = "⚖️"
                verdict_title = "일반 협상 (Negotiate)"
                verdict_desc = "통상적인 수준의 줄다리기가 필요합니다. 적정 마진 범위를 논의하세요."
                verdict_color = "#e6f7ff" # Teal Light
                target_price = fair_price
                timing = "협상 중"
                leverage = "50 : 50 (대등)"
                strategy_point = "시장 평균가와 당사 인정 프리미엄을 근거로 합리적 가격 조정 요청"

            # --- 1. 종합 진단 (The Verdict) ---
            st.markdown(f"""
            <div class="result-card" style="background-color: {verdict_color};">
                <div class="verdict-header" style="color: #333;">{verdict_icon} {verdict_title}</div>
                <div class="verdict-sub">{verdict_desc}</div>
                <div style="display: flex; justify-content: space-between; margin-top: 15px; border-top: 1px solid rgba(0,0,0,0.1); padding-top: 15px;">
                    <div style="text-align: center;">
                        <div class="metric-label">🎯 적정 목표가</div>
                        <div class="metric-value">${target_price:.2f}</div>
                    </div>
                    <div style="text-align: center;">
                        <div class="metric-label">⏱️ 구매 타이밍</div>
                        <div class="metric-value" style="font-size: 1.2em; margin-top:5px;">{timing}</div>
                    </div>
                    <div style="text-align: center;">
                        <div class="metric-label">⚖️ 협상 우위</div>
                        <div class="metric-value" style="font-size: 1.2em; margin-top:5px;">{leverage}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- 2. 3D 트렌드 매트릭스 (Trend Matrix) ---
            st.markdown("#### 📊 3D 트렌드 매트릭스 (Trend Matrix)")
            st.info("시장의 '결'을 읽어 협상 논리를 구성하세요.")
            
            # 데이터 구성
            trend_data = {
                "구분": ["과거 (Trend)", "미래 (Forecast)", "심리 (Context)"],
                "방향성": [
                    market_trend.split(' ')[0], 
                    forecast_trend.split(' ')[0], 
                    "⚠️" if risk_factors else "✅" if opp_factors else "➖"
                ],
                "핵심 해석 (Key Insight)": [
                    f"산지 가격이 {market_trend.split(' ')[1]} 추세입니다.",
                    f"향후 시장은 {forecast_trend.split(' ')[1]}될 전망입니다.",
                    f"{', '.join(risk_factors) if risk_factors else ', '.join(opp_factors) if opp_factors else '특이사항 없음'} 이슈가 있습니다."
                ]
            }
            st.table(pd.DataFrame(trend_data))

            # --- 3. 가격 구조 정밀 분석 (The Logic - Manual Waterfall) ---
            st.markdown("#### 💰 가격 포지셔닝 (Price Positioning)")
            
            # Plotly의 go.Waterfall에서 개별 색상 제어가 어려우므로, 
            # go.Bar를 사용하여 Waterfall 형태를 직접 구현합니다.
            
            fig = go.Figure()
            
            # 1. Market Base (시장 평균가) - 회색/Standard
            fig.add_trace(go.Bar(
                name="시장 평균가",
                x=["시장 평균가 (Standard)"], 
                y=[market_avg_price],
                marker_color="#adb5bd", # Gray
                text=f"${market_avg_price:.2f}", 
                textposition='auto'
            ))
            
            # 2. Premium (인정 프리미엄) - 초록색/Yellowish Green (Base 위로 쌓임)
            fig.add_trace(go.Bar(
                name="인정 프리미엄",
                x=["인정 프리미엄 (Premium)"], 
                y=[fair_price - market_avg_price],
                base=[market_avg_price], # 시작점
                marker_color="#28a745", # Green (Positive/Allowed)
                text=f"+${fair_price - market_avg_price:.2f}", 
                textposition='auto'
            ))
            
            # 3. Bubble (설명 안되는 마진) - 빨간색 (Fair Price 위로 쌓임)
            if gap > 0:
                fig.add_trace(go.Bar(
                    name="설명 안되는 마진",
                    x=["설명 안되는 마진 (Bubble)"], 
                    y=[gap],
                    base=[fair_price], # 시작점
                    marker_color="#dc3545", # Red (Negative/Warning)
                    text=f"+${gap:.2f}", 
                    textposition='auto'
                ))
            
            # 4. Offer (최종 제안가) - 파란색/Total
            fig.add_trace(go.Bar(
                name="최종 제안가",
                x=["최종 제안가 (Offer)"], 
                y=[offer_price],
                marker_color="#004e66", # Blue (Total)
                text=f"${offer_price:.2f}", 
                textposition='auto'
            ))
            
            fig.update_layout(
                title = "가격 구조 분해 (Logic of Price)",
                showlegend = False,
                height=350,
                margin=dict(l=20, r=20, t=40, b=20),
                yaxis=dict(title="단가 ($/kg)")
            )
            st.plotly_chart(fig, use_container_width=True)
            
            if gap > 0:
                st.caption(f"💡 **분석:** 제안가에는 귀사가 인정한 프리미엄 외에도 **${gap:.2f}/kg ({gap_pct:.1f}%)**의 설명되지 않는 추가 마진(Bubble)이 포함되어 있습니다. 이를 제거하는 것이 협상 목표입니다.")

            # --- 4. 전략 가이드 (Strategy Action) ---
            st.markdown("---")
            st.markdown("#### 📝 전략 가이드 (Strategy Action)")
            
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                st.markdown(f"""
                **🔥 핵심 협상 포인트**
                * {strategy_point}
                """)
            with col_act2:
                st.markdown(f"""
                **🔮 왓 이프 (What-If: 대안)**
                * **Wait:** 2주 대기 시 예상가 **${forecast_price:.2f}**
                * **BATNA:** 대체 국가 소싱 시세 확인 필요
                """)

        else:
            st.info("👈 왼쪽 패널에 데이터를 입력하고 '분석 실행'을 눌러주세요.")

# --- Tool 2: 파트너 검증기 ---
elif page == "Tool 2. 파트너 검증기":
    st.title("🕵️ Partner Validator")
    st.markdown("##### 공급사의 실력, 평판, 리스크를 3차원으로 검증합니다.")

    # 2단 레이아웃 적용
    col1, col2 = st.columns([1, 1.4], gap="large")

    with col1:
        st.info("### 1️⃣ 공급사 진단 (Audit)")
        
        with st.expander("📝 Section 1. 기본 정보 (Identity)", expanded=True):
            supplier_name = st.text_input("공급사명", "ABC Export Co.")
            target_spec = st.text_input("핵심 타겟 스펙", "Organic Cavendish Banana")
            
        with st.expander("📝 Section 2. 실력 검증 (Performance)", expanded=True):
            volume_trend = st.selectbox("최근 1년 수출 물량 추세", ["↗️ 성장세 (Growth)", "➡️ 유지 (Stable)", "↘️ 하락세 (Decline)"])
            destinations = st.multiselect("주요 수출 대상국", ["High-Standard (미국/유럽/일본)", "Middle (중국/동남아)", "Low (기타)"])
            
        with st.expander("📝 Section 3. 평판 & 적합성 (Reference)", expanded=True):
            buyer_tier = st.radio("주요 거래처(Buyer) 레벨", ["Global Tier 1 (대기업)", "Regional Tier 2 (중견/도매)", "Unknown (소규모)"])
            export_history = st.radio("내 국가(Target) 수출 이력", ["✅ 최근 1년 내 있음", "⚠️ 과거 이력만 있음", "❌ 없음 (첫 거래)"])
            
        with st.expander("📝 Section 4. 리스크 (Dependency)", expanded=True):
            dependency = st.radio("특정 바이어/국가 의존도", ["🟢 낮음 (분산됨)", "🔴 높음 (50% 이상 집중)"])

        validate_btn = st.button("🔎 검증 실행 (Validate)")

    with col2:
        if validate_btn:
            st.success("### 2️⃣ 검증 결과 (Report)")
            
            # --- 로직 엔진 ---
            score = 0
            grade = "F"
            
            # Scoring Logic
            if volume_trend == "↗️ 성장세 (Growth)": score += 30
            elif volume_trend == "➡️ 유지 (Stable)": score += 20
            
            if "High-Standard (미국/유럽/일본)" in destinations: score += 20
            
            if buyer_tier == "Global Tier 1 (대기업)": score += 30
            elif buyer_tier == "Regional Tier 2 (중견/도매)": score += 15
            
            if export_history == "✅ 최근 1년 내 있음": score += 20
            elif export_history == "⚠️ 과거 이력만 있음": score += 10
            
            if dependency == "🟢 낮음 (분산됨)": score += 0
            else: score -= 20
            
            # Grade Logic
            if score >= 90:
                grade = "S"
                grade_title = "Grade S (전략적 파트너)"
                grade_color = "#d3f9d8" # Green
                text_color = "#0b7285"
                strategy_title = "Lock-in & Grow"
                strategy_desc = "성장성, 품질, 안정성 모두 완벽합니다. 단가보다 '물량 확보'와 '장기 계약'을 우선하세요."
            elif score >= 70:
                if dependency == "🔴 높음 (50% 이상 집중)":
                    grade = "A-"
                    grade_title = "Grade A- (조건부 파트너)"
                    grade_color = "#fff9db" # Yellow
                    text_color = "#e67700"
                    strategy_title = "Penalty & Assurance"
                    strategy_desc = "실력은 좋으나 바쁜 업체입니다. 우리 물량이 밀릴 수 있으니 '납기 보장 조항'을 반드시 넣으세요."
                else:
                    grade = "A"
                    grade_title = "Grade A (우수 파트너)"
                    grade_color = "#e3f2fd" # Blue
                    text_color = "#1864ab"
                    strategy_title = "Competition"
                    strategy_desc = "신뢰할 수 있는 표준 업체입니다. 경쟁 입찰을 통해 단가 경쟁을 유도하세요."
            elif score >= 50:
                grade = "B"
                grade_title = "Grade B (검역 주의)"
                grade_color = "#ffe8cc" # Orange
                text_color = "#d9480f"
                strategy_title = "Quality First, Safety Check"
                strategy_desc = "한국 통관 경험이 부족할 수 있습니다. 샘플 테스트 및 검역 서류 확인이 필수입니다."
            else:
                grade = "C/F"
                grade_title = "Grade C/F (위험군)"
                grade_color = "#ffe3e3" # Red
                text_color = "#c92a2a"
                strategy_title = "Do Not Trade"
                strategy_desc = "부실 위험이 높습니다. 소싱 대상에서 제외하거나 블랙리스트에 등록하세요."

            # --- 결과 화면 ---
            st.markdown(f"""
            <div class="result-card" style="background-color: {grade_color}; border-left: 5px solid {text_color};">
                <div class="verdict-header" style="color: {text_color};">{grade_title}</div>
                <div class="verdict-sub" style="margin-bottom: 0;">종합 점수: <strong>{score} / 100</strong></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### ✅ 입체 분석 (Audit Details)")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.info(f"**📈 성장성**\n\n{volume_trend}")
            with c2:
                st.info(f"**🏆 평판**\n\n{buyer_tier}")
            with c3:
                risk_bg = "error" if "높음" in dependency else "success"
                if risk_bg == "error":
                    st.error(f"**⚠️ 리스크**\n\n의존도 {dependency}")
                else:
                    st.success(f"**🛡️ 리스크**\n\n의존도 {dependency}")

            st.markdown("---")
            st.markdown(f"#### 🎯 전략: {strategy_title}")
            st.write(strategy_desc)

        else:
             st.info("👈 왼쪽 패널에 데이터를 입력하고 '검증 실행'을 눌러주세요.")

# --- 가이드북 ---
elif page == "📘 사용 가이드":
    st.title("📘 Tridge Eye 솔루션 가이드북")
    st.markdown("이 앱에 넣을 데이터를 **Tridge Eye** 웹사이트에서 찾는 방법입니다.")
    
    tab1, tab2 = st.tabs(["Chapter 1. 가격 데이터 찾기", "Chapter 2. 공급사 데이터 찾기"])
    
    with tab1:
        st.header("Step 1. '기준점' 잡기 (Eye Shelf)")
        st.markdown("""
        1. **Eye Shelf > Market** 메뉴 클릭
        2. 품목(Product) 및 국가(Country) 선택
        3. **Export price by exporting country** 탭 클릭
        4. 👉 가장 최신 주차의 평균 가격을 앱의 **'시장 평균가'** 란에 입력하세요.
        """)
        st.divider()
        st.header("Step 2. '방향성' 읽기 (Eye Shelf & Echo)")
        st.markdown("""
        1. **Farmgate price by country** 차트 확인
           - 최근 1달 그래프가 내려가면 ▼ 하락, 올라가면 ▲ 상승
        2. **Eye Echo** 메뉴 클릭
           - 예측 그래프 끝이 위면 ↗️ 상승, 아래면 ↘️ 하락
        """)
    
    with tab2:
        st.header("Step 1. 공급사 기본 체력 (Performance)")
        st.markdown("""
        1. **Eye Shelf > Company** 메뉴 클릭
        2. 회사명 검색
        3. **Export Volume** 그래프 확인: 우상향이면 '성장세'
        4. **Share by destination** 파이 차트 확인: 특정 국가가 50% 넘으면 '의존도 높음'
        """)
        st.divider()
        st.header("Step 2. 거래처 수준 확인 (Reference)")
        st.markdown("""
        1. **Transaction data explorer** 메뉴 클릭
        2. Exporter에 공급사명 입력
        3. **Importer (수입사)** 목록 스캔
           - Walmart, Costco 등 아는 이름이 있으면 **Tier 1**
        """)

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Tridge Action Kit v1.1")
st.sidebar.caption("Based on 'Negotiation & Timing Master' Plan")
