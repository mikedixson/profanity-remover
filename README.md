# Profanity Remover

This Python script uses speech recognition and audio manipulation to censor profanity in an audio file. It transcribes the audio, searches for profanity keywords, and replaces them with asterisks. The script then applies silence to the original audio file based on the location of profanity, effectively "muting" profane sections. The output is a new audio file with profanity silenced.

## Requirements

- Python 3.x
- openai-whisper
- pydub
- whisper
- ffmpeg

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mikedixson/profanity-remover.git
cd profanity-remover
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```
3. Install ffmpeg
Here are some commands for installing `ffmpeg` using common package managers:

- For Ubuntu/Debian:

    ```bash
    sudo apt-get update
    sudo apt-get install ffmpeg
    ```

- For macOS (using Homebrew):

    ```bash
    brew install ffmpeg
    ```
- For Windows (Using Choco):
  ``` cmd
  choco install ffmpeg-full
  ```

Make sure that after installing `ffmpeg`, it is added to your system's PATH so that it can be accessed by other programs, including `pydub` in the provided script.

## Usage

Run the script using the following command:

```bash
python profanity_remover.py input_audio.mp3 output_audio.mp3
```

Replace `input_audio.mp3` with the path to your input audio file and `output_audio.mp3` with the desired output file name.

## Example

```bash
python profanity_remover.py example_audio.mp3 silenced_output.mp3
```

This will transcribe the audio, censor profanity, mute the profane sections, and save the result as `silenced_output.mp3`.

## Issues and Contributions

If you encounter any issues or have suggestions for improvements, feel free to open an issue on the [GitHub repository](https://github.com/mikedixson/profanity-remover).

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

```
