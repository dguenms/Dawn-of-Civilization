## This file is part of Rhye's and Fall of Civilization.
## This file was originally taken from CivPath mod.
##  modified by eN

import CvEventManager
import CvRFCEventHandler
import RiseAndFall
import Congresses
import Religions

class CvRFCEventManager(CvEventManager.CvEventManager, object):

    """Extends the standard event manager by adding support for multiple
    handlers for each event.
    
    Methods exist for both adding and removing event handlers.  A set method 
    also exists to override the default handlers.  Clients should not depend 
    on event handlers being called in a particular order.
    
    This approach works best with mods that have implemented the design
    pattern suggested on Apolyton by dsplaisted.
    
    http://apolyton.net/forums/showthread.php?s=658a68df728b2719e9ebfe842d784002&threadid=142916
    
    The example given in the 8th post in the thread would be handled by adding
    the following lines to the CvCustomEventManager constructor.  The RealFort,
    TechConquest, and CulturalDecay classes can remain unmodified.
    
        self.addEventHandler("unitMove", rf.onUnitMove)
        self.addEventHandler("improvementBuilt", rf.onImprovementBuilt)
        self.addEventHandler("techAcquired", rf.onTechAcquired)
        self.addEventHandler("cityAcquired", tc.onCityAcquired)
        self.addEventHandler("EndGameTurn", cd.onEndGameTurn)
        
    Note that the naming conventions for the event type strings vary from event
    to event.  Some use initial capitalization, some do not; some eliminate the
    "on..." prefix used in the event handler function name, some do not.  Look
    at the unmodified CvEventManager.py source code to determine the correct
    name for a particular event.
    
    Take care with event handlers that also extend CvEventManager.  Since
    this event manager handles invocation of the base class handler function,
    additional handlers should not also call the base class function themselves.

    """

    def __init__(self, *args, **kwargs):
        super(CvRFCEventManager, self).__init__(*args, **kwargs)
        # map the initial EventHandlerMap values into the new data structure
        for eventType, eventHandler in self.EventHandlerMap.iteritems():
            self.setEventHandler(eventType, eventHandler)

        self.CustomEvents = {
            7614 : ('RiseAndFallPopupEvent', self.rnfEventApply7614, self.rnfEventBegin7614),
            7615 : ('FlipPopupEvent', self.rnfEventApply7615, self.rnfEventBegin7615),
            7616 : ('VotePopupEvent', self.congEventApply7616, self.congEventBegin7616),
            7617 : ('AskCityPopupEvent', self.congEventApply7617, self.congEventBegin7617),
            7618 : ('DecisionPopupEvent', self.congEventApply7618, self.congEventBegin7618),
            7619 : ('InvitationPopupEvent', self.congEventApply7619, self.congEventBegin7619),
            7620 : ('BribePopupEvent', self.congEventApply7620, self.congEventBegin7620),
            7621 : ('GoldPopupEvent', self.congEventApply7621, self.congEventBegin7621),
            7622 : ('ResurrectionEvent', self.rnfEventApply7622, self.rnfEventBegin7622),
            7623 : ('AskNoCityPopupEvent', self.congEventApply7623, self.congEventBegin7623),
            7624 : ('ReformationEvent', self.relEventApply7624, self.relEventBegin7624)
        }

        # --> INSERT EVENT HANDLER INITIALIZATION HERE <--
        CvRFCEventHandler.CvRFCEventHandler(self)
        self.rnf = RiseAndFall.RiseAndFall()
        self.cong = Congresses.Congresses()
        self.rel = Religions.Religions()
        

    def addEventHandler(self, eventType, eventHandler):
        """Adds a handler for the given event type.
        
        A list of supported event types can be found in the initialization 
        of EventHandlerMap in the CvEventManager class.

        """
        self.EventHandlerMap[eventType].append(eventHandler)

    def removeEventHandler(self, eventType, eventHandler):
        """Removes a handler for the given event type.
        
        A list of supported event types can be found in the initialization 
        of EventHandlerMap in the CvEventManager class.  It is an error if 
        the given handler is not found in the list of installed handlers.

        """
        self.EventHandlerMap[eventType].remove(eventHandler)
    
    def setEventHandler(self, eventType, eventHandler):
        """Removes all previously installed event handlers for the given 
        event type and installs a new handler .
        
        A list of supported event types can be found in the initialization 
        of EventHandlerMap in the CvEventManager class.  This method is 
        primarily useful for overriding, rather than extending, the default 
        event handler functionality.

        """
        self.EventHandlerMap[eventType] = [eventHandler]

    def handleEvent(self, argsList):
        """Handles events by calling all installed handlers."""
        self.origArgsList = argsList
        flagsIndex = len(argsList) - 6
        self.bDbg, self.bMultiPlayer, self.bAlt, self.bCtrl, self.bShift, self.bAllowCheats = argsList[flagsIndex:]
        eventType = argsList[0]
        return {
            "kbdEvent": self._handleConsumableEvent,
            "mouseEvent": self._handleConsumableEvent,
            "OnSave": self._handleOnSaveEvent,
            "OnLoad": self._handleOnLoadEvent
        }.get(eventType, self._handleDefaultEvent)(eventType, argsList[1:])

    def _handleDefaultEvent(self, eventType, argsList):
        if self.EventHandlerMap.has_key(eventType):
            for eventHandler in self.EventHandlerMap[eventType]:
                # the last 6 arguments are for internal use by handleEvent
                eventHandler(argsList[:len(argsList) - 6])

    def _handleConsumableEvent(self, eventType, argsList):
        """Handles events that can be consumed by the handlers, such as
        keyboard or mouse events.
        
        If a handler returns non-zero, processing is terminated, and no 
        subsequent handlers are invoked.

        """
        if self.EventHandlerMap.has_key(eventType):
            for eventHandler in self.EventHandlerMap[eventType]:
                # the last 6 arguments are for internal use by handleEvent
                result = eventHandler(argsList[:len(argsList) - 6])
                if (result > 0):
                    return result
        return 0

    # TODO: this probably needs to be more complex
    def _handleOnSaveEvent(self, eventType, argsList):
        """Handles OnSave events by concatenating the results obtained
        from each handler to form an overall consolidated save string.

        """
        result = ""
        if self.EventHandlerMap.has_key(eventType):
            for eventHandler in self.EventHandlerMap[eventType]:
                # the last 6 arguments are for internal use by handleEvent
                result = result + eventHandler(argsList[:len(argsList) - 6])
        return result

    # TODO: this probably needs to be more complex
    def _handleOnLoadEvent(self, eventType, argsList):
        """Handles OnLoad events."""
        return self._handleDefaultEvent(eventType, argsList)

    # popup event handlers
    def beginEvent( self, context, argsList=-1 ):
            '''Begin Event'''
            if(self.CustomEvents.has_key(context)):
                    return self.CustomEvents[context][2](argsList)
            else:
                    super(CvRFCEventManager, self).beginEvent(context, argsList)
        
    def applyEvent( self, argsList ):
            '''Apply the effects of an event'''
            context, playerID, netUserData, popupReturn = argsList
            
            if(self.CustomEvents.has_key(context)):
                    entry = self.CustomEvents[context]
                    # the apply function
                    return entry[1]( playerID, netUserData, popupReturn )   
            else:
                    return super(CvRFCEventManager, self).applyEvent(argsList)

    # popup events
    def rnfEventBegin7614(self):
            pass
       
    def rnfEventApply7614(self, playerID, netUserData, popupReturn):
            self.rnf.eventApply7614(popupReturn)

    def rnfEventBegin7615(self):
            pass
       
    def rnfEventApply7615(self, playerID, netUserData, popupReturn):
            self.rnf.eventApply7615(popupReturn)

    def congEventBegin7616(self):
            pass
       
    def congEventApply7616(self, playerID, netUserData, popupReturn):
            self.cong.eventApply7616(popupReturn)

    def congEventBegin7617(self):
            pass
       
    def congEventApply7617(self, playerID, netUserData, popupReturn):
            self.cong.eventApply7617(popupReturn)

    def congEventBegin7618(self):
            pass
       
    def congEventApply7618(self, playerID, netUserData, popupReturn):
            self.cong.eventApply7618(popupReturn)

    def congEventBegin7619(self):
            pass
       
    def congEventApply7619(self, playerID, netUserData, popupReturn):
            self.cong.eventApply7619(popupReturn)

    def congEventBegin7620(self):
            pass
       
    def congEventApply7620(self, playerID, netUserData, popupReturn):
            self.cong.eventApply7620(popupReturn)

    def congEventBegin7621(self):
            pass
       
    def congEventApply7621(self, playerID, netUserData, popupReturn):
            self.cong.eventApply7621(popupReturn)

    def rnfEventBegin7622(self):
            pass
       
    def rnfEventApply7622(self, playerID, netUserData, popupReturn):
            self.rnf.eventApply7622(popupReturn)

    def congEventBegin7623(self):
            pass
       
    def congEventApply7623(self, playerID, netUserData, popupReturn):
            self.cong.eventApply7623(popupReturn)

    def relEventBegin7624(self):
            pass
       
    def relEventApply7624(self, playerID, netUserData, popupReturn):
            self.rel.eventApply7624(popupReturn)
