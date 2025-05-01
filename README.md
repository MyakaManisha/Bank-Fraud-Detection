# 🏦 Bank Fraud Detection

A desktop-based banking application built using **Python (PyQt5)**, **SQLite**, and **Machine Learning** to simulate real-time banking operations such as login, registration, deposit, transfer, and fraud detection.

![Bank UI Screenshot](bank.jpg)

## 🚀 Features

- ✅ **User Registration & Login**
- 💰 **Balance Inquiry, Deposit & Fund Transfer**
- 🔐 **Fraud Detection using Machine Learning (scikit-learn)**
- 📉 **Transaction Logging**
- 🖼️ Intuitive GUI using PyQt5 with animated effects
- 🗃️ SQLite as backend database

## 📂 Project Structure

bash
.
├── BankNH.db                  # SQLite database
├── fraud_detection_model.pkl  # Pre-trained fraud detection model
├── demo.py                    # Database query/test script
├── MainLogin.py               # Main login interface
├── Mainprofile.py             # User profile dashboard
├── registrationNew.py         # Registration interface
├── Transfer.py                # Funds transfer interface (includes fraud check)
├── bank.jpg                   # UI background image
```

## 🧠 Fraud Detection Model

A pre-trained ML model (`fraud_detection_model.pkl`) is integrated to detect fraudulent transactions based on:

- Transaction type (CASH_OUT / TRANSFER)
- Amount
- Sender & Receiver balance info (before and after transaction)

The model uses `scikit-learn` pipelines and was trained on synthetic financial datasets.

## 🛠️ Requirements

Install dependencies with:

```bash
pip install PyQt5 pandas scikit-learn joblib
```

## 🏁 Getting Started

1. **Clone the repo**
2. Ensure `BankNH.db` and `fraud_detection_model.pkl` are in the same directory.
3. Run the application using:

```bash
python MainLogin.py
```

## 📸 Screenshots

| Login Page | Dashboard | Transfer |
|------------|-----------|----------|
| ![Login](bank.jpg) | ![Profile](bank.jpg) | ![Transfer](bank.jpg) |

*(Replace with actual screenshots if needed.)*

## 📌 Notes

- Passwords are stored as plain integers (for demo purposes). Use hashing in production.
- Make sure the database (`BankNH.db`) exists before using the application.
- Fraud detection is invoked during fund transfer only.

## 📃 License

This project is for educational/demo purposes. Use it responsibly.
