# SE CHATBOT - DETAILED SETUP & IMPLEMENTATION GUIDE

## PROJECT OVERVIEW

This is a Structured-Answer Chatbot for Software Engineering education designed for your university.

**What it includes:**
✓ 50 database questions (10 per unit from your syllabus)
✓ Beautiful PyQt5 GUI with chat history
✓ Smart database search with keyword matching
✓ Copy-to-clipboard functionality for answers
✓ Persistent chat history saved to JSON file
✓ Unit-based filtering and organization

---

## STEP-BY-STEP SETUP

### STEP 1: Install Required Software

**A. Python 3.7+ (if not already installed)**
- Download from: https://www.python.org/downloads/
- During installation, CHECK: "Add Python to PATH"
- Verify: Open Command Prompt/Terminal and type:
  ```
  python --version
  ```
  Should show Python 3.x.x

**B. MySQL Server (if not already installed)**
- Download from: https://dev.mysql.com/downloads/mysql/
- Run installer and complete setup
- Remember your root password (used in Step 2)
- Windows: MySQL Command Line Client will be available
- Verify: Open MySQL Command Line and it should connect

---

### STEP 2: Prepare Project Files

1. Create a folder: `C:\Users\YourName\se_chatbot` (Windows)
   or `~/se_chatbot` (Mac/Linux)

2. Place these files in the folder:
   - `se_chatbot_db.sql`
   - `database_helper.py`
   - `chatbot_gui.py`
   - `requirements.txt`
   - `README.md`

3. Verify all files are present

---

### STEP 3: Install Python Dependencies

**Windows:**
1. Open Command Prompt
2. Navigate to your project folder:
   ```
   cd C:\Users\YourName\se_chatbot
   ```
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
4. Wait for installation to complete

**Mac/Linux:**
1. Open Terminal
2. Navigate to project:
   ```
   cd ~/se_chatbot
   ```
3. Install requirements:
   ```
   pip3 install -r requirements.txt
   ```

---

### STEP 4: Set Up Database

**Windows:**
1. Open MySQL Command Line Client (search in Start Menu)
2. Enter your root password when prompted
3. Run these commands:

```sql
-- Create database
CREATE DATABASE se_chatbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE se_chatbot_db;

-- Create table
CREATE TABLE questions_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    unit_id INT NOT NULL,
    unit_name VARCHAR(255) NOT NULL,
    question_keyword VARCHAR(255) NOT NULL,
    question_title VARCHAR(500) NOT NULL,
    definition LONGTEXT NOT NULL,
    explanation LONGTEXT NOT NULL,
    example LONGTEXT NOT NULL,
    conclusion LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_unit_id (unit_id),
    INDEX idx_keyword (question_keyword),
    FULLTEXT INDEX ft_question (question_title, question_keyword)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Verify table creation
SHOW TABLES;
```

**Alternative Method (Using SQL File):**
1. In MySQL Command Line:
```sql
source C:\path\to\se_chatbot_db.sql
-- or on Mac/Linux:
source ~/se_chatbot/se_chatbot_db.sql
```

---

### STEP 5: Insert Q&A Data

The `se_chatbot_db.sql` file contains 50 INSERT statements that populate the database.

**Option A: Import using Command Line**
```bash
mysql -u root -p se_chatbot_db < se_chatbot_db.sql
```
(Enter password when prompted)

**Option B: Import using MySQL Workbench**
1. Open MySQL Workbench
2. File → Open SQL Script
3. Select `se_chatbot_db.sql`
4. Execute the script (Ctrl+Shift+Enter)

**Option C: Manual Import**
1. Open `se_chatbot_db.sql` with any text editor
2. Copy all INSERT statements
3. In MySQL Command Line, paste and execute

---

### STEP 6: Verify Database Setup

**In MySQL Command Line:**

```sql
USE se_chatbot_db;

-- Check total questions
SELECT COUNT(*) as total_questions FROM questions_answers;
-- Should show: 50

-- Check distribution by unit
SELECT unit_id, unit_name, COUNT(*) as count 
FROM questions_answers 
GROUP BY unit_id, unit_name 
ORDER BY unit_id;

-- Should show:
-- Unit 1: 10 questions
-- Unit 2: 10 questions
-- Unit 3: 10 questions
-- Unit 4: 10 questions
-- Unit 5: 10 questions

-- Test a sample question
SELECT question_title, definition FROM questions_answers 
WHERE question_keyword LIKE '%agile%' LIMIT 1;
```

If all counts are correct, database setup is complete! ✓

---

### STEP 7: Run the Chatbot

**From Command Prompt/Terminal:**

Navigate to your project folder and run:

```bash
python chatbot_gui.py
```

**Expected Result:**
- A window titled "SE Chatbot - Software Engineering Q&A Assistant" opens
- Welcome message displays with instructions
- Input box ready for questions

---

## USING THE CHATBOT

### Basic Usage

1. **Ask a Question**
   - Type in the input box: "What is software engineering?"
   - Press Enter or click "Ask"
   - Answer appears with full structure

2. **Copy an Answer**
   - Click the "📋 Copy Answer" button below any answer
   - Answer is copied to clipboard
   - Paste anywhere (Word, Notes, etc.)

3. **View Chat History**
   - Click "📜 View History" button
   - See timestamps and recent questions
   - History saved automatically to `chat_history.json`

4. **Filter by Unit**
   - Use dropdown menu: "Filter by Unit"
   - Shows questions from specific units
   - Helps organize studying by topic

5. **Clear Chat**
   - Click "🗑️ Clear" to clear current display
   - Doesn't delete saved history

### Example Questions to Try

✓ "What is software engineering?"
✓ "Tell me about agile development"
✓ "Explain UML diagrams"
✓ "What is test-driven development?"
✓ "How does refactoring work?"
✓ "What are design patterns?"
✓ "Explain microservices architecture"

---

## FILE DESCRIPTIONS

| File | Purpose |
|------|---------|
| `se_chatbot_db.sql` | Database schema + 50 Q&A entries |
| `database_helper.py` | Database operations, search, history management |
| `chatbot_gui.py` | PyQt5 GUI, user interface, message display |
| `requirements.txt` | Python packages to install |
| `README.md` | Quick reference guide |
| `chat_history.json` | Auto-generated file storing chat history |

---

## DATABASE SCHEMA EXPLANATION

**Table: questions_answers**

```
├── id (Primary Key)
│   └─ Unique identifier for each Q&A entry
│
├── unit_id (1-5)
│   └─ Which unit the question belongs to
│
├── unit_name
│   └─ Full name of the unit (e.g., "Agile Development")
│
├── question_keyword
│   └─ Keywords for searching (e.g., "agile", "methodology")
│   └─ Used by search algorithm
│
├── question_title
│   └─ The actual question (e.g., "What is agile?")
│
├── definition (LONGTEXT)
│   └─ Brief definition (50-75 words)
│
├── explanation (LONGTEXT)
│   └─ Detailed explanation (150-200 words)
│   └─ Key concepts and context
│
├── example (LONGTEXT)
│   └─ Real-world or practical example (75-100 words)
│
├── conclusion (LONGTEXT)
│   └─ Summary and key takeaway (50-75 words)
│
└── Indexes
    ├─ idx_unit_id: Fast lookup by unit
    ├─ idx_keyword: Fast lookup by keyword
    └─ ft_question: FULLTEXT index for text search
```

---

## SEARCH ALGORITHM

The chatbot uses a two-tier search strategy:

**TIER 1: FULLTEXT Search**
- Uses MySQL FULLTEXT search on question_title and question_keyword
- Extracts keywords from user question
- Scores matches by relevance
- Fast and accurate for exact topic matches

**TIER 2: LIKE Pattern Matching**
- Falls back if FULLTEXT finds nothing
- Uses LIKE %keyword% matching
- Catches variations in phrasing
- Ensures users get answers for rephrased questions

**Example:**
- User asks: "Tell me about testing"
- Searches for FULLTEXT match on "testing"
- Finds: "What is software testing?"
- Displays full structured answer

---

## TROUBLESHOOTING

### Problem: "Database connection error"
**Solution:**
1. Verify MySQL is running (Windows: Services > MySQL57)
2. Verify credentials in `database_helper.py` line 16:
   ```python
   password="Forgot@1234"  # Change if your password is different
   ```
3. Verify database exists: `SHOW DATABASES;` in MySQL
4. Restart MySQL service

### Problem: "No module named 'PyQt5'"
**Solution:**
```bash
pip install PyQt5
```

### Problem: "No module named 'mysql'"
**Solution:**
```bash
pip install mysql-connector-python
```

### Problem: "Answer not found for any question"
**Check:**
1. Run: `SELECT COUNT(*) FROM questions_answers;`
2. Should show 50
3. If 0, re-run INSERT statements from `se_chatbot_db.sql`

### Problem: Chat history not saving
**Solution:**
1. Verify folder permissions are writable
2. Check for `chat_history.json` file in project folder
3. Delete old `chat_history.json` and restart

---

## EXTENDING THE SYSTEM

### Adding More Questions

1. Open MySQL Command Line or Workbench
2. Execute:
```sql
INSERT INTO questions_answers 
(unit_id, unit_name, question_keyword, question_title, definition, explanation, example, conclusion)
VALUES 
(1, 'Introduction to Software Engineering & Processes', 
'new_keyword', 'Your new question here?',
'Your definition (50-75 words)...',
'Your explanation (150-200 words)...',
'Your example (75-100 words)...',
'Your conclusion (50-75 words)...');
```

3. Restart chatbot to see new questions

### Creating a New Unit

1. Insert questions with new unit_id (e.g., 6)
2. Update unit_name appropriately
3. GUI will automatically detect in dropdown filter

---

## EVALUATION CHECKLIST

Before submission, verify:

✓ Database contains 50 questions (10 per unit)
✓ GUI opens without errors
✓ Questions can be asked and answers displayed
✓ Copy button works
✓ Chat history saves and displays
✓ Unit filter works
✓ Database connection stable
✓ All files properly organized
✓ README clear and comprehensive
✓ Requirements can be installed

---

## KEY FEATURES DEMONSTRATED

1. **Database Design**
   - Proper schema with indexes
   - FULLTEXT search capability
   - Normalized structure

2. **Python Programming**
   - Object-oriented design (Classes)
   - Database operations (CRUD)
   - File I/O (JSON history)
   - Error handling

3. **GUI Development**
   - PyQt5 framework usage
   - Layout management
   - Event handling
   - User-friendly interface

4. **Software Engineering Concepts**
   - Modular code (database_helper.py, chatbot_gui.py)
   - Clean architecture
   - Documentation
   - Reusability

---

## FINAL NOTES

- The system is designed for educational evaluation
- Covers all major Software Engineering topics
- Scalable design allows adding more questions
- Can be extended with additional features
- All code is well-commented and documented