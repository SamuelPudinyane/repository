# OFO Database - Job Title Matching System

A Flask-based web application that uses TF-IDF (Term Frequency-Inverse Document Frequency) for intelligent job title matching and occupation classification. The system helps match user-input job titles with standardized occupational codes and provides similar job title suggestions.

## Features

- **Intelligent Job Title Matching**: Uses TF-IDF vectorization and cosine similarity to find matching job titles
- **Autocomplete Suggestions**: Real-time search suggestions as users type
- **Abbreviation Support**: Handles abbreviated job titles for shorter queries
- **Database Integration**: SQL Server database integration for storing and retrieving occupation data
- **RESTful API**: JSON-based API endpoints for easy integration
- **Web Interface**: User-friendly HTML interface for searching job titles

## Project Structure

```
ofo_database/
├── app.py                      # Flask application and routes
├── model.py                    # TF-IDF model and matching logic
├── database_query.py           # Database connection and query functions
├── requirement.txt             # Python dependencies
├── job_data_with_tfidf.csv     # Job data with TF-IDF features
├── tfidf_vectorizer.pkl        # Saved TF-IDF vectorizer model
├── tfidf_matrix.pkl            # Precomputed TF-IDF matrix
├── database/
│   └── script.sql              # Database schema and initialization scripts
├── file/
│   └── matched_occupations.csv # Matched occupation reference data
├── static/
│   ├── style.css               # Application styling
│   └── images/                 # Image assets
└── templates/
    └── index.html              # Main web interface
```

## Requirements

- Python 3.8+
- SQL Server (for database functionality)
- Virtual environment (recommended)

## Installation

1. **Clone or download the repository**
   ```bash
   cd c:\Users\JBS LAB\Desktop\ALL_PROJECTS\ofo_database
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Set up the database**
   - Configure your SQL Server connection in `database_query.py`
   - Run the SQL scripts in `database/script.sql` to create necessary tables

5. **Prepare the TF-IDF models**
   - Ensure `tfidf_vectorizer.pkl` and `tfidf_matrix.pkl` are present
   - These contain the pre-trained TF-IDF model and matrix

## Configuration

Update the database connection settings in `database_query.py`:
```python
# Configure your SQL Server connection parameters
SERVER = 'your_server_name'
DATABASE = 'your_database_name'
USERNAME = 'your_username'
PASSWORD = 'your_password'
```

## Usage

### Running the Application

1. Activate the virtual environment:
   ```bash
   .venv\Scripts\Activate.ps1
   ```

2. Start the Flask server:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

### API Endpoints

#### 1. Home Page
```
GET /
```
Returns the main web interface.

#### 2. Job Title Search
```
GET /job_title/<job_title>
```
Returns matching job titles and their details based on the input.

**Example:**
```
GET /job_title/software engineer
```

**Response:**
```json
[
  {
    "job_title": "Software Engineer",
    "ofo_code": "2513",
    "similarity_score": 0.95
  }
]
```

#### 3. Autocomplete Suggestions
```
GET /suggestions?q=<query>
```
Returns job title suggestions for autocomplete functionality.

**Example:**
```
GET /suggestions?q=soft
```

## Key Technologies

- **Flask**: Web framework for Python
- **scikit-learn**: Machine learning library for TF-IDF vectorization
- **pandas**: Data manipulation and analysis
- **pypyodbc**: SQL Server database connectivity
- **joblib**: Model serialization
- **NLTK**: Natural language processing toolkit
- **gensim**: Topic modeling and document similarity

## How It Works

1. **Text Preprocessing**: User input is cleaned and normalized (lowercase, remove special characters, etc.)

2. **TF-IDF Vectorization**: The preprocessed text is transformed using the pre-trained TF-IDF vectorizer

3. **Similarity Calculation**: Cosine similarity is computed between the input vector and all job titles in the database

4. **Ranking**: Results are ranked by similarity score and the top matches are returned

5. **Database Lookup**: Matched job titles are enriched with additional data from the SQL Server database

## Development

### Project Files

- **app.py**: Main Flask application with route definitions
- **model.py**: Contains the machine learning model logic
  - `filtering()`: Main matching function for regular queries
  - `filtering_abb()`: Specialized function for abbreviated queries
  - `preprocess_text()`: Text cleaning and normalization
  - `find_similar_jobs()`: Core similarity matching algorithm

- **database_query.py**: Database interaction layer
  - `get_connection()`: Establishes database connection
  - `search_for_job_titles()`: Query job titles from database
  - `search_for_job_codes()`: Search by occupation codes

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify SQL Server is running
   - Check connection credentials in `database_query.py`
   - Ensure firewall allows SQL Server connections

2. **Model Files Not Found**
   - Ensure `tfidf_vectorizer.pkl` and `tfidf_matrix.pkl` exist
   - Re-train the model if necessary

3. **Import Errors**
   - Verify all dependencies are installed: `pip install -r requirement.txt`
   - Activate the virtual environment before running

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Contact

[Add your contact information here]

## Acknowledgments

- OFO (Organising Framework for Occupations) for occupation classification standards
- scikit-learn community for machine learning tools
