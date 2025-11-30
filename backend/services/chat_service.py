from typing import Dict, List, Optional
import os
from services.csv_service import CSVService
from services.ai_service import AIService

class ChatService:
    """Service for handling chat interactions"""
    
    def __init__(self):
        from services import csv_service as shared_csv
        self.csv_service = shared_csv
        # Don't initialize AIService immediately to avoid heavy initialization on startup.
        # We'll lazy-load AIService on first use (when a chat message requires AI response).
        self.ai_service = None
        self.chat_histories: Dict[str, List[Dict]] = {}
    
    async def get_response(self, message: str, session_id: str = "default") -> str:
        """Get AI response for a user message"""
        # Initialize history for new sessions
        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = []

        # Ensure CSV is loaded from persisted state if needed, then get CSV context
        try:
            self.csv_service._load_last_uploaded()
        except Exception:
            pass
        csv_info = self.csv_service.get_csv_info()
        context = self._build_context(csv_info)

        # Add user message to history
        self.chat_histories[session_id].append({
            "role": "user",
            "content": message
        })

        # Check if the message is a query for the CSV
        if csv_info and any(keyword in message.lower() for keyword in ["count", "average", "total", "json", "how many"]):
            if "json" in message.lower():
                json_data = self.csv_service.convert_to_json()
                response = f"CSV JSON Data: {json_data[:500]}..."  # Limit response to 500 characters
            else:
                query_result = self.csv_service.query_data(message)
                response = f"Query Result: {query_result}"
        else:
                # If AI service isn't initialized, initialize it lazily now.
                if self.ai_service is None:
                    from services.ai_service import AIService
                    self.ai_service = AIService()

                # Get AI response
                response = await self.ai_service.generate_response(
                message=message,
                context=context,
                history=self.chat_histories[session_id][:-1]  # Exclude the current message
            )

        # Add AI response to history
        self.chat_histories[session_id].append({
            "role": "assistant",
            "content": response
        })

        return response
    
    def _build_context(self, csv_info: Optional[Dict]) -> str:
        """Build context string from CSV information"""
        if not csv_info:
            return "No CSV file is currently loaded. Please upload a CSV file first."
        
        context = f"""Current CSV file: {csv_info['filename']}
Rows: {csv_info['rows']}
Columns: {csv_info['columns']}
Column names: {', '.join(csv_info['column_names'])}

You are an AI assistant helping users analyze their CSV data. Answer questions about the data, provide insights, and help with data analysis tasks."""
        
        return context
    
    def clear_history(self, session_id: str = "default"):
        """Clear chat history for a session"""
        if session_id in self.chat_histories:
            self.chat_histories[session_id] = []
    
    def get_history(self, session_id: str = "default") -> List[Dict]:
        """Get chat history for a session"""
        return self.chat_histories.get(session_id, [])

    def clear_session(self, session_id: str = "default"):
        """Clear session and reset chat history"""
        self.chat_histories.pop(session_id, None)
        self.csv_service.df = None
        self.csv_service.filename = None
        self.csv_service.file_path = None
