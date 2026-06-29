class Skill:

    def __init__(self, name, key, cooldown=0, templateLocation=None ):
        self.name = name
        self.key = key
        self.cooldown = cooldown
        self.templateLocation = templateLocation