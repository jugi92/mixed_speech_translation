import os

from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

import azure.cognitiveservices.speech as speechsdk

def speech_to_text(audio_file_path="Romanian_Bus_Route_Recording.m4a"):
    openai_endpoint = "https://jugi-public-sweden-aoai.openai.azure.com/"  # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    api_version = "2023-09-01-preview"

    model_name = "whisper"
    token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=openai_endpoint,
        azure_ad_token_provider=token_provider
    )

    result = client.audio.translations.create(
        file=open(audio_file_path, "rb"), model=model_name
    )

    print(result)
    return result.text


def translate_text(text_to_translate, source_language="en", target_languages=["de", "ro"]):
    # set `<your-key>`, `<your-endpoint>`, and  `<region>` variables with the values from the Azure portal
    key = os.environ.get("TRANSLATOR_TEXT_SUBSCRIPTION_KEY")
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    region = "westeurope"

    credential = TranslatorCredential(key, region)
    text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)
    
    #token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    #text_translator = TextTranslationClient(credential=token_provider, endpoint=endpoint)

    input_text_elements = [InputTextItem(text=text_to_translate)]

    response = text_translator.translate(
        content=input_text_elements, to=target_languages, from_parameter=source_language
    )
    translation = response[0] if response else None

    if translation:
        for translated_text in translation.translations:
            print(
                f"Text was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'."
            )
        return translation.translations

def text_to_speech(text, target_file="output.wav"):
    speech_region = "westeurope"
    speech_key = os.environ.get("SPEECH_KEY")
    # This example requires environment variables named "SPEECH_REGION" 
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    
    # token = DefaultAzureCredential().get_token("https://cognitiveservices.azure.com/.default")
    # speech_config = speechsdk.SpeechConfig(auth_token=token.token, region=speech_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='de-DE-ConradNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
        with open(target_file, 'wb') as audio_file:
            audio_file.write(speech_synthesis_result.audio_data)
    


if __name__ == "__main__":
    text = speech_to_text()
    translations = translate_text(text)
    text_to_speech(translations[0].text, target_file="output.wav")
