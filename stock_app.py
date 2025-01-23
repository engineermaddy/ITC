import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Set up the Streamlit app with a dark theme
st.set_page_config(page_title="Stock Analyzer Tool", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    /* General background and text styling */
    .main {
        background-color: #121212; /* Dark background */
        color: #e0e0e0; /* Light gray text */
    }
    h1, h2, h3, h4 {
        color: #bb86fc; /* Accent purple */
    }
    .stSidebar {
        background-color: #1e1e1e; /* Sidebar darker background */
        color: #e0e0e0; /* Sidebar text */
        border-right: 3px solid #bb86fc; /* Purple accent border */
    }
    footer {
        text-align: center;
        color: #888888;
        font-size: small;
        padding: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌟 Stock Analyzer Tool (Dark Mode)")
st.write("Analyze and compare stocks with the sleek look of dark mode!")

# List of stocks to analyze
stocks = ["META", "KO", "NFLX", "AAPL", "IBM"]

# Stock descriptions
stock_descriptions = {
    "META": "🌐 **Meta Platforms, Inc.**: Formerly Facebook, Meta focuses on virtual reality, social networking, and digital advertising.",
    "AAPL": "🍎 **Apple Inc.**: A global leader in technology, known for the iPhone, iPad, and Mac.",
    "KO": "🥤 **Coca-Cola**: A beverage giant with its flagship drink Coca-Cola and a wide range of non-alcoholic beverages.",
    "NFLX": "📺 **Netflix**: A streaming entertainment platform with global reach, offering movies, TV shows, and original content.",
    "IBM": "💻 **IBM (International Business Machines)**: Known for innovations in cloud computing, AI, and enterprise services.",
}

# Sidebar for stock selection
st.sidebar.header("Stock Selection")
selected_stocks = st.sidebar.multiselect("Select up to 2 stocks:", stocks, default=["META", "AAPL"])

# Sidebar for date range selection
st.sidebar.header("Select Date Range")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

# Function to generate insights
def generate_insights(stock_data, stock_name):
    if stock_data.empty:
        return f"⚠️ No data available for {stock_name} in the selected date range."
    try:
        latest_close = stock_data['Close'].iloc[-1]
        mean_close = stock_data['Close'].mean()
        highest_close = stock_data['Close'].max()
        lowest_close = stock_data['Close'].min()

        insights = f"""
        - 📊 **Latest Close Price**: ${latest_close:.2f}
        - 📉 **Average Close Price**: ${mean_close:.2f}
        - 📈 **Highest Close Price**: ${highest_close:.2f}
        - 📉 **Lowest Close Price**: ${lowest_close:.2f}
        """
        return insights
    except Exception as e:
        return {stock_name}

# Fetch stock data
if len(selected_stocks) == 0:
    st.error("Please select at least one stock.")
elif start_date >= end_date:
    st.error("Start date must be before the end date.")
else:
    stock_data = {}
    for stock in selected_stocks:
        stock_data[stock] = yf.download(stock, start=start_date, end=end_date)

    # Display stock descriptions, data, and insights
    for stock in selected_stocks:
        st.header(f"📈 {stock} Overview")
        st.write(f"**Description**: {stock_descriptions.get(stock, 'No description available.')}")
        insights = generate_insights(stock_data[stock], stock)
        st.markdown(insights)
        if not stock_data[stock].empty:
            st.subheader(f"{stock} Closing Price Data")
            st.write(stock_data[stock])

    # Interactive chart selection
    st.header("📊 Stock Comparison")
    chart_type = st.radio("Choose a chart type:", ["Closing Price", "Volume"], index=0)

    if chart_type == "Closing Price":
        st.subheader("Closing Price Comparison")
        plt.figure(figsize=(10, 5))
        for stock in selected_stocks:
            if not stock_data[stock].empty:
                plt.plot(stock_data[stock]['Close'], label=f"{stock} Closing Price")
        plt.title("Closing Price Comparison", color="white")
        plt.xlabel("Date", color="white")
        plt.ylabel("Price", color="white")
        plt.legend()
        plt.grid(color="#444444")
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['left'].set_color('white')
        st.pyplot(plt)
    elif chart_type == "Volume":
        st.subheader("Volume Comparison")
        plt.figure(figsize=(10, 5))
        for stock in selected_stocks:
            if not stock_data[stock].empty:
                plt.plot(stock_data[stock]['Volume'], label=f"{stock} Volume")
        plt.title("Volume Comparison", color="white")
        plt.xlabel("Date", color="white")
        plt.ylabel("Volume", color="white")
        plt.legend()
        plt.grid(color="#444444")
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['left'].set_color('white')
        st.pyplot(plt)

    # Summary statistics
    st.header("📋 Summary Statistics")
    for stock in selected_stocks:
        st.subheader(f"{stock} Statistics")
        if not stock_data[stock].empty:
            st.write(stock_data[stock].describe())
        else:
            st.write(f"No data available for {stock} in the selected date range.")

# Footer
st.markdown("""
<hr>
<footer>
 📊
</footer>
""", unsafe_allow_html=True)
