class CreateTextChannelAction(Action):
    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id if category_id != None else 0

    async def run(self, bot: commands.Bot):
        gu = guild(bot)
        if self.category_id != 0:
            ct = await gu.fetch_channel(self.category_id)
            await gu.create_text_channel(self.name, category=ct)
        else:
            await gu.create_text_channel(self.name)

    def ID(self):
        return 0

    def as_dict(self):
        return {
            "name": self.name,
            "category_id": self.category_id
        }