# 🔒 Privacy Cleaner - Metadata Remover

A Streamlit web application that removes metadata from various file types, helping you protect your privacy by stripping sensitive information from your files.

## ✨ Features

- 📷 **Images**: Remove EXIF data from JPG, JPEG, PNG files
- 📄 **PDF**: Clean metadata from PDF documents
- 📝 **Word Documents**: Strip metadata from .docx files
- 🎵 **Audio**: Remove ID3 tags from MP3 and WAV files
- 🎬 **Video**: Clean metadata from MP4 video files

## 🛠️ Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/your-username/privacy-cleaner.git
cd privacy-cleaner
```

2. **Create a virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. **Run the Streamlit app**
```bash
streamlit run app.py
```

2. **Open in browser**
   - Streamlit will automatically open at `http://localhost:8501`

3. **Use the app**
   - Select the file type you want to clean
   - Upload your file
   - View detected metadata
   - Download the cleaned file

## 📦 Dependencies

- **streamlit** - Web app framework
- **Pillow** - Image processing
- **pypdf** - PDF manipulation
- **python-docx** - Word document handling
- **mutagen** - Audio/video metadata handling

## 🌐 Deploy to Streamlit Cloud (Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Connect your GitHub repository
5. Select your repo, branch, and `app.py` file
6. Click **Deploy**

Your app will be live on the internet! 🎉

## ⚠️ Important Notes

- Original files are not modified
- Downloaded files contain no metadata
- Large files may take longer to process
- Supported formats: JPG, JPEG, PNG, PDF, DOCX, MP3, WAV, MP4
