# 🛒 Retail Strategy & Market Basket Optimizer

**A Prescriptive Analytics Engine for Maximizing Cross-Sell Revenue**

**🔴 Live Application:** [Launch Dashboard](https://vighnesh-shetty-vs-market-basket-analy-market-basket-app-iv8ny8.streamlit.app/)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io)
[![Algorithm](https://img.shields.io/badge/Algorithm-FP--Growth-green)](https://github.com/rasbt/mlxtend)

This project moves beyond simple data visualization to provide an **Executive Decision Support System**. It utilizes the **FP-Growth Algorithm** to analyze over 500,000 transactions, identifying high-value product bundles that directly increase **Average Order Value (AOV)**.

---

## 🚀 Business Impact & ROI

The goal of this platform is to translate raw transactional data into actionable merchandising strategies.

* **📈 Cross-Sell Optimization:** Identifies products with high **Lift (Multiplier)** to create data-driven "Bundle Deals" (e.g., "Retro Collection Packs").
* **🛒 Frictionless Upselling:** Provides high-certainty recommendations (High Confidence) for "You May Also Like" website widgets.
* **🧠 "Collector" Psychology:** successfully detects niche purchasing behaviors, such as customers completing specific product sets (e.g., matching novelty tins).

---

## 💡 Case study: matching sets in the French market

`python find_bundles.py France` reproduces these results with the app's default settings (support ≥ 5%, confidence ≥ 30%, lift ≥ 1.2) on 382 French invoices. Cancellations, returns and postage lines are removed. Full list: [reports/bundles_france.md](reports/bundles_france.md).

| Anchor product | Add-on | Baskets with both | Confidence | Lift | Action |
|---|---|---|---|---|---|
| Pack of 6 skull paper cups | Pack of 6 skull paper plates | 5.2% | 80% | 13.9x | Sell as one "party set" SKU |
| Children's cutlery Spaceboy | Children's cutlery Dolly Girl | 6.5% | 93% | 12.6x | Twin pack for families with two children |
| Alarm clock Bakelike red | Alarm clock Bakelike green | 8.1% | 84% | 8.4x | "Collect the colours" display |
| Set/6 red spotty paper cups | Set/6 red spotty paper plates | 12.2% | 89% | 7.0x | Highest-volume pair: checkout upsell |

**What this shows:**
- **French customers buy matching sets.** The strongest rules all pair two designs from the same product line.
- **Lift and volume pull in different directions.** Skull cups and plates have the highest lift but appear in only 5% of baskets. Red spotty cups and plates appear in 12%, with an 89% chance plates follow cups. For a checkout upsell, volume × confidence matters more than lift.
- **Next step:** test each bundle against a control group (A/B) before rolling it out. Association rules show what is bought together, not that a bundle would increase sales.

---

## 🛠️ Technical Architecture

This project was engineered for performance and scalability, handling large datasets that typically crash standard algorithms.

### 1. High-Performance Mining
* **FP-Growth vs. Apriori:** Switched to the **Frequent Pattern Growth** algorithm to eliminate the need for candidate generation, significantly reducing computational cost.
* **Sparse Matrix Optimization:** Implemented `TransactionEncoder` with `sparse=True` to handle massive datasets without MemoryErrors.
* **Boolean Typecasting:** Converted data to boolean arrays to reduce memory footprint by **8x** compared to standard integer matrices.

### 2. Executive Visualization (Plotly)
* **Strategic Opportunity Matrix:** A custom bubble chart that maps **Popularity** (Support) vs. **Certainty** (Confidence), utilizing color thresholds to highlight "Precision Targets" for the business team.

---

## 📸 Dashboard Previews

### 1. The Strategic Opportunity Matrix
*Visualizing the "Precision Zone" where high-certainty automation should occur.*
![Opportunity Matrix](assets/matrix.png)

### 2. The Smart Recommendation Engine
*Real-time upsell predictions based on selected products.*
![Recommender Engine](assets/recommender.png)

---

## 💻 Installation & Usage

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Retail-Strategy-Optimizer.git](https://github.com/YOUR_USERNAME/Retail-Strategy-Optimizer.git)
    cd Retail-Strategy-Optimizer
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    streamlit run market_basket_app.py
    ```

---

## 📂 Project Structure

```text
├── market_basket_app.py   # Main Streamlit Application
├── requirements.txt       # Python Dependencies
├── data/
│   └── OnlineRetail.csv   # Dataset (sourced from Kaggle)
├── assets/                # Screenshots for README
└── README.md              # Project Documentation
