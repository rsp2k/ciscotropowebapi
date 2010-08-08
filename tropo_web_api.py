"""
The TropoPython module. This module implements a set of classes and methods for manipulating the Voxeo Tropo WebAPI.

Usage:

tropo = Tropo()
tropo.say("Hello, World")
json = tropo.RenderJson() 

You can write this JSON back to standard output to get Tropo to perform 
the action. For example, on Google Appengine you might write something like:

handler.response.out.write(json)

Much of the time, a you will interact with Tropo by  examining the Result 
object and communicating back to Tropo via the Tropo class methods, such 
as "say". In some cases, you'll want to build a class object directly such as in :

    choices = tropo_web_api.Choices("[5 digits]").obj

    tropo.ask(choices, 
              say="Please enter your 5 digit zip code.", 
              attempts=3, bargein=True, name="zip", timeout=5, voice="dave")
    ...

"""

try:
    import cjson as jsonlib
    jsonlib.dumps = jsonlib.encode
    jsonlib.loads = jsonlib.decode
except ImportError:
    try:
        from django.utils import simplejson as jsonlib
    except ImportError:
        try:
            import simplejson as jsonlib
        except ImportError:
            import json as jsonlib

import logging


class Ask(object):
    """
    Class representing the "ask" Tropo action. Builds an "ask" JSON object.
    Class constructor arg: choices, a Choices object
    Convenience function: Tropo.ask()
    Class constructor options: attempts, bargein, choices, minConfidence, name, recognizer, required, say, timeout, voice

    Request information from the caller and wait for a response.
    (See https://www.tropo.com/docs/webapi/ask.htm)

        { "ask": {
            "attempts": Integer,
            "bargein": Boolean,
            "choices": Object, #Required
            "minConfidence": Integer,
            "name": String,
            "recognizer": String,
            "required": Boolean,
            "say": Object,
            "timeout": Float,
            "voice": String } } 

    """
    def __init__(self, choices, **options):

        dict = {}
        options_array = ['attempts', 'bargein', 'choices', 'minConfidence', 'name', 'recognizer', 'required', 'say', 'timeout', 'voice']
        
        if (isinstance(choices, str)):
            choices1 = Choices(choices).json
            dict['choices'] = choices1
        else:
            dict['choices'] = choices['choices']
        for opt in options_array:
            if opt in options:
                if ((opt == 'say') and (isinstance(options['say'], str))):
                    say_obj = options['say']
                    say_obj1 = Say(say_obj).json
                    dict['say'] = say_obj1
                else:
                    dict[opt] = options[opt]
        self.obj = {'ask' : dict}
        self.json = dict

class Call(object):
    """
    Class representing the "call" Tropo action. Builds a "call" JSON object.
    Class constructor arg: to, a String
    Class constructor options: answerOnMedia, channel, from, headers, name, network, recording, required, timeout
    Convenience function: Tropo.call()

    (See https://www.tropo.com/docs/webapi/call.htm)

    { "call": {
        "to": String or Array,#Required
        "answerOnMedia": Boolean,
        "channel": string,
        "from": string,
        "headers": Object,
        "name": String,
        "network": String,
        "recording": Array or Object,
        "required": Boolean,
        "timeout": Float } } 
    """
    def __init__(self, to, **options):
        dict = {}
        dict['to'] = to
        options_array = ['answerOnMedia', 'channel', 'from', 'headers', 'name', 'network', 'recording', 'required', 'timeout']
        for opt in options_array:
            if opt in options:
                dict[opt] = options[opt]
        self.obj = {'call' : dict}
        self.json = dict

class Choices(object):
    """
    Class representing choice made by a user. Builds a "choices" JSON object.
    Class constructor options: terminator, mode

    (See https://www.tropo.com/docs/webapi/ask.htm)
    """
    def __init__(self, value, **options):
        dict = {}
        options_array = ['terminator', 'mode']

        for opt in options_array:
            if opt in options:
                dict[opt] = options[opt]

        dict['value'] = value

        self.obj = {'choices': dict}
        self.json = dict


class Conference(object):
    """
    Class representing the "conference" Tropo action. Builds a "conference" JSON object.
    Class constructor arg: id, a String
    Convenience function: Tropo.conference()
    Class constructor options: mute, name, playTones, required, terminator

    (See https://www.tropo.com/docs/webapi/conference.htm)

    { "conference": {
        "id": String,#Required
        "mute": Boolean,
        "name": String,
        "playTones": Boolean,
        "required": Boolean,
        "terminator": String } } 
    """

    def __init__(self, id, **options):
        dict = {}

        dict['id'] = id
        options_array = ['mute', 'name', 'playTones', 'required', 'terminator']

        for opt in options_array:
            if opt in options:
                dict[opt] = options[opt]
        self.obj = {'conference' : dict}
        self.json = dict

class Hangup(object):
    """
    Class representing the "hangup" Tropo action. Builds a "hangup" JSON object.
    Class constructor arg: 
    Class constructor options: 
    Convenience function: Tropo.hangup()

    (See https://www.tropo.com/docs/webapi/hangup.htm)

    { "hangup": { } } 
    """
    def __init__(self):
        dict = {}
        self.obj = {'hangup' : dict}
        self.json = dict

class Message(object):
    """
    Class representing the "message" Tropo action. Builds a "message" JSON object.
    Class constructor arg: say_obj, a Say object
    Class constructor arg: to, a String
    Class constructor options: answerOnMedia, channel, from, name, network, required, timeout, voice
    Convenience function: Tropo.message()

    (See https://www.tropo.com/docs/webapi/message.htm)
    { "message": {
            "say": Object,#Required
            "to": String or Array,#Required
            "answerOnMedia": Boolean,
            "channel": string,
            "from": Object,
            "name": String,
            "network": String,
            "required": Boolean,
            "timeout": Float,
            "voice": String } } 
    """
    def __init__(self, say_obj, to, **options):

        dict = {}

        # say_obj = Say(message).obj
        say_payload = say_obj['say']
        dict['say'] = say_payload
        dict['to'] = to

        options_array = ['answerOnMedia', 'channel', 'from', 'name', 'network', 'required', 'timeout', 'voice']

        logging.info ("options: %s" % options)
        for opt in options_array:
            if opt in options:
                dict[opt] = options[opt]
        self.obj = {'message' : dict}
        self.json = dict

class On(object):
    """
    Class representing the "on" Tropo action. Builds an "on" JSON object.
    Class constructor arg: event, a String
    Class constructor options:  name,next,required,say
    Convenience function: Tropo.on()

    (See https://www.tropo.com/docs/webapi/on.htm)

    { "on": {
        "event": String,#Required
        "name": String,
        "next": String,
        "required": Boolean,
        "say": Object } } 
    """
    def __init__(self, event, **options):
        dict = {}
        dict['event'] = event
        options_array = ['name','next','required','say']
        for opt in options_array:
            if opt in options:
                if ((opt == 'say') and (isinstance(options['say'], str))):
                    say_obj = options['say']
                    say_obj1 = Say(say_obj).json
                    dict['say'] = say_obj1
                else:
                    dict[opt] = options[opt]

        self.obj = {'on' : dict}
        self.json = dict


class Record(object):
    """
    Class representing the "record" Tropo action. Builds a "record" JSON object.
    Class constructor arg: 
    Class constructor options: attempts, bargein, beep, choices, format, maxSilence, maxTime, method, minConfidence, name, password, required, say, timeout, transcription, url, username
    Convenience function: Tropo.record()



    (See https://www.tropo.com/docs/webapi/record.htm)

        { "record": {
            "attempts": Integer,
            "bargein": Boolean,
            "beep": Boolean,
            "choices": Object,
            "format": String,
            "maxSilence": Float,
            "maxTime": Float,
            "method": String,
            "minConfidence": Integer,
            "name": String,
            "password": String,
            "required": Boolean,
            "say": Object,
            "timeout": Float,
            "transcription": Array or Object,
            "url": String,#Required ?????
            "username": String } } 
    """

    def __init__(self, **options):
        dict = {}
        options_array = ['attempts', 'bargein', 'beep', 'choices', 'format', 'maxSilence', 'maxTime', 'method', 'minConfidence', 'name', 'password', 'required', 'say', 'timeout', 'transcription', 'url', 'username']
        for opt in options_array:
            if opt in options:
                if ((opt == 'say') and (isinstance(options['say'], str))):
                    say_obj = options['say']
                    say_obj1 = Say(say_obj).json
                    dict['say'] = say_obj1
                else:
                    dict[opt] = options[opt]
        self.obj = {'record' : dict}
        self.json = dict


class Redirect(object):
    """
    Class representing the "redirect" Tropo action. Builds a "redirect" JSON object.
    Class constructor arg: to, a String
    Class constructor options:  name, required
    Convenience function: Tropo.redirect()

    (See https://www.tropo.com/docs/webapi/redirect.htm)

    { "redirect": {
        "to": Object,#Required
        "name": String,
        "required": Boolean } } 
    """
    def __init__(self, to, **options):
        dict = {}
        dict['to'] = to

        options_array = ['name', 'required']

        for opt in options_array:
            if opt in options:
                dict[opt] = options[opt]
        self.obj = {'redirect' : dict}
        self.json = dict


class Reject(object):
    """
    Class representing the "reject" Tropo action. Builds a "reject" JSON object.
    Class constructor arg: 
    Class constructor options: 
    Convenience function: Tropo.reject()

    (See https://www.tropo.com/docs/webapi/reject.htm)

    { "reject": { } } 
    """
    def __init__(self):
        dict = {}
        self.obj = {'reject' : dict}


class Result(object):

    """
    Returned anytime a request is made to the Tropo Web API. 
    Method: getValue 
    (See https://www.tropo.com/docs/webapi/result.htm)

        { "result": {
            "actions": Array or Object,
            "complete": Boolean,
            "error": String,
            "sequence": Integer,
            "sessionDuration": Integer,
            "sessionId": String,
            "state": String } }
    """ 
            
    def __init__(self, result_json):
        logging.info ("result POST data: %s" % result_json)
        result_data = jsonlib.loads(result_json)
        result_dict = result_data['result']

        options_array = ['actions','complete','error','sequence', 'sessionDuration', 'sessionId', 'state']
        self._actions = result_dict['actions']
        self._complete = result_dict['complete']
        self._error = result_dict['error']
        self._actions = result_dict['actions']
        self._sequence = result_dict['sequence']
        self._sessionDuration = result_dict['sessionDuration']
        self._sessionId = result_dict['sessionId']
        self._state = result_dict['state']

    def getValue(self):
        """
        Get the value of the previously POSTed Tropo action.
        """
        actions = self._actions

        if (type (actions) is list):
            logging.info ("Actions is a list")
            dict = actions[0]
        else:
            logging.info ("Actions is a dict")
            dict = actions
        logging.info ("Actions is: %s" % actions)
        return dict['interpretation']


class Say(object):
    """
    Class representing the "say" Tropo action. Builds a "say" JSON object.
    Class constructor arg: message, a String, or a List of Strings
    Class constructor options: attempts, bargein, choices, minConfidence, name, recognizer, required, say, timeout, voice
    Convenience function: Tropo.say()

    (See https://www.tropo.com/docs/webapi/say.htm)

    { "say": {
        "as": String,
        "name": String,
        "required": Boolean,
        "value": String #Required
        } } 
    """
    def __init__(self, message, **options):
        dict = {}
        options_array = ['as', 'name', 'required']
        for opt in options_array:
            if opt in options:
                dict[opt] = options[opt]
        if (isinstance (message, list)):
            lis = []

            for mess in message:
                new_dict = dict.copy()
                new_dict['value'] = mess
                lis.append(new_dict)
            self.obj = {'say' : lis}
            self.json = lis
        else:
            dict['value'] = message
            self.obj = {'say' : dict}
            self.json = dict


class Session(object):
    """
    Session is the payload sent as an HTTP POST to your web application when a new session arrives. 
    (See https://www.tropo.com/docs/webapi/session.htm)
    """
    def __init__(self, session_json):
        logging.info ("POST data: %s" % session_json)
        session_data = jsonlib.loads(session_json)
        session_dict = session_data['session']
        for key in session_dict:
            val = session_dict[key]
            logging.info ("key: %s val: %s" % (key, val))

        for key in session_dict:
            val = session_dict[key]
            self.key = val



class StartRecording(object):
    """
    Class representing the "startRecording" Tropo action. Builds a "startRecording" JSON object.
    Class constructor arg: url, a String
    Class constructor options: format, method, username, password
    Convenience function: Tropo.startRecording()

    (See https://www.tropo.com/docs/webapi/startrecording.htm)

    { "startRecording": {
        "format": String,
        "method": String,
        "url": String,#Required
        "username": String,
        "password": String } } 
    """
    def __init__(self, url, **options):
        dict = {}
        dict['url'] = url
        options_array = ['format', 'method', 'username', 'password']

        for opt in options_array:
            if opt in options:
                dict[opt] = options[opt]
        self.obj = {'startRecording' : dict}
        self.json = dict

class StopRecording(object):
   """
    Class representing the "stopRecording" Tropo action. Builds a "stopRecording" JSON object.
    Class constructor arg:
    Class constructor options:
    Convenience function: Tropo.stopRecording()

   (See https://www.tropo.com/docs/webapi/stoprecording.htm)
      { "stopRecording": { } } 
   """
   def __init__(self):
       dict = {}
       self.obj = {'stopRecording' : dict}
       self.json = dict

class Transfer(object):
    """
    Class representing the "transfer" Tropo action. Builds a "transfer" JSON object.
    Class constructor arg: to, a String, or List
    Class constructor options: answerOnMedia, choices, from, name, required, terminator
    Convenience function: Tropo.transfer()

    (See https://www.tropo.com/docs/webapi/transfer.htm)
    { "transfer": {
        "to": String or Array,#Required
        "answerOnMedia": Boolean,
        "choices": Object,
        "from": Object,
        "name": String,
        "required": Boolean,
        "terminator": String,
        "timeout": Float } } 
    """
    def __init__(self, to, **options):
        dict = {}
        dict['to'] = to

        options_array = ['answerOnMedia', 'choices', 'from', 'name', 'required', 'terminator']

        for opt in options_array:
            if opt in options:
                if (opt == 'from'):
                    dict['from'] = options['from']
                elif(opt == 'choices'):
                    dict['choices'] = {'value' : options['choices']}
                else:
                    dict[opt] = options[opt]
        self.obj = {'transfer' : dict}
        self.json = dict


class Tropo(object):
    """
      This is the top level class for all the Tropo web api actions.
      The methods of this class implement individual Tropo actions.
      Individual actions are each methods on this class.

      Each method takes one or more required arguments, followed by optional
      arguments expressed as key=value pairs.
      
      The optional arguments for these methods are described here:
      https://www.tropo.com/docs/webapi/
    """
    def  __init__(self):
        self._steps = []


    def ask(self, choices, **options):
        """
	 Sends a prompt to the user and optionally waits for a response.
         Arguments: "choices" is a Choices object
         See https://www.tropo.com/docs/webapi/ask.htm
        """
        steps = self._steps
        ask_obj = Ask(choices, **options)
        piece = ask_obj.obj
        steps.append(piece)
        self._steps = steps

    def call (self, to, **options):
        """
	 Places a call or sends an an IM, Twitter, or SMS message. To start a call, use the Session API to tell Tropo to launch your code. 
	 
	 Arguments: to is a String.
	 Argument: **options is a set of optional keyword arguments.
	 See https://www.tropo.com/docs/webapi/call.htm
        """
        steps = self._steps
        call_obj = Call (to, **options)
        piece = call_obj.obj
#        steps.append({'message' : piece})
        steps.append(piece)
        self._steps = steps

    def conference(self, id, **options):
        """
        This object allows multiple lines in separate sessions to be conferenced together so that the parties on each line can talk to each other simultaneously. 
	This is a voice channel only feature. 
	Argument: "id" is a String
        Argument: **options is a set of optional keyword arguments.
	See https://www.tropo.com/docs/webapi/conference.htm
        """
        steps = self._steps
        conference_obj = Conference(id, **options)
        piece = conference_obj.obj
        steps.append(piece)
        self._steps = steps

    def hangup(self):
        """
        This method instructs Tropo to "hang-up" or disconnect the session associated with the current session.
	See https://www.tropo.com/docs/webapi/hangup.htm
        """
        steps = self._steps
        hangup_obj = Hangup()
        piece = hangup_obj.obj
        steps.append(piece)
        self._steps = steps

    def message (self, say_obj, to, **options):
        """
	A shortcut method to create a session, say something, and hang up, all in one step. This is particularly useful for sending out a quick SMS or IM. 
	
 	Argument: "say_obj" is a Say object
        Argument: "to" is a String
        Argument: **options is a set of optional keyword arguments.
        See https://www.tropo.com/docs/webapi/message.htm
        """
        steps = self._steps
        if isinstance(say_obj, str):
           say_obj1 = Say(say_obj).obj
           message_obj = Message(say_obj1, to, **options)
        else:
           message_obj = Message(say_obj, to, **options)
        piece = message_obj.obj
#        steps.append({'message' : piece})
        steps.append(piece)
        self._steps = steps


    def on(self, event, **options):
        """
        Adds an event callback so that your application may be notified when a particular event occurs. 
	Possible events are: "continue", "error", "incomplete" and "hangup". 
	Argument: event is an event
        Argument: **options is a set of optional keyword arguments.
        See https://www.tropo.com/docs/webapi/on.htm
        """
        on_obj = On(event, **options)
        steps = self._steps
        piece = on_obj.obj
#        steps.append({'on' : piece})
        steps.append(piece)
        self._steps = steps

    def record(self, **options):
        """
	 Plays a prompt (audio file or text to speech) and optionally waits for a response from the caller that is recorded. 
         Argument: **options is a set of optional keyword arguments.
	 See https://www.tropo.com/docs/webapi/record.htm
        """
        steps = self._steps
        record_obj = Record(**options)
        piece = record_obj.obj
        steps.append(piece)
        self._steps = steps


    def redirect(self, id, **options):
        """
        Forwards an incoming call to another destination / phone number before answering it. 
        Argument: id is a String
        Argument: **options is a set of optional keyword arguments.
        See https://www.tropo.com/docs/webapi/redirect.htm
        """
        steps = self._steps
        redirect_obj = Redirect(id, **options)
        piece = redirect_obj.obj
        steps.append(piece)
        self._steps = steps

    def reject(self):
        """
        Allows Tropo applications to reject incoming sessions before they are answered. 
        See https://www.tropo.com/docs/webapi/reject.htm
        """
        steps = self._steps
        reject_obj = Reject()
        piece = reject_obj.obj
        steps.append(piece)
        self._steps = steps

# ??? say may take an array of values
    def say(self, message, **options):
        """
	When the current session is a voice channel this key will either play a message or an audio file from a URL. 
	In the case of an text channel it will send the text back to the user via i nstant messaging or SMS. 
        Argument: message is a string
        Argument: **options is a set of optional keyword arguments.
        See https://www.tropo.com/docs/webapi/say.htm
        """
        steps = self._steps
        say_obj = Say(message, **options)
        piece = say_obj.obj
#        steps.append({'say' : piece})
        steps.append(piece)
        self._steps = steps
        return say_obj.json

    def startRecording(self, url, **options):
        """
        Allows Tropo applications to begin recording the current session. 
        Argument: url is a string
        Argument: **options is a set of optional keyword arguments.
        See https://www.tropo.com/docs/webapi/startrecording.htm
        """
        steps = self._steps
        startRecording_obj = StartRecording(url, **options)
        piece = startRecording_obj.obj
        steps.append(piece)
        self._steps = steps

    def stopRecording(self):
        """
        Stops a previously started recording.
	See https://www.tropo.com/docs/webapi/stoprecording.htm
        """
        steps = self._steps
        stopRecording_obj = StopRecording()
        piece = stopRecording_obj.obj
        steps.append(piece)
        self._steps = steps

    def transfer(self, to, **options):
        """
        Transfers an already answered call to another destination / phone number. 
	Argument: to is a string
        Argument: **options is a set of optional keyword arguments.
        See https://www.tropo.com/docs/webapi/transfer.htm
        """
        steps = self._steps
        transfer_obj = Transfer(to, **options)
        piece = transfer_obj.obj
        steps.append(piece)
        self._steps = steps

    def RenderJson(self, pretty=False):
        """
        Render a Tropo object into a Json string.
        """
        steps = self._steps
        topdict = {}
        topdict['tropo'] = steps
        logging.info ("topdict: %s" % topdict)
        if pretty:
            try:
                json = jsonlib.dumps(topdict, indent=4, sort_keys=False)
            except TypeError:
                json = jsonlib.dumps(topdict)
        else:
            json = jsonlib.dumps(topdict)
        return json

