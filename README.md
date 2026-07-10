# 🏠 House Price Prediction Using Machine Learning

A complete, full-stack Machine Learning web application that predicts house prices in real time. Built with **Flask**, **scikit-learn**, and a modern **glassmorphism UI** (White + Blue + Purple theme), it takes property details as input and returns a predicted price, a confidence score, and a price category (Affordable / Medium / Luxury), backed by interactive Chart.js visualizations.

---

**Live Demo:** https://house-priceprediction-emux.onrender.com/

## Project Poster

<img width="1054" height="1492" alt="project-poster" src="https://github.com/user-attachments/assets/39d0fa72-d3f5-4bf9-a51b-152a97da9eed" />



## ✨ Features

- Responsive, animated, glassmorphism UI with light/dark mode
- Sticky navbar, smooth scrolling, hover and gradient animations
- 5 pages: Home, Prediction, About, Contact (+ Result view)
- Client-side form validation (numbers, ranges, required fields)
- Loading animation while the model runs
- Prediction results with:
  - Predicted price
  - Confidence score
  - Price category (Affordable / Medium / Luxury)
  - Pie chart (category distribution) and bar chart (price range) via Chart.js
- Prediction history saved locally (LocalStorage) — no backend DB required
- Download result as CSV, save as PDF (via print), print, and share
- Toast notifications and reset button
- Trained and compared 3 ML models: Linear Regression, Decision Tree, Random Forest
- Model evaluation with MAE, MSE, RMSE, and R² Score
- Clean, GitHub-ready project structure, ready to deploy on Render/Railway

---

## 🖼️ Screenshots

> Add your own screenshots to the `screenshots/` folder and reference them here, e.g.:
>
> `screenshots/home.png`, `screenshots/prediction.png`, `screenshots/result.png`

---

## 🧰 Tech Stack

| Layer          | Technology                                   |
|----------------|-----------------------------------------------|
| Frontend       | HTML5, CSS3, Vanilla JavaScript, Chart.js     |
| Backend        | Python, Flask                                 |
| Machine Learning | Scikit-Learn, Pandas, NumPy, Pickle         |
| Deployment     | GitHub, Render, Railway                        |

---

## 📁 Folder Structure

```
House-Price-Prediction/
│
├── app.py                  # Flask application & routes
├── model.py                 # Loads trained model & runs predictions
├── train_model.py           # Trains & compares ML models, saves best one
├── generate_dataset.py      # (Optional) regenerates the sample dataset
├── requirements.txt         # Python dependencies
├── README.md                 # This file
├── Procfile                  # For Render/Railway (gunicorn entrypoint)
├── runtime.txt                # Python version pin
├── .gitignore
│
├── model/
│   ├── house_model.pkl       # Best trained model (pickled)
│   ├── scaler.pkl             # StandardScaler used at inference time
│   ├── encoders.pkl           # LabelEncoders for categorical fields
│   └── metadata.pkl           # Model comparison results & metadata
│
├── dataset/
│   └── House_Price_Dataset.csv   # Sample training dataset (1,200 rows)
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
├── templates/
│   ├── base.html             # Shared layout (navbar, footer, scripts)
│   ├── index.html             # Home page
│   ├── about.html             # About / ML explanation page
│   ├── prediction.html        # Prediction form page
│   ├── result.html            # Prediction result page
│   └── contact.html           # Contact page
│
└── screenshots/
```

---

## ⚙️ Installation & How to Run (Local / VS Code)

### 1. Clone or download the project
```bash
git clone https://github.com/<your-username>/House-Price-Prediction.git
cd House-Price-Prediction
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the model (already included, but you can retrain anytime)
```bash
python train_model.py
```
This reads `dataset/House_Price_Dataset.csv`, trains Linear Regression, Decision Tree, and Random Forest models, prints a comparison table, and saves the best model to `model/house_model.pkl` (along with the scaler and encoders).

### 5. Run the Flask app
```bash
python app.py
```

### 6. Open in your browser
```
http://127.0.0.1:5000
```

---

## 🧪 Requirements

- Python 3.10+
- pip
- A modern web browser

All Python dependencies are listed in `requirements.txt`:
```
Flask==3.0.3
scikit-learn==1.5.1
pandas==2.2.2
numpy==1.26.4
gunicorn==22.0.0
```

---

## 🔀 Flask Routes

| Route          | Method | Description                              |
|----------------|--------|--------------------------------------------|
| `/`            | GET    | Home page                                  |
| `/about`       | GET    | About page with model comparison table     |
| `/prediction`  | GET    | Prediction form                            |
| `/prediction`  | POST   | Runs the model, renders the result page    |
| `/contact`     | GET    | Contact page                               |
| `/contact`     | POST   | Handles contact form submission            |

---

## 📊 Model Evaluation

`train_model.py` evaluates every model with:

- **MAE** — Mean Absolute Error
- **MSE** — Mean Squared Error
- **RMSE** — Root Mean Squared Error
- **R² Score** — Coefficient of determination

On the included sample dataset, results look roughly like:

| Model                    | R² Score |
|---------------------------|----------|
| Linear Regression          | ~0.79    |
| Decision Tree Regressor    | ~0.95    |
| Random Forest Regressor    | ~0.97    |

The best model (highest R²) is automatically selected and saved as `model/house_model.pkl`.

> Exact numbers vary slightly run to run because of random train/test splits and model randomness.

---

## 🌐 GitHub Deployment

1. Initialize git and commit:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: House Price Prediction ML app"
   ```
2. Create a new repository on GitHub (do **not** initialize it with a README).
3. Link and push:
   ```bash
   git remote add origin https://github.com/<your-username>/House-Price-Prediction.git
   git branch -M main
   git push -u origin main
   ```

---

## 🚀 Render Deployment

1. Push your project to GitHub (see above).
2. Go to [render.com](https://render.com) and click **New → Web Service**.
3. Connect your GitHub repository.
4. Configure the service:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3
5. Click **Create Web Service** — Render will build and deploy automatically.
6. Once deployed, Render gives you a live URL like `https://house-price-prediction.onrender.com`.

---

## 🚂 Railway Deployment

1. Push your project to GitHub.
2. Go to [railway.app](https://railway.app) and click **New Project → Deploy from GitHub repo**.
3. Select your repository.
4. Railway auto-detects Python; it will use the `Procfile` (`web: gunicorn app:app`) to start the app.
5. Add a `PORT` environment variable if prompted (Railway usually sets this automatically).
6. Deploy — Railway will give you a public URL once the build finishes.

---

## 🔮 Future Scope

- Connect to a real-world housing dataset (e.g., Zillow, Kaggle housing datasets) for production-grade accuracy
- Add user authentication to save prediction history server-side
- Add map-based location picker instead of a dropdown
- Support model retraining from the UI with file upload
- Add more advanced models (XGBoost, Gradient Boosting, Neural Networks)
- Add unit tests and CI/CD pipeline

---

## 📄 License

This project is released under the **MIT License**. You are free to use, modify, and distribute it for personal or commercial projects.

---

## 🙌 Acknowledgements

Built as a learning/portfolio project to demonstrate a complete ML web app pipeline: data → training → evaluation → deployment → interactive UI.
