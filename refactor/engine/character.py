class Character:

    def __init__(self, name):
        self.name = name
        self.rotations = {}

    def addRotation(self, rotation):
        self.rotations[rotation.name] = rotation

    def getRotation(self, name):
        return self.rotations.get(name)