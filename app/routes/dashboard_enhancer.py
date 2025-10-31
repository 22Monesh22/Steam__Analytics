import pandas as pd
from flask import Blueprint, request, jsonify, current_app
from pathlib import Path

dashboard_enhancer_bp = Blueprint('dashboard_enhancer', __name__)

def get_dashboard_context(dashboard_type):
    """Get quick insights about the dashboard data"""
    try:
        base_path = Path(current_app.root_path).parent / "data" / "raw"
        
        if dashboard_type == "user-analytics":
            file_path = base_path / "users.csv"
            if file_path.exists():
                # Quick sample analysis without loading full file
                sample = pd.read_csv(file_path, nrows=10000)
                return {
                    "total_users": sample['user_id'].nunique(),
                    "has_products": 'products' in sample.columns,
                    "has_reviews": 'reviews' in sample.columns,
                    "data_size": f"{file_path.stat().st_size / 1024 / 1024:.1f}MB",
                    "sample_columns": list(sample.columns)
                }
        
        elif dashboard_type == "game-analytics":
            file_path = base_path / "games.csv"
            if file_path.exists():
                sample = pd.read_csv(file_path, nrows=10000)
                return {
                    "total_games": len(sample),
                    "columns": list(sample.columns),
                    "data_size": f"{file_path.stat().st_size / 1024 / 1024:.1f}MB"
                }
        
        elif dashboard_type == "recommendation-engine":
            file_path = base_path / "recommendations.csv"
            if file_path.exists():
                sample = pd.read_csv(file_path, nrows=10000)
                return {
                    "total_recommendations": len(sample),
                    "columns": list(sample.columns),
                    "data_size": f"{file_path.stat().st_size / 1024 / 1024:.1f}MB"
                }
        
        return {"error": "No data found"}
        
    except Exception as e:
        current_app.logger.error(f"Error getting dashboard context: {str(e)}")
        return {"error": str(e)}

@dashboard_enhancer_bp.route('/get-context', methods=['POST'])
def get_dashboard_context_route():
    """Get dashboard context for AI enhancement"""
    data = request.json
    dashboard_type = data.get('dashboard_type', '')
    
    context = get_dashboard_context(dashboard_type)
    return jsonify({
        "success": True,
        "context": context
    })