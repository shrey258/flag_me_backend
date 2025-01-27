# Flag Me Backend

A FastAPI-based backend service that uses machine learning to provide personalized recommendations based on user preferences and behavior. The system employs a sophisticated approach combining content-based filtering and sentiment analysis using multiple rich datasets.

## 🚀 Current Development Status

### Completed Features
✅ Data Preprocessing Pipeline
- Implemented robust data cleaning
- Added sentiment analysis
- Created feature engineering pipeline
- Generated final processed dataset

✅ Product Search & Affiliate Integration
- Real-time product search across e-commerce platforms
- Amazon affiliate link integration
- Price comparison and sorting
- Deduplication of similar products
- Automatic affiliate tag application

### In Progress
🔄 Recommendation Model Development
- Setting up model architecture
- Implementing content-based filtering
- Planning collaborative filtering integration

### Pending
⏳ Additional Platform Integration
- Flipkart affiliate integration
- Other e-commerce platforms

## 🎯 Features

- 🎯 Smart recommendations based on multiple data sources
- 🔍 Content-based filtering with sentiment analysis
- 📊 Interactive Jupyter notebooks for ML development
- 🚀 Fast and async API endpoints
- 📝 Comprehensive input validation
- 💰 Price-aware suggestions
- 🔎 Real-time product search with affiliate links

## 📁 Project Structure

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
│   ├── amazon_com-product_reviews_sample.csv  # Amazon product reviews
│   ├── content_based_recommendation_dataset.csv # Product features
│   ├── review_and_ratings.csv                  # Additional reviews
│   ├── processed/        # Processed datasets
│   │   ├── processed_amazon.csv      # Cleaned Amazon reviews
│   │   ├── processed_content.csv     # Normalized product features
│   │   └── processed_data.csv        # Final merged dataset
│   └── models/          # Trained model files
└── requirements.txt       # Project dependencies
```

## 🔧 Development Progress

### 1. Data Preprocessing (Completed)
The preprocessing pipeline (`scripts/preprocess.ipynb`) handles:

#### Input Datasets
- Amazon Reviews: Product reviews and ratings
- Content-based: Product features and specifications
- Reviews & Ratings: Additional user feedback

#### Processing Steps Implemented
1. **Text Processing**
   - Cleaned descriptions and reviews
   - Applied sentiment analysis using TextBlob
   - Standardized text format
   - Removed noise and special characters

2. **Feature Engineering**
   - Generated sentiment scores
   - Combined product identifiers
   - Created multi-dimensional preference tags
   - Normalized numerical features
   - Implemented dynamic column handling

3. **Data Quality**
   - Comprehensive error handling
   - Missing value treatment
   - Safe data transformations
   - Type validation and conversion

#### Output Dataset Structure
The final processed dataset (`data/processed/processed_data.csv`) contains:

| Column | Description | Example |
|--------|-------------|---------|
| name | Product identifier | "Schmidt's Deodorant - Beauty & Personal Care" |
| description | Cleaned product text | "natural deodorant with innovative ingredients..." |
| preferences | Category tags | ["beauty & personal care", "personal care", "positive"] |
| price | Normalized value | 0.0615539858728557 |
| relationship | Category relation | "general" |

### 2. Recommendation Model (In Progress)
Working on implementing:
- Content-based filtering using processed features
- Sentiment-aware recommendation logic
- Price and category relationship handling

### 3. API Development (Pending)
Planning to create:
- Product recommendation endpoints
- User preference management
- Search functionality
- Input validation schemas

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- pip (Python package installer)
- Virtual environment tool (venv)

### Setup Instructions

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

### Running the Backend

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
2. Access:
   - API: `http://127.0.0.1:8000`
   - Swagger docs: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## 📊 Development Workflow

### 1. Data Processing
- Use `scripts/preprocess.ipynb`
- Run cells sequentially
- Check output quality
- Monitor for warnings/errors

### 2. Model Development
- Work in `scripts/train_model.ipynb`
- Test different approaches
- Evaluate performance
- Save best models

### 3. API Development
- Implement endpoints in `app/routes.py`
- Define schemas in `app/schemas.py`
- Add model integration in `app/models.py`
- Test endpoints thoroughly

## 🧪 Testing

### Current Coverage
✅ Data preprocessing functions
⏳ Model evaluation (planned)
⏳ API endpoints (planned)

### Running Tests
```bash
# Unit tests
pytest tests/

# Coverage report
pytest --cov=app tests/
```

## 📚 Dependencies

Key libraries:
- FastAPI: Web framework
- Pandas: Data manipulation
- TextBlob: Sentiment analysis
- Scikit-learn: Machine learning
- NumPy: Numerical operations
- Jupyter: Interactive development

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions
- Include unit tests
- Update documentation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🛠️ New Features

### Product Search with Affiliate Links
The backend now supports real-time product search with automatic affiliate link generation. This feature allows you to:
- Search for products across e-commerce platforms
- Get detailed product information including prices, ratings, and images
- Generate affiliate links automatically
- Sort and deduplicate results for better user experience

#### API Endpoints

1. **Product Search**
```http
POST /search-products
Content-Type: application/json

{
    "query": "gaming laptop"
}
```

Response:
```json
{
    "products": [
        {
            "title": "Product Title",
            "price": 49999.99,
            "url": "affiliate-link-url",
            "platform": "Amazon",
            "image_url": "product-image-url"
        }
    ]
}
```

2. **Recommendations with Products**
```http
POST /recommendations
Content-Type: application/json

{
    "user_preferences": {
        "interests": ["gaming", "technology"],
        "price_range": "medium"
    }
}
```

Response includes both recommendations and matching products with affiliate links.

### Environment Setup

1. Create a `.env` file in the project root:
```env
AMAZON_AFFILIATE_TAG=your-tag-21
FLIPKART_AFFILIATE_TAG=your-flipkart-tag  # Coming soon
```

2. Install new dependencies:
```bash
pip install -r requirements.txt
```

### Testing the API

1. Using Postman:
   - Import the provided Postman collection
   - Set the environment variables
   - Test the endpoints with sample queries

2. Using the Test Script:
```bash
python test_api.py
```

3. Using Swagger UI:
   - Access `http://127.0.0.1:8000/docs`
   - Try out the endpoints interactively