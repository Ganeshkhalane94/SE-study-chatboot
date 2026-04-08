"""
Software Engineering Chatbot - Enhanced GUI
Features: Chat history, copy button, beautiful UI, structured answers
"""

import sys
import json
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QColor, QTextCursor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QLabel, QScrollArea, QFrame, QComboBox, QMessageBox)
from database_helper import DatabaseHelper, ChatHistory


class ChatMessage(QFrame):
    """Custom widget for displaying chat messages"""

    def __init__(self, message_text, is_question=True, answer_id=None, parent=None):
        super().__init__(parent)
        self.is_question = is_question
        self.answer_id = answer_id
        self.message_text = message_text

        self.init_ui()

    def init_ui(self):
        """Initialize message UI"""
        layout = QVBoxLayout()

        # Header with timestamp and role
        header_layout = QHBoxLayout()
        timestamp = datetime.now().strftime("%H:%M:%S")
        role = "You" if self.is_question else "Chatbot"
        header_label = QLabel(f"{role} • {timestamp}")
        header_font = QFont()
        header_font.setPointSize(8)
        header_font.setItalic(True)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: #888888;")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Message content
        message_label = QLabel(self.message_text)
        message_label.setWordWrap(True)
        message_font = QFont()
        message_font.setPointSize(10)
        message_label.setFont(message_font)

        if self.is_question:
            message_label.setStyleSheet("color: #2c3e50; background-color: #ecf0f1; padding: 10px; border-radius: 5px;")
        else:
            message_label.setStyleSheet("color: #2c3e50; background-color: #d5f4e6; padding: 10px; border-radius: 5px;")

        layout.addWidget(message_label)

        # Copy button for answers
        if not self.is_question:
            button_layout = QHBoxLayout()
            copy_button = QPushButton("📋 Copy Answer")
            copy_button.setMaximumWidth(150)
            copy_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #1f618d;
                }
            """)
            copy_button.clicked.connect(lambda: self.copy_to_clipboard())
            button_layout.addWidget(copy_button)
            button_layout.addStretch()
            layout.addLayout(button_layout)

        self.setLayout(layout)

        # Styling
        if self.is_question:
            self.setStyleSheet("QFrame { background-color: #e8f4f8; border-radius: 5px; margin: 5px 0px; }")
        else:
            self.setStyleSheet("QFrame { background-color: #e8f8f0; border-radius: 5px; margin: 5px 0px; }")

    def copy_to_clipboard(self):
        """Copy message text to clipboard"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.message_text)
        # Show confirmation
        msg = QMessageBox()
        msg.setWindowTitle("Copied")
        msg.setText("Answer copied to clipboard!")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #2c3e50;
            }
        """)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class SEChatbotGUI(QMainWindow):
    """Main Chatbot GUI Application"""

    def __init__(self):
        super().__init__()
        self.db = DatabaseHelper()
        self.chat_history = ChatHistory()
        self.init_ui()
        self.show()
        self.show_welcome_message()

    def init_ui(self):
        """Initialize user interface"""
        # Window settings
        self.setWindowTitle("SE Chatbot - Software Engineering Q&A Assistant")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 11pt;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Software Engineering Chatbot")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin: 10px;")
        main_layout.addWidget(title)

        # Subtitle with database info
        subtitle = QLabel("Ask questions about Software Engineering topics")
        subtitle_font = QFont()
        subtitle_font.setPointSize(9)
        subtitle_font.setItalic(True)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #7f8c8d; margin: 0px 10px 10px 10px;")
        main_layout.addWidget(subtitle)

        # Filter section
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by Unit:")
        filter_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        self.unit_combo = QComboBox()
        self.unit_combo.addItem("All Units", None)

        units = self.db.get_units()
        for unit in units:
            self.unit_combo.addItem(f"Unit {unit['unit_id']}: {unit['unit_name']}", unit['unit_id'])

        self.unit_combo.currentIndexChanged.connect(self.on_unit_changed)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.unit_combo)
        filter_layout.addStretch()

        # Chat history button
        history_button = QPushButton("📜 View History")
        history_button.setMaximumWidth(120)
        history_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        history_button.clicked.connect(self.show_history)
        filter_layout.addWidget(history_button)

        main_layout.addLayout(filter_layout)

        # Chat display area with scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: 1px solid #bdc3c7; border-radius: 5px; }")

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setSpacing(10)
        self.chat_layout.setContentsMargins(10, 10, 10, 10)
        self.chat_container.setLayout(self.chat_layout)

        scroll_area.setWidget(self.chat_container)
        main_layout.addWidget(scroll_area, 1)

        # Input section
        input_layout = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask me about Software Engineering... (e.g., 'What is agile methodology?')")
        self.input_box.returnPressed.connect(self.get_answer)
        input_layout.addWidget(self.input_box)

        ask_button = QPushButton("🔍 Ask")
        ask_button.setMaximumWidth(100)
        ask_button.clicked.connect(self.get_answer)
        input_layout.addWidget(ask_button)

        clear_button = QPushButton("🗑️ Clear")
        clear_button.setMaximumWidth(100)
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_button.clicked.connect(self.clear_chat)
        input_layout.addWidget(clear_button)

        main_layout.addLayout(input_layout)

        # Status bar
        self.statusBar().showMessage("Ready • Database: se_chatbot_db")

        central_widget.setLayout(main_layout)

    def show_welcome_message(self):
        """Display welcome message with instructions"""
        welcome_text = """Welcome to the SE Chatbot! 👋

I'm your Software Engineering learning assistant. I have answers to 50 common questions covering:
• Unit 1: Introduction & Software Processes
• Unit 2: Agile Development & Requirements
• Unit 3: System Modeling & Architecture
• Unit 4: Design & Implementation
• Unit 5: Testing & Dependability

How to use:
1. Type your question in the input box below
2. Press Enter or click "Ask"
3. I'll search my database and provide a structured answer
4. Copy any answer you like using the "Copy Answer" button
5. View your chat history anytime

Try asking: "What is software engineering?" or "Explain agile methods"
"""
        self.add_message(welcome_text, is_question=False)

    def add_message(self, text, is_question=True, answer_id=None):
        """Add message to chat display"""
        message = ChatMessage(text, is_question, answer_id)
        self.chat_layout.addWidget(message)

        # Scroll to bottom
        scroll_area = self.findChild(QScrollArea)
        if scroll_area:
            scroll_area.verticalScrollBar().setValue(
                scroll_area.verticalScrollBar().maximum()
            )

    def get_answer(self):
        """Get answer for user's question"""
        question = self.input_box.text().strip()

        if not question:
            QMessageBox.warning(self, "Input Required", "Please enter a question.")
            return

        # Add question to display
        self.add_message(question, is_question=True)
        self.input_box.clear()

        self.statusBar().showMessage("Searching database...")
        QApplication.processEvents()

        # Search for answer
        answer_data = self.db.search_answer(question)

        if answer_data:
            # Format structured answer
            answer_text = f"""
📚 QUESTION: {answer_data['question_title']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 DEFINITION:
{answer_data['definition']}

💡 EXPLANATION:
{answer_data['explanation']}

🔧 EXAMPLE:
{answer_data['example']}

✓ CONCLUSION:
{answer_data['conclusion']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Unit: {answer_data['unit_name']}
"""
            self.add_message(answer_text, is_question=False, answer_id=answer_data['id'])
            self.chat_history.add_entry(question, answer_text, answer_data['id'])
            self.statusBar().showMessage("Answer found! ✓")
        else:
            no_answer_text = """I'm sorry, I couldn't find an answer to your question in my database.

This could mean:
• The question is phrased differently than what I have stored
• The topic might not be covered in my current database

My database contains answers for these topics:
✓ Software Engineering fundamentals
✓ Software processes and methodologies
✓ Requirements engineering
✓ System modeling and design
✓ Object-oriented design
✓ Software testing
✓ Dependability and quality

Try rephrasing your question or asking about one of these topics!
"""
            self.add_message(no_answer_text, is_question=False)
            self.statusBar().showMessage("No answer found. Try rephrasing your question.")

    def on_unit_changed(self):
        """Handle unit filter change"""
        selected_unit = self.unit_combo.currentData()
        if selected_unit:
            message = f"Showing questions from Unit {selected_unit}: {self.unit_combo.currentText()}"
        else:
            message = "Showing all units"

        self.statusBar().showMessage(message)

    def clear_chat(self):
        """Clear chat display"""
        reply = QMessageBox.question(
            self, 
            "Clear Chat", 
            "Clear all messages from the current session?\n(Chat history will still be saved)",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Clear layout
            while self.chat_layout.count():
                child = self.chat_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            self.show_welcome_message()
            self.statusBar().showMessage("Chat cleared!")

    def show_history(self):
        """Show chat history in a dialog"""
        history = self.chat_history.get_history()
        stats = self.chat_history.get_stats()

        if not history:
            QMessageBox.information(self, "Chat History", "No chat history yet.")
            return

        history_text = f"Chat History ({stats['total_interactions']} interactions)\n"
        history_text += "━" * 50 + "\n\n"

        for i, entry in enumerate(history[-10:], 1):  # Show last 10
            timestamp = entry['timestamp']
            question = entry['question'][:50] + "..." if len(entry['question']) > 50 else entry['question']
            history_text += f"{i}. [{timestamp}]\n   Q: {question}\n\n"

        if len(history) > 10:
            history_text += f"\n... and {len(history) - 10} more interactions"

        msg = QMessageBox()
        msg.setWindowTitle("Chat History")
        msg.setText(history_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def main():
    print("Entering main()...")  # Add this
    app = QApplication(sys.argv)
    print("App created.")         # Add this
    try:
        chatbot = SEChatbotGUI()
        print("GUI initialized.") # Add this
        sys.exit(app.exec_())
    except Exception as e:
        print("Exception occurred:", e)  # Add this
        # Show error dialog here if needed



if __name__ == "__main__":
    main()
