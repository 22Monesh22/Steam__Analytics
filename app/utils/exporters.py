import pandas as pd
import json
import csv
from io import StringIO, BytesIO
from flask import Response

class DataExporter:
    @staticmethod
    def export_to_csv(data, filename='export.csv'):
        """Export data to CSV"""
        if isinstance(data, list) and data:
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame()
        
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
    
    @staticmethod
    def export_to_json(data, filename='export.json'):
        """Export data to JSON"""
        if isinstance(data, pd.DataFrame):
            json_data = data.to_json(orient='records', indent=2)
        else:
            json_data = json.dumps(data, indent=2)
        
        return Response(
            json_data,
            mimetype="application/json",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
    
    @staticmethod
    def export_to_excel(data, filename='export.xlsx'):
        """Export data to Excel"""
        if isinstance(data, list) and data:
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame()
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        
        output.seek(0)
        
        return Response(
            output.getvalue(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )