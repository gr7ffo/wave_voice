# -*- coding: utf-8 -*-
#
# Copyright by Christopher Sauer and Christof Küstner
"""
@author: CSr and CfK
"""
# ==============================================================================
# IMPORT
# ==============================================================================
import os
import subprocess
from pathlib import Path
from google.cloud import texttospeech


# ==============================================================================
# CONFIG
# ==============================================================================
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
DEFAULT_INPUT_FILE_PATH = Path(r"example.pdf")
DEFAULT_OUTPUT_FILE_PATH = Path(r"output.mp3")


# ==============================================================================
# DEFINITION
# ==============================================================================
def convert_pdf_to_string(pdf_file_path: Path) -> str:
    """Convert pdf_filename to string"""
    subprocess.call(['pdftotext', '-enc', 'UTF-8', pdf_file_path.absolute()])
    with open(pdf_file_path.with_suffix(".txt").absolute(), 'r', encoding='UTF-8') as txt_file:
        text = txt_file.read()
    return text


def synthesize_text(text: str, output_audio_file_path: Path, language='DE'):
    """Synthesize text from String and write to output.mp3"""
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    if language == 'DE':
        voice = texttospeech.VoiceSelectionParams(
            language_code="de-DE",
            name="de-DE-Wavenet-F",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
    elif language == 'EN':
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-F",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
    else:
        raise NotImplementedError

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text,
                 "voice": voice,
                 "audio_config": audio_config}
    )

    with open(output_audio_file_path.absolute(), "wb") as out:
        out.write(response.audio_content)


def wave_voice():
    """Main method"""
    # convert pdf to text
    text = convert_pdf_to_string(DEFAULT_INPUT_FILE_PATH)
    # convert text to speech
    synthesize_text(text, DEFAULT_OUTPUT_FILE_PATH, language='EN')


if __name__ == "__main__":
    wave_voice()
