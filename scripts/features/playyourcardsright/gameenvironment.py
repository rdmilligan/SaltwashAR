from pybrain.rl.environments.environment import Environment
 
class GameEnvironment(Environment):
     
    def __init__(self, game_interaction):
        self.game_interaction = game_interaction
 
    def getSensors(self):
        return self.game_interaction.get_card()
                    
    def performAction(self, action):
        self.game_interaction.give_command(action)