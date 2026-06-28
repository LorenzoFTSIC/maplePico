class Character:

    def __init__(self, name):
        self.name = name
        self.skills = {}
        self.rotations = {}

    def add_skill(self, skill):
        self.skills[skill.name] = skill

    def add_rotation(self, name, rotation):
        self.rotations[name] = rotation