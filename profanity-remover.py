"""
Profanity Remover

This Python script uses speech recognition and audio manipulation to censor profanity in an audio file.
It transcribes the audio, searches for profanity keywords, and replaces them with asterisks.
The script then applies silence to the original audio file based on the location of profanity, effectively "muting" profane sections.
The output is a new audio file with profanity silenced.

Requirements:
- Python 3.x
- openai-whisper
- pydub
- whisper

Installation:
1. Clone the repository:
   git clone https://github.com/mikedixson/profanity-remover.git
   cd profanity-remover

2. Install the required Python packages:
   pip install -r requirements.txt

3. Install ffmpeg

Usage:
Run the script using the following command:
python profanity_remover.py input_audio.mp3 output_audio.mp3

Replace input_audio.mp3 with the path to your input audio file and output_audio.mp3 with the desired output file name.

Example:
python profanity_remover.py example_audio.mp3 silenced_output.mp3
This will transcribe the audio, censor profanity, mute the profane sections, and save the result as silenced_output.mp3.

Issues and Contributions:
If you encounter any issues or have suggestions for improvements, feel free to open an issue on the GitHub repository (https://github.com/mikedixson/profanity-remover).
Contributions are welcome! Fork the repository, make your changes, and submit a pull request.
"""

import argparse
import csv
import os
import whisper
from stable_whisper import modify_model
from pydub import AudioSegment

def parse_tsv(tsv_string):
    """
    Parses a TSV string into a list of tuples.

    Parameters:
    - tsv_string (str): The TSV string.

    Returns:
    - list: List of tuples, each containing a word and its start and end times.
    """
    words = []
    reader = csv.reader(tsv_string.split('\n'), delimiter='\t')
    for row in reader:
        if len(row) == 3:
            start_time, end_time, word = row
            words.append((float(start_time), float(end_time), word))
    return words

def convert_to_wav(input_file):
    """
    Converts the input audio file to WAV format.

    Parameters:
    - input_file (str): Path to the input audio file.

    Returns:
    - str: Path to the converted WAV file.
    """
    audio = AudioSegment.from_file(input_file)
    wav_file = os.path.splitext(input_file)[0] + ".wav"
    audio.export(wav_file, format="wav")
    return wav_file

def transcribe_audio(audio_file):
    """
    Transcribes the audio using the Whisper ASR model.

    Parameters:
    - audio_file (str): Path to the audio file.

    Returns:
    - list: List of tuples, each containing a word and its start and end times.
    """
    model = whisper.load_model("base")
    modify_model(model)
    result = model.transcribe(audio_file, suppress_silence=True, ts_num=16)
    result.to_tsv('transcribe.tsv', segment_level=False, word_level=True)
    return result.to_tsv('', segment_level=False, word_level=True) #TSV
    #return result["words"]

def censor_profanity(words):
    """
    Flags profanity in the provided list of words.

    Parameters:
    - words (list): List of tuples, each containing a word and its start and end times.

    Returns:
    - list: List of tuples with censored words and a profanity flag.
    """
    profanity_keywords = ["fucking", "fuck", "shit", "god damn", "damn"]
    censored_words = []
    for start_time, end_time, word in words:
        is_profanity = any(profanity in word.lower() for profanity in profanity_keywords)
        censored_words.append((start_time, end_time, word, is_profanity))
    return censored_words

def mute_profanity(audio_file, words):
    """
    Mutes sections of the audio where profanity is flagged.

    Parameters:
    - audio_file (str): Path to the input audio file.
    - words (list): List of tuples, each containing a word, its start and end times, and a profanity flag.

    Returns:
    - pydub.AudioSegment: Muted audio.
    """
    audio = AudioSegment.from_file(audio_file)
    for start_time, end_time, word, is_profanity in words:
        if is_profanity:
            start_ms = int(start_time)
            end_ms = int(end_time)
            silence = AudioSegment.silent(duration=end_ms - start_ms)
            audio = audio[:start_ms] + silence + audio[end_ms:]
    return audio




def main():
    """
    Main function to handle command line arguments and execute the profanity removal process.
    """
    parser = argparse.ArgumentParser(description='Profanity Silencer for Audio Files')
    parser.add_argument('input', help='Input audio file path')
    parser.add_argument('output', help='Output audio file path')
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    if not input_file.lower().endswith(".wav"):
        print("Converting input audio to WAV format...")
        input_file = convert_to_wav(input_file)

    try:
        #transcript = transcribe_audio(input_file)
        tsv_string = transcribe_audio(input_file)
        words = parse_tsv(tsv_string)
        censored_words = censor_profanity(words)
        muted_audio = mute_profanity(input_file, censored_words)
        muted_audio.export(output_file, format="mp3")
        print("Profanity silenced successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
