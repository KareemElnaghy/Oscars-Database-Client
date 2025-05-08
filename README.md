
# 🎬 OscarDB – Oscars Database Client

**OscarDB** is a comprehensive database application that catalogs Academy Awards (Oscars) information — including movies, nominations, winners, and people involved in the film industry. The application features an intuitive graphical user interface (GUI) for exploring Oscar data, adding nominations, and viewing statistics about winners and nominees.

---

## Development Process

### 1. Database Design
- Created an Entity-Relationship Diagram (ERD) to model relationships between movies, people, nominations, and other entities  
- Developed a relational schema with tables for:
  - Movies
  - People
  - Nominations
  - Roles
  - Production companies
  - Users  
- Enforced data integrity using primary keys, foreign keys, and constraints

### 2. Data Collection
- Built Python web crawlers to scrape Oscar data from Wikipedia
- Created category-specific scripts for scraping:
  - Movies
  - Nominees
  - Oscar categories  
- Cleaned and processed scraped data for consistency and accuracy

### 3. Database Implementation
- Created a MySQL database with all required tables
- Implemented appropriate foreign key constraints with `ON DELETE` and `ON UPDATE` actions
- Populated the database using cleaned data from scraping

### 4. Client Application Development
- Developed a Python GUI application using **Tkinter**
- Applied a **three-tier architecture**: UI, business logic, and database access
- Designed a modern, responsive dark-themed interface for enhanced usability

---

## Features

- **User Management**: Register and log in with user accounts  
- **Nomination Management**: Add/view user-specific nominations  
- **Statistical Analysis**:
  - View top nominated movies by category or year  
  - Display stats for staff members (directors, actors, etc.)  
  - Top 5 birth countries of Best Actor winners  
  - List nominees from a specific country  
  - Top 5 Oscar-winning production companies  
  - Non-English Oscar-winning movies  
- **Dream Team**: Shows the highest-awarded living cast members in their respective roles  

---

## 📁 Project Structure

```
OscarDB/
├── main.py              # Main application (UI and event handling)
├── database.py          # Database connection and query functions
├── SQL/                 # SQL scripts for DB creation and seeding
├── scripts/             # Web scraping scripts (Python)
└── CSV/                 # Scraped and cleaned data in CSV format
```

---

## 💻 Technologies Used

- **Python**
- **Tkinter (GUI)**
- **MySQL (Database)**
