
class MessagesPlace():
    """docstring for ."""

    def __init__(self):
        self.SendableMessages = {}

    async def CheckMessage(self, MessageId, Reaction, User):
        if MessageId in self.SendableMessages:
            await self.SendableMessages[MessageId](Reaction, User)
