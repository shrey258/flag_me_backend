Flag me Backend

A FastAPI-based backend service that uses machine learning to provide personalized recommendations based on user preferences and behavior. The system employs a sophisticated approach combining content-based filtering and sentiment analysis using multiple rich datasets.

## Features

- 🎯 Smart recommendations based on multiple data sources
- 🔍 Content-based filtering with sentiment analysis
- 📊 Interactive Jupyter notebooks for ML development
- 🚀 Fast and async API endpoints
- 📝 Comprehensive input validation
- 💰 Price-aware suggestions

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
│   ├── amazon_reviews.csv # Amazon product reviews dataset
│   ├── content_based.csv  # Content-based recommendation dataset
│   ├── reviews_ratings.csv# Additional reviews dataset
│   ├── processed/        # Processed and merged datasets
│   ├── models/          # Trained model files
│   └── .gitkeep         # Ensures data directory is tracked
└── requirements.txt       # Project dependencies
```

## Prerequisites

- Python 3.8+
- Git
- pip (Python package installer)
- Virtual environment tool (venv)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/shrey258/flag_me_backend.git
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
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Access points:
   - API: `http://127.0.0.1:8000`
   - Interactive docs: `http://127.0.0.1:8000/docs`
   - Alternative docs: `http://127.0.0.1:8000/redoc`

## Machine Learning Development

### Using Jupyter Notebooks

1. Start Jupyter Notebook server:
   ```bash
   jupyter notebook
   ```
2. Navigate to the `scripts` directory
3. Available notebooks:
   - `preprocess.ipynb`: Data cleaning and preparation
   - `train_model.ipynb`: Model training and evaluation

### Dataset Requirements

Create `data/gift_data.csv` with the following structure:
```csv
name,description,preferences,price,relationship
"Smart Watch","Digital watch with fitness tracking",["technology","fitness","modern"],199.99,"friend"
```

Required columns:
- `name`: Gift name (string)
- `description`: Gift description (string)
- `preferences`: List of tags/preferences (list of strings)
- `price`: Gift price (float)
- `relationship`: Target relationship (string)

### Model Training Pipeline

1. Data Preprocessing:
   - Open `scripts/preprocess.ipynb`
   - Configure data loading parameters
   - Run all cells to process the data

2. Model Training:
   - Open `scripts/train_model.ipynb`
   - Adjust model parameters if needed
   - Run all cells to train and save the model

## Datasets

The recommendation system uses three primary datasets:

### 1. Amazon Product Reviews Dataset
- Contains 43,729 product reviews from Amazon.com
- Time period: Jan 2020 - Mar 2020
- Key features:
  - Product ratings and reviews
  - Brand and category information
  - User verification status
  - Review helpfulness metrics
  - Manufacturer responses

### 2. Content-based Recommendation Dataset
- Features for building content-based filtering
- Key attributes:
  - Click-through rates
  - Purchase history
  - Average ratings
  - Gender demographics
  - Price information
  - Brand data
  - Sentiment scores
  - Seasonal factors
  - Geographic data

### 3. Reviews and Ratings Dataset
- Customer reviews from a European toy store
- Focused on sentiment analysis and text mining
- Contains product-specific feedback

## Data Preprocessing Pipeline

### 1. Data Cleaning
- Remove duplicate entries
- Handle missing values
- Standardize text fields
- Normalize price ranges
- Convert timestamps to consistent format

### 2. Feature Engineering
- Extract sentiment scores from review text
- Generate product embeddings
- Create category hierarchies
- Compute user-product interaction metrics
- Normalize numerical features

### 3. Dataset Integration
- Merge relevant features from all datasets
- Create unified product representations
- Build comprehensive user profiles
- Generate final training dataset with structure:
  ```csv
  name,description,preferences,price,relationship
  "Product Name","Detailed Description",["tag1","tag2"],price_value,"relationship_type"
  ```

### 4. Quality Assurance
- Validate data consistency
- Check for data leakage
- Ensure proper feature scaling
- Verify category mappings

## API Documentation

### POST `/recommendations`

Get personalized gift recommendations.

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
        {
            "name": "Wireless Gaming Mouse",
            "description": "High-precision gaming mouse",
            "price": 49.99
        }
    ]
}
```

## Development Guidelines

- Follow PEP 8 style guide for Python code
- Use type hints for better code clarity
- Add docstrings to functions and classes
- Write unit tests for new features
- Keep notebooks clean and well-documented

## Error Handling

The API implements comprehensive error handling:
- Invalid input validation
- Model not found/initialized
- Internal processing errors
- Budget constraint violations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the web framework
- scikit-learn for ML capabilities
- Jupyter for interactive development