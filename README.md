# Software Engineering Chatbot

A structured-answer chatbot for Software Engineering education, built with PyQt5 and MySQL.

## Features

✨ **50+ Structured Answers**
- 10 answers per unit (5 units total)
- Structured format: Definition → Explanation → Example → Conclusion
- Medium-length answers (300-500 words each)
- Cover all major Software Engineering topics

🎯 **Smart Search**
- FULLTEXT search with keyword matching
- Fallback LIKE matching for robustness
- Handles various question phrasings

💬 **Rich Chat Interface**
- Beautiful PyQt5 GUI
- Chat history with timestamps
- Copy answer to clipboard functionality
- Unit-based filtering
- View past conversations

📚 **Unit Coverage**
1. **Unit 1**: Introduction to Software Engineering & Processes
2. **Unit 2**: Agile Software Development & Requirements Engineering
3. **Unit 3**: System Modeling & Architectural Design
4. **Unit 4**: Design and Implementation
5. **Unit 5**: Software Testing & Dependability

## Installation

### Prerequisites
- Python 3.7+
- MySQL Server (running locally on localhost)

### Setup Steps

1. **Clone/Download this project**
```bash
cd se_chatbot
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up the database**

Open MySQL command line:
```bash
mysql -u root -p
```

Execute the SQL setup file:
```sql
source se_chatbot_db.sql
```

Or paste the contents of `se_chatbot_db.sql` directly.

4. **Verify database setup**
```sql
USE se_chatbot_db;
SELECT COUNT(*) as total_questions FROM questions_answers;
-- Should show: 50
```

## Running the Application

```bash
python chatbot_gui.py
```

The chatbot window will open. Start asking questions!

## Project Structure

```
se_chatbot/
├── se_chatbot_db.sql          # Database creation script (50 Q&A entries)
├── database_helper.py         # Database operations & chat history
├── chatbot_gui.py             # Main PyQt5 GUI application
├── requirements.txt           # Python dependencies
├── chat_history.json          # Auto-generated chat history file
└── README.md                  # This file
```

## Database Schema

### Table: questions_answers
```sql
- id: AUTO_INCREMENT PRIMARY KEY
- unit_id: INT (1-5)
- unit_name: VARCHAR
- question_keyword: VARCHAR (searchable)
- question_title: VARCHAR (searchable)
- definition: LONGTEXT (50-75 words)
- explanation: LONGTEXT (150-200 words)
- example: LONGTEXT (75-100 words)
- conclusion: LONGTEXT (50-75 words)
- created_at: TIMESTAMP
- FULLTEXT INDEX on (question_title, question_keyword)
```

## Using the Chatbot

### Asking Questions
1. Type your question in the input box
2. Press Enter or click "Ask"
3. The chatbot searches its database
4. Answer appears with full structured format

### Examples of Good Questions
- "What is software engineering?"
- "Explain agile methodology"
- "How does test-driven development work?"
- "What are design patterns?"
- "Tell me about microservices"

### Features

**Copy Answer**
- Each answer has a "Copy Answer" button
- Copies formatted answer to clipboard
- Useful for study notes

**Chat History**
- Click "View History" to see recent interactions
- Automatically saved to `chat_history.json`
- Shows timestamps and question snippets

**Filter by Unit**
- Use dropdown to filter questions by unit
- Helps organize study by topic

**Clear Chat**
- Clears current session display
- History is still preserved in file

## Database Connection

The default database configuration in `database_helper.py`:
```python
host="localhost"
user="root"
password="Forgot@1234"
database="se_chatbot_db"
```

To change credentials, edit `database_helper.py` before running.

## Troubleshooting

### "Database connection error"
- Ensure MySQL server is running
- Verify database exists: `SHOW DATABASES;`
- Check credentials in `database_helper.py`

### "No answer found"
- Try different phrasing
- Use keywords from question titles
- Available topics cover: processes, agile, design, testing, dependability

### "Module not found"
- Ensure all requirements installed: `pip install -r requirements.txt`
- Check Python version (3.7+)

### Chat history not saving
- Check file permissions in project directory
- Ensure `chat_history.json` is writable

## Extending the Chatbot

### Adding More Answers
1. Create new entries in `questions_answers` table
2. Follow the structured format (Definition → Explanation → Example → Conclusion)
3. Ensure `unit_id` is set correctly (1-5)
4. Use meaningful `question_keyword` for better search

```sql
INSERT INTO questions_answers 
(unit_id, unit_name, question_keyword, question_title, definition, explanation, example, conclusion)
VALUES 
(1, 'Unit Name', 'keyword', 'Full Question?', 'def...', 'exp...', 'ex...', 'conc...');
```

### Adding New Units
1. Create new unit entries in `questions_answers`
2. Update unit_id (e.g., 6 for new unit)
3. Update GUI unit_combo in `chatbot_gui.py` if needed

## Performance Notes

- FULLTEXT search provides fast keyword matching
- Indexes on unit_id and question_keyword for quick lookups
- Chat history stored as JSON for simplicity
- Suitable for 50-500 Q&A entries

## License

This project is created for educational purposes.

## Support

For issues or questions:
1. Check troubleshooting section
2. Verify database setup with verification queries
3. Check Python/MySQL versions match requirements

---

**Created**: November 2025
**Last Updated**: November 2025
**Database Entries**: 50 (10 per unit)
**Units Covered**: 5
