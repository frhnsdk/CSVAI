import pandas as pd
import os
from typing import Optional, Dict, List

class CSVService:
    """Service for handling CSV file operations"""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.filename: Optional[str] = None
        self.file_path: Optional[str] = None
        # Initialize upload directory and try to load last uploaded CSV
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.UPLOAD_DIR = os.path.join(project_root, "uploads")
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        self._load_last_uploaded()
    
    def load_csv(self, file_path: str) -> Dict:
        """Load a CSV file and return basic information"""
        try:
            print(f"Loading CSV from path: {file_path}")
            self.df = pd.read_csv(file_path)
            self.file_path = file_path
            self.filename = os.path.basename(file_path)
            # persist the current csv path so other processes can pick it up
            self._write_current_csv_path(file_path)
            print(f"Loaded DataFrame: {self.df.head()} with shape {self.df.shape}")

            return self.get_csv_info()
        except Exception as e:
            print(f"Error loading CSV: {str(e)}")
            raise Exception(f"Error loading CSV: {str(e)}")
    
    def get_csv_info(self) -> Optional[Dict]:
        """Get information about the loaded CSV"""
        # If we currently have no DataFrame, attempt to reload any persisted state from disk
        if self.df is None:
            try:
                self._load_last_uploaded()
            except Exception:
                pass
        if self.df is None:
            return None
        
        return {
            "filename": self.filename,
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "column_names": self.df.columns.tolist(),
            "dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()},
            "memory_usage": f"{self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }
    
    def get_preview(self, rows: int = 10) -> Optional[List[Dict]]:
        """Get a preview of the CSV data"""
        # Ensure we attempt to reload a persisted CSV if the service is currently empty
        if self.df is None:
            return None
        
        preview_df = self.df.head(rows)
        return preview_df.to_dict(orient='records')
    
    def get_dataframe(self) -> Optional[pd.DataFrame]:
        """Get the loaded DataFrame"""
        # Make an attempt to reload persisted CSV if needed
        if self.df is None:
            try:
                self._load_last_uploaded()
            except Exception:
                pass
        return self.df
    
    def query_data(self, query: str) -> str:
        """Execute a query and return results as string"""
        # Attempt to reload any persisted CSV file if no DataFrame is present
        if self.df is None:
            try:
                self._load_last_uploaded()
            except Exception:
                pass
        if self.df is None:
            return "No CSV file is loaded."

        try:
            query = query.lower()
            if ("count" in query or "how many" in query) and "female" in query:
                return str(len(self.df[self.df['Gender'] == 'Female']))
            elif "average" in query and "salary" in query:
                return str(self.df['Salary'].mean())
            elif "total" in query and "revenue" in query:
                return str(self.df['Revenue'].sum())
            else:
                return "Query not recognized. Please refine your question."
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def convert_to_json(self) -> Optional[str]:
        """Convert the loaded CSV file to JSON format"""
        if self.df is None:
            return "No CSV file is loaded."

        try:
            json_data = self.df.to_json(orient='records')
            print(f"Converted CSV to JSON: {json_data[:100]}...")  # Log first 100 characters for debugging
            return json_data
        except Exception as e:
            print(f"Error converting CSV to JSON: {str(e)}")
            return f"Error converting CSV to JSON: {str(e)}"

    def _current_csv_state_file(self) -> str:
        return os.path.join(self.UPLOAD_DIR, "current_csv.json")

    def _write_current_csv_path(self, file_path: str):
        try:
            import json
            state = {"file_path": file_path}
            with open(self._current_csv_state_file(), "w", encoding="utf-8") as f:
                json.dump(state, f)
                print(f"Wrote current CSV state to {self._current_csv_state_file()}")
        except Exception as e:
            print(f"Error writing current csv state: {e}")

    def _load_last_uploaded(self):
        # Attempt to load last uploaded CSV if it exists
        try:
            import json
            state_file = self._current_csv_state_file()
            if os.path.exists(state_file):
                with open(state_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    file_path = state.get("file_path")
                    if file_path and os.path.exists(file_path):
                        print(f"Found last uploaded CSV: {file_path}, attempting to load")
                        self.load_csv(file_path)
        except Exception as e:
            print(f"Error loading last uploaded CSV: {e}")
