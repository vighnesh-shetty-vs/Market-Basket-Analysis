import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Retail Strategy Optimizer",
    page_icon="⚡",
    layout="wide"
)

# --- 2. OPTIMIZED DATA LOADING ---
@st.cache_data
def load_data():
    try:
        # Define types to save memory during load
        dtype_dict = {
            'InvoiceNo': 'str',
            'Description': 'str',
            'Quantity': 'int32',
            'Country': 'category'
        }
        df = pd.read_csv("data/OnlineRetail.csv", encoding="ISO-8859-1", dtype=dtype_dict)
        
        # Fast Cleaning
        df = df.dropna(subset=['InvoiceNo', 'Description'])
        df['Description'] = df['Description'].str.strip()
        df = df[~df['InvoiceNo'].str.startswith('C')] # Remove cancellations
        return df
    except FileNotFoundError:
        return None

# --- 3. OPTIMIZED RULE GENERATION ---
@st.cache_data
def generate_rules(df, country, min_sup, min_conf, min_lift):
    # Filter by Country FIRST to reduce data size immediately
    subset = df[df['Country'] == country]
    
    # High-Performance Transaction Grouping (List of Lists)
    transactions = subset.groupby('InvoiceNo')['Description'].apply(list).tolist()
    
    # Use TransactionEncoder (Memory Efficient)
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions, sparse=True)
    df_bool = pd.DataFrame.sparse.from_spmatrix(te_ary, columns=te.columns_)
    
    # Run FP-Growth on Sparse Matrix
    frequent_itemsets = fpgrowth(df_bool, min_support=min_sup, use_colnames=True)
    
    if frequent_itemsets.empty:
        return pd.DataFrame()
        
    # Generate Rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
    
    # Filter by Confidence
    rules = rules[rules['confidence'] >= min_conf]
    
    # String Conversion for Display
    rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
    
    return rules.sort_values(['lift', 'confidence'], ascending=[False, False])

# --- 4. APP HEADER ---
st.title("⚡ Retail Strategy Optimizer (Enterprise Edition)")
st.markdown("Identifies high-value product pairings to drive **Average Order Value (AOV)** and **Cross-Sell Revenue**.")
st.divider()

df = load_data()

if df is not None:
    # --- 5. CONTROLS ---
    st.sidebar.header("🕹️ Strategy Parameters")
    country = st.sidebar.selectbox("Market Region", df['Country'].unique(), index=list(df['Country'].unique()).index('France'))
    
    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Fine-Tune Filters")
    min_pop = st.sidebar.slider("Market Popularity (%)", 0.01, 0.20, 0.05)
    min_cert = st.sidebar.slider("Purchase Certainty (%)", 0.10, 1.0, 0.30)
    min_str = st.sidebar.slider("Strategic Strength (Lift)", 1.0, 10.0, 1.2)

    # --- 6. PROCESSING ---
    with st.spinner('Analyzing consumer baskets...'):
        rules = generate_rules(df, country, min_pop, min_cert, min_str)

    # --- 7. EXECUTIVE KPI DASHBOARD (Updated) ---
    st.subheader("📊 Executive Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 Active Bundles", 
            value=len(rules),
            delta="Identified Patterns",
            delta_color="off",
            help="Total number of product pairings identified. Recommendation: Focus resources on the Top 10% highest-lift rules."
        )
    
    with col2:
        max_lift = rules['lift'].max() if not rules.empty else 0
        st.metric(
            label="🚀 Max Cross-Sell Multiplier", 
            value=f"{max_lift:.2f}x",
            help="The strongest relationship found. How much more likely products are bought together vs alone. Recommendation: Create a dedicated 'Bundle Deal' for this pair."
        )
        
    with col3:
        avg_conf = rules['confidence'].mean() if not rules.empty else 0
        st.metric(
            label="🎯 Avg. Buy Probability", 
            value=f"{avg_conf:.0%}",
            help="Average likelihood of the second product being purchased if the first is in the cart. Recommendation: Use for 'You May Also Like' widgets."
        )
        
    with col4:
        st.metric(
            label="🔍 Strategy Focus", 
            value="Top 500 Rules", 
            help="Visualizing only the highest-impact rules to ensure quick decision making and fast loading."
        )

    # --- 8. BUSINESS RECOMMENDATIONS (New Section) ---
    with st.expander("💡 Executive Guide: How to Achieve these Metrics", expanded=True):
        st.markdown("""
        * **To Increase Cross-Sell Multiplier:** Focus on *complementary* items rather than just popular ones. High lift comes from specific pairs (e.g., 'Flashlight + Batteries') rather than generic bestsellers.
        * **To Boost Buy Probability:** Improve the *visibility* of the recommended item. Place the 'Add-On' product directly next to the 'Add to Cart' button of the main product on the website.
        * **To Scale Active Bundles:** If 'Active Bundles' is low, try lowering the 'Market Popularity' slider to find 'Long Tail' opportunities hidden in niche customer segments.
        """)

    # --- 9. OPTIMIZED VISUALIZATION ---
    st.divider()
    st.subheader("🌐 Strategic Opportunity Matrix")
    
    if not rules.empty:
        # PERFORMANCE SAFEGUARD: Only plot top 500 rules
        plot_data = rules.head(500)
        
        fig = px.scatter(
            plot_data, 
            x="support", 
            y="confidence", 
            size="lift", 
            color="lift",
            hover_name="consequents_str",
            hover_data={'antecedents_str': True, 'lift': ':.2f', 'support': ':.3f', 'confidence': ':.2f'},
            labels={'support': 'Market Popularity', 'confidence': 'Buy Probability', 'lift': 'ROI Multiplier'},
            template="plotly_dark", 
            color_continuous_scale="RdYlGn", 
            height=600,
            title=f"Top {len(plot_data)} Strategic Patterns (Sorted by Strength)"
        )
        
        fig.add_annotation(x=plot_data['support'].max()*0.9, y=plot_data['confidence'].max(), 
                           text="💎 PRECISION ZONE", showarrow=False, font=dict(color="#00FF00"))
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No patterns found. Try lowering the 'Market Popularity' slider.")

    # --- 10. RECOMMENDATION ENGINE ---
    st.divider()
    col_rec, col_data = st.columns([1, 1])
    
    with col_rec:
        st.subheader("💡 Smart Recommender")
        if not rules.empty:
            all_prods = sorted(list(set(rules['antecedents_str'])))
            selected_prod = st.selectbox("Customer Views:", all_prods)
            
            recs = rules[rules['antecedents_str'] == selected_prod].head(5)
            if not recs.empty:
                st.write("**Top Upsell Opportunities:**")
                for _, row in recs.iterrows():
                    st.success(f"➕ **{row['consequents_str']}** (Lift: {row['lift']:.2f}x)")
            else:
                st.info("No strong rules for this specific item.")
    
    with col_data:
        st.subheader("📥 Export Data")
        if not rules.empty:
            csv = rules[['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift']].to_csv(index=False).encode('utf-8')
            st.download_button("Download Strategy CSV", csv, "rules.csv", "text/csv")

else:
    st.error("Data not found. Please ensure 'data/OnlineRetail.csv' exists.")