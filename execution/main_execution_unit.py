from . node_sorting import sortNodes
from . code_generator import (getInitialSocketVariables,
                              getSetupCode,
                              getNodeExecutionLines,
                              linkOutputSocketsToTargets)

class MainExecutionUnit:
    def __init__(self, network):
        self.network = network
        self.setupScript = ""
        self.executeScript = ""
        self.setupCodeObject = None
        self.executeCodeObject = None

        self.generateScripts()
        self.compileScripts()
        self.execute = self.raiseNotPreparedException


    def prepare(self):
        self.executionData = {}
        exec(self.setupCodeObject, self.executionData, self.executionData)
        self.execute = self.executeUnit

    def insertExecutionData(self, data):
        self.executionData.update(data)

    def finish(self):
        self.executionData.clear()
        self.execute = self.raiseNotPreparedException

    def executeUnit(self):
        exec(self.executeCodeObject, self.executionData, self.executionData)

    def raiseNotPreparedException(self):
        raise Exception()

    def getCode(self):
        return self.setupScript + "\n"*5 + self.executeScript



    def generateScripts(self):
        nodes = self.network.getAnimationNodes()
        nodes = sortNodes(nodes)

        socketVariables = getInitialSocketVariables(nodes)
        self.setupScript = getSetupCode(nodes, socketVariables)
        self.executeScript = self.getExecutionScript(nodes, socketVariables)

    def getExecutionScript(self, nodes, socketVariables):
        lines = []
        for node in nodes:
            lines.extend(getNodeExecutionLines(node, socketVariables))
            linkOutputSocketsToTargets(node, socketVariables)
        return "\n".join(lines)

    def compileScripts(self):
        self.setupCodeObject = compile(self.setupScript, "<setup>", "exec")
        self.executeCodeObject = compile(self.executeScript, "<execute>", "exec")