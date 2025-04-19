import os
import sys
import time
from urllib.parse import urlparse, parse_qs
import re
import yt_dlp
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.text import Text
from rich.table import Table
from rich import box
from rich.prompt import Prompt, Confirm
import colorama
from colorama import Fore, Back, Style
import platform

# Initialize colorama for cross-platform colored terminal output
colorama.init(autoreset=True)

# Initialize Rich console
console = Console()

# ASCII Art Banner
BANNER = f"""
{Fore.CYAN}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ {Fore.YELLOW}██╗   ██╗{Fore.RED}██████╗ {Fore.GREEN}██╗   ██╗{Fore.BLUE}████████╗{Fore.MAGENTA}██╗   ██╗{Fore.CYAN}██████╗ ███████╗{Fore.YELLOW} ┃
┃ {Fore.YELLOW}╚██╗ ██╔╝{Fore.RED}██╔══██╗{Fore.GREEN}██║   ██║{Fore.BLUE}╚══██╔══╝{Fore.MAGENTA}██║   ██║{Fore.CYAN}██╔══██╗██╔════╝{Fore.YELLOW} ┃
┃ {Fore.YELLOW} ╚████╔╝ {Fore.RED}██║  ██║{Fore.GREEN}██║   ██║{Fore.BLUE}   ██║   {Fore.MAGENTA}██║   ██║{Fore.CYAN}██████╔╝█████╗  {Fore.YELLOW} ┃
┃ {Fore.YELLOW}  ╚██╔╝  {Fore.RED}██║  ██║{Fore.GREEN}██║   ██║{Fore.BLUE}   ██║   {Fore.MAGENTA}██║   ██║{Fore.CYAN}██╔══██╗██╔══╝  {Fore.YELLOW} ┃
┃ {Fore.YELLOW}   ██║   {Fore.RED}██████╔╝{Fore.GREEN}╚██████╔╝{Fore.BLUE}   ██║   {Fore.MAGENTA}╚██████╔╝{Fore.CYAN}██████╔╝███████╗{Fore.YELLOW} ┃
┃ {Fore.YELLOW}   ╚═╝   {Fore.RED}╚═════╝ {Fore.GREEN} ╚═════╝ {Fore.BLUE}   ╚═╝   {Fore.MAGENTA} ╚═════╝ {Fore.CYAN}╚═════╝ ╚══════╝{Fore.YELLOW} ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.RED}「YOUTUBE DOWNLOADER v1.0」{Fore.CYAN}━━━━━━━━━━━━━━━┛
"""

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def validate_url(url):
    """Validate if the URL is a valid YouTube URL."""
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)[\w-]+(\S*)?$'
    return bool(re.match(youtube_regex, url))

def format_filesize(bytes):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"

class YTLogger:
    """Custom logger for yt-dlp."""
    def __init__(self, progress):
        self.progress = progress
        self.task_id = None
        self.downloaded_bytes = 0
        self.total_bytes = 0
        self.last_update = 0
        self.filename = ""

    def debug(self, msg):
        if msg.startswith('[download]'):
            # Parse download progress
            if 'Destination:' in msg:
                self.filename = msg.split('Destination: ')[1]
                if self.task_id is not None:
                    self.progress.update(self.task_id, description=f"Downloading: {os.path.basename(self.filename)}")
            elif 'has already been downloaded' in msg:
                if self.task_id is None:
                    self.task_id = self.progress.add_task("", total=100, completed=100)
                self.progress.update(self.task_id, description=f"[green]Already downloaded: {os.path.basename(self.filename)}")
            elif '% of' in msg:
                try:
                    # Extract percentage
                    percent_str = msg.split('[download]')[1].split('%')[0].strip()
                    percent = float(percent_str)
                    
                    if self.task_id is None:
                        self.task_id = self.progress.add_task("", total=100)
                    
                    self.progress.update(self.task_id, completed=percent)
                except (ValueError, IndexError):
                    pass

    def warning(self, msg):
        pass

    def error(self, msg):
        console.print(f"[bold red]Error: {msg}")

def download_with_progress(url, options):
    """Download with a fancy progress bar."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=50),
        TextColumn("[bold green]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        logger = YTLogger(progress)
        options["logger"] = logger
        
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
                return True
        except Exception as e:
            console.print(f"\n[bold red]Download failed: {str(e)}")
            return False

def show_completion_animation(filename):
    """Show a completion animation."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]Processing..."),
        console=console
    ) as progress:
        task = progress.add_task("", total=100)
        for i in range(101):
            progress.update(task, completed=i)
            time.sleep(0.01)
    
    # Success message
    console.print("\n[bold green]✓ Download completed successfully!")
    console.print(f"[cyan]File saved in: [yellow]{filename}")

def download_video(url, output_path="downloads"):
    """Download video with best quality."""
    filename = os.path.join(output_path, "%(title)s.%(ext)s")
    options = {
        "outtmpl": filename,
        "format": "bv*+ba/best",  # Best video + best audio
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
        ],
    }
    
    console.print(Panel("[bold]Downloading video in best quality...", border_style="cyan"))
    success = download_with_progress(url, options)
    
    if success:
        show_completion_animation(output_path)
        return True
    return False

def download_audio(url, output_path="downloads"):
    """Download audio with best quality."""
    filename = os.path.join(output_path, "%(title)s.%(ext)s")
    options = {
        "outtmpl": filename,
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "noplaylist": True,
        "writethumbnail": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "320"},
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata"}
        ],
    }
    
    console.print(Panel("[bold]Downloading audio in best quality...", border_style="cyan"))
    success = download_with_progress(url, options)
    
    if success:
        show_completion_animation(output_path)
        return True
    return False

def main():
    """Main function to run the program."""
    try:
        while True:
            # Clear screen and show banner
            clear_screen()
            print(BANNER)
            
            # Create downloads directory
            os.makedirs("downloads", exist_ok=True)
            
            # Get URL
            while True:
                url = Prompt.ask("\n[bold cyan]Enter YouTube video URL")
                if validate_url(url):
                    break
                console.print("[bold red]❌ Invalid YouTube URL! Please try again.")
            
            # Ask for download type
            download_type = Prompt.ask(
                "\n[bold cyan]Choose download type",
                choices=["video", "audio"],
                default="video"
            )
            
            # Select output path
            output_path = Prompt.ask(
                "[bold cyan]Output directory",
                default="downloads"
            )
            os.makedirs(output_path, exist_ok=True)
            
            # Download based on type
            success = False
            if download_type == "video":
                success = download_video(url, output_path)
            else:  # audio
                success = download_audio(url, output_path)
            
            # Ask if user wants to download more or exit
            if not Confirm.ask("\n[bold yellow]Do you want to download another file?", default=True):
                break
        
        # Final message
        console.print("\n[bold green]✨ Thank you for using SCOUT Downloader! ✨")
        
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Program interrupted by user. Exiting...")
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred: {str(e)}")
        console.print("[bold yellow]Please try again or report this issue.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"[bold red]Critical error: {str(e)}")
        sys.exit(1)