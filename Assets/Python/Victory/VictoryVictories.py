


class Victory(object):

	def __init__(self, iPlayer, descriptions):
		self.iPlayer = iPlayer
		self.goals = tuple(self.create_goal(description) for description in descriptions)

	def on_success(self, goal):
		goal.announce_success()

	def on_failure(self, goal):
		goal.announce_failure()

	def succeeded_goals(self):
		return count(goal.succeeded() for goal in self.goals)

	def create_goal(self, description):
		def succeed(goal):
			goal.set_state(SUCCESS)
			self.on_success(goal)

		def failure(goal):
			goal.set_state(FAILURE)
			self.on_failure(goal)

		goal = description(self.iPlayer)
		
		goal.succeed = succeed.__get__(goal, Goal)
		goal.fail = fail.__get__(goal, Goal)
		