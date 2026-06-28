# 🛡️ Phishing Website Detection Using Machine Learning

An end-to-end Machine Learning pipeline that detects phishing websites by analyzing 30 URL-based and webpage-based features. The project includes data ingestion from MongoDB, automated data validation, transformation, model training with hyperparameter tuning, and a Flask web application for real-time batch predictions.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Project Architecture](#project-architecture)
- [Tech Stack](#tech-stack)
- [Dataset & Features](#dataset--features)
- [ML Models & Results](#ml-models--results)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [API Endpoints](#api-endpoints)
- [Docker Support](#docker-support)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Phishing is a type of cyber attack where attackers create fraudulent websites that mimic legitimate ones to steal sensitive information such as login credentials, credit card numbers, and personal data. This project builds a **machine learning classifier** that can predict whether a given website is **phishing** or **safe** based on its URL and webpage characteristics.

### Key Highlights

- **Modular ML Pipeline**: Data Ingestion → Data Validation → Data Transformation → Model Training
- **Automated Hyperparameter Tuning**: Uses GridSearchCV with 5-fold cross-validation
- **Best Model**: XGBClassifier achieving **~97.8% accuracy**
- **Web Interface**: Flask-based UI for uploading CSV files and getting batch predictions
- **MongoDB Integration**: Training data stored and retrieved from MongoDB Atlas
- **Offline Support**: Runs entirely on your local machine without requiring AWS

---

## Project Architecture

```
                    ┌──────────────────┐
                    │   MongoDB Atlas  │
                    │  (Training Data) │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Data Ingestion  │
                    │  (Export to CSV)  │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Data Validation │
                    │ (Schema Checks)  │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Data Transform.  │
                    │ (Impute+Resample)│
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Model Trainer   │
                    │(Train+Tune+Save) │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │   Flask Web App  │
                    │ (Predict via UI) │
                    └──────────────────┘
```

---

## Tech Stack

| Category         | Technology                                          |
| ---------------- | --------------------------------------------------- |
| **Language**      | Python 3.10+                                        |
| **Web Framework** | Flask 2.0.3                                         |
| **ML Libraries**  | Scikit-learn, XGBoost, Imbalanced-learn (SMOTE)     |
| **Database**      | MongoDB Atlas (via PyMongo)                         |
| **Data Handling** | Pandas, NumPy                                       |
| **Visualization** | Matplotlib, Seaborn (in notebooks)                  |
| **Serialization** | Pickle / Dill                                       |
| **Containerization** | Docker                                           |
| **CI/CD**         | GitHub Actions (optional AWS ECR deployment)        |

---

## Dataset & Features

The dataset contains **11,055 samples** with **30 features** extracted from website URLs and webpages. Each feature is encoded as:
- `1` → Legitimate  
- `0` → Suspicious  
- `-1` → Phishing  

### Feature Categories

| Category                  | Features                                                                                                 |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Address Bar Based**     | `having_IP_Address`, `URL_Length`, `Shortining_Service`, `having_At_Symbol`, `double_slash_redirecting`, `Prefix_Suffix`, `having_Sub_Domain`, `SSLfinal_State`, `Domain_registeration_length`, `Favicon`, `port`, `HTTPS_token` |
| **Abnormal Based**        | `Request_URL`, `URL_of_Anchor`, `Links_in_tags`, `SFH`, `Submitting_to_email`, `Abnormal_URL`, `Redirect` |
| **HTML & JS Based**       | `on_mouseover`, `RightClick`, `popUpWidnow`, `Iframe`                                                   |
| **Domain Based**          | `age_of_domain`, `DNSRecord`, `web_traffic`, `Page_Rank`, `Google_Index`, `Links_pointing_to_page`, `Statistical_report` |
| **Target**                | `Result` — `1` (Safe) / `-1` (Phishing)                                                                 |

---

## ML Models & Results

Three classifiers are trained, evaluated, and compared using **accuracy score**. The best model is then fine-tuned using **GridSearchCV** with 5-fold cross-validation.

| Model                | Test Accuracy |
| -------------------- | ------------- |
| Gaussian Naive Bayes | ~60%          |
| Logistic Regression  | ~92%          |
| **XGBoost Classifier** | **~97.8%** ✅ |

### Hyperparameter Search Space (XGBClassifier)

```yaml
max_depth: [3, 5, 7, 9, 11]
n_estimators: [50, 100, 130]
random_state: [0, 50, 100]
```

**Best Parameters Found**: `max_depth=11`, `n_estimators=130`, `random_state=0`

---

## Project Structure

```
phishing-classifier/
│
├── app.py                          # Flask application entry point
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup for src module
├── model.pkl                       # Trained model (generated after training)
├── upload_data.py                  # Script to upload CSV data to MongoDB
├── DockerFile                      # Docker container configuration
├── .env                            # Environment variables (MongoDB URL) — NOT committed
├── .gitignore                      # Git ignore rules
│
├── config/
│   ├── model.yaml                  # Hyperparameter grid for model tuning
│   └── training_schema.json        # Schema for data validation (column names & types)
│
├── src/
│   ├── __init__.py
│   ├── exception.py                # Custom exception handler
│   ├── logger.py                   # Logging configuration
│   │
│   ├── components/
│   │   ├── data_ingestion.py       # Fetches data from MongoDB → CSV
│   │   ├── data_validation.py      # Validates schema, column count, file naming
│   │   ├── data_transformation.py  # Imputation, resampling, train-test split
│   │   └── model_trainer.py        # Model training, tuning, evaluation, saving
│   │
│   ├── configuration/
│   │   └── mongo_db_connection.py  # MongoDB client connection handler
│   │
│   ├── constant/
│   │   └── __init__.py             # Project-wide constants
│   │
│   ├── data_access/
│   │   └── phising_data.py         # Data access layer for MongoDB collections
│   │
│   ├── pipeline/
│   │   ├── train_pipeline.py       # Orchestrates the full training pipeline
│   │   └── predict_pipeline.py     # Handles file upload, prediction, CSV download
│   │
│   └── utils/
│       └── main_utils.py           # Utility functions (save/load objects, YAML reader)
│
├── templates/
│   └── prediction.html             # Web UI for CSV file upload & prediction
│
├── static/
│   └── css/style.css               # Stylesheet for the web interface
│
├── upload_data_to_db/
│   ├── phising_08012020_120000.csv  # Raw dataset for MongoDB upload
│   └── mongodbupload.ipynb         # Jupyter notebook for manual data upload
│
├── notebook implementation/         # EDA and experimentation notebooks
│
├── predictions/                     # Output directory for predicted CSV files
├── prediction_artifacts/            # Uploaded input files for prediction
├── artifacts/                       # Training artifacts (generated at runtime)
└── logs/                            # Application logs
```

---

## Setup & Installation

### Prerequisites

- **Python 3.10+** installed on your system
- **MongoDB Atlas** account (free tier works) — [Sign up here](https://www.mongodb.com/atlas)
- **Git** for cloning the repository

### Step 1: Clone the Repository

```bash
git clone https://github.com/Yash13Agrawal/Phishing-Website-Detection-Using-Machine-Learning.git
cd Phishing-Website-Detection-Using-Machine-Learning
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure MongoDB

1. Create a `.env` file in the project root directory.
2. Add your MongoDB Atlas connection string:

```env
MONGO_DB_URL="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
```

> ⚠️ **Important**: Never commit the `.env` file to version control. It is already listed in `.gitignore`.

### Step 5: Upload the Dataset to MongoDB

**Option A — Using the upload script:**
```bash
python upload_data.py
```

**Option B — Using MongoDB Compass or Atlas UI:**
1. Create a database named `phising`
2. Create a collection named `phising_08012020_120000`
3. Import the CSV file from `upload_data_to_db/phising_08012020_120000.csv`

---

## How to Run

### Start the Flask Application

```bash
python app.py
```

The server will start at **`http://localhost:8080`**.

### Train the Model

Open your browser and navigate to:

```
http://localhost:8080/train
```

This will trigger the full ML pipeline:
1. **Data Ingestion** — Exports data from MongoDB to local CSV files
2. **Data Validation** — Checks file naming conventions, column count, and data types against the schema
3. **Data Transformation** — Handles missing values (imputation with most frequent strategy), applies RandomOverSampler for class balancing, and splits the data (80/20)
4. **Model Training** — Trains GaussianNB, LogisticRegression, and XGBClassifier, then fine-tunes the best model using GridSearchCV
5. **Model Saving** — Saves the trained model as `model.pkl` in the project root

When complete, the page will display: **"Training Completed."**

### Make Predictions

Navigate to:

```
http://localhost:8080/predict
```

1. Upload a CSV file containing website features (all 30 feature columns, **without** the `Result` column)
2. Click **Upload file**
3. The app will process the data and automatically download a `predicted_file.csv` with a new `Result` column:
   - `safe` — The website is predicted as legitimate
   - `phising` — The website is predicted as a phishing site

> 💡 **Tip**: You can use the dataset file `upload_data_to_db/phising_08012020_120000.csv` for testing — just remove the `Result` column before uploading.

---

## API Endpoints

| Method | Endpoint    | Description                                        |
| ------ | ----------- | -------------------------------------------------- |
| GET    | `/`         | Home page — returns a JSON response                |
| GET    | `/train`    | Triggers the full training pipeline                |
| GET    | `/predict`  | Renders the CSV file upload page                   |
| POST   | `/predict`  | Accepts a CSV file and returns predictions as download |

---

## Docker Support

Build and run the application using Docker:

```bash
# Build the Docker image
docker build -t phishing-classifier .

# Run the container
docker run -p 8080:8080 --env-file .env phishing-classifier
```

The application will be accessible at `http://localhost:8080`.

---

## Screenshots

### Training Pipeline Output
```
feature_store_file_path-----artifacts\...\data_ingestion\phising_08012020_120000.csv
Fitting 5 folds for each of 45 candidates, totalling 225 fits
best params are: {'max_depth': 11, 'n_estimators': 130, 'random_state': 0}
best model name XGBClassifier and score: 0.9813235891189607
training completed. Trained model score: 0.9813235891189607
```

### Prediction Output (predicted_file.csv)
| having_IP_Address | URL_Length | ... | Statistical_report | Result  |
| ----------------- | ---------- | --- | ------------------ | ------- |
| -1                | 1          | ... | -1                 | phising |
| 1                 | 0          | ... | 1                  | safe    |

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is open source and available for educational purposes.

---

## Author

**Yash Agrawal**  
📧 yashagrawal13032004@gmail.com  
🔗 [GitHub](https://github.com/Yash13Agrawal)
