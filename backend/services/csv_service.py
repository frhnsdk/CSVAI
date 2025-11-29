import pandas as pd
import os
from typing import Optional, Dict, List

class CSVService:
    """Service for handling CSV file operations"""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.filename: Optional[str] = None
        self.file_path: Optional[str] = None
    
    def load_csv(self, file_path: str) -> Dict:
        """Load a CSV file and return basic information"""
        try:
            self.df = pd.read_csv(file_path)
            self.file_path = file_path
            self.filename = os.path.basename(file_path)
            
            return self.get_csv_info()
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")
    
    def get_csv_info(self) -> Optional[Dict]:
        """Get information about the loaded CSV"""
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
        if self.df is None:
            return None
        
        preview_df = self.df.head(rows)
        return preview_df.to_dict(orient='records')
    
    def get_dataframe(self) -> Optional[pd.DataFrame]:
        """Get the loaded DataFrame"""
        return self.df
    
    def query_data(self, query: str) -> str:
        """Execute a query and return results as string"""
        if self.df is None:
            return "No CSV file is loaded."
        
        try:
            # This is a simple example - you can enhance this
            result = eval(query, {"df": self.df, "pd": pd})
            return str(result)
        except Exception as e:
            return f"Error executing query: {str(e)}"
