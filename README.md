# MyHomeBank

A personal finance tracking application built with Flask that helps you manage your income and expenses.

## Features

- Track income and expenses
- Categorize transactions
- Generate financial reports
- Import expenses in bulk
- Need vs Want classification
- Daily average expense calculation

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/myhomebank.git
cd myhomebank
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
venv\Scripts\activate
```

4. Install the required packages:
```bash
pip install flask flask-sqlalchemy
```

## Running the Application

1. Make sure your virtual environment is activated

2. Run the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Database

The application uses SQLite as its database. The database file (`expenses.db`) will be automatically created when you first run the application.

## Usage

- Add income and expenses through the web interface
- View your transactions on the home page
- Generate reports with various statistics
- Import expenses in bulk using the import feature
- Delete transactions as needed

## Development

The application is built with:
- Flask (Web framework)
- SQLAlchemy (Database ORM)
- SQLite (Database)
- HTML/CSS (Frontend)
