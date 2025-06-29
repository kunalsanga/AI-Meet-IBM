# 🚀 AI Meeting Assistant using IBM Granite

An intelligent web application that automates meeting minutes and task extraction using IBM's Granite models.

## 🎯 Objective

Transform recorded meeting audio into structured summaries with actionable insights using:
- **IBM Granite Speech 8B** for audio transcription
- **IBM Granite 3.3 Instruct** for summarization and task extraction

## ✨ Features

- 📁 **Audio Upload**: Support for MP3/WAV/M4A/FLAC files
- 🎤 **Speech-to-Text**: High-accuracy transcription using Granite Speech 8B
- 📝 **Smart Summarization**: Structured meeting summaries with key topics
- ✅ **Action Item Extraction**: Automatic identification of tasks, deadlines, and owners
- 🎨 **Clean UI**: User-friendly Streamlit interface
- 📊 **Visual Output**: Organized display of transcript, summary, and tasks
- 📈 **Analytics**: Charts and insights for task distribution and timelines
- 📤 **Export Options**: Download results in Text, Markdown, or JSON formats

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Models**: IBM Granite Speech 8B + Granite 3.3 Instruct
- **Audio Processing**: librosa, pydub
- **Data Visualization**: Plotly, Pandas
- **Containerization**: Docker

## 📁 Project Structure

```
AI meet IBM/
├── app.py                 # Main Streamlit application
├── Dockerfile             # Docker configuration
├── utils/
│   ├── granite_api.py     # IBM Granite API integration
│   └── summarizer.py      # Summarization and prompt engineering
├── samples/
│   └── sample_meeting.mp3 # Sample audio file
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
└── README.md             # Project documentation
```

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

#### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

#### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/kunalsanga/AI-Meet-IBM.git
   cd AI-Meet-IBM
   ```

2. **Set up environment variables**
   ```bash
   # Copy the example file
   cp env_example.txt .env
   
   # Edit .env with your IBM credentials
   IBM_API_KEY=your_ibm_api_key_here
   IBM_PROJECT_ID=your_project_id_here
   IBM_URL=https://us-south.ml.cloud.ibm.com
   DEMO_MODE=true
   ```

3. **Build the Docker image**
   ```bash
   docker build -t ai-meet-ibm .
   ```

4. **Run the application**
   ```bash
   docker run -p 8501:8501 ai-meet-ibm
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

### Option 2: Local Installation

#### Prerequisites
- Python 3.10 or 3.11 (Python 3.13 is not supported due to dependency compatibility)
- pip package manager

#### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/kunalsanga/AI-Meet-IBM.git
   cd AI-Meet-IBM
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   # Copy the example file
   cp env_example.txt .env
   
   # Edit .env with your IBM credentials
   IBM_API_KEY=your_ibm_api_key_here
   IBM_PROJECT_ID=your_project_id_here
   IBM_URL=https://us-south.ml.cloud.ibm.com
   DEMO_MODE=true
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## �� Usage

1. **Upload Audio**: Drag and drop or select an MP3/WAV/M4A/FLAC file
2. **Process**: Click "Process Meeting" to start transcription and analysis
3. **Review Results**: View the transcript, summary, and extracted action items
4. **Export**: Download results or share via email/Slack (optional)

## 🔧 IBM Granite Integration

### Granite Speech 8B (ASR)
- Handles audio transcription with high accuracy
- Supports multiple languages and accents
- Processes long-form audio efficiently

### Granite 3.3 Instruct (Summarization)
- Generates structured meeting summaries
- Extracts action items, deadlines, and owners
- Uses advanced prompt engineering for optimal results

## 📊 Sample Output

### Meeting Summary
- **Topics Discussed**: Project timeline, resource allocation, technical challenges
- **Key Decisions**: Launch date set to Q2 2024, additional developer hired
- **Action Items**: 
  - John: Complete API documentation by Friday
  - Sarah: Review budget proposal by Monday
  - Team: Schedule follow-up meeting next week

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Real-time Processing**: Live progress indicators
- **Export Options**: Download results in multiple formats
- **Dark/Light Mode**: Toggle between themes
- **Analytics Dashboard**: Charts and insights for better understanding

## 🚀 Deployment Options

### Local Development
- Use Docker or local Python installation as described above

### Cloud Deployment
- **IBM Cloud Code Engine**: Deploy your Docker image to IBM Cloud
- **Heroku**: Use Heroku's container deployment
- **AWS/Azure/GCP**: Deploy to cloud container services
- **Streamlit Cloud**: Deploy directly from GitHub (note: requires compatible Python version)

## 🔮 Future Enhancements

- [ ] Email integration for automatic meeting minutes
- [ ] Slack bot for team notifications
- [ ] Calendar integration for action item tracking
- [ ] Multi-language support
- [ ] Advanced analytics and insights
- [ ] Real-time collaboration features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the development team.

## 🔧 Troubleshooting

### Docker Issues
- Make sure Docker Desktop is running
- Check your internet connection for Docker Hub access
- If you get network errors, try restarting Docker Desktop

### Python Compatibility
- Use Python 3.10 or 3.11 (Python 3.13 is not supported)
- If you encounter dependency issues, use the Docker option

### IBM API Issues
- Verify your API key and project ID are correct
- Check that your IBM Watsonx.ai service is active
- Use demo mode (`DEMO_MODE=true`) for testing without API credentials

---

**Built with ❤️ using IBM Granite AI Models** 