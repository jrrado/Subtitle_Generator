#!/usr/bin/env python3

import subprocess
import sys
import os
from vosk import Model, KaldiRecognizer, SetLogLevel
from googletrans import Translator

SAMPLE_RATE = 16000

SetLogLevel(-1)

model_path = os.path.join(
    os.path.dirname(__file__), "vosk-model-small-en-us-0.15", "vosk-model-small-en-us-0.15"
)
print(model_path)
model = Model(model_path)
rec = KaldiRecognizer(model, SAMPLE_RATE)
rec.SetWords(True)

translator = Translator()

try:
    audio_file = sys.argv[1]
except IndexError:
    audio_file = input("Which file do you want to generate subtitles for? ").strip()

# Check if the file exists
if not os.path.isfile(audio_file):
    print(f"Error: The file '{audio_file}' does not exist.")
    sys.exit(1)

# Determine output file name
output_file = os.path.splitext(audio_file)[0] + "_subtitles.srt"
translated_output_file = os.path.splitext(audio_file)[0] + "_subtitles_translated.srt"

with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                       audio_file,
                       "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-"],
                      stdout=subprocess.PIPE).stdout as stream:

    subtitles = ""
    while True:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            subtitles += result + "\n"
        else:
            subtitles += rec.PartialResult() + "\n"

    subtitles += rec.FinalResult()

    # Check if subtitles are not empty before translation
    if subtitles.strip():
        # Translate subtitles
        translated_subtitles = translator.translate(subtitles, dest='es').text  # Change 'es' to desired language code

        with open(output_file, "w") as file:
            file.write(subtitles)

        with open(translated_output_file, "w") as file:
            file.write(translated_subtitles)

print(f"Subtitles have been generated and saved to '{output_file}'.")
print(f"Translated subtitles have been saved to '{translated_output_file}'.")
