import argparse
import os
import whisper
from pydub import AudioSegment
from pydub.silence import split_on_silence

def convert_to_wav(input_file):
    audio = AudioSegment.from_file(input_file)
    wav_file = os.path.splitext(input_file)[0] + ".wav"
    audio.export(wav_file, format="wav")
    return wav_file

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    print (result["text"])
    return result["text"]

def censor_profanity(text):
    # Add your list of profanity keywords
    profanity_keywords = ["fuck", "fucking", "shit", "damn", "god damn"]
    
    for profanity in profanity_keywords:
        text = text.replace(profanity, '*' * len(profanity))
    print (text)
    return text

def mute_profanity(audio_file, transcript):
    audio = AudioSegment.from_file(audio_file)

    for phrase in transcript.split():
        if '*' in phrase:
            start_time = transcript.index(phrase) / len(transcript) * len(audio)
            end_time = start_time + len(phrase) / len(transcript) * len(audio)
            audio = audio.overlay(AudioSegment.silent(duration=int(end_time - start_time)), position=int(start_time))

    return audio

def main():
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
        transcript = transcribe_audio(input_file)
        censored_transcript = censor_profanity(transcript)
        muted_audio = mute_profanity(input_file, censored_transcript)
        muted_audio.export(output_file, format="mp3")
        print("Profanity silenced successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
