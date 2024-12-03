# Gift Recommendation App Backend

A FastAPI-based backend service for gift recommendations using machine learning. The system uses a nearest neighbors approach to suggest gifts based on user preferences and relationships.

## Project Structure

```
flag_me_backend/
├── app/                    # Main application directory
│   ├── main.py            # FastAPI application entry point
│   ├── routes.py          # API endpoint definitions
│   ├── models.py          # ML model integration
│   └── schemas.py         # Data validation schemas
├── scripts/               # ML notebooks directory
│   ├── preprocess.ipynb   # Data preprocessing notebook
│   └── train_model.ipynb  # Model training notebook
├── data/                  # Data storage directory
│   └── gift_data.csv      # Gift dataset (to be added)
└── requirements.txt       # Project dependencies
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flag_me_backend.git
   cd flag_me_backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv env
   env\Scripts\activate

   # Linux/MacOS
   python -m venv env
   source env/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Backend Server

1. Ensure your virtual environment is activated
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. The API will be available at `http://127.0.0.1:8000`
4. Access the API documentation at `http://127.0.0.1:8000/docs`

## Working with ML Models

### Using Jupyter Notebooks

1. Start Jupyter Notebook server:
   ```bash
   jupyter notebook
   ```
2. Navigate to the `scripts` directory
3. Open either `preprocess.ipynb` or `train_model.ipynb`

### Training the Model

1. Prepare your gift dataset:
   - Create `data/gift_data.csv` with columns:
     - name: Gift name
     - description: Gift description
     - preferences: List of preferences/tags
     - price: Gift price
     - relationship: Target relationship

2. Run the preprocessing notebook:
   - Open `scripts/preprocess.ipynb`
   - Run all cells to preprocess the data

3. Train the model:
   - Open `scripts/train_model.ipynb`
   - Run all cells to train and save the model

### API Endpoints

#### POST `/recommendations`
Get gift recommendations based on user preferences.

Request body:
```json
{
    "relationship": "friend",
    "preferences": ["technology", "gaming", "modern"],
    "budget": 100
}
```

Response:
```json
{
    "recommendations": [
        "Gift 1",
        "Gift 2",
        "Gift 3"
    ]
}
```

## Development

- The ML code is in Jupyter notebooks for easier experimentation
- The FastAPI backend loads functions from these notebooks
- Model files are saved in the `data` directory
- Use the API documentation at `/docs` to test endpoints

## Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies