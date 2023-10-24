import streamlit as st
from st_pages import Page, show_pages
import sqlalchemy as sa
from sqlalchemy import inspect
import pandas as pd
import json

with st.sidebar:
    show_pages([
        Page("main.py", "Chatbot"),
        Page("database_connection.py", "Database Connection"),
        Page("model_settings.py", "Language Model Settings"),
        Page("about_contact.py", "About & Contact"),
    ])

db_products_dict = {
    'Sample Database': ['postgres', 'postgresql+psycopg2'],
    'Postgres Database': ['postgres', 'postgresql+psycopg2'],
    'MySQL Database': ['mysql', 'mysql+pymysql://'],
    'MS SQL Server': ['mssql', 'mssql+pyodbc://'],
    'Oracle Database': ['oracle', 'oracle+cx_oracle://'],
}

def try_connecting(connection_str):
    """Attempt to connect to the database using the provided connection string."""
    try:
        engine = sa.create_engine(connection_str)
        connection = engine.connect()  # Attempt to connect
        connection.close()  # Close connection after successful test
        return True
    except:
        return False

def get_schema_details(connection_str):
    """Retrieve the database schema: tables, columns names, and column types."""
    engine = sa.create_engine(connection_str)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    schema_details = {}
    for table in tables:
        columns = []
        for column in inspector.get_columns(table):
            # Convert column type to string
            columns.append((column['name'], str(column['type'])))
        schema_details[table] = columns
    return schema_details

st.title("Database Configuration")
st.markdown("### Configure your Database connection")
db_type = st.selectbox('Choose a Database connection', list(db_products_dict.keys()))

if db_type == 'Sample Database':
    db_host = st.text_input('host', 'psql-mock-database-cloud.postgres.database.azure.com')
    db_port = st.text_input('port', '5432')
    db_user = st.text_input('user', 'ngdwciqxopjtcfotyejybbqg@psql-mock-database-cloud')
    db_password = st.text_input('password', 'sfvldfqrqfyqdmqqzycxltkn', type='password')
    db_name = st.text_input('database', 'cars1695905525019gkakjrfdczmfzouj')

elif db_type == 'Postgres Database':
    db_host = st.text_input('host', 'your-postgres-host')
    db_port = st.text_input('port', '5432')
    db_user = st.text_input('user', 'your-postgres-user')
    db_password = st.text_input('password', '', type='password')
    db_name = st.text_input('database', 'your-database-name')

elif db_type == 'MySQL Database':
    db_host = st.text_input('host', 'your-mysql-host')
    db_port = st.text_input('port', '3306')
    db_user = st.text_input('user', 'your-mysql-user')
    db_password = st.text_input('password', '', type='password')
    db_name = st.text_input('database', 'your-database-name')

elif db_type == 'MS SQL Server':
    db_host = st.text_input('host', 'your-mssql-host')
    db_port = st.text_input('port', '1433')
    db_user = st.text_input('user', 'your-mssql-user')
    db_password = st.text_input('password', '', type='password')
    db_name = st.text_input('database', 'your-database-name')

elif db_type == 'Oracle Database':
    db_host = st.text_input('host', 'your-oracle-host')
    db_port = st.text_input('port', '1521')
    db_user = st.text_input('user', 'your-oracle-user')
    db_password = st.text_input('password', '', type='password')
    db_name = st.text_input('database', 'your-database-name')
    
if st.button('Connect', use_container_width=True):
    with st.spinner('Connecting to the database...'):
        # Construct connection string based on database type
        connector = db_products_dict[db_type][1]
        connection_str = f"{connector}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Try connecting
        if try_connecting(connection_str):

            # Save the database variables into the session state
            st.session_state['db_host'] = db_host
            st.session_state['db_port'] = db_port
            st.session_state['db_user'] = db_user
            st.session_state['db_password'] = db_password
            st.session_state['db_name'] = db_name
            st.session_state['db_type'] = db_type
                    
            # Display schema details in an expander           
            with st.expander("Database Schema"):
                schema_details = get_schema_details(connection_str)
                schema_details_json = json.dumps(schema_details, indent=4)
                                
                st.session_state['schema_details_json'] = schema_details_json
                st.session_state['connection_str'] = connection_str
                
                for table, columns in schema_details.items():
                    st.write(f"Table: {table}")
                    df = pd.DataFrame(columns, columns=['Column Name', 'Data Type'])
                    st.dataframe(df, use_container_width=True)

            st.success('Connected successfully!')
        else:
            st.error('Failed to connect. Please check your credentials.')