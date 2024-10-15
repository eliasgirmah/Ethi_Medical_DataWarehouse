# Medical Data Warehouse using YOLOv5

A comprehensive data warehouse solution for Ethiopian medical business data scraped from Telegram channels. This project includes data scraping, object detection with YOLOv5, and ETL/ELT processes to transform and store the data efficiently.

## Project Directory Structure

The repository is organized into the following directories:

- `.github/workflows/`: Contains configurations for GitHub Actions, enabling continuous integration (CI) and automated testing.

- `.vscode/`: Configuration files for the Visual Studio Code editor, optimizing the development environment.

- `app/`: Contains the implementation of the machine learning model API, which allows interaction with the object detection model through RESTful endpoints.

- `notebooks/`: Jupyter notebooks for tasks such as data exploration, feature engineering, and preliminary modeling.

- `scripts/`: Python scripts for data preprocessing, feature extraction, object detection with YOLOv5, and handling the medical data.

- `tests/`: Unit tests to ensure the correctness and robustness of the implemented model and data processing logic.

## Installation Instructions

To run the project locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/eliasgirmah/Ethi_Medical_DataWarehouse.git
cd Ethi_Medical_DataWarehouse

2. Set up the Virtual Environment
Create a virtual environment to manage the project's dependencies.

For Linux/MacOS:
```bash
python3 -m venv .venv
source .venv/bin/activate

## Install Dependencies
```bash
pip install -r requirements.txt

