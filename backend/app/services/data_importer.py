import pandas as pd
import io
import json
from typing import Dict, List, Tuple, Any, Optional

from app.models.data_source import DataSource


def get_data_preview(file_name: str, file_contents: bytes, source_type: str) -> Tuple[List[Dict], Dict]:
    """
    Get a preview of the data from a file, along with the detected schema.
    
    Args:
        file_name: The name of the file
        file_contents: The contents of the file as bytes
        source_type: The type of data source (CSV, Excel, etc.)
        
    Returns:
        A tuple containing (preview_data, schema)
    """
    df = None
    
    # Convert bytes to file-like object
    file_obj = io.BytesIO(file_contents)
    
    # Process file based on type
    if source_type.lower() == 'csv':
        df = pd.read_csv(file_obj, nrows=100)
    elif source_type.lower() == 'excel':
        df = pd.read_excel(file_obj, nrows=100)
    elif source_type.lower() == 'json':
        data = json.loads(file_contents.decode('utf-8'))
        df = pd.json_normalize(data)
    else:
        raise ValueError(f"Unsupported file type: {source_type}")
    
    # Generate schema from DataFrame
    schema = {}
    for column in df.columns:
        dtype = str(df[column].dtype)
        if 'int' in dtype:
            schema[column] = 'integer'
        elif 'float' in dtype:
            schema[column] = 'number'
        elif 'datetime' in dtype:
            schema[column] = 'datetime'
        elif 'bool' in dtype:
            schema[column] = 'boolean'
        else:
            schema[column] = 'string'
    
    # Convert preview to list of dicts
    preview_data = df.head(10).to_dict(orient='records')
    
    return preview_data, schema


def import_data(data_source: DataSource) -> List[Dict]:
    """
    Import data from a data source.
    
    Args:
        data_source: The DataSource object containing connection info
        
    Returns:
        The imported data as a list of dictionaries
    """
    source_type = data_source.source_type.lower()
    connection_info = data_source.connection_info
    
    if source_type == 'csv':
        # Import from CSV file
        file_path = connection_info.get('file_path')
        if not file_path:
            raise ValueError("File path is required for CSV data source")
        
        df = pd.read_csv(file_path)
        return df.to_dict(orient='records')
    
    elif source_type == 'excel':
        # Import from Excel file
        file_path = connection_info.get('file_path')
        sheet_name = connection_info.get('sheet_name')
        
        if not file_path:
            raise ValueError("File path is required for Excel data source")
        
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)
            
        return df.to_dict(orient='records')
    
    elif source_type == 'database':
        # Import from database (using SQLAlchemy)
        connection_string = connection_info.get('connection_string')
        query = connection_info.get('query')
        
        if not connection_string or not query:
            raise ValueError("Connection string and query are required for database data source")
        
        df = pd.read_sql(query, connection_string)
        return df.to_dict(orient='records')
    
    elif source_type == 'api':
        # Import from API (using requests)
        import requests
        
        url = connection_info.get('url')
        method = connection_info.get('method', 'GET')
        headers = connection_info.get('headers', {})
        params = connection_info.get('params', {})
        body = connection_info.get('body')
        
        if not url:
            raise ValueError("URL is required for API data source")
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, params=params, json=body)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        
        # Parse response as JSON
        data = response.json()
        
        # If data is a list, convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            # If data is a dict, try to extract the data array
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    df = pd.DataFrame(value)
                    break
            else:
                # If no list found, use the entire response
                df = pd.json_normalize(data)
        
        return df.to_dict(orient='records')
    
    else:
        raise ValueError(f"Unsupported data source type: {source_type}")


def export_data(data: List[Dict], format: str, file_path: Optional[str] = None) -> Optional[bytes]:
    """
    Export data to various formats.
    
    Args:
        data: The data to export as a list of dictionaries
        format: The format to export to (csv, excel, json)
        file_path: The path to save the file to (optional)
        
    Returns:
        The exported data as bytes if file_path is None, otherwise None
    """
    df = pd.DataFrame(data)
    
    if format.lower() == 'csv':
        if file_path:
            df.to_csv(file_path, index=False)
            return None
        else:
            output = io.BytesIO()
            df.to_csv(output, index=False)
            return output.getvalue()
    
    elif format.lower() == 'excel':
        if file_path:
            df.to_excel(file_path, index=False)
            return None
        else:
            output = io.BytesIO()
            df.to_excel(output, index=False)
            return output.getvalue()
    
    elif format.lower() == 'json':
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(data, f)
            return None
        else:
            return json.dumps(data).encode('utf-8')
    
    else:
        raise ValueError(f"Unsupported export format: {format}") 