from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import requests
import urllib3
from flask import Flask, request
import telegram

class Buscar(Action):

    def name(self) -> Text:
        return "Buscar"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        urllib3.disable_warnings()
        informacion = tracker.get_slot("informacion")##Busca el tema en el url de abajo
        # url = 'https://proyectobot.test/Tema.php'#Aqui tambien va la url de nuestra BD 
        url = 'https://proyectobot2.000webhostapp.com/ProyectoBot/Tema.php'#Aqui tambien va la url de nuestra BD 
        params = {'tema': informacion}## Manda parametros al URL
        response = requests.get(url, params=params,verify=False)


        #SI LA CONEXION AL SERVIDOR FUE EXITOSA EJECUTA EL SIGUIENTE BLOQUE DE CODIGO
        if response.status_code < 400 and response.text != '0':
            respuesta_php = response.text
            json_objeto = json.loads(respuesta_php)
            tema = json_objeto[0]["Capitulo"]## Extrae variable del capitulo
            id = json_objeto[0]["Id tema"]
            # url2 = 'https://proyectobot.test/Informacion.php' #en espera para ver que es este link
            url2 = 'https://proyectobot2.000webhostapp.com/ProyectoBot/Informacion.php' #en espera para ver que es este link
            params = {'cap' : tema, 'id':id}
            response2= requests.get(url2, params=params,verify=False)

            if response.status_code == 200:
                respuesta_php2 = response2.text
                respuesta_json2 = json.loads(respuesta_php2)

                #AQUI SE DECLARAN LAS COLUMNSA DE NUESTRA BASE DE DATOS PARA ACCEDER A ELLAS COMO SI FUERAN MATRICES

                conceptobreve = respuesta_json2[0]["Conceptobreve"]     
                linkPag = respuesta_json2[0]["LinkPagina"]

                #ESTA ES LA SEGUNDA SINTAXIS PARA DECLARAR LAS COLUMNAS, MUY IMPORTANTE ESTA SINTAXIS YA QUE SIN ELLA NO SE DELCARAN LAS ANTERIORES

                dispatcher.utter_message(text="{}".format(conceptobreve))
                dispatcher.utter_message(text="{}".format(linkPag))

            else:
                response.raise_for_status()
        else:
           dispatcher.utter_message(text="Lo siento al parecer no tengo informacion sobre eso")
           dispatcher.utter_message(text="Lamento decirte que no tengo esa informacion")

        return []
      
    

    class Buscar_img(Action):

        def name(self) -> Text:
            return "Buscar_img"
        
        def run(self, dispatcher: CollectingDispatcher, 
                tracker: Tracker, 
                domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
            urllib3.disable_warnings()
            informacion = tracker.get_slot("informacion")##Busca el tema en el url de abajo
            # url = 'https://proyectobot.test/Tema.php'
            url = 'https://proyectobot2.000webhostapp.com/ProyectoBot/Tema.php'#Aqui tambien va la url de nuestra BD 
            params = {'tema': informacion}## Manda parametros al URL
            response = requests.get(url, params=params,verify=False)


            #SI LA CONEXION AL SERVIDOR FUE EXITOSA EJECUTA EL SIGUIENTE BLOQUE DE CODIGO
            if response.status_code < 400 and response.text != '0':
                respuesta_php = response.text
                json_objeto = json.loads(respuesta_php)
                tema = json_objeto[0]["Capitulo"]## Extrae variable del capitulo
                id = json_objeto[0]["Id tema"]
                # url2 = 'https://proyectobot.test/Imagenes.php'
                url2 = 'https://proyectobot2.000webhostapp.com/ProyectoBot/Imagenes.php' #en espera para ver que es este link
                params = {'cap' : tema, 'id':id}
                response2= requests.get(url2, params=params,verify=False)

                if response.status_code == 200:
                    respuesta_php2 = response2.text
                    respuesta_json2 = json.loads(respuesta_php2)

                    #AQUI SE DECLARAN LAS COLUMNSA DE NUESTRA BASE DE DATOS PARA ACCEDER A ELLAS COMO SI FUERAN MATRICES

                    linkvid = respuesta_json2[0]["Video"]
                    imagenReferencia = respuesta_json2[0]["Imagen"]

                    #ESTA ES LA SEGUNDA SINTAXIS PARA DECLARAR LAS COLUMNAS, MUY IMPORTANTE ESTA SINTAXIS YA QUE SIN ELLA NO SE DELCARAN LAS ANTERIORES

                    dispatcher.utter_message(text="{}".format(linkvid))
                    dispatcher.utter_message(text="{}".format(imagenReferencia))

                else:
                    response.raise_for_status()
            else:
                dispatcher.utter_message(text="Al parecer no cuento con mas informacion sobre el tema")
                
            return []


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_fallback")
        return []
            

