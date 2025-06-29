"""
AI Meeting Assistant - Main Streamlit Application

A web application that uses IBM Granite models to transcribe meeting audio,
summarize content, and extract action items automatically.
"""

import streamlit as st
import os
import tempfile
import time
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import our custom modules
from utils.granite_api import granite_api
from utils.summarizer import summarizer

# Page configuration
st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .action-item {
        background-color: #f8f9fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .priority-high {
        border-left-color: #dc3545;
    }
    .priority-medium {
        border-left-color: #ffc107;
    }
    .priority-low {
        border-left-color: #28a745;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🎤 AI Meeting Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform meeting audio into actionable insights using IBM Granite AI</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model status
        if granite_api.mock_mode:
            st.warning("🔧 Running in Demo Mode")
            st.info("Using mock data for demonstration. Set IBM_API_KEY in .env file for live processing.")
        else:
            st.success("✅ Connected to IBM Granite")
        
        # Export options
        st.subheader("📤 Export Options")
        export_format = st.selectbox(
            "Export Format",
            ["Text", "Markdown", "JSON"],
            help="Choose the format for downloading results"
        )
        
        # Processing options
        st.subheader("🔧 Processing Options")
        enable_insights = st.checkbox("Generate Insights", value=True)
        enable_timeline = st.checkbox("Timeline Analysis", value=True)
        
        st.divider()
        
        # About section
        st.subheader("ℹ️ About")
        st.markdown("""
        **Powered by:**
        - IBM Granite Speech 8B (ASR)
        - IBM Granite 3.3 Instruct (Summarization)
        
        **Features:**
        - Audio transcription
        - Smart summarization
        - Action item extraction
        - Timeline analysis
        """)
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["🎤 Upload & Process", "📊 Results", "📈 Analytics"])
    
    with tab1:
        upload_and_process_tab()
    
    with tab2:
        results_tab()
    
    with tab3:
        analytics_tab()


def upload_and_process_tab():
    """Handle file upload and processing."""
    
    # File upload section
    st.header("📁 Upload Meeting Audio")
    
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'wav', 'm4a', 'flac'],
        help="Supported formats: MP3, WAV, M4A, FLAC"
    )
    
    if uploaded_file is not None:
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Name", uploaded_file.name)
        with col2:
            st.metric("File Size", f"{uploaded_file.size / 1024 / 1024:.2f} MB")
        with col3:
            st.metric("File Type", uploaded_file.type or "Unknown")
        
        # Process button
        if st.button("🚀 Process Meeting", type="primary", use_container_width=True):
            process_audio_file(uploaded_file)


def process_audio_file(uploaded_file):
    """Process the uploaded audio file."""
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name
        
        # Step 1: Transcription
        status_text.text("🎤 Transcribing audio...")
        progress_bar.progress(25)
        
        transcript = granite_api.transcribe_audio(temp_path)
        
        # Step 2: Summarization
        status_text.text("📝 Analyzing and summarizing...")
        progress_bar.progress(50)
        
        summary_data = granite_api.summarize_text(transcript)
        
        # Step 3: Enhancement
        status_text.text("🔍 Enhancing results...")
        progress_bar.progress(75)
        
        enhanced_summary = summarizer.enhance_summary(summary_data)
        
        # Step 4: Complete
        status_text.text("✅ Processing complete!")
        progress_bar.progress(100)
        
        # Store results in session state
        st.session_state.transcript = transcript
        st.session_state.summary = enhanced_summary
        st.session_state.processed = True
        
        # Clean up temp file
        os.unlink(temp_path)
        
        # Show success message
        st.success("🎉 Meeting processed successfully! Check the Results tab to view your analysis.")
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        progress_bar.progress(0)
        status_text.text("")


def results_tab():
    """Display processing results."""
    
    st.header("📊 Meeting Analysis Results")
    
    if not st.session_state.get('processed', False):
        st.info("👆 Upload and process an audio file to see results here.")
        return
    
    # Get data from session state
    transcript = st.session_state.get('transcript', '')
    summary = st.session_state.get('summary', {})
    
    # Create tabs for different views
    result_tab1, result_tab2, result_tab3, result_tab4 = st.tabs([
        "📋 Summary", "✅ Action Items", "📝 Full Transcript", "📤 Export"
    ])
    
    with result_tab1:
        display_summary(summary)
    
    with result_tab2:
        display_action_items(summary)
    
    with result_tab3:
        display_transcript(transcript)
    
    with result_tab4:
        display_export_options(summary)


def display_summary(summary):
    """Display the meeting summary."""
    
    # Header metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Meeting Type", summary.get('metadata', {}).get('meeting_type', 'Unknown'))
    
    with col2:
        st.metric("Duration", summary.get('metadata', {}).get('estimated_duration', 'Unknown'))
    
    with col3:
        st.metric("Action Items", summary.get('metadata', {}).get('total_action_items', 0))
    
    with col4:
        st.metric("Topics", len(summary.get('topics_discussed', [])))
    
    # Main summary
    st.subheader("📝 Executive Summary")
    st.write(summary.get('summary', 'No summary available.'))
    
    # Topics discussed
    st.subheader("🗣️ Topics Discussed")
    topics = summary.get('topics_discussed', [])
    if topics:
        for i, topic in enumerate(topics, 1):
            st.write(f"{i}. {topic}")
    else:
        st.info("No specific topics identified.")
    
    # Key decisions
    st.subheader("🎯 Key Decisions")
    decisions = summary.get('key_decisions', [])
    if decisions:
        for i, decision in enumerate(decisions, 1):
            st.write(f"{i}. {decision}")
    else:
        st.info("No specific decisions identified.")
    
    # Next steps
    st.subheader("🔄 Next Steps")
    next_steps = summary.get('next_steps', '')
    if next_steps:
        st.write(next_steps)
    else:
        st.info("No next steps identified.")
    
    # Insights
    insights = summary.get('insights', [])
    if insights:
        st.subheader("💡 Insights")
        for insight in insights:
            st.info(insight)


def display_action_items(summary):
    """Display action items in an organized format."""
    
    action_items = summary.get('action_items', [])
    
    if not action_items:
        st.info("No action items identified in this meeting.")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        priority_filter = st.selectbox(
            "Filter by Priority",
            ["All", "High", "Medium", "Low"]
        )
    
    with col2:
        owner_filter = st.selectbox(
            "Filter by Owner",
            ["All"] + list(set([item.get('owner', 'Unknown') for item in action_items]))
        )
    
    with col3:
        timeline_filter = st.selectbox(
            "Filter by Timeline",
            ["All", "Immediate", "This Week", "Next Week", "Future"]
        )
    
    # Filter action items
    filtered_items = action_items
    
    if priority_filter != "All":
        filtered_items = [item for item in filtered_items if item.get('priority') == priority_filter]
    
    if owner_filter != "All":
        filtered_items = [item for item in filtered_items if item.get('owner') == owner_filter]
    
    if timeline_filter != "All":
        timeline_map = {
            "Immediate": "immediate",
            "This Week": "this_week", 
            "Next Week": "next_week",
            "Future": "future"
        }
        timeline_key = timeline_map.get(timeline_filter)
        if timeline_key:
            timeline_items = summary.get('timeline', {}).get(timeline_key, [])
            filtered_items = [item for item in filtered_items if item in timeline_items]
    
    # Display filtered items
    st.subheader(f"✅ Action Items ({len(filtered_items)} found)")
    
    for item in filtered_items:
        priority_class = f"priority-{item.get('priority', 'medium').lower()}"
        
        with st.container():
            st.markdown(f"""
            <div class="action-item {priority_class}">
                <h4>{item.get('task', 'No task description')}</h4>
                <p><strong>Owner:</strong> {item.get('owner', 'Unassigned')} | 
                   <strong>Priority:</strong> {item.get('priority', 'Medium')} | 
                   <strong>Deadline:</strong> {item.get('deadline', 'No deadline')}</p>
                <p><strong>Effort:</strong> {item.get('estimated_effort', 'Not estimated')}</p>
            </div>
            """, unsafe_allow_html=True)


def display_transcript(transcript):
    """Display the full transcript."""
    
    st.subheader("📝 Full Meeting Transcript")
    
    # Add copy button
    if st.button("📋 Copy Transcript"):
        st.write("Transcript copied to clipboard!")
    
    # Display transcript
    st.text_area(
        "Transcript",
        value=transcript,
        height=400,
        disabled=True,
        help="Full meeting transcript generated by IBM Granite Speech 8B"
    )


def display_export_options(summary):
    """Display export options."""
    
    st.subheader("📤 Export Results")
    
    # Export format selection
    export_format = st.selectbox(
        "Choose Export Format",
        ["Text", "Markdown", "JSON"],
        help="Select the format for your exported meeting summary"
    )
    
    # Generate export content
    format_map = {"Text": "text", "Markdown": "markdown", "JSON": "json"}
    export_content = summarizer.format_for_export(summary, format_map[export_format])
    
    # Display preview
    st.subheader("Preview")
    if export_format == "JSON":
        st.json(summary)
    else:
        st.text_area("Export Preview", value=export_content, height=300, disabled=True)
    
    # Download button
    file_extension = {"Text": "txt", "Markdown": "md", "JSON": "json"}
    filename = f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension[export_format]}"
    
    st.download_button(
        label=f"📥 Download {export_format}",
        data=export_content,
        file_name=filename,
        mime="text/plain",
        use_container_width=True
    )


def analytics_tab():
    """Display analytics and insights."""
    
    st.header("📈 Meeting Analytics")
    
    if not st.session_state.get('processed', False):
        st.info("👆 Process a meeting to see analytics here.")
        return
    
    summary = st.session_state.get('summary', {})
    
    # Analytics overview
    col1, col2 = st.columns(2)
    
    with col1:
        # Action items by priority
        action_items = summary.get('action_items', [])
        if action_items:
            priority_counts = {}
            for item in action_items:
                priority = item.get('priority', 'Unknown')
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            fig_priority = px.pie(
                values=list(priority_counts.values()),
                names=list(priority_counts.keys()),
                title="Action Items by Priority",
                color_discrete_map={
                    'High': '#dc3545',
                    'Medium': '#ffc107', 
                    'Low': '#28a745'
                }
            )
            st.plotly_chart(fig_priority, use_container_width=True)
    
    with col2:
        # Action items by owner
        if action_items:
            owner_counts = {}
            for item in action_items:
                owner = item.get('owner', 'Unknown')
                owner_counts[owner] = owner_counts.get(owner, 0) + 1
            
            fig_owner = px.bar(
                x=list(owner_counts.keys()),
                y=list(owner_counts.values()),
                title="Action Items by Owner",
                labels={'x': 'Owner', 'y': 'Number of Tasks'}
            )
            st.plotly_chart(fig_owner, use_container_width=True)
    
    # Timeline analysis
    st.subheader("⏰ Timeline Analysis")
    timeline = summary.get('timeline', {})
    
    if timeline:
        timeline_data = []
        for period, items in timeline.items():
            timeline_data.append({
                'Period': period.replace('_', ' ').title(),
                'Count': len(items)
            })
        
        if timeline_data:
            fig_timeline = px.bar(
                timeline_data,
                x='Period',
                y='Count',
                title="Action Items by Timeline",
                color='Count',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Meeting insights
    st.subheader("💡 Meeting Insights")
    insights = summary.get('insights', [])
    
    if insights:
        for i, insight in enumerate(insights, 1):
            st.info(f"{i}. {insight}")
    else:
        st.info("No specific insights generated for this meeting.")


if __name__ == "__main__":
    # Initialize session state
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    
    main() 