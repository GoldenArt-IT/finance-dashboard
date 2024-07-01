import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page to always wide
st.set_page_config(layout="wide")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file (A/R Receivable ONLY)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:

        collection_by_year_column, collection_by_month = st.columns(2)

        with collection_by_year_column:

            st.header('Total Collection by Year')

            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            
            # Ensure the Date column is in datetime format
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Extract year and month for filterings
            df['Year'] = df['Date'].dt.year.astype(int)
            df['Month'] = df['Date'].dt.month_name()

            #sort months correctly
            months_in_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            df['Month'] = pd.Categorical(df['Month'], categories=months_in_order, ordered=True)
            
            # # Display the dataframe
            # st.write("Data Preview:")
            # st.write(df)
            
            # Select year and month
            # selected_year = st.selectbox('Select Year:', sorted(df['Year'].unique()))
            # selected_month = st.selectbox('Select Month:', df['Month'].unique())
            
            # # Filter data based on selection
            # filtered_df = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]
            
            # st.write(f"Data for {selected_year} - {selected_month}:")
            # st.write(filtered_df.head())
            
            # Group data by Year and calculate the total amount
            grouped_df = df.groupby('Year')['Amount'].sum().reset_index()
            
            # Plotting the bar chart for total amount by year
            fig1, ax1 = plt.subplots(figsize=(13,6))
            bars1 = ax1.bar(grouped_df['Year'], grouped_df['Amount'])
            ax1.set_title('Total Collection by Year')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Total Collection')

            # # Add annotations
            # for bar in bars:
            #     height = bar.get_height()
            #     ax.annotate(f'{height:.2f}',
            #                 xy=(bar.get_x() + bar.get_width() / 2, height),
            #                 xytext=(0, 3),  # 3 points vertical offset
            #                 textcoords="offset points",
            #                 ha='center', va='bottom')
            st.pyplot(fig1)
        
        with collection_by_month:
            st.header('Total Collection by Month')

            selected_year = st.selectbox('Select Year: ', sorted(df['Year'].unique(), reverse=True))
            filtered_year_df = df[df['Year'] == selected_year]
            filtered_year_grouped_df = filtered_year_df.groupby('Month')['Amount'].sum().reset_index().sort_values(by='Month')

            fig2, ax2 = plt.subplots(figsize=(13,6))
            bars2 = ax2.bar(filtered_year_grouped_df['Month'], filtered_year_grouped_df['Amount'])
            ax2.set_title('Total Collection by Month for Year {}'.format(selected_year))
            st.pyplot(fig2)

        collection_by_company, top_collection = st.columns(2)
        
        with collection_by_company:
            st.header('Total Collection by Company')

            selected_company = st.selectbox('Select Company: ', sorted(df['Company Name'].unique()))
            filtered_company_df = filtered_year_df[filtered_year_df['Company Name'] == selected_company]
            filtered_company_grouped_df = filtered_company_df.groupby('Month')['Amount'].sum().reset_index().sort_values(by='Month')

            fig3, ax3 = plt.subplots(figsize=(13,6))
            bars3 = ax3.bar(filtered_company_grouped_df['Month'], filtered_company_grouped_df['Amount'])
            ax3.set_title('Total Collection by Company {}'.format(selected_company) + ' in Year {}'.format(selected_year))
            st.pyplot(fig3)

        with top_collection:
            st.header('Top Collection by Company')

            filtered_top_company_grouped_df = filtered_year_df.groupby('Company Name')['Amount'].sum().reset_index()
            top_15_company = filtered_top_company_grouped_df.sort_values(by='Amount', ascending=False).head(20)

            fig4, ax4 = plt.subplots(figsize=(13,11))
            bar4 = ax4.barh(top_15_company['Company Name'], top_15_company['Amount'])
            ax4.set_title('Top Collection for Year {}'.format(selected_year))
            ax4.invert_yaxis()

            st.pyplot(fig4)

    except Exception as e:
        st.error(f"Error: {e}")
