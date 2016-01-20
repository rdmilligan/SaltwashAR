# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from pybrain.rl.learners.valuebased import ActionValueTable
import numpy
 
class GameTable(ActionValueTable):
     
    PARAMS_FILENAME = 'scripts/features/playyourcardsright/params.npy'
 
    # load table parameters from file
    def loadParameters(self):
        try:
            self._params = numpy.load(self.PARAMS_FILENAME)
            print "Loaded parameters: {}".format(self._params)
            return True
        except:
            print "Error loading params file"
            return False
     
    # save table parameters to file
    def saveParameters(self):
        try:
            self._params.dump(self.PARAMS_FILENAME)
            print "Saved parameters: {}".format(self._params)
            return True
        except:
            print "Error saving params file"
            return False