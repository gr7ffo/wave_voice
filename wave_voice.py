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
import click
from pathlib import Path
from google.cloud import texttospeech


# ==============================================================================
# CONFIG
# ==============================================================================
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
DEFAULT_INPUT_FILE = r"example.pdf"
DEFAULT_OUTPUT_FILE = r"output.mp3"


# ==============================================================================
# DEFINITION
# ==============================================================================
def yes_or_no(question):
    """Ask user a closed question"""
    while True:
        reply = str(input(question + " (y/N): ")).strip()
        if len(reply) == 0:
            return False
        else:
            if reply[0] == "y":
                return True
            elif reply[0] == "N":
                return False


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


@click.command()
@click.argument("input_file",
                required=False,
                default=DEFAULT_INPUT_FILE,
                type=click.Path(file_okay=True, dir_okay=False,
                                resolve_path=True, allow_dash=False,
                                exists=True))
@click.argument("language",
                required=False,
                default="EN",
                type=str)
@click.argument("output_audio_file",
                required=False,
                default=DEFAULT_OUTPUT_FILE,
                type=click.Path(file_okay=True, dir_okay=False,
                                resolve_path=True, allow_dash=False,
                                exists=False))
@click.option("-y", "--yes", "yes",
              is_flag=True, default=False,
              help="yes: Do not ask for user input and proceed")
def wave_voice(input_file: str, language: str, output_audio_file: str, yes=False):
    """
    Converts text of an INPUT_FILE (*.pdf, *.txt) into speech
    as OUTPUT_AUDIO_FILE (.mp3) in LANGUAGE (default:'EN')
    """
    input_file_path = Path(input_file)
    output_audio_file_path = Path(output_audio_file)
    if input_file_path.suffix == ".pdf":
        # convert pdf to text
        text = convert_pdf_to_string(input_file_path)
    elif input_file_path.suffix == ".txt":
        with open(input_file_path.absolute(), "r", encoding="UTF-8") as txt_file:
            text = txt_file.read()
    else:
        raise NotImplementedError

    # Count chars and ask user to proceed
    text_chars = len(text)
    if yes or yes_or_no(f"Do you want to proceed with {text_chars} chars?"):
        # convert text to speech
        synthesize_text(text, output_audio_file_path, language=language)


if __name__ == "__main__":
    wave_voice()
