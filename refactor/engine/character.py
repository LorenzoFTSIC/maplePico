class Character:

    def __init__(self, name):

        self.name = name
        self.skills = {}
        self.rotation = []

    def add_skill(self, skill):

        self.skills[skill.name] = skill