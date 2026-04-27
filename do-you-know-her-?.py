import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os

CHANNEL_NAME = "BigJim713" 

def get_joke_words(text):
    words = re.findall(r'\b\w+[eo]r\b', text, re.IGNORECASE)
    # Filter
    return [word for word in words if len(word) > 4]

def main():
    print(f"Scraping video list for {CHANNEL_NAME}... this might take a minute.")
    videos = scrapetube.get_channel(channel_username=CHANNEL_NAME)
    
    # Create a folder
    output_folder = f"{CHANNEL_NAME}_Jokes"
    os.makedirs(output_folder, exist_ok=True)
    print(f"Created folder: '{output_folder}'. Files will be saved here.\n")
    
    for video in videos:
        video_id = video['videoId']
        
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            jokes_to_write = [] 
            
            for entry in transcript:
                text = entry['text'].replace('\n', ' ') 
                joke_words = get_joke_words(text)
                
                if joke_words:
          
                    for word in joke_words: 
                        timestamp = entry['start']
                        minutes = int(timestamp // 60)
                        seconds = int(timestamp % 60)
                        
                        #formating it
                        log_entry = (
                            f"[{minutes:02d}:{seconds:02d}] "
                            f"Setup: \"{text.strip()}\"\n"
                            f"         Punchline: {word.capitalize()}? I barely know her!\n"
                        )
                        jokes_to_write.append(log_entry)
        
            if jokes_to_write:
                filename = os.path.join(output_folder, f"video_{video_id}.txt")
                
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(f"--- 'I Barely Know Her' Log ---\n")
                    file.write(f"Video URL: https://youtu.be/{video_id}\n")
                    file.write(f"========================================\n\n")
                    
                    for joke in jokes_to_write:
                        file.write(joke)
                
                print(f"Created '{filename}' ({len(jokes_to_write)} jokes found)")
                        
        except Exception as e:
            pass
            
    print(f"\nMission Accomplished! All files have been sorted into the '{output_folder}' folder.")

if __name__ == "__main__":
    main()
