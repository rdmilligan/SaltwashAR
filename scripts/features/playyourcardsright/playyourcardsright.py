# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from features.base import Feature
from gametable import GameTable
from pybrain.rl.learners import Q
from pybrain.rl.explorers import EpsilonGreedyExplorer
from pybrain.rl.agents import LearningAgent
from gameinteraction import GameInteraction
from gameenvironment import GameEnvironment
from gametask import GameTask
from pybrain.rl.experiments import Experiment

class PlayYourCardsRight(Feature):
  
    def __init__(self, text_to_speech, speech_to_text):
        Feature.__init__(self)

        # setup AV Table
        self.av_table = GameTable(13, 2)
        if(self.av_table.loadParameters() == False):
            self.av_table.initialize(0.)
 
        # setup a Q-Learning agent
        learner = Q(0.5, 0.0)
        learner._setExplorer(EpsilonGreedyExplorer(0.0))
        self.agent = LearningAgent(self.av_table, learner)
 
        # setup game interaction
        self.game_interaction = GameInteraction(text_to_speech, speech_to_text)

        # setup environment
        environment = GameEnvironment(self.game_interaction)
 
        # setup task
        task = GameTask(environment, self.game_interaction)
 
        # setup experiment
        self.experiment = Experiment(task, self.agent)
    
    @property
    def is_speaking(self):
        return self.game_interaction.is_speaking

    def _thread(self, args):
        # let's play our cards right!
        while not self.is_stop:
            self.experiment.doInteractions(1)
            self.agent.learn()
            self.av_table.saveParameters()