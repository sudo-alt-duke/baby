import discord
from discord import app_commands, ui
import asyncio
import random

TOKEN = 'token here'

BABY_WORDS = [
    "apple", "banana", "cherry", "dragon", "elephant", "flower", "guitar", "house", 
    "island", "jungle", "kite", "lemon", "mountain", "night", "ocean", "piano",
    "queen", "rainbow", "sunset", "tiger", "umbrella", "violin", "waterfall", "xylophone",
    "yellow", "zebra", "angel", "baby", "cloud", "diamond", "eagle", "fire",
    "garden", "honey", "ice", "jewel", "king", "love", "moon", "star",
    "tree", "unicorn", "violet", "wolf", "box", "yacht", "zoo", "air",
    "book", "cat", "dog", "egg", "fish", "gold", "hat", "ink",
    "jar", "key", "lamp", "mouse", "nest", "orange", "pig", "quilt",
    "rose", "snake", "train", "unity", "voice", "wind", "fox", "yo-yo",
    "zip", "atom", "beam", "cube", "disk", "energy", "flame", "globe",
    "heart", "iris", "jade", "koala", "lotus", "mist", "nova", "opal",
    "pearl", "quartz", "ruby", "sage", "topaz", "aura", "bloom", "crimson",
    "dawn", "echo", "frost", "glade", "haven", "ivory", "jasmine", "karma",
    "lunar", "mystic", "nebula", "obsidian", "phoenix", "quiver", "ripple", "shadow",
    "thunder", "umbra", "valley", "whisper", "zenith", "azure", "bliss", "cascade",
    "drift", "ember", "fable", "glimmer", "harbor", "illusion", "journey", "kindle",
    "lagoon", "mirage", "nimbus", "oracle", "prism", "quest", "radiant", "solstice",
    "tide", "unity", "voyage", "wander", "yearn", "zephyr", "arctic", "breeze",
    "coral", "dusk", "eternal", "fjord", "gale", "horizon", "inferno", "jungle",
    "kelp", "lagoon", "meadow", "nature", "oasis", "plasma", "quartz", "reef",
    "savanna", "tundra", "utopia", "volcano", "willow", "xenon", "yonder", "zen",
    "acorn", "brook", "cliff", "dune", "estuary", "fern", "grove", "hill",
    "icicle", "jetty", "knoll", "lake", "marsh", "nook", "oak", "pond",
    "quarry", "ridge", "stream", "thicket", "undergrowth", "vale", "wood", "yew",
    "alley", "bridge", "canyon", "desert", "escarpment", "field", "glacier", "heath",
    "inlet", "juniper", "karst", "loch", "moor", "narrows", "outcrop", "prairie",
    "quagmire", "rainforest", "savannah", "taiga", "upland", "valley", "wetland", "xeric",
    "yardang", "zone", "amber", "bronze", "copper", "denim", "emerald", "fuchsia",
    "green", "hazel", "indigo", "jade", "khaki", "lime", "magenta", "navy",
    "olive", "pink", "quince", "red", "silver", "teal", "ultramarine", "vermilion",
    "white", "yellow", "aquamarine", "burgundy", "cerulean", "chartreuse", "cobalt", "damson",
    "ebony", "flax", "garnet", "heliotrope", "ivory", "jet", "kelly", "lavender",
    "maroon", "ochre", "periwinkle", "rose", "saffron", "taupe", "umber", "vanilla",
    "wheat", "zaffre", "alabaster", "beige", "carmine", "dandelion", "ecru", "fulvous"
]

IMAGE_LINKS = [
    "https://files.catbox.moe/f2xnwf.png",
    "https://files.catbox.moe/hp3v69.png",
    "https://files.catbox.moe/yl5or3.jpg",
    "https://files.catbox.moe/x8alvd.gif"
]

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.dm_messages = True

class BabyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.is_spamming = False
        self.target_channel_id = None

    async def setup_hook(self):
        await self.tree.sync()

bot = BabyBot()


class SayModal(ui.Modal, title="Enter your message"):
    user_input = ui.TextInput(
        label="Your message",
        placeholder="Type what you want to spam here...",
        required=True,
        max_length=1000
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        view = SayButtonView(self.user_input.value)
        await interaction.response.send_message(
            f"Click the button to spam 3 messages with: `{self.user_input.value}`",
            ephemeral=True,
            view=view
        )


class BabyButtonView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.click_count = 0
        self.add_item(ui.Button(label="join the discord", url="dead link", style=discord.ButtonStyle.link))
    
    @ui.button(label="Start Spam", style=discord.ButtonStyle.green, custom_id="baby_spam_button")
    async def start_spam_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer(ephemeral=False)
        
        message_count = 10 if self.click_count == 0 else 3
        
        for i in range(message_count):
            try:
                random_words = " ".join(random.sample(BABY_WORDS, 10))
                msg = f"{random_words}\n\n" + "\n".join(IMAGE_LINKS)
                await interaction.followup.send(msg)
                print(f"sent #{i+1}")
                if i < message_count - 1:
                    await asyncio.sleep(0.5)
            except discord.errors.HTTPException as e:
                if e.status == 429:
                    await asyncio.sleep(e.retry_after if hasattr(e, 'retry_after') else 1)
                else:
                    print(f'http error: {e}')
                    break
            except Exception as e:
                print(f'error: {e}')
                break
        
        self.click_count += 1


class SayButtonView(ui.View):
    def __init__(self, user_text):
        super().__init__(timeout=None)
        self.user_text = user_text
        self.click_count = 0
        self.add_item(ui.Button(label="join the discord", url="dead link", style=discord.ButtonStyle.link))
    
    @ui.button(label="Start Spam", style=discord.ButtonStyle.green, custom_id="say_spam_button")
    async def start_spam_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer(ephemeral=False)
        
        message_count = 10 if self.click_count == 0 else 3
        
        for i in range(message_count):
            try:
                await interaction.followup.send(self.user_text)
                print(f"sent #{i+1}")
                if i < message_count - 1:
                    await asyncio.sleep(0.5)
            except discord.errors.HTTPException as e:
                if e.status == 429:
                    await asyncio.sleep(e.retry_after if hasattr(e, 'retry_after') else 1)
                else:
                    print(f'http error: {e}')
                    break
            except Exception as e:
                print(f'error: {e}')
                break
        
        self.click_count += 1


@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')
    print(f'{len(bot.guilds)} guilds')


@app_commands.command(name="baby", description="sdjibabyasdhwaskdaskdwaskhaddsasdasdsad skibidi toilet mama")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def baby_command(interaction: discord.Interaction):
    view = BabyButtonView()
    await interaction.response.send_message(
        "Click the button below to start spamming 3 messages with random words and images!",
        ephemeral=True,
        view=view
    )


@app_commands.command(name="stop", description="it doesnt work geg")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def stop_baby(interaction: discord.Interaction):
    if not bot.is_spamming:
        await interaction.response.send_message('Baby spam is not currently running.', ephemeral=True)
        return
    bot.is_spamming = False
    await interaction.response.send_message('Stopping baby spam!')


@app_commands.command(name="ping", description="up status")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f'Pong! Latency: {latency}ms')


@app_commands.command(name="say2", description="qwahre")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def say2_command(interaction: discord.Interaction):
    modal = SayModal()
    await interaction.response.send_modal(modal)


bot.tree.add_command(baby_command)
bot.tree.add_command(stop_baby)
bot.tree.add_command(ping)
bot.tree.add_command(say2_command)

if __name__ == '__main__':
    bot.run(TOKEN)
    
    # made by margetock
