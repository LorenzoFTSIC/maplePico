class Character:

    def __init__(self, name):
        self.name = name
        self.skills = {}
        self.rotations = {}

    def addSkill(self, skill):
        self.skills[skill.name] = skill

    def addRotation(self, name, rotation):
        self.rotations[name] = rotation