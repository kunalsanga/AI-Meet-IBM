# 🚀 AI Meeting Assistant using IBM Granite

An intelligent web application that automates meeting minutes and task extraction using IBM's Granite models.

## 🎯 Objective

Transform recorded meeting audio into structured summaries with actionable insights using:
- **IBM Granite Speech 8B** for audio transcription
- **IBM Granite 3.3 Instruct** for summarization and task extraction

## ✨ Features

- 📁 **Audio Upload**: Support for MP3/WAV files
- 🎤 **Speech-to-Text**: High-accuracy transcription using Granite Speech 8B
- 📝 **Smart Summarization**: Structured meeting summaries with key topics
- ✅ **Action Item Extraction**: Automatic identification of tasks, deadlines, and owners
- 🎨 **Clean UI**: User-friendly Streamlit interface
- 📊 **Visual Output**: Organized display of transcript, summary, and tasks

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Models**: IBM Granite Speech 8B + Granite 3.3 Instruct
- **Audio Processing**: librosa, pydub
- **Data Visualization**: Plotly, Pandas

## 📁 Project Structure

```
AI meet IBM/
├── app.py                 # Main Streamlit application
├── utils/
│   ├── granite_api.py     # IBM Granite API integration
│   └── summarizer.py      # Summarization and prompt engineering
├── samples/
│   └── sample_meeting.mp3 # Sample audio file
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up IBM Credentials
Create a `.env` file in the project root:
```env
IBM_API_KEY=your_ibm_api_key_here
IBM_URL=your_ibm_service_url_here
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Access the App
Open your browser and navigate to `http://localhost:8501`

## 🎯 Usage

1. **Upload Audio**: Drag and drop or select an MP3/WAV file
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

## 🔮 Future Enhancements

- [ ] Email integration for automatic meeting minutes
- [ ] Slack bot for team notifications
- [ ] Calendar integration for action item tracking
- [ ] Multi-language support
- [ ] Advanced analytics and insights

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

---

**Built with ❤️ using IBM Granite AI Models** 