import yt_dlp
import urllib.request
import re

def clean_transcript_text(raw_text):
    """
    Removes timestamps, metadata tags, and repetitive fragments 
    common in YouTube auto-generated captions.
    """
    # 1. Remove timestamps like <00:00:09.440>
    text = re.sub(r'<[^>]+>', '', raw_text)
    
    # 2. Remove tags like [Music], [Applause], or Kind: captions
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'Kind: captions|Language: \w+', '', text, flags=re.IGNORECASE)
    
    # 3. Fix the "repeated fragments" issue
    # Auto-captions often look like: "today we today we today we will learn"
    words = text.split()
    cleaned_words = []
    for i in range(len(words)):
        # Only add the word if it isn't an exact duplicate of the previous one
        if i == 0 or words[i].lower() != words[i-1].lower():
            cleaned_words.append(words[i])
            
    return " ".join(cleaned_words).strip()

def get_clean_transcript(video_url):
    ydl_opts = {
        'skip_download': True,
        'writesubscriptions': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            if 'requested_subtitles' in info and 'en' in info['requested_subtitles']:
                sub_url = info['requested_subtitles']['en']['url']
                
                with urllib.request.urlopen(sub_url) as response:
                    vtt_data = response.read().decode('utf-8')
                    
                    # Initial VTT structure cleaning
                    lines = vtt_data.split('\n')
                    content_lines = []
                    for line in lines:
                        # Filter out VTT headers and timing lines
                        if '-->' not in line and line.strip() and not line.strip().isdigit() and 'WEBVTT' not in line:
                            content_lines.append(line.strip())
                    
                    raw_text = " ".join(content_lines)
                    
                    # CRITICAL STEP: Run the advanced cleaner
                    final_text = clean_transcript_text(raw_text)
                    
                    return final_text if len(final_text) > 50 else "Transcript too short after cleaning."
            
            return "Error: No English subtitles found for this video."

    except Exception as e:
        return f"yt_dlp Fetcher Error: {e}"