import pysrt
from gtts import gTTS
from pydub import AudioSegment
from tqdm import tqdm

def generate_audio_from_srt(srt_file_path, output_audio_path, lang='pt-br'):
    subs = pysrt.open(srt_file_path)
    combined_audio = AudioSegment.empty()

    for sub in tqdm(subs):
        text = sub.text
        start_ms = sub.start.ordinal
        end_ms = sub.end.ordinal
        duration_ms = end_ms - start_ms

        # Generate audio for the current subtitle text
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save("temp_sub_audio.mp3")

        # Load the generated audio and ensure it fits the subtitle duration
        sub_audio = AudioSegment.from_mp3("temp_sub_audio.mp3")

        # Adjust audio length if necessary (e.g., add silence or speed up/slow down)
        if len(sub_audio) < duration_ms:
            silence_needed = duration_ms - len(sub_audio)
            sub_audio += AudioSegment.silent(duration=silence_needed)
        elif len(sub_audio) > duration_ms:
            # Simple approach: trim excess or consider speeding up speech
            sub_audio = sub_audio[:duration_ms]

        combined_audio += sub_audio

    combined_audio.export(output_audio_path, format="mp3")
    print(f"Audio generated and saved to {output_audio_path}")

# Example usage:
generate_audio_from_srt("output.srt", "output_audio.mp3")