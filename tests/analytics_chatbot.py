import google.generativeai as genai
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import io
import os

class AnalyticsChatbot:
    def __init__(self, api_key: str, meta_json_path: str):
        """
        Initialize the Analytics Chatbot
        
        Args:
            api_key (str): Your Gemini API key
            meta_json_path (str): Path to your existing meta JSON file
        """
        self.api_key = api_key
        self.meta_data = self._load_meta_data(meta_json_path)
        self._configure_gemini()
        self.conversation_history = []
        
    def _load_meta_data(self, json_path: str) -> dict:
        """Load your existing project meta JSON file"""
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                meta_data = json.load(file)
            print(f"✅ Successfully loaded meta data from {json_path}")
            return meta_data
        except FileNotFoundError:
            raise Exception(f"Meta JSON file not found at: {json_path}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON format: {e}")
    
    def _configure_gemini(self):
        """Configure the Gemini API"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            # Test the configuration with a simple prompt
            test_response = self.model.generate_content("Hello")
            print("✅ Gemini API configured successfully")
        except Exception as e:
            raise Exception(f"Gemini API configuration failed: {e}")
    
    def _get_system_context(self) -> str:
        """Create system context from your meta JSON data"""
        project_context = f"""
        PROJECT META DATA:
        - Name: {self.meta_data.get('project_name', 'Not specified')}
        - Version: {self.meta_data.get('version', 'Not specified')}
        - Description: {self.meta_data.get('description', 'Not specified')}
        
        KEY CAPABILITIES:
        {self._format_list(self.meta_data.get('features', []), 'Features')}
        {self._format_list(self.meta_data.get('data_sources', []), 'Data Sources')}
        {self._format_list(self.meta_data.get('supported_analyses', []), 'Supported Analyses')}
        {self._format_list(self.meta_data.get('report_types', []), 'Report Types')}
        {self._format_list(self.meta_data.get('output_formats', []), 'Output Formats')}
        
        YOUR ROLE: You are an expert analytics assistant. Based on the project capabilities above:
        1. Answer user questions about analytics and reports
        2. Provide insights based on available data sources and analyses
        3. Suggest appropriate analysis methods
        4. Help interpret results and create reports
        5. Be interactive and provide detailed, actionable advice
        """
        return project_context
    
    def _format_list(self, items: list, title: str) -> str:
        """Format list items for better context"""
        if not items:
            return f"{title}: None specified"
        items_str = "\n".join([f"  - {item}" for item in items])
        return f"{title}:\n{items_str}"
    
    def send_message(self, user_message: str) -> str:
        """
        Send message to chatbot and get response
        
        Args:
            user_message (str): User's query
            
        Returns:
            str: AI response
        """
        try:
            # Build conversation context
            context = self._get_system_context()
            
            # Add conversation history for context
            history_context = ""
            for msg in self.conversation_history[-6:]:  # Keep last 6 messages for context
                role = "User" if msg["role"] == "user" else "Assistant"
                history_context += f"{role}: {msg['content']}\n"
            
            full_prompt = f"{context}\n\nCONVERSATION HISTORY:\n{history_context}\nUser: {user_message}\nAssistant:"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            response_text = response.text
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            return response_text
            
        except Exception as e:
            error_msg = f"❌ Error generating response: {str(e)}"
            print(error_msg)
            return error_msg
    
    def generate_sample_analysis(self, analysis_type: str) -> dict:
        """
        Generate sample analysis with visualization
        
        Args:
            analysis_type (str): Type of analysis ('trend', 'correlation', 'summary')
            
        Returns:
            dict: Analysis results with figure and insights
        """
        # Generate sample data
        np.random.seed(42)  # For reproducible results
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        
        sample_data = {
            'date': dates,
            'sales': np.random.normal(1000, 200, 30).cumsum(),
            'users': np.random.randint(800, 1200, 30),
            'conversion_rate': np.random.uniform(2.5, 4.5, 30),
            'revenue': np.random.normal(5000, 1000, 30)
        }
        df = pd.DataFrame(sample_data)
        
        analysis_methods = {
            'trend': self._create_trend_analysis,
            'correlation': self._create_correlation_analysis,
            'summary': self._create_summary_report
        }
        
        if analysis_type in analysis_methods:
            return analysis_methods[analysis_type](df)
        else:
            return self._create_general_analysis(df)
    
    def _create_trend_analysis(self, df: pd.DataFrame) -> dict:
        """Create trend analysis visualization and insights"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Sales trend
        axes[0,0].plot(df['date'], df['sales'], marker='o', linewidth=2, color='blue')
        axes[0,0].set_title('📈 Sales Trend Over Time', fontweight='bold')
        axes[0,0].set_ylabel('Sales')
        axes[0,0].tick_params(axis='x', rotation=45)
        axes[0,0].grid(True, alpha=0.3)
        
        # Users trend
        axes[0,1].plot(df['date'], df['users'], marker='s', linewidth=2, color='green')
        axes[0,1].set_title('👥 Users Trend Over Time', fontweight='bold')
        axes[0,1].set_ylabel('Users')
        axes[0,1].tick_params(axis='x', rotation=45)
        axes[0,1].grid(True, alpha=0.3)
        
        # Conversion rate
        axes[1,0].plot(df['date'], df['conversion_rate'], marker='^', linewidth=2, color='red')
        axes[1,0].set_title('📊 Conversion Rate Trend', fontweight='bold')
        axes[1,0].set_ylabel('Conversion Rate (%)')
        axes[1,0].tick_params(axis='x', rotation=45)
        axes[1,0].grid(True, alpha=0.3)
        
        # Revenue
        axes[1,1].plot(df['date'], df['revenue'], marker='d', linewidth=2, color='purple')
        axes[1,1].set_title('💰 Revenue Trend', fontweight='bold')
        axes[1,1].set_ylabel('Revenue')
        axes[1,1].tick_params(axis='x', rotation=45)
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Calculate insights
        insights = {
            'analysis_type': 'Trend Analysis',
            'time_period': f"{len(df)} days",
            'sales_growth': f"{(df['sales'].iloc[-1] - df['sales'].iloc[0]) / df['sales'].iloc[0] * 100:.1f}%",
            'avg_daily_users': f"{df['users'].mean():.0f}",
            'avg_conversion_rate': f"{df['conversion_rate'].mean():.2f}%",
            'total_revenue': f"${df['revenue'].sum():,.0f}"
        }
        
        return {'figure': fig, 'insights': insights}
    
    def _create_correlation_analysis(self, df: pd.DataFrame) -> dict:
        """Create correlation analysis"""
        numeric_cols = ['sales', 'users', 'conversion_rate', 'revenue']
        correlation_matrix = df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, 
                   annot=True, 
                   cmap='RdYlBu', 
                   center=0,
                   square=True, 
                   ax=ax,
                   fmt='.2f',
                   linewidths=0.5)
        ax.set_title('🔗 Feature Correlation Matrix', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        # Generate correlation insights
        insights = {'analysis_type': 'Correlation Analysis', 'correlations': {}}
        
        for i, col1 in enumerate(correlation_matrix.columns):
            for j, col2 in enumerate(correlation_matrix.columns):
                if i < j:  # Avoid duplicates and self-correlation
                    corr = correlation_matrix.iloc[i, j]
                    strength = 'strong' if abs(corr) > 0.7 else 'moderate' if abs(corr) > 0.5 else 'weak'
                    direction = 'positive' if corr > 0 else 'negative'
                    
                    insights['correlations'][f'{col1}_vs_{col2}'] = {
                        'correlation_coefficient': round(corr, 3),
                        'strength': strength,
                        'direction': direction
                    }
        
        return {'figure': fig, 'insights': insights}
    
    def _create_summary_report(self, df: pd.DataFrame) -> dict:
        """Create comprehensive summary report"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Sales distribution
        axes[0,0].hist(df['sales'], bins=12, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0,0].set_title('Sales Distribution', fontweight='bold')
        axes[0,0].set_xlabel('Sales')
        axes[0,0].set_ylabel('Frequency')
        
        # Users distribution
        axes[0,1].hist(df['users'], bins=12, alpha=0.7, color='lightcoral', edgecolor='black')
        axes[0,1].set_title('Users Distribution', fontweight='bold')
        axes[0,1].set_xlabel('Users')
        axes[0,1].set_ylabel('Frequency')
        
        # Box plot
        box_data = [df['sales'], df['users'], df['revenue']]
        axes[1,0].boxplot(box_data, labels=['Sales', 'Users', 'Revenue'])
        axes[1,0].set_title('Distribution Comparison', fontweight='bold')
        axes[1,0].set_ylabel('Values')
        
        # Conversion rate distribution
        axes[1,1].hist(df['conversion_rate'], bins=12, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[1,1].set_title('Conversion Rate Distribution', fontweight='bold')
        axes[1,1].set_xlabel('Conversion Rate (%)')
        axes[1,1].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        # Statistical summary
        insights = {
            'analysis_type': 'Comprehensive Summary Report',
            'dataset_period': f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}",
            'records_analyzed': len(df),
            'key_metrics': {
                'sales': {
                    'mean': f"${df['sales'].mean():.2f}",
                    'std': f"${df['sales'].std():.2f}",
                    'min': f"${df['sales'].min():.2f}",
                    'max': f"${df['sales'].max():.2f}"
                },
                'users': {
                    'mean': f"{df['users'].mean():.1f}",
                    'std': f"{df['users'].std():.1f}",
                    'min': f"{df['users'].min()}",
                    'max': f"{df['users'].max()}"
                },
                'conversion_rate': {
                    'mean': f"{df['conversion_rate'].mean():.2f}%",
                    'std': f"{df['conversion_rate'].std():.2f}%",
                    'min': f"{df['conversion_rate'].min():.2f}%",
                    'max': f"{df['conversion_rate'].max():.2f}%"
                }
            }
        }
        
        return {'figure': fig, 'insights': insights}
    
    def get_conversation_history(self) -> list:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("✅ Conversation history cleared")