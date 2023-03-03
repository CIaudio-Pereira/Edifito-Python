# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
from ask_sdk_core.utils import is_request_type, is_intent_name, get_account_linking_access_token
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import json
import requests

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        #Identificar idioma y traducciones
        locale = handler_input.request_envelope.request.locale
        with open('languages/'+locale+'.json', 'r') as diccionario:
            translation = json.load(diccionario)
        
        #Obtener las URLS
        with open('config.json', 'r') as urlsetting:
            urlsedifito = json.load(urlsetting)
        
        #Recuperar token
        account_linking_token = get_account_linking_access_token(handler_input)
        
        if account_linking_token is not None:
            #Informacion de la API
            url = "http://eta.edifitolabs.com/api/unidades.php"
            payload={}
            headers = {
                'Authorization': f'Bearer {account_linking_token}'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            
            data = json.loads(response.text)
            
            unidad = data[0]['idUnidad']
            nombre = data[0]['nombreCopropietario']
            
            #Mensaje de inicio
            speak_output = translation['WELCOME_MSG']
            
        else:
            #Mensaje de inicio sin iniciar sesion
            speak_output = translation['NOT_REGISTERED_MSG']
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class GastosComunesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("GastosComunesIntent")(handler_input) or
                ask_utils.is_intent_name("CommonExpensesIntent")(handler_input))

    def handle(self, handler_input):
        #Identificar idioma y traducciones
        locale = handler_input.request_envelope.request.locale
        with open('languages/'+locale+'.json', 'r') as diccionario:
            translation = json.load(diccionario)
        
        #Recuperar el token
        account_linking_token = get_account_linking_access_token(handler_input)
        
        if account_linking_token is not None:
            #Informacion de la API unidades
            url = "http://eta.edifitolabs.com/api/unidades.php"
            payload={}
            headers = {
                'Authorization': f'Bearer {account_linking_token}'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            
            data = json.loads(response.text)
            
            unidad = data[0]['idUnidad']
            
            #Informacion de la API gastoscomunes
            url = "http://eta.edifitolabs.com/api/gastoComun.php"
            payload= f'id_unidad=%5B{unidad}%5D'
            headers = {
                'Authorization': f'Bearer {account_linking_token}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            
            data = json.loads(response.text)
            
            deudaTotal = data[0]['deudaTotal']
            
            #Mostrar gatos comunes
            #speak_output = f'Tienes una deuda total de ${deudaTotal}'
            speak_output = translation['COMMON_EXPENSES'] + str(deudaTotal)
            
        else:
            #Mensaje de inicio sin iniciar sesion
                
            speak_output = translation['NOT_REGISTERED_MSG']

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class RealizarInvitacionIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("RealizarInvitacionIntent")(handler_input) or
                ask_utils.is_intent_name("MakeInvitationIntent")(handler_input))

    def handle(self, handler_input):
        #Identificar idioma y traducciones
        locale = handler_input.request_envelope.request.locale
        with open('languages/'+locale+'.json', 'r') as diccionario:
            translation = json.load(diccionario)
        
        slots = handler_input.request_envelope.request.intent.slots
        guestname = slots['guestname'].value
        
        speak_output = translation['SUCCESSFUL_INVITATION'] + guestname

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class RealizarReservaIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("RealizarReservaIntent")(handler_input) or
                ask_utils.is_intent_name("MakeReservationIntent")(handler_input))

    def handle(self, handler_input):
        #Identificar idioma y traducciones
        locale = handler_input.request_envelope.request.locale
        with open('languages/'+locale+'.json', 'r') as diccionario:
            translation = json.load(diccionario)
        
        slots = handler_input.request_envelope.request.intent.slots
        place = slots['place'].value
        
        speak_output = translation['SUCCESSFUL_BOOKING'] + place

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        #Identificar idioma y traducciones
        locale = handler_input.request_envelope.request.locale
        with open('languages/'+locale+'.json', 'r') as diccionario:
            translation = json.load(diccionario)
        
        speak_output = translation['HELP_MSG']
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        #Identificar idioma y traducciones
        locale = handler_input.request_envelope.request.locale
        with open('languages/'+locale+'.json', 'r') as diccionario:
            translation = json.load(diccionario)
        
        speak_output = translation['CANCEL_STOP_MSG']

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        #Identificar idioma y traducciones
        locale = handler_input.request_envelope.request.locale
        with open('languages/'+locale+'.json', 'r') as diccionario:
            translation = json.load(diccionario)
        
        logger.info("In FallbackIntentHandler")
        speak_output = translation['ACTION_NOT_FOUND_MSG']
        
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        #Identificar idioma y traducciones
        locale = handler_input.request_envelope.request.locale
        with open('languages/'+locale+'.json', 'r') as diccionario:
            translation = json.load(diccionario)
        
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = translation['ERROR_MSG'] + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        #Identificar idioma y traducciones
        locale = handler_input.request_envelope.request.locale
        with open('languages/'+locale+'.json', 'r') as diccionario:
            translation = json.load(diccionario)
        
        logger.error(exception, exc_info=True)

        speak_output = translation['ERROR_WITH_REQUEST_MSG']

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

    
# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(GastosComunesIntentHandler())
sb.add_request_handler(RealizarInvitacionIntentHandler())
sb.add_request_handler(RealizarReservaIntentHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()