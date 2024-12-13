# RedBus Route Scraper and Analysis Project

## Project Overview
This project is a comprehensive web scraping and data analysis application for bus routes, utilizing Selenium for web scraping, PyMySQL for database management, and Streamlit for creating an interactive web interface.

## Technology Stack
- **Web Scraping**: Selenium
- **Database**: MySQL (PyMySQL)
- **Web Interface**: Streamlit
- **Data Handling**: Pandas

## Features
- 🚌 Automated bus route scraping from RedBus
- 📊 Data extraction including:
  - Bus Name
  - Bus Type
  - Departing Time
  - Arriving Time
  - Duration
  - Seat Availability
  - Price
- 💾 Data storage in MySQL database
- 🔍 Interactive Streamlit dashboard with advanced filtering:
  - Source and Destination selection
  - Multiple bus type filters
  - Duration-based filtering
  - Star rating selection

## Prerequisites
- Python 3.8+
- Chrome WebDriver
- MySQL Server
- Required Python libraries:
  - selenium
  - pandas
  - pymysql
  - streamlit

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/redbus-route-scraper.git
cd redbus-route-scraper
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
- Ensure MySQL is installed and running
- Create database and configure connection in `config.py`
```sql
CREATE DATABASE redbus;
USE redbus;
```

### 5. WebDriver Setup
- Download Chrome WebDriver compatible with your Chrome version
- Add WebDriver path to system PATH or specify in script

## Project Structure
```
redbus-route-scraper/
│
├── scraper.py         # Selenium web scraping script
├── database.py        # MySQL database connection and data insertion
├── app.py             # Streamlit dashboard
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Running the Project

### 1. Web Scraping
```bash
python scraper.py
```

### 2. Database Import
```bash
python database.py
```

### 3. Streamlit Dashboard
```bash
streamlit run app.py
```

## Configuration
Modify `config.py` to set:
- Web scraping parameters
- Database connection details
- Streamlit dashboard configurations

## Challenges and Learning
- Handling dynamic web content with Selenium
- Efficient data extraction and transformation
- MySQL data insertion using pandas
- Creating interactive Streamlit filters

## Future Improvements
- [ ] Add error handling for web scraping
- [ ] Implement caching mechanism
- [ ] Create more advanced visualizations
- [ ] Support multiple bus websites

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## Contact
Your Name - krebinfernart@gmail.com

Project Link: [https://github.com/yourusername/redbus-route-scraper](https://github.com/REBINFERNART/REBIN_RED_BUS/tree/main/SRC)
