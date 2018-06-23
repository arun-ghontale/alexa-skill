# -*- coding: utf-8 -*-
""" simple fact sample app """

from __future__ import print_function

import random
import re
import pandas as pd
from extract_dates import parseLogs,load_dates

SKILL_NAME = "Network Bot"
HELP_MESSAGE = """You can request for error logs between two time slots . 
                    For example , you can say "ask network bot for logs from 5:53 am to 10:53 am" """
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = """The """+SKILL_NAME+""" skill can't help you with that.  
                    It can help you get error logs between two specific time periods. 
                    For example """+HELP_MESSAGE+"""" What can I help you with?"""

FALLBACK_REPROMPT = 'What can I help you with?'

dataframe = load_dates(SAVE_DF = False)

# --------------- App entry point -----------------

def request_handler(json_input):
    """  App entry point  """

    #On launch send the helper message
    if json_input['session']['new']:
        on_session_started()

    #On launch send the helper message
    if json_input['request']['type'] == "LaunchRequest":
        return on_launch(json_input['request'])

    #handle the intent requests
    elif json_input['request']['type'] == "IntentRequest":
        return on_intent(json_input['request'], json_input['session'])
    elif json_input['request']['type'] == "SessionEndedRequest":
        return on_session_ended()

# --------------- Response handlers -----------------

def on_intent(request, session):
    """ called on receipt of an Intent  """

    intent_name = request['intent']['name']
    
    # process the intents
    if intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()
    
    elif intent_name == "recognizeDates":
        slots = request['intent']['slots']
        date_start_slot = slots.get('dateStart',{'value':'NA'}).get('value','NA')
        date_end_slot = slots.get('dateEnd',{'value':'NA'}).get('value','NA')

        return get_intent_response(date_start_slot,date_end_slot)
    
    elif intent_name == "PollHprofs":
        slots = request['intent'].get('slots','')
        print(slots)
        speechOutput = "Under development"
        return response(speech_response(speechOutput, True))

    elif intent_name == "SpinVMs":
        slots = request['intent'].get('slots','')
        print(slots)
        speechOutput = "Under development"
        return response(speech_response(speechOutput, True))

    else:
        print("For invalid Intents reply with help")
        return get_help_response()

def get_intent_response(date_start_slot,date_end_slot):
    """ parse and return their response"""
    print("here",date_start_slot,date_end_slot)    
    if date_start_slot != 'NA' and date_end_slot != 'NA':
        speechOutput = re.sub(' +',' ','Parsing error Logs from '+ date_start_slot + ' to '+date_end_slot)

    elif date_start_slot == 'NA' and date_end_slot != 'NA':
        speechOutput = 'Parsing error logs at '+date_end_slot

    elif date_start_slot != 'NA' and date_end_slot == 'NA':
        speechOutput = 'Parsing error logs at '+date_start_slot

    else:
        speechOutput = 'Start and end times are unrecognizable'
        
    return_value = parseLogs(date_start_slot,date_end_slot,dataframe)
    logs = return_value[0]
    stats = return_value[1]
    
    with open('logs.txt','w') as f:
        for each in logs:
            f.write(each)

    with open('log_stats.txt','w') as f:
        for each_key,each_value in stats.items():
            f.write("Time : "+each_key+'\t'+"Number of logs : "+len(each_value)+"\n\n")
            for each_logs in each_value:
                f.write(each_logs+"\n")
            f.write("\n\n\n\n")
    
    os.system("nohup python send_mail.py &")
    
    return response(speech_response(speechOutput, True))

def get_help_response():
    """ get and return the help string  """

    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message,
                                                       speech_message, False))
    
def get_launch_error_response():
    """Helper message"""
    speechOutput = HELP_MESSAGE

    return response(speech_response(speechOutput, True))
    

def get_stop_response():
    """ end the session, user wants to quit the game """

    speech_output = STOP_MESSAGE
    return response(speech_response(speech_output, True))

def get_fallback_response():
    """ end the session, user wants to quit the game """

    speech_output = FALLBACK_MESSAGE
    return response(speech_response(speech_output, False))

def on_session_started():
    """" called when the session starts  """
    #print("on_session_started")

def on_session_ended():
    """ called on session ends """
    #print("on_session_ended")

def on_launch(request):
    """ called on Launch, we reply with a launch message  """

    return get_launch_error_response()


# --------------- Speech response handlers -----------------

def speech_response(output, endsession):
    """  create a simple json response  """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def speech_response_prompt(output, reprompt_text, endsession):
    """ create a simple json response with a prompt """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': endsession
    }

def response(speech_message):
    """ create a simple json response  """
    return {
        'version': '1.0',
        'response': speech_message
    }