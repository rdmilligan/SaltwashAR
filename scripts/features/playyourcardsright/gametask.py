# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from pybrain.rl.environments.task import Task
  
class GameTask(Task):
  
    def __init__(self, environment, game_interaction):
        self.env = environment
        self.game_interaction = game_interaction
      
    def getObservation(self):
        return self.env.getSensors()
  
    def performAction(self, action):
        self.env.performAction(action)
  
    def getReward(self):
        return self.game_interaction.get_result()