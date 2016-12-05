#call as follows:
#python test.py 001_sent01_PCGITA.wav 001_sent03_PCGITA.wav 

"""Google Cloud Speech API sample application using the REST API for batch
processing."""

import argparse
import base64
import json
import re, math
from collections import Counter

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials


DISCOVERY_URL = ('https://speech.googleapis.com/$discovery/rest?'
                 'version=v1beta1')


def get_speech_service():
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build(
        'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

def main(speech_one, speech_two):
    """Transcribe the given audio file.

    Args:
        speech_file: the name of the audio file.
    """
        ##############################################
    transcriptOne = ''
    with open(speech_one, 'rb') as speech:
        speech_content = base64.b64encode(speech.read())

    service = get_speech_service()
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                'sampleRate': 16000,  # 16 khz
                'languageCode': 'es',  # a BCP-47 language tag
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    response = service_request.execute()
    for segment in response['results']:
        transcript_segment = segment['alternatives'][0]['transcript']
        transcriptOne += transcript_segment
        ##################################################
    transcriptTwo = ''
    with open(speech_two, 'rb') as speech:
        speech_content = base64.b64encode(speech.read())

    service = get_speech_service()
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                'sampleRate': 16000,  # 16 khz
                'languageCode': 'es',  # a BCP-47 language tag
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    response = service_request.execute()
    transcriptTwo = ''
    for segment in response['results']:
        transcript_segment = segment['alternatives'][0]['transcript']
        transcriptTwo += transcript_segment

    print ("==============================================")
    print ("transcript one: " + ' '.join(transcriptOne.split()))

    print ("==============================================")
    print ("transcript two: " + ' '.join(transcriptTwo.split()))


    vector1 = text_to_vector(transcriptOne)
    vector2 = text_to_vector(transcriptTwo)

    cosine = get_cosine(vector1, vector2)

    print ("==============================================")
    print ('Cosine similarity:', cosine)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('speech_one')
    parser.add_argument('speech_two')
    args = parser.parse_args()
    main(args.speech_one, args.speech_two)