import streamlit as st

def methodology():
    st.title("Methodology")
    
    st.markdown("""
    ### Data Flow and Implementation Details
    
    Our application is built around two main use cases:
    
    1. **Chat with Information**  
    Users interact via a chat interface that uses large language models to understand and improve content drafts.
    
    2. **Intelligent Search**  
    Enables users to query a curated content playbook for governance best practices and guidelines.
    
    ---
    
    ### Process Flowcharts
    
    #### 1. Chat with Information Flow
    """)
    
    # st.image("resources/chat_flowchart.png", caption="Chat with Information Flowchart", use_column_width=True)
    
    st.markdown("""
    #### 2. Intelligent Search Flow
    """)
    
    # st.image("resources/search_flowchart.png", caption="Intelligent Search Flowchart", use_column_width=True)

if __name__ == "__main__":
    methodology()