
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="가격 정책 시뮬레이터",
    page_icon="📊",
    layout="wide"
)

st.title("📊 가격 정책 시뮬레이터")
st.write(
    "상품의 가격과 할인율에 따라 예상 판매량, "
    "매출, 이익이 어떻게 달라지는지 확인해 보세요."
)

st.info(
    "예상 판매량은 가격탄력성을 이용해 계산한 값이며, "
    "실제 판매 결과와 다를 수 있습니다."
)

# 1. 사용자 입력
st.sidebar.header("조건 설정")

price = st.sidebar.slider(
    "정가 (원)", 5000, 30000, 10000, 500
)

cost = st.sidebar.slider(
    "원가 (원)", 1000, 20000, 5000, 500
)

base_quantity = st.sidebar.slider(
    "기준 판매량 (개)", 10, 500, 100, 10
)

elasticity = st.sidebar.slider(
    "가격탄력성", 0.1, 3.0, 1.5, 0.1
)

discount = st.sidebar.slider(
    "할인율 (%)", 0, 50, 10, 5
)

# 2. 예상 결과 계산
actual_price = price * (1 - discount / 100)

estimated_quantity = (
    base_quantity
    * (actual_price / price) ** (-elasticity)
)

revenue = actual_price * estimated_quantity
profit = (actual_price - cost) * estimated_quantity

# 3. 결과 출력
st.subheader("현재 조건의 예상 결과")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "할인 후 판매 가격",
    f"{actual_price:,.0f}원"
)

col2.metric(
    "예상 판매량",
    f"{estimated_quantity:,.1f}개"
)

col3.metric(
    "예상 매출",
    f"{revenue:,.0f}원"
)

col4.metric(
    "예상 이익",
    f"{profit:,.0f}원"
)

if profit > 0:
    st.success("예상 매출에서 상품 원가를 제외한 이익이 발생합니다.")
elif profit < 0:
    st.warning("현재 조건에서는 예상 손실이 발생합니다.")
else:
    st.info("현재 조건에서는 이익과 손실이 없습니다.")

# 4. 할인율별 결과 계산
discount_rates = np.arange(0, 51, 5)

prices = price * (1 - discount_rates / 100)

quantities = (
    base_quantity * (prices / price) ** (-elasticity)
)

revenues = prices * quantities
profits = (prices - cost) * quantities

# 예상 이익이 가장 큰 할인율
best_index = np.argmax(profits)
best_discount = discount_rates[best_index]
best_profit = profits[best_index]

# 5. 그래프 출력
st.subheader("할인율별 결과 비교")

left, right = st.columns(2)

with left:
    fig, ax = plt.subplots()

    ax.plot(
        discount_rates,
        revenues,
        marker="o"
    )

    ax.axvline(
        discount,
        linestyle="--",
        label=f"현재 할인율 {discount}%"
    )

    ax.set_title("할인율에 따른 예상 매출")
    ax.set_xlabel("할인율 (%)")
    ax.set_ylabel("예상 매출 (원)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()

    st.pyplot(fig)
    plt.close(fig)

with right:
    fig, ax = plt.subplots()

    ax.plot(
        discount_rates,
        profits,
        marker="o"
    )

    ax.axvline(
        discount,
        linestyle="--",
        label=f"현재 할인율 {discount}%"
    )

    ax.axhline(0, linestyle=":", linewidth=1)

    ax.set_title("할인율에 따른 예상 이익")
    ax.set_xlabel("할인율 (%)")
    ax.set_ylabel("예상 이익 (원)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()

    st.pyplot(fig)
    plt.close(fig)

# 6. 최적 할인율 안내
st.subheader("💡 할인율 분석")

st.write(
    f"0~50% 할인율 중 예상 이익이 가장 큰 할인율은 "
    f"**{best_discount}%**입니다."
)

st.write(f"해당 할인율에서 예상 이익은 **{best_profit:,.0f}원**입니다.")

st.caption(
    "계산 모형: 예상 판매량 = 기준 판매량 × "
    "(할인 후 가격 ÷ 정가) ^ (−가격탄력성)"
)
