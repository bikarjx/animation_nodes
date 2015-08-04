import bpy
from ... base_types.node import AnimationNode

class SeparateVector(bpy.types.Node, AnimationNode):
    bl_idname = "an_SeparateVector"
    bl_label = "Separate Vector"
    isDetermined = True

    inputNames = { "Vector" : "vector" }

    outputNames = { "X" : "x",
                    "Y" : "y",
                    "Z" : "z" }

    def create(self):
        self.inputs.new("an_VectorSocket", "Vector")
        self.outputs.new("an_FloatSocket", "X")
        self.outputs.new("an_FloatSocket", "Y")
        self.outputs.new("an_FloatSocket", "Z")
        
    def execute(self, vector):
        return vector[0], vector[1], vector[2]