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
        base_path = Path(current_app.root_path).parent / "data" / "raw"
        dashboard_info = DASHBOARD_CONTENT.get(dashboard_type, {})
        csv_file = dashboard_info.get('csv_file', '')
        
        if not csv_file:
            return {"error": f"No CSV mapping found for {dashboard_type}"}
            
        file_path = base_path / csv_file
        
        current_app.logger.info(f"Looking for CSV file at: {file_path}")
        current_app.logger.info(f"File exists: {file_path.exists()}")
        
        if not file_path.exists():
            # Try alternative paths
            alternative_paths = [
                Path(".") / "data" / "raw" / csv_file,
                Path("..") / "data" / "raw" / csv_file,
                Path(current_app.root_path) / "data" / "raw" / csv_file,
            ]
            
            for alt_path in alternative_paths:
                current_app.logger.info(f"Trying alternative path: {alt_path}")
                if alt_path.exists():
                    file_path = alt_path
                    break
            
            if not file_path.exists():
                return {"error": f"CSV file not found: {csv_file}. Tried: {file_path}"}
        
        # Read CSV with efficient chunking for large files
        current_app.logger.info(f"Reading CSV file: {file_path}")
        
        # First, let's check the file size and structure
        file_size = file_path.stat().st_size
        current_app.logger.info(f"File size: {file_size / 1024 / 1024:.2f} MB")
        
        # Read first few rows to understand structure
        sample_df = pd.read_csv(file_path, nrows=5)
        current_app.logger.info(f"CSV columns: {list(sample_df.columns)}")
        current_app.logger.info(f"Sample data shape: {sample_df.shape}")
        
        # Now read the full file with optimized settings
        df = pd.read_csv(file_path)
        current_app.logger.info(f"Full dataset loaded: {df.shape}")
        current_app.logger.info(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
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

def analyze_recommendations_data(df, dashboard_info):
    """Analyze recommendations.csv data with better error handling"""
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
            "sample_data": df.head(3).to_dict('records')
        }
        
        current_app.logger.info(f"Analyzing recommendations data with columns: {list(df.columns)}")
        
        # Safe column analysis with fallbacks
        if 'user_id' in df.columns:
            unique_users = df['user_id'].nunique()
            insights["key_metrics"]["unique_users"] = f"{unique_users:,} users"
            insights["trends"].append(f"Total unique users: {unique_users:,}")
        else:
            # Try to find user identifier columns
            user_cols = [col for col in df.columns if 'user' in col.lower()]
            if user_cols:
                unique_users = df[user_cols[0]].nunique()
                insights["key_metrics"]["unique_users"] = f"{unique_users:,} users"
        
        if 'game_id' in df.columns or 'item_id' in df.columns:
            game_col = 'game_id' if 'game_id' in df.columns else 'item_id'
            unique_games = df[game_col].nunique()
            insights["key_metrics"]["unique_games"] = f"{unique_games:,} games"
            insights["trends"].append(f"Total unique games: {unique_games:,}")
        
        # Analyze rating/score columns
        score_columns = [col for col in df.columns if any(x in col.lower() for x in ['score', 'rating', 'prediction'])]
        if score_columns:
            score_col = score_columns[0]
            avg_score = df[score_col].mean()
            insights["key_metrics"]["avg_score"] = f"{avg_score:.3f}"
            insights["key_metrics"]["score_range"] = f"{df[score_col].min():.3f} - {df[score_col].max():.3f}"
            
            # Calculate high confidence recommendations
            high_score_threshold = 0.7  # Adjust based on your data
            high_score_count = len(df[df[score_col] > high_score_threshold])
            high_score_pct = (high_score_count / len(df)) * 100
            insights["trends"].append(f"High-confidence recommendations (>0.7): {high_score_count:,} ({high_score_pct:.1f}%)")
        
        # Analyze interaction types if available
        interaction_cols = [col for col in df.columns if any(x in col.lower() for x in ['type', 'interaction', 'action'])]
        if interaction_cols:
            interaction_col = interaction_cols[0]
            interaction_counts = df[interaction_col].value_counts().head(3)
            insights["trends"].append(f"Top interactions: {', '.join([f'{itype} ({count:,})' for itype, count in interaction_counts.items()])}")
        
        # Calculate recommendation density
        if 'user_id' in df.columns and ('game_id' in df.columns or 'item_id' in df.columns):
            game_col = 'game_id' if 'game_id' in df.columns else 'item_id'
            avg_recommendations_per_user = len(df) / df['user_id'].nunique()
            insights["key_metrics"]["avg_recommendations_per_user"] = f"{avg_recommendations_per_user:.1f}"
        
        # Add data quality metrics
        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isnull().sum().sum()
        null_percentage = (null_cells / total_cells) * 100
        insights["trends"].append(f"Data completeness: {100 - null_percentage:.1f}%")
        
        current_app.logger.info(f"Recommendations analysis completed successfully")
        return insights
        
    except Exception as e:
        current_app.logger.error(f"Error in analyze_recommendations_data: {str(e)}")
        import traceback
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return {"error": f"Analysis failed: {str(e)}"}

def analyze_users_data(df, dashboard_info):
    """Analyze users.csv data"""
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
        
        # Your existing users analysis code...
        return insights
    except Exception as e:
        current_app.logger.error(f"Error in analyze_users_data: {str(e)}")
        return {"error": str(e)}

def analyze_games_data(df, dashboard_info):
    """Analyze games.csv data"""
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
        
        # Your existing games analysis code...
        return insights
    except Exception as e:
        current_app.logger.error(f"Error in analyze_games_data: {str(e)}")
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
        columns_text = ", ".join(data_insights['data_overview']['data_columns'][:8])  # Show first 8 columns
        if len(data_insights['data_overview']['data_columns']) > 8:
            columns_text += f" and {len(data_insights['data_overview']['data_columns']) - 8} more"
        
        return f"📋 **{title} Dashboard Analysis**\n\n**Data Overview:**\n• Records: {data_insights['data_overview']['total_records']:,}\n• Columns: {columns_text}\n• Size: {data_insights['data_overview']['memory_usage']}\n\n**Key Metrics:**\n{metrics_text}"
    
    elif "recommend" in lower_question or "suggest" in lower_question:
        if "user" in title.lower():
            return f"🎯 **Data-Driven Recommendations - User Analytics**\n\n{metrics_text}\n\n**Suggestions:**\n• Focus retention on high-engagement segments\n• Analyze geographic patterns\n• Optimize premium conversion funnels"
        elif "game" in title.lower():
            return f"🎯 **Data-Driven Recommendations - Game Analytics**\n\n{metrics_text}\n\n**Suggestions:**\n• Invest in top-performing genres\n• Optimize pricing strategies\n• Improve quality of lower-rated games"
        else:
            return f"🎯 **Data-Driven Recommendations - Recommendation Engine**\n\n{metrics_text}\n\n**Suggestions:**\n• Improve algorithm accuracy based on current performance\n• Personalize recommendations for better engagement\n• A/B test new recommendation strategies"
    
    else:
        # Default comprehensive response
        return f"🤖 **{title} - Real-time Analysis**\n\n**Live Data Summary:**\n{metrics_text}\n\n**What this dashboard shows:**\n{', '.join(visualizations[:3])}\n\n**Data Source:** {data_insights['data_overview']['total_records']:,} records from {dashboard_info['data_source']}\n\nAsk me about specific metrics or insights!"