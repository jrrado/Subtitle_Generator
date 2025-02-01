import sys
import os
import wave
import json
from vosk import Model, KaldiRecognizer
from googletrans import Translator

# Load the Vosk model
model_path = os.path.join(
    os.path.dirname(__file__), "vosk-model-small-en-us-0.15", "vosk-model-small-en-us-0.15"
)
model = Model(model_path)
rec = KaldiRecognizer(model, 16000)

translator = Translator()

# Check for audio file input
try:
    audio_path = sys.argv[1]
except IndexError:
    audio_path = input("Please provide the path to the audio file: ").strip()

# Open the audio stream
wf = wave.open(audio_path, "rb")

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
    print("Audio file must be WAV format mono PCM.")
    sys.exit(1)

# Determine output file name
output_file = os.path.splitext(audio_path)[0] + "_transcription.srt"
translated_output_file = os.path.splitext(audio_path)[0] + "_transcription_translated.srt"

# Process the audio stream and generate subtitles
with open(output_file, "w") as file:
    start_time = 0.0
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result_json = json.loads(result)
            if 'text' in result_json and result_json['text']:
                end_time = start_time + (len(data) / 16000)  # Calculate end time based on data length
                file.write(f"{start_time:.3f} --> {end_time:.3f}\n{result_json['text']}\n\n")
                start_time = end_time
        else:
            rec.PartialResult()

    # Final result
    final_result = rec.FinalResult()
    final_json = json.loads(final_result)
    if 'text' in final_json and final_json['text']:
        end_time = start_time + (len(data) / 16000)  # Calculate end time for final result
        file.write(f"{start_time:.3f} --> {end_time:.3f}\n{final_json['text']}\n\n")

# Translate the transcription
with open(translated_output_file, "w") as file:
    translated_text = translator.translate(final_json['text'], dest='es').text  # Change 'es' to desired language code
    file.write(f"{start_time:.3f} --> {end_time:.3f}\n{translated_text}\n\n")

print(f"Transcription has been generated and saved to '{output_file}'.")
print(f"Translated transcription has been saved to '{translated_output_file}'.")
