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

- Python 3.8+ (for local installation)
- SQL Server (for database functionality)
- Virtual environment (recommended for local installation)

**OR**

- Docker and Docker Compose (recommended for easy setup)

## Installation

### Option 1: Docker Installation (Recommended)

Docker provides the easiest way to run the application with all dependencies pre-configured, including SQL Server.

1. **Install Docker and Docker Compose**
   - Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Ensure Docker is running

2. **Clone or download the repository**
   ```bash
   cd c:\Users\JBS LAB\Desktop\ALL_PROJECTS\ofo_database
   ```

3. **Configure environment variables**
   ```bash
   # Copy the example environment file
   copy .env.example .env
   
   # Edit .env file with your configuration
   # Update DB_PASSWORD and SECRET_KEY for security
   ```

4. **Build and start the containers**
   ```bash
   docker-compose up -d
   ```

5. **Initialize the database** (first time only)
   ```bash
   # Wait for SQL Server to be ready (about 30 seconds)
   # Then run your SQL initialization scripts
   docker exec -it ofo_sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourStrong@Passw0rd -i /docker-entrypoint-initdb.d/script.sql
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

7. **View logs**
   ```bash
   # View all logs
   docker-compose logs -f
   
   # View specific service logs
   docker-compose logs -f web
   docker-compose logs -f sqlserver
   ```

8. **Stop the containers**
   ```bash
   docker-compose down
   ```

9. **Stop and remove all data** (including database)
   ```bash
   docker-compose down -v
   ```

### Option 2: Local Installation

For local development without Docker:

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

### Docker Configuration

When using Docker, configure the application through environment variables in the `.env` file:

```env
# Database Configuration
DB_SERVER=sqlserver
DB_NAME=ofo_db
DB_USER=sa
DB_PASSWORD=YourStrong@Passw0rd

# FlUsing Docker

1. **Start the application**:
   ```bash
   docker-compose up -d
   ```

2. **Access the web interface**:
   ```
   http://localhost:5000
   ```

3. **Check container status**:
   ```bash
   docker-compose ps
   ```

4. **Access the database directly**:
   ```bash
   docker exec -it ofo_sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourStrong@Passw0rd
   ```

### Running Locally
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Application Settings
HOST=0.0.0.0
PORT=5000
DEBUG=False
```

**Security Note**: Change the default `DB_PASSWORD` and `SECRET_KEY` before deploying to production!

### Local Configuration

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

### Docker-Specific Issues

1. **Container won't start**
   ```bash
   # Check container logs
   docker-compose logs web
   docker-compose logs sqlserver
   
   # Restart containers
   docker-compose restart
   ```

2. **Port already in use**
   - Change the port mapping in `docker-compose.yml`:
   ```yaml
   ports:
     - "8080:5000"  # Use port 8080 instead of 5000
   ```

3. **Database connection failed**
   - Wait 30-60 seconds for SQL Server to fully initialize
   - Check SQL Server container is healthy: `docker-compose ps`
   - Verify environment variables in `.env` file
   - Check logs: `docker-compose logs sqlserver`

4. **Model files not found in container**
   - Ensure `.pkl` and `.csv` files are in the project directory
   - Rebuild the image: `docker-compose build --no-cache`

5. **Permission denied errors**
   ```bash
   # Fix file permissions (Linux/Mac)
   chmod -R 755 .
   
   # On Windows, run Docker Desktop as administrator
   ```

### Common Issues (Local Installation)

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

## Docker Commands Reference

### Basic Commands
```bash
# Build and start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild images
docker-compose build

# Remove everything including volumes
docker-compose down -v
```

### Container Management
```bash
# List running containers
docker ps

# Execute command in container
docker exec -it ofo_database_app /bin/bash

# View container logs
docker logs ofo_database_app

# Inspect container
docker inspect ofo_database_app
```

### Database Management
```bash
# Connect to SQL Server
docker exec -it ofo_sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourStrong@Passw0rd

# Backup database
docker exec -it ofo_sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourStrong@Passw0rd -Q "BACKUP DATABASE ofo_db TO DISK='/var/opt/mssql/backup/ofo_db.bak'"

# Copy backup from container
docker cp ofo_sqlserver:/var/opt/mssql/backup/ofo_db.bak ./backup/
```

## Deployment

### Production Deployment with Docker

1. **Update environment variables for production**:
   - Set strong passwords
   - Set `FLASK_ENV=production`
   - Set `DEBUG=False`
   - Use a strong `SECRET_KEY`

2. **Use Docker Compose with production overrides**:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

3. **Setup reverse proxy** (nginx/traefik) for HTTPS

4. **Enable container auto-restart**:
   - Already configured with `restart: unless-stopped`

5. **Setup monitoring and logging**:
   - Use Docker logging drivers
   - Implement health checks (already included)

## Performance Optimization

### Docker Performance Tips

1. **Use volumes for persistent data**:
   - Database data is stored in named volumes
   - Survives container restarts

2. **Optimize image size**:
   - Uses `python:3.11-slim` base image
   - Multi-stage builds can further reduce size

3. **Resource limits** (add to docker-compose.yml):
   ```yaml
   services:
     web:
       deploy:
         resources:
           limits:
             cpus: '1'
             memory: 1G
   ```

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
