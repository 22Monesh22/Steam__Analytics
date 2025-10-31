import pandas as pd
import json
from flask import Blueprint, request, jsonify, current_app
import os
from pathlib import Path
import numpy as np

dashboard_chat_bp = Blueprint('dashboard_chat', __name__)

# Power BI Dashboard Content Mapping
DASHBOARD_CONTENT = {
    "user-analytics": {
        "title": "User Analytics",
        "csv_file": "users.csv",
        "description": "User behavior, demographics, and engagement metrics",
        "key_visualizations": [
            "User growth over time",
            "Geographic distribution heatmap", 
            "Age and gender demographics",
            "User engagement trends",
            "Premium vs free user analysis"
        ],
        "data_source": "users.csv"
    },
    "game-analytics": {
        "title": "Game Analytics", 
        "csv_file": "games.csv",
        "description": "Game performance, ratings, and market analysis",
        "key_visualizations": [
            "Game sales performance",
            "Rating distribution analysis",
            "Genre performance comparison",
            "Price vs rating correlation",
            "Release timeline analysis"
        ],
        "data_source": "games.csv"
    },
    "recommendation-engine": {
        "title": "Recommendation Engine",
        "csv_file": "recommendations.csv", 
        "description": "AI recommendation performance and user preferences",
        "key_visualizations": [
            "Recommendation accuracy metrics",
            "User preference patterns",
            "Algorithm performance trends",
            "Personalization effectiveness",
            "Click-through rate analysis"
        ],
        "data_source": "recommendations.csv"
    }
}

def analyze_csv_data(dashboard_type):
    """Analyze the actual CSV data for the dashboard"""
    try:
        # Try multiple possible base paths
        base_paths = [
            Path(current_app.root_path).parent / "data" / "raw",
            Path(".") / "data" / "raw",
            Path("..") / "data" / "raw",
            Path(current_app.root_path) / "data" / "raw",
        ]
        
        dashboard_info = DASHBOARD_CONTENT.get(dashboard_type, {})
        csv_file = dashboard_info.get('csv_file', '')
        
        if not csv_file:
            return {"error": f"No CSV mapping found for {dashboard_type}"}
        
        file_path = None
        for base_path in base_paths:
            potential_path = base_path / csv_file
            current_app.logger.info(f"Checking path: {potential_path}")
            if potential_path.exists():
                file_path = potential_path
                break
        
        if not file_path:
            return {"error": f"CSV file not found: {csv_file}. Checked paths: {[str(p / csv_file) for p in base_paths]}"}
        
        current_app.logger.info(f"Found CSV file at: {file_path}")
        
        # Read CSV with optimized settings
        current_app.logger.info(f"Reading CSV file: {file_path}")
        
        # First check file size
        file_size = file_path.stat().st_size
        current_app.logger.info(f"File size: {file_size / 1024 / 1024:.2f} MB")
        
        # Read first few rows to understand structure
        try:
            sample_df = pd.read_csv(file_path, nrows=5)
            current_app.logger.info(f"CSV columns: {list(sample_df.columns)}")
            current_app.logger.info(f"Sample data shape: {sample_df.shape}")
        except Exception as e:
            current_app.logger.error(f"Error reading sample: {str(e)}")
            return {"error": f"Cannot read CSV file: {str(e)}"}
        
        # Now read the full file with optimized settings for large files
        try:
            # For very large files, use optimized reading
            if file_size > 100 * 1024 * 1024:  # If file > 100MB
                current_app.logger.info("Large file detected, using optimized reading...")
                # Read in chunks for analysis
                chunks = []
                for chunk in pd.read_csv(file_path, chunksize=100000):  # 100k rows at a time
                    chunks.append(chunk)
                    if len(chunks) >= 3:  # Only read first 300k rows for analysis
                        break
                df = pd.concat(chunks, ignore_index=True)
                current_app.logger.info(f"Sampled dataset loaded: {df.shape} (first 300k rows)")
            else:
                df = pd.read_csv(file_path)
                current_app.logger.info(f"Full dataset loaded: {df.shape}")
        except Exception as e:
            current_app.logger.error(f"Error reading full CSV: {str(e)}")
            return {"error": f"Cannot read full CSV file: {str(e)}"}
        
        # Generate insights based on dashboard type
        if dashboard_type == "user-analytics":
            return analyze_users_data(df, dashboard_info)
        elif dashboard_type == "game-analytics":
            return analyze_games_data(df, dashboard_info)
        elif dashboard_type == "recommendation-engine":
            return analyze_recommendations_data(df, dashboard_info)
        else:
            return {"error": f"Unknown dashboard type: {dashboard_type}"}
            
    except Exception as e:
        current_app.logger.error(f"Error analyzing CSV data for {dashboard_type}: {str(e)}")
        import traceback
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return {"error": str(e)}

def analyze_users_data(df, dashboard_info):
    """Analyze users.csv data with actual column structure"""
    try:
        insights = {
            "dashboard_info": dashboard_info,
            "data_overview": {
                "total_records": len(df),
                "data_columns": list(df.columns),
                "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
                "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()}
            },
            "key_metrics": {},
            "trends": [],
            "sample_data": df.head(2).to_dict('records')
        }
        
        current_app.logger.info(f"Analyzing users data with columns: {list(df.columns)}")
        
        # Analyze based on actual columns found in your CSV
        if 'user_id' in df.columns:
            unique_users = df['user_id'].nunique()
            insights["key_metrics"]["unique_users"] = f"{unique_users:,} users"
            insights["trends"].append(f"Total unique users: {unique_users:,}")
        
        if 'products' in df.columns:
            # Analyze products column (assuming it contains game/product information)
            try:
                # Check if products is a string that can be analyzed
                if df['products'].dtype == 'object':
                    # Count non-empty product entries
                    products_count = df['products'].notna().sum()
                    insights["key_metrics"]["users_with_products"] = f"{products_count:,} users"
                    
                    # Sample analysis of products data
                    sample_products = df['products'].dropna().head(5).tolist()
                    if sample_products:
                        insights["trends"].append(f"Sample products data available for analysis")
            except Exception as e:
                current_app.logger.warning(f"Could not analyze products column: {e}")
        
        if 'reviews' in df.columns:
            # Analyze reviews column
            try:
                reviews_count = df['reviews'].notna().sum()
                insights["key_metrics"]["users_with_reviews"] = f"{reviews_count:,} users"
                review_percentage = (reviews_count / len(df)) * 100
                insights["trends"].append(f"Users with reviews: {review_percentage:.1f}%")
            except Exception as e:
                current_app.logger.warning(f"Could not analyze reviews column: {e}")
        
        # Add general data quality metrics
        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isnull().sum().sum()
        null_percentage = (null_cells / total_cells) * 100
        insights["trends"].append(f"Data completeness: {100 - null_percentage:.1f}%")
        
        current_app.logger.info(f"Users analysis completed successfully")
        return insights
        
    except Exception as e:
        current_app.logger.error(f"Error in analyze_users_data: {str(e)}")
        import traceback
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return {"error": f"Analysis failed: {str(e)}"}

def analyze_games_data(df, dashboard_info):
    """Analyze games.csv data - update this when you check games.csv structure"""
    try:
        insights = {
            "dashboard_info": dashboard_info,
            "data_overview": {
                "total_records": len(df),
                "data_columns": list(df.columns),
                "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
                "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()}
            },
            "key_metrics": {},
            "trends": [],
            "sample_data": df.head(2).to_dict('records')
        }
        
        current_app.logger.info(f"Analyzing games data with columns: {list(df.columns)}")
        
        # Add basic analysis that works with any columns
        insights["key_metrics"]["total_games"] = f"{len(df):,} records"
        
        # You'll need to update this based on your actual games.csv columns
        # For now, provide generic insights
        insights["trends"].append("Game data loaded successfully")
        insights["trends"].append(f"Dataset contains {len(df.columns)} different data dimensions")
        
        return insights
        
    except Exception as e:
        current_app.logger.error(f"Error in analyze_games_data: {str(e)}")
        return {"error": str(e)}

def analyze_recommendations_data(df, dashboard_info):
    """Analyze recommendations.csv data - update this when you check recommendations.csv structure"""
    try:
        insights = {
            "dashboard_info": dashboard_info,
            "data_overview": {
                "total_records": len(df),
                "data_columns": list(df.columns),
                "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
                "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()}
            },
            "key_metrics": {},
            "trends": [],
            "sample_data": df.head(2).to_dict('records')
        }
        
        current_app.logger.info(f"Analyzing recommendations data with columns: {list(df.columns)}")
        
        # Add basic analysis that works with any columns
        insights["key_metrics"]["total_recommendations"] = f"{len(df):,} records"
        
        # You'll need to update this based on your actual recommendations.csv columns
        # For now, provide generic insights
        insights["trends"].append("Recommendation data loaded successfully")
        insights["trends"].append(f"Dataset contains {len(df.columns)} different data dimensions")
        
        # Try to identify user and item columns
        user_cols = [col for col in df.columns if 'user' in col.lower()]
        item_cols = [col for col in df.columns if any(x in col.lower() for x in ['game', 'item', 'product'])]
        
        if user_cols:
            unique_users = df[user_cols[0]].nunique()
            insights["key_metrics"]["unique_users"] = f"{unique_users:,} users"
        
        if item_cols:
            unique_items = df[item_cols[0]].nunique()
            insights["key_metrics"]["unique_items"] = f"{unique_items:,} items"
        
        return insights
        
    except Exception as e:
        current_app.logger.error(f"Error in analyze_recommendations_data: {str(e)}")
        return {"error": str(e)}

@dashboard_chat_bp.route('/analyze-dashboard', methods=['POST'])
def analyze_dashboard():
    """Main endpoint to analyze dashboard content and data"""
    try:
        data = request.json
        dashboard_type = data.get('dashboard_type', '')
        question = data.get('question', '')
        
        current_app.logger.info(f"Analyzing dashboard: {dashboard_type}, Question: {question}")
        
        # Get dashboard content info
        dashboard_info = DASHBOARD_CONTENT.get(dashboard_type, {})
        if not dashboard_info:
            return jsonify({
                "success": False,
                "response": f"Unknown dashboard type: {dashboard_type}"
            })
        
        # Analyze CSV data
        data_insights = analyze_csv_data(dashboard_type)
        
        current_app.logger.info(f"Data insights result: {'error' in data_insights}")
        
        if "error" in data_insights:
            current_app.logger.warning(f"Data analysis error: {data_insights['error']}")
            # Even with error, try to provide some basic info
            response = generate_fallback_response(dashboard_info, question, data_insights['error'])
        else:
            # Generate response using actual data insights
            response = generate_ai_response_with_data(dashboard_info, question, data_insights)
        
        return jsonify({
            "success": True,
            "response": response,
            "dashboard_info": dashboard_info,
            "data_insights": data_insights,
            "suggestions": [
                "Show detailed metrics from data",
                "Explain current trends", 
                "Compare performance segments",
                "Provide data-driven recommendations"
            ]
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in analyze_dashboard endpoint: {str(e)}")
        import traceback
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            "success": False,
            "response": f"Server error: {str(e)}"
        })

@dashboard_chat_bp.route('/test-csv-access', methods=['GET'])
def test_csv_access():
    """Test endpoint to check CSV file access and structure"""
    try:
        base_paths = [
            Path(current_app.root_path).parent / "data" / "raw",
            Path(".") / "data" / "raw",
            Path("..") / "data" / "raw",
            Path(current_app.root_path) / "data" / "raw",
        ]
        
        results = {}
        
        for dashboard_type, info in DASHBOARD_CONTENT.items():
            csv_file = info['csv_file']
            file_found = False
            
            for base_path in base_paths:
                file_path = base_path / csv_file
                if file_path.exists():
                    results[dashboard_type] = {
                        'file_path': str(file_path),
                        'exists': True,
                        'file_size': f"{file_path.stat().st_size / 1024 / 1024:.2f} MB",
                        'base_path_used': str(base_path)
                    }
                    
                    # Try to read a sample
                    try:
                        sample = pd.read_csv(file_path, nrows=5)
                        results[dashboard_type]['sample_columns'] = list(sample.columns)
                        results[dashboard_type]['sample_shape'] = sample.shape
                        results[dashboard_type]['sample_data'] = sample.to_dict('records')
                        results[dashboard_type]['column_descriptions'] = describe_columns(sample)
                    except Exception as e:
                        results[dashboard_type]['read_error'] = str(e)
                    
                    file_found = True
                    break
            
            if not file_found:
                results[dashboard_type] = {
                    'exists': False,
                    'checked_paths': [str(p / csv_file) for p in base_paths]
                }
        
        return jsonify({
            "success": True,
            "results": results,
            "base_paths_tried": [str(p) for p in base_paths]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

def describe_columns(df):
    """Generate descriptions for each column"""
    descriptions = {}
    for col in df.columns:
        desc = f"Type: {df[col].dtype}, "
        if df[col].dtype in ['int64', 'float64']:
            desc += f"Range: {df[col].min()} to {df[col].max()}"
        elif df[col].dtype == 'object':
            sample_values = df[col].dropna().unique()[:3]
            desc += f"Sample values: {list(sample_values)}"
        descriptions[col] = desc
    return descriptions

def generate_fallback_response(dashboard_info, question, error_msg):
    """Generate response when CSV data analysis fails"""
    title = dashboard_info['title']
    visualizations = dashboard_info['key_visualizations']
    
    lower_question = question.lower()
    
    if "metric" in lower_question or "kpi" in lower_question:
        return f"📊 **{title} - Key Metrics**\n\nI'm currently experiencing issues accessing the live data. Normally, this dashboard shows metrics from {dashboard_info['data_source']} including recommendation accuracy, user engagement, and algorithm performance.\n\n*Note: Data access issue - {error_msg}*"
    
    elif "insight" in lower_question or "trend" in lower_question:
        viz_text = "\n".join([f"• {viz}" for viz in visualizations])
        return f"🔍 **{title} - Insights**\n\n**Visualizations available:**\n{viz_text}\n\n*Note: Live data analysis temporarily unavailable*"
    
    else:
        return f"📋 **{title} Dashboard**\n\nThis dashboard provides analytics for {dashboard_info['description']}. It includes visualizations for {', '.join(visualizations[:3])}.\n\n*Note: Currently using dashboard metadata only*"

def generate_ai_response_with_data(dashboard_info, question, data_insights):
    """Generate AI response using both dashboard info and actual data insights"""
    
    lower_question = question.lower()
    title = dashboard_info['title']
    visualizations = dashboard_info['key_visualizations']
    
    # Build metrics text from actual data
    metrics_text = "\n".join([f"• {value}" for value in data_insights.get('key_metrics', {}).values()])
    trends_text = "\n".join([f"• {trend}" for trend in data_insights.get('trends', [])])
    
    if not metrics_text:
        metrics_text = "• Processing live data metrics..."
    
    if "metric" in lower_question or "kpi" in lower_question or "key" in lower_question:
        return f"📊 **{title} - Live Data Metrics**\n\n{metrics_text}\n\n*Based on analysis of {data_insights['data_overview']['total_records']:,} records from {dashboard_info['data_source']}*"
    
    elif "insight" in lower_question or "trend" in lower_question or "analy" in lower_question:
        viz_text = "\n".join([f"• {viz}" for viz in visualizations])
        trends_display = trends_text if trends_text else "• Analyzing patterns in the data..."
        return f"🔍 **{title} - Data Insights**\n\n**Current Trends:**\n{trends_display}\n\n**Dashboard Visualizations:**\n{viz_text}\n\n*Data source: {data_insights['data_overview']['total_records']:,} records*"
    
    elif "explain" in lower_question or "what" in lower_question or "show" in lower_question:
        columns_text = ", ".join(data_insights['data_overview']['data_columns'][:8])
        if len(data_insights['data_overview']['data_columns']) > 8:
            columns_text += f" and {len(data_insights['data_overview']['data_columns']) - 8} more"
        
        return f"📋 **{title} Dashboard Analysis**\n\n**Data Overview:**\n• Records: {data_insights['data_overview']['total_records']:,}\n• Columns: {columns_text}\n• Size: {data_insights['data_overview']['memory_usage']}\n\n**Key Metrics:**\n{metrics_text}"
    
    elif "recommend" in lower_question or "suggest" in lower_question:
        if "user" in title.lower():
            return f"🎯 **Data-Driven Recommendations - User Analytics**\n\n{metrics_text}\n\n**Suggestions:**\n• Focus retention on high-engagement segments\n• Analyze user product preferences\n• Optimize review collection strategies"
        elif "game" in title.lower():
            return f"🎯 **Data-Driven Recommendations - Game Analytics**\n\n{metrics_text}\n\n**Suggestions:**\n• Invest in top-performing game categories\n• Optimize pricing and promotion strategies\n• Improve game quality based on user feedback"
        else:
            return f"🎯 **Data-Driven Recommendations - Recommendation Engine**\n\n{metrics_text}\n\n**Suggestions:**\n• Improve algorithm accuracy based on current performance\n• Personalize recommendations for better engagement\n• A/B test new recommendation strategies"
    
    else:
        # Default comprehensive response
        return f"🤖 **{title} - Real-time Analysis**\n\n**Live Data Summary:**\n{metrics_text}\n\n**What this dashboard shows:**\n{', '.join(visualizations[:3])}\n\n**Data Source:** {data_insights['data_overview']['total_records']:,} records from {dashboard_info['data_source']}\n\nAsk me about specific metrics or insights!"