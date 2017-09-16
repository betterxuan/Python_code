
from mako.template import Template
from mako.lookup import TemplateLookup
from ubTptBase import TptBase
from ubDataPool import DataPool
from ubCommonUtils import *
import os

class TptEnv(TptBase):
    """DataPool: all extracted environment data are stored
    """
    def __init__(self):
        TptBase.__init__(self)
        self._genDir = '/env/'

    def updateFnameDict(self):
#        self._fnameDict['refbox_env.svh.py'] = self._dataPool.getTopName() + '_configs.svh'
        self._fnameDict['refbox_env.sv.py'] = 'refbox_env.sv'
        self._fnameDict['refbox_pkg.sv.py'] =  'refbox_pkg.sv'
        self._fnameDict['refbox_virtual_sequencer.sv.py'] = 'refbox_virtual_sequencer.sv'
        #=======================================================================
        # add some template elements for genbox  fnameDict refbox_env.svh
        #=======================================================================
        self._fnameDict['refbox_env1.sv.py'] = 'refbox_env1.sv'
#        self._fnameDict['try.py'] =  'try.txt'

    def renderAll(self):
        self.updateFnameDict()
        genDir = self._dataPool.getGenboxPath() + self._genDir
        for (key, val) in self._fnameDict.items():
            tpt = Template(filename=self._tptDir +key)
            logPrint(tpt.render())
            self.write(val, tpt.render(), genDir)


if __name__ == '__main__' :

    moduleTestList = []

    def testTptRender():
        tpt = TptEnv()
        dp = DataPool()
        dp.getValFromArchDict()
        setCoreDP(dp)
        tpt.setDataPool(dp)
        tpt.renderAll()


    moduleTestList.append(testTptRender)


    testTptRender()

#    for moduleTest in moduleTestList:
#        moduleTest()


