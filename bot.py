import discord
from discord.ext import commands
import random
import os

PORT = os.getenv('PORT', 8000)
app.run(host='0.0.0.0', port=PORT)

# Enable member intents so the bot can see who's in the server.
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  

# Set the command prefix and pass intents
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------------------
# Global game state variables
# ---------------------------
game_state = {
    "players": [],       # List of discord.Member objects representing players
    "theme": None,       # Current theme (e.g., "animals", "movies", etc.)
    "mode": None,        # Game mode: 1 for words mode, 2 for questions mode
    "imposter": None,    # The chosen imposter for the round
    # Dictionary for theme words.
    # Replace the example words with your own. For custom themes, add your own key and list.
    "theme_words": {
        "animals": ["lion", "tiger", "penguin", "seal", "elephant", "giraffe", "zebra", "kangaroo", "koala", "bear", "cheetah", "leopard", "wolf", "fox", "crocodile", "hippopotamus", "rhinoceros", "camel", "donkey", "horse", "cow", "sheep", "goat", "pig", "chicken", "duck", "goose", "turkey", "ostrich", "emu", "flamingo", "peacock", "parrot", "eagle", "hawk", "falcon", "owl", "bat", "squirrel", "rabbit", "mouse", "rat", "hamster", "guinea pig", "otter", "beaver", "raccoon", "skunk", "deer", "moose", "elk", "bison", "buffalo", "antelope", "lemur", "chimpanzee", "orangutan", "baboon", "macaw", "toucan", "seagull", "walrus", "narwhal", "dolphin", "whale", "shark", "octopus", "jellyfish", "starfish", "crab", "lobster", "shrimp", "snail", "turtle", "tortoise", "lizard", "snake", "frog", "toad", "newt", "salamander", "crow", "raven", "sparrow", "robin", "woodpecker", "hummingbird", "swan", "pigeon", "dove", "badger", "hedgehog", "porcupine", "armadillo", "sloth", "llama", "alpaca", "yak", "ferret", "mole"],
        "movies": ["Inception", "The Shawshank Redemption", "The Godfather", "The Dark Knight"],
        "actors": ["Sydney Sweeney", "Johnny Depp", "Leonardo DiCaprio", "Tom Cruise"],
        "food": ["Pizza", "Burger", "Sushi", "Pasta", "Tacos", "Sandwich", "Fried Chicken", "Ice Cream", "Steak", "French Fries", "Chocolate", "Cheeseburger", "Ramen", "Hot Dog", "Donut", "Nachos", "Salad", "Burrito", "Curry", "Lasagna", "Chicken Wings", "Dumplings", "Pancakes", "Waffles", "Quesadilla", "Mac and Cheese", "Spaghetti", "Spring Rolls", "Pho", "BBQ Ribs", "Bagel", "Croissant", "Apple Pie", "Grilled Cheese", "Chicken Nuggets", "Samosa", "Meatballs", "Churros", "Falafel", "Onion Rings", "Mashed Potatoes", "Tuna Sandwich", "Fajitas", "Pad Thai", "Lobster", "Shrimp", "Omelette", "Gnocchi", "Pita", "Tortilla", "Schnitzel", "Fish and Chips", "Peking Duck", "Kimchi", "Banh Mi", "Clam Chowder", "Gyoza", "Tofu", "Miso Soup", "Tempura", "Crepe", "Pudding", "Goulash", "Pierogi", "Jambalaya", "Beef Stew", "Stuffed Peppers", "Pork Belly", "Beef Wellington", "Risotto", "Tiramisu", "Chili", "Meatloaf", "Ceviche", "Enchiladas", "Shepherd's Pie", "Eggs Benedict", "Frittata", "Biryani", "Shawarma", "Hummus", "Tabbouleh", "Cornbread", "Ravioli", "Sushi Roll", "Muffin", "Bruschetta", "Deviled Eggs", "Sloppy Joe", "Ziti", "Cannoli", "Turkey", "Ham", "Beef Jerky", "Crab Cakes", "Pork Chops", "Scallops", "Mussels", "Calamari", "Tartar", "Coleslaw", "Guacamole", "Chips", "Popcorn", "Cereal", "Toast", "Yogurt", "Granola", "Smoothie", "Milkshake", "Brownies", "Cupcake", "Cake", "Cookies", "Pretzel", "Trail Mix", "Fruit Salad", "Watermelon", "Pineapple", "Strawberries", "Blueberries", "Banana", "Apple", "Orange", "Grapes", "Peach", "Mango", "Papaya", "Avocado", "Lychee", "Dragonfruit", "Passionfruit", "Kiwifruit", "Tomato", "Cucumber", "Carrot", "Corn", "Zucchini", "Broccoli", "Cauliflower", "Spinach", "Kale", "Green Beans", "Peas", "Bell Pepper", "Mushrooms", "Eggplant", "Artichoke", "Brussels Sprouts", "Beetroot", "Radish", "Leeks", "Asparagus", "Pumpkin", "Sweet Potato", "Potato", "Rice", "Quinoa", "Couscous", "Barley", "Oats", "Lentils", "Chickpeas", "Black Beans", "Red Beans", "Naan", "Roti", "Chapati", "Paratha", "Tandoori Chicken", "Saag Paneer", "Paneer Tikka", "Vindaloo", "Korma", "Dal", "Rogan Josh", "Butter Chicken", "Chicken Tikka", "Malai Kofta", "Aloo Gobi", "Chana Masala", "Pakora", "Idli", "Dosa", "Uttapam", "Vada", "Sambar", "Momo", "Yakitori", "Okonomiyaki", "Tonkatsu", "Takoyaki", "Udon", "Soba", "Chow Mein", "Lo Mein", "Egg Rolls", "Orange Chicken", "Sesame Chicken", "General Tso's Chicken", "Kung Pao Chicken", "Beef and Broccoli", "Sweet and Sour Pork", "Fried Rice", "Sticky Rice", "Mongolian Beef", "Mapo Tofu", "Bulgogi", "Bibimbap", "Japchae", "Galbi", "Kimchi Stew", "Tteokbokki", "Sundae", "Hoddeok", "Kimbap", "Sopapilla", "Tamales", "Chilaquiles", "Elote", "Pozole", "Menudo", "Tostada", "Arroz con Pollo", "Carne Asada", "Mole", "Empanada", "Arepa", "Feijoada", "Moqueca", "Pastel", "Coxinha", "Acarajé", "Chimichurri", "Matambre", "Milanesa", "Asado", "Poutine", "Beavertail", "Tourtière", "Butter Tart", "Nanaimo Bar", "Pho Bo", "Bun Cha", "Bun Bo Hue", "Com Tam", "Hu Tieu", "Xoi", "Cha Gio", "Banh Xeo", "Banh Cuon", "Banh Bao", "Banh Flan", "Banh Ran", "Kebabs", "Dolma", "Manti", "Baklava", "Halva", "Kofta", "Shakshuka", "Tagine", "Harira", "Couscous Salad", "Bastilla", "Fufu", "Jollof Rice", "Egusi Soup", "Suya", "Chapati", "Injera", "Doro Wat", "Kitfo", "Nyama Choma", "Matoke", "Boerewors", "Bobotie", "Bunny Chow", "Vetkoek", "Peri Peri Chicken", "Pavlova", "Meat Pie", "Sausage Roll", "Lamington", "Tim Tam", "Vegemite", "Damper", "Fairy Bread", "Chicken Parmigiana", "Beef Pie", "Fish Pie", "Cornish Pasty", "Eton Mess", "Sticky Toffee Pudding", "Toad in the Hole", "Yorkshire Pudding", "Black Pudding", "Bubble and Squeak", "Welsh Rarebit", "Cullen Skink", "Irish Stew", "Boxty", "Colcannon", "Soda Bread", "Bangers and Mash", "Scones", "Trifle", "Clotted Cream", "Crumpet"],
        "custom": ["dog", "jack"],
    },
    # List of question pairs for gamemode 2.
    # Each tuple is structured as (question for non-imposters, corresponding question for the imposter).
    "question_pairs": [
        ("What is your favourite movie?", "What is the scariest movie you've watched?"),
        # <-- Enter your own pairs here.
    ]
}

# ---------------------------
# Command: Join the game
# ---------------------------
@bot.command(name="join")
async def join_game(ctx):
    if ctx.author in game_state["players"]:
        await ctx.send(f"{ctx.author.mention}, you have already joined the game.")
    else:
        game_state["players"].append(ctx.author)
        await ctx.send(f"{ctx.author.mention} joined the game!")

# ---------------------------
# Command: Leave the game
# ---------------------------
@bot.command(name="leave")
async def leave_game(ctx):
    if ctx.author in game_state["players"]:
        game_state["players"].remove(ctx.author)
        await ctx.send(f"{ctx.author.mention} left the game.")
    else:
        await ctx.send(f"{ctx.author.mention}, you are not currently in the game.")

# ---------------------------
# Command: Set the theme
# ---------------------------
@bot.command(name="set_theme")
async def set_theme(ctx, theme: str):
    if theme.lower() in game_state["theme_words"]:
        game_state["theme"] = theme.lower()
        await ctx.send(f"Theme set to **{theme}**.")
    else:
        available = ", ".join(game_state["theme_words"].keys())
        await ctx.send(f"Theme not found. Available themes: {available}")

# ---------------------------
# Command: Set the game mode
# ---------------------------
@bot.command(name="set_mode")
async def set_mode(ctx, mode: int):
    if mode in [1, 2]:
        game_state["mode"] = mode
        await ctx.send(f"Game mode set to **{mode}**.")
    else:
        await ctx.send("Invalid mode. Please choose **1** (word mode) or **2** (question mode).")

# ---------------------------
# Command: Start the game round
# ---------------------------
@bot.command(name="start")
async def start_game(ctx):
    # Check if enough players are present.
    if len(game_state["players"]) < 3:
        await ctx.send("Need at least **3 players** to start the game.")
        return
    # Ensure a theme and mode have been selected.
    if game_state["theme"] is None:
        await ctx.send("Theme not set. Use `!set_theme <theme>` to set one.")
        return
    if game_state["mode"] is None:
        await ctx.send("Game mode not set. Use `!set_mode <1 or 2>` to set a mode.")
        return

    # Randomly select one player to be the imposter.
    imposter = random.choice(game_state["players"])
    game_state["imposter"] = imposter
    await ctx.send("The game is starting! Everyone check your DMs for your role.")

    # -------------------------------------
    # Gamemode 1: Each non-imposter gets a word.
    # -------------------------------------
    if game_state["mode"] == 1:
        words_list = game_state["theme_words"].get(game_state["theme"], [])
        if not words_list:
            await ctx.send("No words available for this theme. Please add words in the code.")
            return
        # Choose a random word for the round.
        word = random.choice(words_list)
        for player in game_state["players"]:
            try:
                if player == imposter:
                    await player.send("You are the **imposter**! Try to blend in.")
                else:
                    await player.send(f"Your word is: **{word}**")
            except Exception as e:
                await ctx.send(f"Could not send DM to {player.mention}.")

    # -------------------------------------
    # Gamemode 2: Each non-imposter gets one question,
    # and the imposter gets a corresponding (different) question.
    # -------------------------------------
    elif game_state["mode"] == 2:
        if not game_state["question_pairs"]:
            await ctx.send("No question pairs available. Please add them in the code.")
            return
        # Choose a random pair from the list.
        question_pair = random.choice(game_state["question_pairs"])
        for player in game_state["players"]:
            try:
                if player == imposter:
                    await player.send(f"You are the **imposter**! Your question is: **{question_pair[1]}**")
                else:
                    await player.send(f"Your question is: **{question_pair[0]}**")
            except Exception as e:
                await ctx.send(f"Could not send DM to {player.mention}.")

# ---------------------------
# Command: Start a new round
# ---------------------------
@bot.command(name="new_round")
async def new_round(ctx):
    # Instead of clearing players, only reset the imposter.
    game_state["imposter"] = None
    await ctx.send("New round started! Current players are still in the game. Use `!start` to begin the round.")

# ---------------------------
# Run the bot (replace YOUR_TOKEN_HERE with your bot's token)
# ---------------------------
import os
bot.run(os.environ["TOKEN"])
