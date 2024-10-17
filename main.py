import streamlit as st
import pandas as pd
from salesforce_utils import connect_to_salesforce, get_metadata_types, get_metadata
from diff_utils import compare_metadata
import base64

st.set_page_config(page_title="Salesforce Metadata Diff Checker", layout="wide")

def main():
    st.title("Salesforce Metadata Diff Checker")

    # Sidebar for org credentials
    st.sidebar.header("Salesforce Org Credentials")
    
    # Org 1 credentials
    st.sidebar.subheader("Org 1")
    username1 = st.sidebar.text_input("Username (Org 1)", key="username1")
    password1 = st.sidebar.text_input("Password (Org 1)", type="password", key="password1")
    security_token1 = st.sidebar.text_input("Security Token (Org 1)", type="password", key="security_token1")
    
    # Org 2 credentials
    st.sidebar.subheader("Org 2")
    username2 = st.sidebar.text_input("Username (Org 2)", key="username2")
    password2 = st.sidebar.text_input("Password (Org 2)", type="password", key="password2")
    security_token2 = st.sidebar.text_input("Security Token (Org 2)", type="password", key="security_token2")

    if st.sidebar.button("Connect and Compare"):
        try:
            # Connect to both Salesforce orgs
            sf1 = connect_to_salesforce(username1, password1, security_token1)
            sf2 = connect_to_salesforce(username2, password2, security_token2)

            # Get metadata types
            metadata_types = get_metadata_types(sf1)

            # Allow user to select metadata types
            selected_types = st.multiselect("Select metadata types to compare", metadata_types)

            if selected_types:
                # Retrieve metadata for selected types from both orgs
                metadata1 = get_metadata(sf1, selected_types)
                metadata2 = get_metadata(sf2, selected_types)

                # Compare metadata
                diff_results = compare_metadata(metadata1, metadata2)

                # Create a single DataFrame with all differences
                all_differences = []
                for metadata_type, differences in diff_results.items():
                    for diff in differences:
                        diff['Metadata Type'] = metadata_type
                        all_differences.append(diff)

                df = pd.DataFrame(all_differences)

                # Display results
                st.header("Metadata Differences")

                # Add a filter for metadata types
                selected_type = st.selectbox("Filter by Metadata Type", ["All"] + list(diff_results.keys()))

                # Filter the dataframe based on selection
                if selected_type != "All":
                    filtered_df = df[df['Metadata Type'] == selected_type]
                else:
                    filtered_df = df

                # Display all differences in a single dataframe
                st.dataframe(filtered_df)

                # Export results as CSV
                if st.button("Export Results as CSV"):
                    csv = export_results_as_csv(filtered_df)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="metadata_diff_results.csv",
                        mime="text/csv",
                    )
            else:
                st.warning("Please select at least one metadata type to compare.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def export_results_as_csv(df):
    return df.to_csv(index=False)

if __name__ == "__main__":
    main()
