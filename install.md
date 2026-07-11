**You should change the content of this file. Please use all second-level headings.**

# Installation Guide

## Prerequisites

You will need:
* Docker

## Installation Steps


## 1. Download the datasets

Download the required dataset files using the link provided in:

[`data/DataSets.txt`](data/DataSets.txt)

Copy the downloaded `.parquet` files into the project's [`data/`](/data) directory.


## 2. Install Python dependencies

Create a virtual environment and install the required packages:

```bash
cd api

python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

---

## 3. Train the offline recommendation models

Run:

```bash
python api/ml/train_content_based.py
python api/ml/train_item_cf.py
```

The scripts will generate the required model files under the `models/` directory.

> **Note:** This step only needs to be performed once (or whenever the datasets change).

---

## 3. Install dependencies

### Using Docker (Recommended)

1. Make sure Docker Desktop is running.
2. Run:

**Windows**
```bash
start.bat
```

**macOS / Linux**
```bash
chmod +x start.sh      # first time only
./start.sh
```

The first startup may take about 30 seconds while Docker builds the containers.

---

### Without Docker

```bash
cd api

python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

---

## 4. Run the application

### Without Docker

```bash
python -m uvicorn api.main:app --reload
```

Then start the frontend:

```bash
cd frontend
npm install
npm run dev
```

---

### With Docker

Running `start.bat` (Windows) or `./start.sh` (macOS/Linux) starts both the backend and frontend automatically.
