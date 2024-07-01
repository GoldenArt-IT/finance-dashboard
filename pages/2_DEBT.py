import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page to always wide
st.set_page_config(layout="wide")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file (Outstanding A/R Invoice)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try: 
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

        df['Due Date'] = pd.to_datetime(df['Due Date'])
        df['Due Year'] = df['Due Date'].dt.year.astype(int)
        df['Due Month'] = df['Due Date'].dt.month_name()
        months_in_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        df['Due Month'] = pd.Categorical(df['Due Month'], categories=months_in_order, ordered=True)

        # st.write(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.header('Total Due Payment')
            selected_year = st.selectbox('Select Due Year: ', sorted(df['Due Year'].unique(), reverse=True))
            filtered_year = df[df['Due Year'] == selected_year]
            total_due = filtered_year.groupby('Due Month')['Local Outstanding'].sum().reset_index()

            fig1, ax1 = plt.subplots(figsize=(13, 6))
            bar1 = ax1.bar(total_due['Due Month'], total_due['Local Outstanding'])
            ax1.set_title('Total Due Payment for Year {}'.format(selected_year))

            st.pyplot(fig1)

        with col2:
            st.header('Total Due by Company')
            selected_company = st.selectbox('Select Company: ', sorted(df['Company Name'].unique()))
            filtered_company = filtered_year[df['Company Name'] == selected_company]
            total_due_company = filtered_company.groupby('Due Month')['Local Outstanding'].sum().reset_index()

            fig2, ax2 = plt.subplots(figsize=(13,6))
            bar2 = ax2.bar(total_due_company['Due Month'], total_due_company['Local Outstanding'])
            ax2.set_title(f'Total Due Payment {selected_company} for Year {selected_year}')

            st.pyplot(fig2)

        st.header('Total Due Payment by Month')

        selected_month = st.selectbox('Select Month: ', months_in_order)
        filtered_month = filtered_year[filtered_year['Due Month'] == selected_month]
        total_due_month = filtered_month.groupby('Company Name')['Local Outstanding'].sum().reset_index()

        fig3, ax3 = plt.subplots(figsize=(20,10))
        bar3 = ax3.barh(total_due_month['Company Name'], total_due_month['Local Outstanding'])
        ax3.set_title(f'Total Due Payment in {selected_month} {selected_year}')

        st.pyplot(fig3)

        st.write(total_due_month)

    except Exception as e:
        st.error(f"Error: {e}")