class Error:
    def __init__(self, enum, type, text, *args, resolved=False):
        self.enum = enum
        self.type = type
        self.text = text
        self.resolved = resolved
        self.instructions = args
