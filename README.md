# YOUTUBE Downloader

![GitHub](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20MacOS%20%7C%20Linux%20%7C%20Android-lightgrey)

A professional-grade YouTube video and audio downloader with a beautiful interactive terminal interface.

![Screenshot](/api/placeholder/800/400)

## Features

- **Stunning Terminal UI** - Colorful ASCII art banner and professional design
- **High-Quality Downloads** - Download videos in the best available quality
- **Audio Extraction** - Extract MP3 audio with embedded thumbnails and metadata
- **Real-time Progress Tracking** - Beautiful progress bars with time estimates
- **Streamlined Experience** - Simple interface with intuitive operation
- **Multi-platform Support** - Works on Windows, macOS, Linux, and Android (Termux)
- **Continuous Operation** - Download multiple videos in a single session

## Requirements

- Python 3.6 or higher
- FFmpeg (required for media conversion)
- Internet connection

## Dependencies

The script requires the following Python libraries:
- yt-dlp
- rich
- colorama

## Installation Guide

### Standard Installation (Windows, macOS, Linux)

1. **Clone this repository:**
   ```bash
   git clone https://github.com/FakeScoutBot/TermuxYTDownloader.git
   cd TermuxYTDownloader
   ```

2. **Install required Python packages:**
   ```bash
   pip install yt-dlp rich colorama
   ```

3. **Install FFmpeg:**
   - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS:** `brew install ffmpeg`
   - **Ubuntu/Debian:** `sudo apt install ffmpeg`
   - **Fedora:** `sudo dnf install ffmpeg`

4. **Run the script:**
   ```bash
   python3 yt.py
   ```

### Termux Installation (Android)

1. **Update packages and install Python:**
   ```bash
   pkg update
   pkg upgrade
   pkg install python
   ```

2. **Install FFmpeg:**
   ```bash
   pkg install ffmpeg
   ```

3. **Install required Python libraries:**
   ```bash
   pip install yt-dlp rich colorama
   ```

4. **Download the script:**
   ```bash
   curl -o youtube_downloader.py https://raw.githubusercontent.com/FakeScoutBot/TermuxYTDownloader/main/yt.py
   ```

5. **Run the script:**
   ```bash
   python yt.py
   ```

### Quick Setup for Termux (Single Command)

Copy and paste this single command to get everything set up:

```bash
pkg update && pkg upgrade -y && pkg install python ffmpeg -y && pip install yt-dlp rich colorama && curl -o yt.py https://raw.githubusercontent.com/FakeScoutBot/TermuxYTDownloader/main/yt.py && python yt.py
```

## Usage

1. Run the script:
   ```bash
   python yt.py
   ```

2. Enter a valid YouTube URL when prompted.

3. Choose to download video or audio:
   - **video**: Downloads full video in best quality
   - **audio**: Extracts audio in MP3 format with embedded thumbnail

4. Specify an output directory (defaults to "downloads").

5. After download completes, choose whether to download another file or exit.

## Troubleshooting

### Common Issues:

1. **"FFmpeg not found" error:**
   - Make sure FFmpeg is properly installed and available in your system PATH

2. **Permission denied errors:**
   - Run the command with appropriate permissions
   - For Termux, make sure storage permission is granted: `termux-setup-storage`

3. **SSL Certificate errors:**
   - Update your Python installation or install certificates package

4. **Output directory issues:**
   - Make sure the specified output directory exists or can be created
   - Check if you have write permissions for that location

## Legal Disclaimer

This tool is for personal use only. Downloading copyrighted content might be illegal in your country. Users are responsible for their own actions and compliance with local laws.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Core downloading functionality
- [Rich](https://github.com/Textualize/rich) - Terminal formatting and UI
- [Colorama](https://github.com/tartley/colorama) - Cross-platform colored terminal output
