"""
Database Helper Module for SE Chatbot
Handles all database operations including connection, queries, and answer retrieval
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
import json

class DatabaseHelper:
    """Manages database connections and queries for the SE Chatbot"""

    def __init__(self, host="localhost", user="root", password="Your password", database="se_chatbot_db"):
        """
        Initialize database connection
        Args:
            host: Database host
            user: Database user
            password: Database password
            database: Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print(f"✓ Database connected successfully to {self.database}")
        except Error as e:
            print(f"✗ Database connection error: {e}")
            raise

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("✓ Database disconnected")

    def search_answer(self, question):
        """
        Search for answer using keyword matching
        Uses FULLTEXT search for better results

        Args:
            question: User's question string

        Returns:
            dict: Answer object with all fields or None if not found
        """
        try:
            # Extract keywords from question (split and filter)
            keywords = question.lower().strip().split()
            keywords = [k for k in keywords if len(k) > 2]  # Remove short words

            if not keywords:
                return None

            # Try FULLTEXT search first
            search_query = " OR ".join([f"MATCH(question_title, question_keyword) AGAINST('{k}' IN BOOLEAN MODE)" 
                                       for k in keywords[:3]])  # Limit to first 3 keywords

            query = f"""
            SELECT * FROM questions_answers 
            WHERE {search_query}
            ORDER BY MATCH(question_title, question_keyword) AGAINST('{' '.join(keywords[:3])}' IN BOOLEAN MODE) DESC
            LIMIT 1
            """

            self.cursor.execute(query)
            result = self.cursor.fetchone()

            # If no FULLTEXT result, try LIKE matching as fallback
            if not result:
                like_conditions = " OR ".join([f"question_keyword LIKE '%{k}%' OR question_title LIKE '%{k}%'" 
                                              for k in keywords[:3]])
                query = f"""
                SELECT * FROM questions_answers 
                WHERE {like_conditions}
                LIMIT 1
                """
                self.cursor.execute(query)
                result = self.cursor.fetchone()

            return result

        except Error as e:
            print(f"✗ Search query error: {e}")
            return None

    def get_all_questions(self, unit_id=None):
        """
        Retrieve all questions (optionally filtered by unit)

        Args:
            unit_id: Optional unit ID to filter by

        Returns:
            list: List of all questions or questions for specific unit
        """
        try:
            if unit_id:
                query = "SELECT id, unit_id, question_title, question_keyword FROM questions_answers WHERE unit_id = %s ORDER BY id"
                self.cursor.execute(query, (unit_id,))
            else:
                query = "SELECT id, unit_id, question_title, question_keyword FROM questions_answers ORDER BY unit_id, id"
                self.cursor.execute(query)

            results = self.cursor.fetchall()
            return results

        except Error as e:
            print(f"✗ Query error: {e}")
            return []

    def get_units(self):
        """
        Retrieve all available units

        Returns:
            list: List of (unit_id, unit_name) tuples
        """
        try:
            query = "SELECT DISTINCT unit_id, unit_name FROM questions_answers ORDER BY unit_id"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results

        except Error as e:
            print(f"✗ Query error: {e}")
            return []

    def get_answer_by_id(self, answer_id):
        """
        Retrieve specific answer by ID

        Args:
            answer_id: ID of the answer

        Returns:
            dict: Answer object or None
        """
        try:
            query = "SELECT * FROM questions_answers WHERE id = %s"
            self.cursor.execute(query, (answer_id,))
            result = self.cursor.fetchone()
            return result

        except Error as e:
            print(f"✗ Query error: {e}")
            return None

    def get_statistics(self):
        """
        Get database statistics

        Returns:
            dict: Statistics about database content
        """
        try:
            self.cursor.execute("SELECT COUNT(*) as total_questions FROM questions_answers")
            total = self.cursor.fetchone()['total_questions']

            self.cursor.execute("""
            SELECT unit_id, unit_name, COUNT(*) as count 
            FROM questions_answers 
            GROUP BY unit_id, unit_name 
            ORDER BY unit_id
            """)
            by_unit = self.cursor.fetchall()

            return {
                'total_questions': total,
                'by_unit': by_unit
            }

        except Error as e:
            print(f"✗ Query error: {e}")
            return {}


class ChatHistory:
    """Manages chat history - saves to JSON file for persistence"""

    def __init__(self, history_file="chat_history.json"):
        """
        Initialize chat history

        Args:
            history_file: Path to store chat history JSON
        """
        self.history_file = history_file
        self.history = self.load_history()

    def load_history(self):
        """Load chat history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load history: {e}")

        return []

    def save_history(self):
        """Save chat history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save history: {e}")

    def add_entry(self, question, answer_text, answer_id=None):
        """
        Add a Q&A entry to history

        Args:
            question: User's question
            answer_text: Full answer text
            answer_id: ID of answer in database
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'answer_id': answer_id,
            'answer_length': len(answer_text)
        }
        self.history.append(entry)
        self.save_history()

    def get_history(self):
        """Get all history entries"""
        return self.history

    def clear_history(self):
        """Clear all history"""
        self.history = []
        self.save_history()

    def get_stats(self):
        """Get history statistics"""
        return {
            'total_interactions': len(self.history),
            'file': self.history_file
        }


# Example usage
if __name__ == "__main__":
    # Test database connection
    db = DatabaseHelper()

    # Get statistics
    stats = db.get_statistics()
    print(f"\nDatabase Statistics: {stats}")

    # Test search
    test_question = "What is software engineering?"
    answer = db.search_answer(test_question)
    if answer:
        print(f"\nFound answer for: {test_question}")
        print(f"Title: {answer['question_title']}")
    else:
        print(f"No answer found for: {test_question}")

    # Test chat history
    history = ChatHistory()
    print(f"\nChat History Stats: {history.get_stats()}")

    db.disconnect()
