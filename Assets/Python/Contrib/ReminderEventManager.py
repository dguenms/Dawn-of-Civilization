##-------------------------------------------------------------------
## Modified from reminder by eotinb
## by Ruff and EF
##-------------------------------------------------------------------
## Reorganized to work via CvCustomEventManager
## using Civ4lerts as template.
## CvCustomEventManager & Civ4lerts by Gillmer J. Derge
##-------------------------------------------------------------------
## EF: Turned into a real queue, can be disabled
##-------------------------------------------------------------------

from CvPythonExtensions import *
import CvMainInterface
import CvUtil
import Popup as PyPopup
import BugCore
import BugUtil
import PlayerUtil
import SdToolKit
import autolog

SD_MOD_ID = "Reminders"
SD_QUEUES_ID = "queues"
SD_QUEUE_ID = "queue" # old format saves a single queue

STORE_EVENT_ID = CvUtil.getNewEventID("Reminder.Store")
RECALL_EVENT_ID = CvUtil.getNewEventID("Reminder.Recall")
RECALL_AGAIN_EVENT_ID = CvUtil.getNewEventID("Reminder.RecallAgain")

gc = CyGlobalContext()

ReminderOpt = BugCore.game.Reminder
g_eventMgr = None
g_autolog = None

g_reminders = None

# Used to display flashing end-of-turn text
g_turnReminderTexts = None

# Used to receive network messages
g_hasNetMessage = hasattr(CyPlayer, "addReminder")
def hasNetMessage():
	return g_hasNetMessage
def netAddReminder(args):
	playerID, turn, message = args
	g_reminders.push(playerID, Reminder(turn, message))
# expose to DLL
import CvAppInterface
CvAppInterface.netAddReminder = netAddReminder

# Shortcut - Create Reminder
def createReminder(argsList):
	g_eventMgr.beginEvent(STORE_EVENT_ID)

class ReminderEventManager:

	def __init__(self, eventManager):
		global g_autolog
		g_autolog = autolog.autologInstance()
		global g_eventMgr
		g_eventMgr = eventManager
		self.initReminders()
		eventManager.addEventHandler("BeginActivePlayerTurn", self.onBeginActivePlayerTurn)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)
		eventManager.addEventHandler("endTurnReady", self.onEndTurnReady)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("PythonReloaded", self.onLoadGame)
		eventManager.addEventHandler("OnPreSave", self.onPreSave)
		eventManager.addEventHandler("SwitchHotSeatPlayer", self.onSwitchHotSeatPlayer)
		eventManager.setPopupHandlers(STORE_EVENT_ID, 'Reminder.Store', self.__eventReminderStoreBegin, self.__eventReminderStoreApply)
		eventManager.setPopupHandlers(RECALL_EVENT_ID, 'Reminder.Recall', self.__eventReminderRecallBegin, self.__eventReminderRecallApply)
		eventManager.setPopupHandlers(RECALL_AGAIN_EVENT_ID, 'Reminder.RecallAgain', self.__eventReminderRecallAgainBegin, self.__eventReminderRecallAgainApply)

	def __eventReminderStoreBegin(self, argsList):
		header = BugUtil.getPlainText("TXT_KEY_REMINDER_HEADER")
		prompt = BugUtil.getPlainText("TXT_KEY_REMINDER_PROMPT")
		ok = BugUtil.getPlainText("TXT_KEY_MAIN_MENU_OK")
		cancel = BugUtil.getPlainText("TXT_KEY_POPUP_CANCEL")
		popup = PyPopup.PyPopup(STORE_EVENT_ID, EventContextTypes.EVENTCONTEXT_SELF)
		popup.setHeaderString(header)
		popup.setBodyString(prompt)
		popup.createSpinBox(0, "", 1, 1, 1500, 0)
		popup.createEditBox("", 1)
		popup.addButton(ok)
		popup.addButton(cancel)
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __eventReminderStoreApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() != 1):
			turns = popupReturn.getSpinnerWidgetValue(0)
			if turns < 0:
				BugUtil.error("Invalid number of turns (%d) for reminder", turns)
			else:
				reminderTurn = turns + gc.getGame().getGameTurn()
				reminderText = popupReturn.getEditBoxString(1)
				self.addReminder(playerID, Reminder(reminderTurn, reminderText))
				if (g_autolog.isLogging() and ReminderOpt.isAutolog()):
					g_autolog.writeLog("Reminder: On Turn %d, %s" % (reminderTurn, reminderText))

	def __eventReminderRecallBegin(self, argsList):
		self.showReminders(False)

	def __eventReminderRecallApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() != 1):
			if (self.reminder):
				self.reminder.turn = gc.getGame().getGameTurn()
				self.addReminder(playerID, self.reminder)
				self.reminder = None

	def __eventReminderRecallAgainBegin(self, argsList):
		self.showReminders(True)

	def __eventReminderRecallAgainApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() != 1):
			if (self.reminder):
				# Put it back into the queue for next turn
				self.reminder.turn += 1
				self.addReminder(playerID, self.reminder)
				self.reminder = None

	def showReminders(self, endOfTurn):
		global g_turnReminderTexts
		thisTurn = gc.getGame().getGameTurn()
		if (endOfTurn):
			prompt = BugUtil.getPlainText("TXT_KEY_REMIND_NEXT_TURN_PROMPT")
			eventId = RECALL_AGAIN_EVENT_ID
		else:
			g_turnReminderTexts = ""
			prompt = BugUtil.getPlainText("TXT_KEY_REMIND_END_TURN_PROMPT")
			eventId = RECALL_EVENT_ID
		yes = BugUtil.getPlainText("TXT_KEY_POPUP_YES")
		no = BugUtil.getPlainText("TXT_KEY_POPUP_NO")
		queue = self.reminders.get(PlayerUtil.getActivePlayerID())
		while (not queue.isEmpty()):
			nextTurn = queue.nextTurn()
			if (nextTurn > thisTurn):
				break
			elif (nextTurn < thisTurn):
				# invalid (lost) reminder
				reminder = queue.pop()
				BugUtil.warn("Reminder - skipped turn %d: %s", reminder.turn, reminder.message)
			else:
				self.reminder = queue.pop()
				if (g_autolog.isLogging() and ReminderOpt.isAutolog()):
					g_autolog.writeLog("Reminder: %s" % self.reminder.message)
				if (not endOfTurn):
					if (g_turnReminderTexts):
						g_turnReminderTexts += ", "
					g_turnReminderTexts += self.reminder.message
				if (ReminderOpt.isShowMessage()):
					CyInterface().addMessage(PlayerUtil.getActivePlayerID(), True, 10, self.reminder.message, 
											 None, 0, None, ColorTypes(8), 0, 0, False, False)
				if (ReminderOpt.isShowPopup()):
					popup = PyPopup.PyPopup(eventId, EventContextTypes.EVENTCONTEXT_SELF)
					popup.setHeaderString(self.reminder.message)
					popup.setBodyString(prompt)
					popup.addButton(yes)
					popup.addButton(no)
					popup.launch(False)

	def initReminders(self):
		self.setReminders(Reminders())
		self.reminder = None
	
	def setReminders(self, queues):
		self.reminders = queues
		global g_reminders
		g_reminders = queues

	def clearReminders(self):
		self.reminders.clear()
		global g_turnReminderTexts
		g_turnReminderTexts = None
	
	def addReminder(self, playerID, reminder):
		if hasNetMessage():
			player = gc.getPlayer(playerID)
			player.addReminder(reminder.turn, reminder.message)
		else:
			self.reminders.push(playerID, reminder)
	
	def createReminder(self):
		g_eventMgr.beginEvent(STORE_EVENT_ID)
	
	def onSwitchHotSeatPlayer(self, argsList):
		"""
		Clears the end turn text so hot seat players don't see each other's reminders.
		"""
		ePlayer = argsList[0]
		global g_turnReminderTexts
		g_turnReminderTexts = None

	def onBeginActivePlayerTurn(self, argsList):
		"""
		Display the active player's reminders.
		"""
		iGameTurn = argsList[0]
		global g_turnReminderTexts
		g_turnReminderTexts = None
		if (ReminderOpt.isEnabled()):
			g_eventMgr.beginEvent(RECALL_EVENT_ID)

	def onEndGameTurn(self, argsList):
		"""
		Clears reminders up to and including the turn that just ended for all players.
		"""
		iGameTurn = argsList[0]
		self.reminders.clearBefore(iGameTurn + 1)

	def onEndTurnReady(self, argsList):
		"""
		Display reminders set to repeat this turn.
		"""
		iGameTurn = argsList[0]
		if (ReminderOpt.isEnabled()):
			g_eventMgr.beginEvent(RECALL_AGAIN_EVENT_ID)

	def onGameStart(self, argsList):
		"""
		Clear all reminders.
		"""
		self.clearReminders()

	def onLoadGame(self, argsList):
		"""
		Load saved reminders.
		"""
		self.clearReminders()
		queues = SdToolKit.sdGetGlobal(SD_MOD_ID, SD_QUEUES_ID)
		if queues:
			self.setReminders(queues)
		else:
			# check for old save format (single queue)
			queue = SdToolKit.sdGetGlobal(SD_MOD_ID, SD_QUEUE_ID)
			if queue:
				BugUtil.info("Reminder - Converting single-queue format")
				self.setReminders(Reminders(queue))
				SdToolKit.sdDelGlobal(SD_MOD_ID, SD_QUEUE_ID)

	def onPreSave(self, argsList):
		"""
		Save reminders.
		"""
		if self.reminders.isEmpty():
			SdToolKit.sdDelGlobal(SD_MOD_ID, SD_QUEUES_ID)
		else:
			SdToolKit.sdSetGlobal(SD_MOD_ID, SD_QUEUES_ID, self.reminders)


class Reminder(object):
	def __init__(self, turn, message):
		self.turn = turn
		self.message = message

class ReminderQueue(object):
	def __init__(self):
		self.clear()
	def clear(self):
		self.queue = []
	def clearBefore(self, turn, log=False):
		while not self.isEmpty() and self.nextTurn() < turn:
			reminder = self.pop()
			if log:
				BugUtil.warn("Reminder - skipped turn %d: %s", reminder.turn, reminder.message)
	def size(self):
		return len(self.queue)
	def isEmpty(self):
		return self.size() == 0
	def nextTurn(self):
		reminder = self.peek()
		if reminder:
			return reminder.turn
		else:
			return -1
	def push(self, reminder):
		for i, r in enumerate(self.queue):
			if (reminder.turn < r.turn):
				self.queue.insert(i, reminder)
				break
		else:
			self.queue.append(reminder)
	def pop(self):
		if self.isEmpty():
			return None
		else:
			return self.queue.pop(0)
	def peek(self):
		if self.isEmpty():
			return None
		else:
			return self.queue[0]

class EmptyQueue(object):
	def clear(self):
		BugUtil.warn("Cannot call EmptyQueue.clear()")
	def clearBefore(self, turn, log=False):
		pass
	def size(self):
		return 0
	def isEmpty(self):
		return True
	def nextTurn(self):
		return -1
	def push(self, reminder):
		BugUtil.error("Cannot call EmptyQueue.push()")
	def pop(self):
		return None
	def peek(self):
		return None
EMPTY_QUEUE = EmptyQueue()

class Reminders(object):
	def __init__(self, queue=None):
		self.clear()
		if queue:
			self.queues[PlayerUtil.getActivePlayerID()] = queue
	def clear(self):
		self.queues = {}
	def clearBefore(self, turn, log=False):
		for queue in self.queues.itervalues():
			queue.clearBefore(turn, log)
	def exists(self, playerID):
		return playerID in self.queues
	def get(self, playerID):
		if self.exists(playerID):
			return self.queues[playerID]
		else:
			return EMPTY_QUEUE
	def getForUpdate(self, playerID):
		if self.exists(playerID):
			return self.queues[playerID]
		else:
			queue = self.queues[playerID] = ReminderQueue()
			return queue
	def size(self, playerID=None):
		if playerID:
			return self.get(playerID).size()
		else:
			return len(self.queues)
	def isEmpty(self, playerID=None):
		return self.size(playerID) == 0
	def nextTurn(self, playerID):
		return self.get(playerID).nextTurn()
	def push(self, playerID, reminder):
		self.getForUpdate(playerID).push(reminder)
	def pop(self, playerID):
		self.get(playerID).pop()
	def peek(self, playerID):
		return self.get(playerID).peek()
