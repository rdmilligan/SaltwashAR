from threading import Thread
from gametable import GameTable
from pybrain.rl.learners import Q
from pybrain.rl.explorers import EpsilonGreedyExplorer
from pybrain.rl.agents import LearningAgent
from gameinteraction import GameInteraction
from gameenvironment import GameEnvironment
from gametask import GameTask
from pybrain.rl.experiments import Experiment

class PlayYourCardsRight:
  
    def __init__(self, text_to_speech, speech_to_text):
        self.thread = None
        self.is_stop = False

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

    def start(self):
        self.is_stop = False
        
        if self.thread and self.thread.is_alive(): return

        self.thread = Thread(target=self._thread)
        self.thread.start()

    def stop(self):
        self.is_stop = True

    def _thread(self):
        # let's play our cards right!
        while not self.is_stop:
            self.experiment.doInteractions(1)
            self.agent.learn()
            self.av_table.saveParameters()