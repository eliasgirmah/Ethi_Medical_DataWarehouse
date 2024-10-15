import pandas as pd
import psycopg2
import emoji
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to clean the message by removing emojis and unnecessary characters
def clean_message(message):
    # Remove emojis using the emoji library
    message = emoji.replace_emoji(message, replace='')
    # Remove extra whitespace
    message = ' '.join(message.split())
    return message

# Database connection parameters from .env
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST', 'localhost'),  # Default to localhost if not specified
    'port': os.getenv('DB_PORT', 5432)          # Default port for PostgreSQL
}

# Read the CSV file
df = pd.read_csv('./telegram_data.csv')

# Clean the data
df['Message'] = df['Message'].apply(clean_message)
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d %H:%M:%S')

# Connect to PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Create table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS Clean_medical_data (
    channel_title VARCHAR(255),
    channel_username VARCHAR(255),
    id SERIAL PRIMARY KEY,
    message TEXT,
    date TIMESTAMP,
    media_path TEXT
);
'''
cursor.execute(create_table_query)

# Insert cleaned data into the database
insert_query = '''
INSERT INTO doctors_data (channel_title, channel_username, id, message, date, media_path)
VALUES (%s, %s, %s, %s, %s, %s);
'''

for index, row in df.iterrows():
    cursor.execute(insert_query, (row['Channel Title'], row['Channel Username'], row['ID'], row['Message'], row['Date'], row['Media Path']))

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data cleaned and stored in PostgreSQL database successfully.")