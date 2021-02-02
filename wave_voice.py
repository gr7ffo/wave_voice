# -*- coding: utf-8 -*-
#
# Copyright by Christopher Sauer
"""
@author: CSr
"""
# ==============================================================================
# IMPORT
# ==============================================================================
import os
import subprocess
from google.cloud import texttospeech


# ==============================================================================
# CONFIG
# ==============================================================================
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'


# ==============================================================================
# DEFINITION
# ==============================================================================
def convert_pdf_to_string(pdf_filename: str) -> str:
    """Convert pdf_filename to string"""
    subprocess.call(['pdftotext', '-enc', 'UTF-8', pdf_filename])
    txt_file = open(pdf_filename[:-3] + 'txt', 'r', encoding='UTF-8')
    return txt_file.read()


def synthesize_text(text: str, language='DE'):
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

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)


def main():
    """Main method"""
    text = convert_pdf_to_string('example.pdf')
    synthesize_text(text, language='EN')


if __name__ == "__main__":
    main()
