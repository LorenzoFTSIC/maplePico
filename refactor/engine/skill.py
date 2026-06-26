class Skill:

    def __init__(
        self,
        name,
        key,
        action,
        hold_duration=0,
        spam_interval=0,
        cooldown=0,
        notes=""
    ):
        self.name = name
        self.key = key
        self.action = action

        self.hold_duration = hold_duration
        self.spam_interval = spam_interval
        self.cooldown = cooldown

        self.notes = notes