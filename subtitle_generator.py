from http import client
import os
import subprocess
from moviepy import VideoFileClip
from googletrans import Translator
from google.cloud import speech_v1p1 as speech
from pysrt import SubRipFile, SubRipTime

def extract_audio(video_path, audio_path):
    """Extracts audio from a video file."""
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        print(f"Audio extracted to {audio_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")

def generate_subtitles(audio_path, output_file, language="en-US"):  # Added language parameter
    """Generates subtitles using a speech-to-text engine (replace with your preferred engine)."""
    try:
        # Replace this with your actual speech-to-text engine implementation
        # Here's an example using Google Speech-to-Text (requires additional setup and credentials)
        # ... (Authentication and configuration for Google Speech-to-Text)

        with open(audio_path, 'rb') as audio_file:
            content = audio_file.read()

        audio = speech.Audio(content=content)
        config = speech.RecognitionConfig(
            language_code=language,
            audio_channel_count=audio.channels,
            sample_rate_hertz=audio.sample_rate
        )

        response = client.recognize(config=config, audio=audio)

        # Extract text from the response
        text = ""
        for result in response.results:
            for alternative in result.alternatives:
                text += f"{alternative.transcript}\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"Subtitles generated to {output_file}")

    except Exception as e:
        print(f"Error generating subtitles: {e}")

def translate_subtitles(subtitle_file, src_lang, tgt_lang):
    """Translates subtitles to the target language."""
    try:
        subs = SubRipFile(subtitle_file)
        translator = Translator()

        for sub in subs:
            sub.text = translator.translate(sub.text, src=src_lang, dest=tgt_lang).text

        subs.save(f"{subtitle_file.replace('.srt', f'_{tgt_lang}.srt')}")
        print(f"Subtitles translated to {tgt_lang}")

    except Exception as e:
        print(f"Error translating subtitles: {e}")

if __name__ == "__main__":
    video_path = "input.mp4"  # Replace with the actual video path
    audio_path = "audio.wav"
    subtitle_file = "subtitles.srt"
    src_lang = "en"
    tgt_lang = "fr"

    extract_audio(video_path, audio_path)
    generate_subtitles(audio_path, subtitle_file)
    translate_subtitles(subtitle_file, src_lang, tgt_lang)