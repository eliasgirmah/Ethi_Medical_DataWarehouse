import os
import psycopg2
from dotenv import load_dotenv
import torch
import cv2
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# PostgreSQL database credentials
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connect to PostgreSQL database
def create_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Create table if it doesn't exist
def create_table(conn):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS detections (
        id SERIAL PRIMARY KEY,
        image_name TEXT,
        class_name TEXT,
        confidence FLOAT,
        x_min FLOAT,
        y_min FLOAT,
        x_max FLOAT,
        y_max FLOAT
    );
    '''
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
        conn.commit()

# Insert detection results into the database
def insert_detection(conn, image_name, class_name, confidence, bbox):
    insert_query = '''
    INSERT INTO detections (image_name, class_name, confidence, x_min, y_min, x_max, y_max)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    '''
    with conn.cursor() as cursor:
        cursor.execute(insert_query, (image_name, class_name, confidence, *bbox))
        conn.commit()

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)

# Directory containing images
images_dir = './images'  # Update this path
results_dir = './results'  # Update this path

# Create a database connection
conn = create_connection()
if conn:
    create_table(conn)  # Create the detections table

    # Iterate over images
    for image_name in os.listdir(images_dir):
        image_path = os.path.join(images_dir, image_name)
        img = cv2.imread(image_path)

        # Perform detection
        results = model(img)

        # Process results
        for detection in results.xyxy[0]:  # detections for the first image
            x_min, y_min, x_max, y_max, confidence, class_id = detection.tolist()
            class_name = results.names[int(class_id)]

            # Insert the detection into the database
            insert_detection(conn, image_name, class_name, confidence, (x_min, y_min, x_max, y_max))

            # Optionally, save the detection results to a file
            # You can also visualize the results and save images with bounding boxes

    # Close the database connection
    conn.close()
else:
    print("Failed to create database connection.")
