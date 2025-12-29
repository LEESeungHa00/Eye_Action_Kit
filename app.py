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

# 스타일링 (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #004e66;
        color: white;
    }
    .stButton>button:hover {
        background-color: #003344;
        color: white;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .verdict-box {
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .analysis-box {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #004e66;
        margin-top: 10px;
    }
    h1, h2, h3 {
        color: #004e66;
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
    st.markdown("##### 시장 데이터를 기반으로 적정 가격(Should-Cost)을 산출하고 협상 전략을 수립합니다.")
    
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.info("### 1️⃣ 데이터 입력 (Input)")
        
        with st.expander("📝 Section 1. 미래 예측 (Eye Echo)", expanded=True):
            target_date = st.text_input("구매 예정 시점 (예: 2025.12.W2)", "2025.12.W2")
            forecast_trend = st.selectbox("예측 방향성 (Trend)", ["↗️ 상승 (Rise)", "➡️ 보합 (Stable)", "↘️ 하락 (Fall)"])
            forecast_price = st.number_input("해당 시점 예상 단가 ($/kg)", min_value=0.0, format="%.2f")

        with st.expander("📝 Section 2. 현재 시장 추세 (Eye Shelf)", expanded=True):
            st.markdown("**산지 도매가 / 농가 출하가 추이**")
            market_trend = st.radio("최근 가격 추세", ["▲ 급등 (Surge)", "↗️ 상승 (Rise)", "➖ 보합 (Stable)", "▼ 하락 (Drop)"], horizontal=True)
            market_avg_price = st.number_input("현재 시장 평균가 (Wholesale/Export Avg) ($/kg)", min_value=0.0, value=0.50, format="%.2f")

        with st.expander("📝 Section 3. 공급사 제안 (Supplier)", expanded=True):
            offer_price = st.number_input("공급사 제안가 ($/kg)", min_value=0.0, value=0.58, format="%.2f")
            supplier_avg_margin = st.slider("공급사 인정 프리미엄 (%)", 0, 20, 5, help="브랜드 가치, 품질 차이 등으로 시장가보다 더 쳐줄 수 있는 비율")
            
        with st.expander("📝 Section 4. 뉴스 리스크 (Context)", expanded=True):
            risk_factors = st.multiselect("🚨 가격 인상/리스크 요인 (악재)", 
                                          ["작황 부진/기상 악화", "질병/해충", "물류 대란/항만 적체", "관세/규제", "원부자재 상승"])
            opp_factors = st.multiselect("✅ 가격 인하 요인 (호재)", 
                                         ["풍작 (Bumper Crop)", "수요 감소/재고 과잉", "환율 호재", "신규 공급처 진입"])

        analyze_btn = st.button("🚀 분석 실행 (Analyze)")

    with col2:
        if analyze_btn:
            st.success("### 2️⃣ 분석 결과 (Verdict)")
            
            # --- 로직 엔진 (Logic Engine) ---
            # 1. 가격 차이 분석
            fair_price = market_avg_price * (1 + supplier_avg_margin/100) # 적정가 (시장가 + 프리미엄)
            gap = offer_price - fair_price # 총 격차
            gap_pct = (gap / fair_price) * 100 if fair_price > 0 else 0
            
            # 2. 케이스 분류
            case = "Normal"
            verdict_color = "#gray"
            verdict_title = "판단 보류"
            verdict_desc = "데이터가 충분하지 않습니다."
            target_price = fair_price
            
            # 뉴스 리스크 유무
            has_supply_risk = any(r in ["작황 부진/기상 악화", "질병/해충", "관세/규제"] for r in risk_factors)
            has_logistics_risk = "물류 대란/항만 적체" in risk_factors
            has_bumper = "풍작 (Bumper Crop)" in opp_factors
            
            # Case Logic Implementation
            if has_supply_risk or "▲ 급등 (Surge)" in market_trend:
                case = "Supply Shortage"
                verdict_color = "#007bff" # Blue
                verdict_title = "🔵 물량 선확보 (Secure Volume)"
                verdict_desc = "가격 협상보다 물량 확보가 시급합니다. 지금 안 사면 나중에 못 살 수 있습니다."
                target_price = offer_price # 수용
                
            elif has_logistics_risk:
                case = "Logistics Risk"
                verdict_color = "#ffc107" # Yellow
                verdict_title = "🟡 조건부 협상 (Conditional)"
                verdict_desc = "가격 거품이 있으나 납기 리스크가 더 큽니다. 단가를 조금 양보하고 '선적 보장'을 받으세요."
                target_price = fair_price * 1.05 # 약간 양보

            elif "▼ 하락 (Drop)" in market_trend and gap_pct > 10:
                case = "Greed"
                verdict_color = "#dc3545" # Red
                verdict_title = "🔴 강력 인하 요구 (Strong Push)"
                verdict_desc = "명분 없는 인상입니다. 시장 트렌드와 미래 전망 모두 귀하의 편입니다."
                target_price = market_avg_price # 프리미엄 제거 요구
                
            elif "▼ 하락 (Drop)" in market_trend and "↗️ 상승 (Rise)" in forecast_trend:
                case = "Golden Time"
                verdict_color = "#28a745" # Green
                verdict_title = "🟢 골든 타임 (Strike Price)"
                verdict_desc = "지금이 최저가일 확률이 높습니다. 장기 계약으로 전환하세요."
                target_price = offer_price # 현재가 락인

            elif "↘️ 하락 (Fall)" in forecast_trend or has_bumper:
                case = "Bear Market"
                verdict_color = "#6c757d" # Gray
                verdict_title = "⚪ 구매 보류 (Wait & See)"
                verdict_desc = "떨어지는 칼날입니다. 급한 물량이 아니라면 구매를 미루세요."
                target_price = market_avg_price * 0.8 # 던지기 유도
                
            else:
                case = "General"
                verdict_color = "#17a2b8" # Teal
                verdict_title = "⚖️ 일반 협상 (Negotiate)"
                verdict_desc = "통상적인 수준의 줄다리기가 필요합니다."
                target_price = fair_price

            # --- 결과 화면 출력 ---
            st.markdown(f"""
            <div class="verdict-box" style="background-color: {verdict_color};">
                {verdict_title}
                <div style="font-size: 0.6em; margin-top: 10px; font-weight: normal;">{verdict_desc}</div>
            </div>
            """, unsafe_allow_html=True)

            # Metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("제안가", f"${offer_price:.2f}")
            with m2:
                st.metric("적정 목표가", f"${target_price:.2f}", delta=f"{target_price - offer_price:.2f}")
            with m3:
                leverage = "구매자 우위" if case in ["Greed", "Bear Market"] else "공급자 우위" if case in ["Supply Shortage"] else "중립"
                st.metric("협상 우위", leverage)

            st.markdown("---")
            
            # 📊 가격 구조 정밀 분석 (Gap Analysis)
            st.subheader("📊 가격 적정성 분석 (Gap Analysis)")
            
            # 데이터 준비 for Stacked Bar
            premium_amt = market_avg_price * (supplier_avg_margin/100)
            overprice_amt = max(0, offer_price - fair_price)
            
            # Bar 1: 적정 가치 모델 (Should-Cost Model)
            # 구성: 시장가(Base) + 인정 프리미엄(Premium) + 초과 마진(Gap)
            # Bar 2: 공급사 제안가 (Supplier Offer)
            
            fig = go.Figure()

            # 1. Market Base (시장 기준가) - 회색
            fig.add_trace(go.Bar(
                name='Market Base (시장가)',
                x=['가격 구조 분석'], y=[market_avg_price],
                marker_color='#adb5bd',
                text=f"${market_avg_price}", textposition='auto'
            ))

            # 2. Premium (인정 프리미엄) - 녹색
            fig.add_trace(go.Bar(
                name='Allowed Premium (인정 마진)',
                x=['가격 구조 분석'], y=[premium_amt],
                marker_color='#28a745',
                text=f"+${premium_amt:.2f}", textposition='auto'
            ))
            
            # 3. Gap (협상 대상) - 빨간색 (제안가가 적정가보다 높을 때만 표시)
            if overprice_amt > 0:
                fig.add_trace(go.Bar(
                    name='Negotiation Target (거품/조정대상)',
                    x=['가격 구조 분석'], y=[overprice_amt],
                    marker_color='#dc3545',
                    pattern_shape="/", # 빗금 처리로 강조
                    text=f"GAP: ${overprice_amt:.2f}", textposition='auto'
                ))
            
            # Layout 설정
            fig.update_layout(
                barmode='stack',
                title_text="적정 가격 모델링 (Should-Cost Model)",
                yaxis_title="단가 ($/kg)",
                height=400,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            # 제안가 라인 추가 (점선)
            fig.add_shape(type="line",
                x0=-0.5, y0=offer_price, x1=0.5, y1=offer_price,
                line=dict(color="Black", width=2, dash="dash"),
            )
            fig.add_annotation(
                x=0.5, y=offer_price,
                text=f"공급사 제안가: ${offer_price}",
                showarrow=False,
                yshift=10, xshift=60
            )

            st.plotly_chart(fig, use_container_width=True)

            # 📝 전문 분석 리포트 (Text Analysis)
            st.markdown("#### 💡 분석 리포트")
            
            analysis_text = f"""
            **1. 시장 기준 (Market Base):** 현재 시장 평균가는 **${market_avg_price}**입니다. 이는 협상의 출발점(Baseline)입니다.<br>
            **2. 인정 프리미엄 (Premium):** 귀사는 공급사의 브랜드 및 품질 가치로 **{supplier_avg_margin}% (+${premium_amt:.2f})**를 인정했습니다.<br>
            """
            
            if overprice_amt > 0:
                gap_percentage = (overprice_amt / offer_price) * 100
                analysis_text += f"""
                <span style='color: #dc3545; font-weight: bold;'>3. 협상 타겟 (Negotiation Target):</span> 
                공급사의 제안가(${offer_price})는 귀하가 산출한 적정가(${fair_price:.2f})보다 **${overprice_amt:.2f}** 높습니다.<br>
                이는 전체 제안 금액의 **{gap_percentage:.1f}%**에 달하며, 설명되지 않는 초과 마진으로 추정됩니다.
                이 부분(Red Zone)을 제거하는 것이 이번 협상의 핵심 목표입니다.
                """
            else:
                analysis_text += f"""
                <span style='color: #28a745; font-weight: bold;'>3. 가격 적정성 (Fair Price):</span> 
                공급사의 제안가(${offer_price})는 귀하가 산출한 적정가(${fair_price:.2f}) 범위 내에 있습니다.
                가격보다는 물량 확보나 결제 조건 등 비가격 조건 협상에 집중하는 것이 유리합니다.
                """
                
            st.markdown(f"<div class='analysis-box'>{analysis_text}</div>", unsafe_allow_html=True)
            
            # 🔮 What-If
            with st.expander("🔮 왓 이프 시뮬레이션 (What-If: 대안 분석)"):
                st.write(f"**Option 1 (대기):** 2주 대기 시 예상 가격 **${forecast_price:.2f}** (Eye Echo 전망)")
                st.write("**Option 2 (산지 변경):** 대체 국가(예: 필리핀, 베트남) 소싱 시 평균 단가 확인 필요")
        else:
            st.info("👈 왼쪽 패널에 데이터를 입력하고 '분석 실행'을 눌러주세요.")

# --- Tool 2: 파트너 검증기 ---
elif page == "Tool 2. 파트너 검증기":
    st.title("🕵️ Partner Validator")
    st.markdown("##### 공급사의 실력, 평판, 리스크를 3차원으로 검증합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.info("### 1️⃣ 공급사 진단 (Audit)")
        
        with st.expander("📝 Section 1. 기본 정보 (Identity)", expanded=True):
            supplier_name = st.text_input("공급사명", "ABC Export Co.")
            target_spec = st.text_input("핵심 타겟 스펙", "Organic Cavendish Banana")
            spec_match = st.radio("프로필 스펙 일치 여부", ["✅ 예 (Yes)", "❓ 불분명 (Unknown)"])
            
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
            strategy_title = ""
            strategy_desc = ""
            
            # Scoring Logic
            if volume_trend == "↗️ 성장세 (Growth)": score += 30
            elif volume_trend == "➡️ 유지 (Stable)": score += 20
            
            if "High-Standard (미국/유럽/일본)" in destinations: score += 20
            
            if buyer_tier == "Global Tier 1 (대기업)": score += 30
            elif buyer_tier == "Regional Tier 2 (중견/도매)": score += 15
            
            if export_history == "✅ 최근 1년 내 있음": score += 20
            elif export_history == "⚠️ 과거 이력만 있음": score += 10
            
            if dependency == "🟢 낮음 (분산됨)": score += 0 # 감점 없음
            else: score -= 20 # 감점
            
            # Grade Logic
            if score >= 90:
                grade = "S"
                grade_title = "Grade S (전략적 파트너)"
                grade_color = "#28a745"
                strategy_title = "Lock-in & Grow"
                strategy_desc = "성장성, 품질, 안정성 모두 완벽합니다. 단가보다 '물량 확보'와 '장기 계약'을 우선하세요."
                email_tone = "존중과 파트너십 제안"
            elif score >= 70:
                if dependency == "🔴 높음 (50% 이상 집중)":
                    grade = "A-"
                    grade_title = "Grade A- (조건부 파트너)"
                    grade_color = "#ffc107"
                    strategy_title = "Penalty & Assurance"
                    strategy_desc = "실력은 좋으나 바쁜 업체입니다. 우리 물량이 밀릴 수 있으니 '납기 보장 조항'을 반드시 넣으세요."
                    email_tone = "납기/안정성 강조"
                else:
                    grade = "A"
                    grade_title = "Grade A (우수 파트너)"
                    grade_color = "#17a2b8"
                    strategy_title = "Competition"
                    strategy_desc = "신뢰할 수 있는 표준 업체입니다. 경쟁 입찰을 통해 단가 경쟁을 유도하세요."
                    email_tone = "표준적인 견적 요청"
            elif score >= 50:
                if export_history == "❌ 없음 (첫 거래)":
                    grade = "B+"
                    grade_title = "Grade B+ (검역 주의)"
                    grade_color = "#fd7e14"
                    strategy_title = "Quality First, Safety Check"
                    strategy_desc = "물건은 좋으나(선진국 수출), 한국 통관은 처음입니다. 검역 사고 방지를 위해 샘플 테스트가 필수입니다."
                    email_tone = "검역 절차 안내 및 샘플 요청"
                else:
                    grade = "B"
                    grade_title = "Grade B (백업 파트너)"
                    grade_color = "#6c757d"
                    strategy_title = "Backup Option"
                    strategy_desc = "주력으로 쓰긴 애매합니다. 협상 결렬 시 압박용 카드로만 활용하세요."
                    email_tone = "시장 조사 차원 접근"
            else:
                grade = "C/F"
                grade_title = "Grade C/F (위험군)"
                grade_color = "#dc3545"
                strategy_title = "Do Not Trade"
                strategy_desc = "부실 위험이 높습니다. 소싱 대상에서 제외하거나 블랙리스트에 등록하세요."
                email_tone = "거절 또는 무응답"

            # --- 결과 화면 ---
            st.markdown(f"""
            <div style="border: 2px solid {grade_color}; border-radius: 10px; padding: 20px; text-align: center;">
                <h1 style="color: {grade_color}; margin: 0;">{grade_title}</h1>
                <h3 style="color: #666;">종합 점수: {score} / 100</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### ✅ 입체 분석")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.info(f"**성장성**\n\n{volume_trend}")
            with c2:
                st.info(f"**평판/레퍼런스**\n\n{buyer_tier}")
            with c3:
                risk_status = "안정적" if dependency == "🟢 낮음 (분산됨)" else "위험 (의존도 높음)"
                st.error(f"**리스크**\n\n{risk_status}") if "위험" in risk_status else st.success(f"**리스크**\n\n{risk_status}")

            st.markdown("---")
            st.subheader(f"🎯 전략: {strategy_title}")
            st.write(strategy_desc)
            
            st.markdown("---")
            st.subheader("🗣️ AI 오프닝 이메일 초안")
            
            email_body = ""
            if grade == "S":
                email_body = f"""Tridge 데이터를 통해 귀사가 최근 수출 물량을 지속적으로 확대하고 있으며, 
특히 글로벌 리더들과 성공적인 파트너십을 맺고 있음을 확인했습니다.

귀사의 이러한 역량은 저희가 찾는 '{target_spec}'의 기준에 완벽히 부합합니다.
또한, 귀사의 안정적인 공급망 구조를 높게 평가하며, 단순 거래를 넘어 
한국 시장 확대를 위한 장기적인 파트너십(Key Account)을 제안드립니다.

MOU 체결 또는 연간 계약 논의를 위해 미팅이 가능할지요? """
            elif grade == "A-":
                 email_body = f"""귀사의 제품 품질과 성장세에 깊은 인상을 받았습니다.
저희는 '{target_spec}' 구매를 긍정적으로 검토 중입니다.

다만, 귀사의 물량이 특정 시기에 집중되는 경향을 확인했습니다.
저희는 안정적인 납기를 최우선으로 고려하므로, 
계약 진행 시 '선적 우선순위 보장(Priority Shipping)' 조항 포함이 가능한지 문의드립니다.
가능하다면 구체적인 견적 부탁드립니다."""
            elif grade == "B+":
                 email_body = f"""미국/유럽 시장에서의 귀사의 명성을 익히 들었습니다.
한국 시장으로의 수출 경험은 아직 없으신 것으로 확인되나, 
귀사의 우수한 품질이라면 충분히 통할 것으로 판단됩니다.

본 계약에 앞서, 한국 검역 기준(Quarantine Standards) 통과 여부를 확인하기 위해
샘플 테스트 및 관련 서류 검토를 먼저 요청드립니다."""
            else:
                 email_body = f"""저희는 현재 '{target_spec}' 공급사를 찾고 있습니다.
귀사의 제품 사양과 FOB 기준 견적서를 보내주시면 검토하겠습니다."""

            st.text_area("이메일 내용", email_body, height=250)

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
st.sidebar.caption("Tridge Action Kit v1.0")
st.sidebar.caption("Based on 'Negotiation & Timing Master' Plan")
