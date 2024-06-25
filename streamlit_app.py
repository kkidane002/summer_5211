import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on June 20th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("Addition Below")


# Extract unique categories from the 'Category' column
categories = df['Category'].unique()

# Create a selectbox with the unique categories
selected_category = st.selectbox(
    "Select a category:",
    categories
    )
# Check if 'Sub-Category' column exists
if 'Sub_Category' in df.columns:
    # Extract unique sub-categories based on the selected category
    sub_categories = df[df['Category'] == selected_category]['Sub_Category'].unique()

    # Create a multiselect with the unique sub-categories
    selected_sub_categories = st.multiselect(
        "Select sub-categories:",
        sub_categories
    )

    # Display the selected sub-categories
    st.write("You selected:", selected_sub_categories)

    # Filter data for the selected sub-categories
    if selected_sub_categories:
        filtered_data = df[df['Sub_Category'].isin(selected_sub_categories)]

        # Aggregate sales by month for the filtered data
        sales_by_month_filtered = filtered_data.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

        # Display the line chart of sales for the selected sub-categories
        st.line_chart(sales_by_month_filtered, y="Sales")

        # Calculate metrics for selected sub-categories
        total_sales = filtered_data['Sales'].sum()
        total_profit = filtered_data['Profit'].sum()
        overall_profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

        # Calculate overall average profit margin
        total_sales_all = df['Sales'].sum()
        total_profit_all = df['Profit'].sum()
        overall_profit_margin_all = (total_profit_all / total_sales_all) * 100 if total_sales_all > 0 else 0

        # Calculate delta
        delta = overall_profit_margin - overall_profit_margin_all

        # Display metrics
        st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
        st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
        st.metric(label="Overall Profit Margin (%)", value=f"{overall_profit_margin:.2f}%", delta=f"{delta:.2f}%")
else:
    st.write("Error: 'Sub-Category' column not found in the dataset.")







