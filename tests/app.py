import streamlit as st
import matplotlib.pyplot as plt
from analytics_chatbot import AnalyticsChatbot

# Page configuration
st.set_page_config(
    page_title="Analytics Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🤖 Analytics Chatbot")
    st.markdown("### Your Interactive Analytics Assistant")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("Gemini API Key:", type="password")
        meta_json_path = st.text_input("Meta JSON Path:", value="project_meta.json")
        
        if st.button("Initialize Chatbot"):
            if api_key and meta_json_path:
                try:
                    st.session_state.chatbot = AnalyticsChatbot(api_key, meta_json_path)
                    st.success("✅ Chatbot initialized!")
                    
                    # Add welcome message
                    welcome_msg = f"Hello! I'm your analytics assistant for **{st.session_state.chatbot.meta_data.get('project_name', 'the project')}**. How can I help you with data analysis today?"
                    st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]
                    
                except Exception as e:
                    st.error(f"❌ Initialization failed: {e}")
            else:
                st.error("Please provide both API key and JSON path")
        
        st.markdown("---")
        st.header("📊 Quick Actions")
        
        if st.session_state.get('chatbot'):
            analysis_type = st.selectbox(
                "Generate Sample Analysis:",
                ["", "trend", "correlation", "summary"]
            )
            
            if st.button("Run Analysis") and analysis_type:
                with st.spinner("Generating analysis..."):
                    result = st.session_state.chatbot.generate_sample_analysis(analysis_type)
                    st.session_state.analysis_result = result
                    st.success("Analysis completed!")
    
    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Initialize messages in session state
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about analytics, reports, or project features..."):
            if st.session_state.get('chatbot'):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Generate and display response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = st.session_state.chatbot.send_message(prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error("Please initialize the chatbot first!")
    
    with col2:
        st.header("📈 Analysis Results")
        
        if st.session_state.get('analysis_result'):
            result = st.session_state.analysis_result
            
            # Display plot
            st.pyplot(result['figure'])
            
            # Display insights
            st.subheader("Key Insights")
            insights = result['insights']
            
            if isinstance(insights, dict):
                for key, value in insights.items():
                    if isinstance(value, dict):
                        st.write(f"**{key.replace('_', ' ').title()}:**")
                        for k, v in value.items():
                            st.write(f"  - {k}: {v}")
                    else:
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        # Project info
        if st.session_state.get('chatbot'):
            st.markdown("---")
            st.header("ℹ️ Project Info")
            meta = st.session_state.chatbot.meta_data
            st.write(f"**Project:** {meta.get('project_name', 'N/A')}")
            st.write(f"**Version:** {meta.get('version', 'N/A')}")
            st.write(f"**Description:** {meta.get('description', 'N/A')}")

if __name__ == "__main__":
    main()