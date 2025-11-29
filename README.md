# CSV AI - Chat with Your Data 📊

A modular web application that allows users to upload CSV files and chat with their data using AI. Built with FastAPI backend and vanilla JavaScript frontend with a GitHub-inspired theme.

## Features

- 📁 **CSV Upload** - Upload and analyze CSV files
- 💬 **AI Chat** - Ask questions about your data using GPT4All
- 🧠 **Memory** - AI remembers previous chat context
- 🎨 **GitHub Theme** - Clean, modern dark theme
- ⚡ **Fast** - Built with FastAPI
- 🔧 **Modular** - Well-organized code structure
- 🖥️ **GPU/CPU Support** - Runs on CUDA if available, falls back to CPU

## Project Structure

```
CSV AI/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── routes/
│   │   ├── csv_routes.py    # CSV upload and info endpoints
│   │   └── chat_routes.py   # Chat endpoints
│   ├── services/
│   │   ├── csv_service.py   # CSV processing logic
│   │   ├── chat_service.py  # Chat orchestration
│   │   └── ai_service.py    # GPT4All model integration
│   ├── models/              # Data models (Pydantic)
│   └── utils/               # Utility functions
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── css/
│   │   └── styles.css       # GitHub theme styles
│   └── js/
│       └── app.js           # Frontend logic
├── ai_model/                # Place GPT4All model here
├── uploads/                 # Uploaded CSV files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) NVIDIA GPU with CUDA for faster AI inference

## Installation & Setup

### 1. Clone or Download the Project

```powershell
cd "z:\GithubProjects\CSV AI"
```

### 2. Create a Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

**Note:** If you have an NVIDIA GPU and want to use CUDA, the `gpt4all[cuda]` package will be installed. If CUDA is not available, the application will automatically fall back to CPU.

### 5. Download AI Model

1. Visit [GPT4All Models](https://gpt4all.io/index.html)
2. Download a GGUF format model (recommended models below)
3. Place the `.gguf` file in the `ai_model/` folder

**Recommended Models:**
- **mistral-7b-instruct-v0.1.Q4_0.gguf** (4-5 GB) - Good balance
- **gpt4all-falcon-newbns-q4_0.gguf** (4 GB) - Fast and accurate
- **orca-mini-3b.gguf** (2 GB) - Lightweight option

### 6. Run the Application

```powershell
cd backend
python main.py
```

The application will start on `http://localhost:8000`

### 7. Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

## Usage

1. **Upload CSV File**
   - Click "Choose File" or drag and drop your CSV file
   - The file will be uploaded and analyzed

2. **View Data Info**
   - See file statistics (rows, columns, memory usage)
   - Click "View Data Preview" to see sample data

3. **Chat with Your Data**
   - Type questions in the chat input
   - Examples:
     - "What are the column names?"
     - "How many rows are in this dataset?"
     - "What is the average value of the sales column?"
     - "Show me summary statistics"

4. **Clear History**
   - Click "Clear History" to start a fresh conversation

## Configuration

### Changing Server Port

Edit `backend/main.py`, line at the bottom:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### AI Model Settings

Edit `backend/services/ai_service.py` to adjust model parameters:
- `max_tokens`: Maximum response length
- `temp`: Temperature (0.0-1.0, higher = more creative)
- `top_k`: Top-K sampling
- `top_p`: Top-P sampling

## Troubleshooting

### CUDA Not Available
If you see "CUDA initialization failed", the app will automatically use CPU. This is normal if you don't have an NVIDIA GPU.

### Model Not Loading
- Ensure the model file is in `ai_model/` folder
- Check that the file is in `.gguf` format
- Verify file isn't corrupted by re-downloading

### Import Errors
Make sure virtual environment is activated and all dependencies are installed:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Port Already in Use
If port 8000 is busy, change the port in `main.py` or kill the process:
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### CORS Errors
The backend allows all origins by default. If you need to restrict, edit `main.py`:
```python
allow_origins=["http://localhost:8000"]
```

## Development

### Running in Development Mode

The server runs with auto-reload enabled by default. Any changes to Python files will automatically restart the server.

### Adding New Features

1. **New API Endpoints**: Add routes in `backend/routes/`
2. **Business Logic**: Add services in `backend/services/`
3. **Frontend**: Edit `frontend/js/app.js` and `frontend/css/styles.css`

## Dependencies

- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **Pandas** - Data manipulation
- **GPT4All** - Local AI model runner
- **Pydantic** - Data validation

## Security Notes

- This is a local development setup
- For production, add authentication and input validation
- Don't expose to public internet without proper security measures
- CSV files are stored in `uploads/` folder

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to fork and modify this project for your needs!

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review GPT4All documentation: https://docs.gpt4all.io/
3. Check FastAPI documentation: https://fastapi.tiangolo.com/

---

**Built with ❤️ using FastAPI, GPT4All, and Vanilla JavaScript**
