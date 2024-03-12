# Mixed speech translation

This notebook demonstrates how to use the different Azure AI services together to translate mixed / multilingual speech. The `Azure OpenAI Whisper` service is used to transcribe the speech and the `AI text translation` service is used to translate the transcribed text. The `Azure AI text to speech service` is used to verbalize the output again.

In qualitative comparison it seems this translation style is better then the plain `Azure AI speech translation service` if different languages are mixed together, like in this scenario where the language is Romanian but the city and village names are german.

## Getting started
To get started you need the following services deployed:
1. Azure OpenAI with Whisper Model
1. Azure AI Translation Service
1. Azure AI Speech Service

Create an environment for example by running:
```
python -m venv .venv
```
And activate the environment. (A quick search will tell you how to do it on your OS)
```
.\.venv\Scripts\activate.ps1
```

Then configure the `.env template` file with the proper keys and rename it to `.env`

Sign in to azure command line via az cli.
This is used to authenticate against Azure OpenAI Service.
```
az login
```

Then run the script:
```
python translate.py
```
It should play the translation on your default speaker and also output the multiple steps of the translation.