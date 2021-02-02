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
from google.cloud import texttospeech


# ==============================================================================
# CONFIG
# ==============================================================================
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'


# ==============================================================================
# DEFINITION
# ==============================================================================
def synthesize_text(text: str):
    """Synthesize text from String and write to output.mp3"""
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="de-DE",
        name="de-DE-Wavenet-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

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
    synthesize_text("Hallo, Welt!")


if __name__ == "__main__":
    main()
