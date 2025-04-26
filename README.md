# Flag Me Backend

A FastAPI-based backend service that uses Gemini AI to provide personalized gift suggestions and e-commerce product search capabilities. The system employs a sophisticated approach combining AI-generated suggestions with multi-platform e-commerce integration.

## 🚀 Features

### Gemini AI Integration
- **Gift Suggestions**: Generate personalized gift ideas based on recipient details
- **Message Generation**: Create custom messages for special occasions
- **Structured Prompts**: Carefully crafted prompts for optimal AI responses

### E-commerce Integration
- **Multi-Platform Search**: Search across Amazon, Flipkart, and Myntra
- **Affiliate Link Generation**: Automatic application of affiliate tags
- **Price Filtering**: Filter products by price range
- **Platform Filtering**: Search on specific platforms only

### API Endpoints
- `/gift-suggestions`: Get AI-powered gift recommendations
- `/search-products`: Search for products across e-commerce platforms
- `/generate-message`: Create personalized messages for occasions
- `/health`: Health check endpoint

## 📁 Project Structure

```
flag_me_backend/
├── app/                    # Main application directory
│   ├── main.py            # FastAPI application entry point
│   ├── routes.py          # API endpoint definitions
│   ├── ecommerce.py       # E-commerce search functionality
│   ├── gift_recommender.py # Gift recommendation service
│   ├── message_generator.py # Message generation service
│   ├── models.py          # Database models
│   └── schemas.py         # Pydantic schemas for request/response validation
├── scripts/               # Data processing scripts
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

## 🔧 Implementation Details

### 1. E-commerce Search (`ecommerce.py`)

The e-commerce search functionality provides a unified interface to search for products across multiple platforms:

#### Key Components
- **`EcommerceSearcher` Class**: Main class that handles product searches across platforms
- **Platform-Specific Search Methods**:
  - `search_amazon()`: Searches Amazon for products
  - `search_flipkart()`: Searches Flipkart for products
  - `search_myntra()`: Searches Myntra for products
- **Affiliate Link Generation**:
  - `_create_amazon_affiliate_url()`: Adds Amazon affiliate tags to URLs
  - `_create_flipkart_affiliate_url()`: Adds Flipkart affiliate tags to URLs
  - `_create_myntra_affiliate_url()`: Adds Myntra affiliate tags to URLs
- **Unified Search Method**:
  - `search_all()`: Searches all platforms with optional price and platform filtering

#### HTML Extraction Approach
- Uses BeautifulSoup for HTML parsing
- Implements multiple fallback strategies for different site layouts
- Handles mobile and desktop site variations
- Manages user agent rotation to avoid blocking

### 2. Gift Recommendation (`gift_recommender.py`)

The gift recommendation service uses Gemini AI to generate personalized gift suggestions:

#### Key Components
- **`GiftRecommender` Class**: Handles gift suggestion generation
- **Prompt Engineering**:
  - `_create_prompt()`: Creates structured prompts for Gemini based on person details
- **Response Processing**:
  - `get_gift_suggestions()`: Processes Gemini responses into structured gift suggestions

#### Prompt Design
- Includes detailed recipient information (age, gender, interests, occasion)
- Specifies budget constraints and relationship context
- Provides clear instructions for response format
- Emphasizes specificity and relevance in suggestions

### 3. Message Generation (`message_generator.py`)

The message generation service creates personalized messages for special occasions:

#### Key Components
- **`MessageGenerator` Class**: Handles personalized message generation
- **Prompt Engineering**:
  - Creates structured prompts for Gemini based on recipient details and occasion
- **Response Processing**:
  - Processes Gemini responses into formatted messages

### 4. API Endpoints (`routes.py`)

The API endpoints provide a clean interface for the frontend to access backend services:

#### Implemented Endpoints
- **`/gift-suggestions`**: Get personalized gift suggestions
- **`/search-products`**: Search for products across e-commerce platforms
- **`/generate-message`**: Create personalized messages for occasions
- **`/health`**: Health check endpoint

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

## 📊 Technical Implementation

### HTML Extraction Strategy

The system uses a multi-layered approach to extract product information from e-commerce sites:

1. **Request Handling**:
   - Uses random user agents to avoid detection
   - Implements proper headers and cookies
   - Handles redirects and mobile site detection

2. **HTML Parsing**:
   - Uses BeautifulSoup for structured parsing
   - Implements multiple selector patterns for each site
   - Handles different HTML structures between mobile and desktop sites

3. **Data Extraction**:
   - Extracts product titles, prices, URLs, and images
   - Implements fallback mechanisms for missing data
   - Handles currency formatting and price parsing

4. **Affiliate Link Generation**:
   - Automatically applies affiliate tags to product URLs
   - Preserves existing URL parameters
   - Handles different affiliate link formats per platform

### Gemini AI Integration

The system leverages Google's Gemini AI for intelligent gift recommendations and message generation:

1. **Prompt Engineering**:
   - Creates detailed, structured prompts for optimal results
   - Includes specific instructions for output format
   - Provides context about the recipient and occasion

2. **Response Processing**:
   - Parses and cleans AI-generated responses
   - Handles formatting inconsistencies
   - Implements fallbacks for unexpected responses

3. **Error Handling**:
   - Manages API rate limits and quotas
   - Provides meaningful error messages
   - Logs detailed information for debugging

### Running Tests
```bash
# Unit tests
pytest tests/

# Coverage report
pytest --cov=app tests/
```

## 📚 Dependencies

Key libraries:
- **FastAPI**: Web framework for building APIs
- **Google Generative AI**: Client for Gemini AI
- **BeautifulSoup4**: HTML parsing and extraction
- **httpx**: Asynchronous HTTP client
- **Pydantic**: Data validation and settings management
- **python-dotenv**: Environment variable management

## 🔍 Common Issues and Solutions

### HTML Extraction
- **Issue**: WebView might not fully load before extraction
- **Solution**: Implement proper loading detection and wait mechanisms

### Gemini API
- **Issue**: Gemini sometimes returns null values for product fields
- **Solution**: Implement fallback mechanisms and validation

### E-commerce Sites
- **Issue**: Mobile site HTML structure differs from desktop sites
- **Solution**: Implement separate parsers for mobile and desktop versions

### Error Handling
- **Issue**: Error messages sometimes appear as product titles
- **Solution**: Implement validation to detect and filter error messages

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🛠️ API Reference

### 1. Gift Suggestions Endpoint

```http
POST /gift-suggestions
Content-Type: application/json

{
  "person_details": {
    "age": 28,
    "gender": "female",
    "interests": ["photography", "hiking", "cooking"],
    "occasion": "birthday",
    "relationship": "friend",
    "min_budget": 2000,
    "max_budget": 5000,
    "platforms": ["Amazon", "Flipkart"],
    "additional_notes": "She recently started a food blog"
  }
}
```

Response:
```json
{
  "gift_suggestions": [
    "Portable Ring Light",
    "Cooking Masterclass Subscription",
    "Hiking Daypack",
    "Food Photography Props Set",
    "Compact Tripod"
  ]
}
```

### 2. Product Search Endpoint

```http
POST /search-products
Content-Type: application/json

{
  "query": "portable ring light",
  "min_price": 1500,
  "max_price": 3000,
  "platforms": ["Amazon", "Flipkart"]
}
```

Response:
```json
{
  "products": [
    {
      "title": "10-inch Ring Light with Tripod Stand",
      "price": 1999.0,
      "url": "https://www.amazon.in/dp/B08GC3...",
      "platform": "Amazon",
      "image_url": "https://m.media-amazon.com/images/I/71..."
    },
    {
      "title": "Selfie Ring Light with Phone Holder",
      "price": 2499.0,
      "url": "https://www.flipkart.com/selfie-ring-light/p/itm...",
      "platform": "Flipkart",
      "image_url": "https://rukminim2.flixcart.com/image/416/..."
    }
  ]
}
```

### 3. Message Generation Endpoint

```http
POST /generate-message
Content-Type: application/json

{
  "name": "Priya",
  "age": 28,
  "occasion": "birthday",
  "gender": "female",
  "relationship": "friend",
  "length": "medium"
}
```

Response:
```json
{
  "message": "Happy Birthday, Priya! Another year of amazing adventures, laughter, and memories. May this new chapter of your life bring you all the joy and success you deserve. Here's to celebrating you today and always! Cheers to 28!"
}
```

## ⚙️ Environment Setup

1. Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key
AMAZON_AFFILIATE_TAG=your-tag-21
FLIPKART_AFFILIATE_TAG=your-flipkart-tag
MYNTRA_AFFILIATE_TAG=your-myntra-tag
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
uvicorn app.main:app --reload
```

4. Access the API documentation:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`