import discord
import os
from discord.ext import commands
from keep_alive import keep_alive
import random

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
    "imposter": None,    # Primary imposter for backward compatibility
    "imposters": [],     # List of chosen imposters for the round
    "last_question_pair": None,  # The last selected question pair for game mode 2
    # Dictionary for theme words.
    "theme_words": {
        "animals": ["lion", "tiger", "penguin", "seal", "elephant", "giraffe", "zebra", "kangaroo", "koala", "bear", "cheetah", "leopard", "wolf", "fox", "crocodile", "hippopotamus", "rhinoceros", "camel", "donkey", "horse", "cow", "sheep", "goat", "pig", "chicken", "duck", "goose", "turkey", "ostrich", "emu", "flamingo", "peacock", "parrot", "eagle", "hawk", "falcon", "owl", "bat", "squirrel", "rabbit", "mouse", "rat", "hamster", "guinea pig", "otter", "beaver", "raccoon", "skunk", "deer", "moose", "elk", "bison", "buffalo", "antelope", "lemur", "chimpanzee", "orangutan", "baboon", "macaw", "toucan", "seagull", "walrus", "narwhal", "dolphin", "whale", "shark", "octopus", "jellyfish", "starfish", "crab", "lobster", "shrimp", "snail", "turtle", "tortoise", "lizard", "snake", "frog", "toad", "newt", "salamander", "crow", "raven", "sparrow", "robin", "woodpecker", "hummingbird", "swan", "pigeon", "dove", "badger", "hedgehog", "porcupine", "armadillo", "sloth", "llama", "alpaca", "yak", "ferret", "mole"],
        "movies": ["Inception", "The Shawshank Redemption", "The Godfather", "The Dark Knight", "Pulp Fiction", "Fight Club", "Forrest Gump", "The Matrix", "Interstellar", "The Lord of the Rings: The Return of the King", "The Empire Strikes Back", "Star Wars: A New Hope", "The Lord of the Rings: The Fellowship of the Ring", "The Lord of the Rings: The Two Towers", "The Prestige", "Gladiator", "Memento", "The Departed", "The Social Network", "The Avengers", "Jurassic Park", "Titanic", "Avatar", "Back to the Future", "The Lion King", "Braveheart", "Schindler's List", "Goodfellas", "Se7en", "Saving Private Ryan", "The Green Mile", "The Silence of the Lambs", "Casablanca", "One Flew Over the Cuckoo's Nest", "City of God", "American Beauty", "The Wolf of Wall Street", "Whiplash", "Parasite", "Joker", "Avengers: Endgame", "Avengers: Infinity War", "Django Unchained", "Mad Max: Fury Road", "Inglourious Basterds", "The Truman Show", "Toy Story", "Toy Story 3", "Finding Nemo", "Up", "WALL-E", "Coco", "Inside Out", "Ratatouille", "Spirited Away", "Your Name", "Oldboy", "The Sixth Sense", "A Beautiful Mind", "The Shining", "Blade Runner 2049", "Logan", "Deadpool", "Guardians of the Galaxy", "The Incredibles", "Monsters, Inc.", "Shutter Island", "Arrival", "Her", "La La Land", "Moonlight", "The Revenant", "12 Years a Slave", "Room", "Brooklyn", "The Big Short", "Birdman", "No Country for Old Men", "There Will Be Blood", "Requiem for a Dream", "The Grand Budapest Hotel", "The Hateful Eight", "Once Upon a Time in Hollywood", "Spotlight", "The Imitation Game", "Argo", "The King's Speech", "Slumdog Millionaire", "The Curious Case of Benjamin Button", "Life of Pi", "The Fighter", "Hugo", "The Aviator", "Black Swan", "The Martian", "Doctor Strange", "Captain America: The Winter Soldier", "Iron Man", "Shazam!", "Wonder Woman"],
        "actors": ["Sydney Sweeney", "Johnny Depp", "Leonardo DiCaprio", "Tom Cruise", "Brad Pitt", "Angelina Jolie", "Denzel Washington", "Scarlett Johansson", "Jennifer Lawrence", "Robert Downey Jr.", "Chris Hemsworth", "Natalie Portman", "George Clooney", "Kate Winslet", "Hugh Jackman", "Keanu Reeves", "Emma Stone", "Ryan Reynolds", "Morgan Freeman", "Viola Davis", "Sandra Bullock", "Matt Damon", "Anne Hathaway", "Joaquin Phoenix", "Ben Affleck", "Tom Hanks", "Gal Gadot", "Samuel L. Jackson", "Nicole Kidman", "Christian Bale", "Emma Watson", "Bradley Cooper", "Zoe Saldana", "Channing Tatum", "Zac Efron", "Alicia Vikander", "Margot Robbie", "Idris Elba", "Saoirse Ronan", "Michael Fassbender", "Emily Blunt", "Jake Gyllenhaal", "Michelle Williams", "Ryan Gosling", "Julianne Moore", "Daniel Craig", "Eddie Redmayne", "Kristen Stewart", "Lupita Nyong'o", "Chiwetel Ejiofor", "Amy Adams", "Tessa Thompson", "Daniel Kaluuya", "Rami Malek", "Zendaya", "John Boyega", "Regina King", "Octavia Spencer", "Liam Neeson", "Chris Pratt", "Mila Kunis", "Chloe Grace Moretz", "Shailene Woodley", "Dakota Johnson", "Timothée Chalamet", "Anya Taylor-Joy", "Florence Pugh", "John Krasinski", "Constance Wu", "Awkwafina", "Elizabeth Olsen", "Olivia Colman", "Andrew Garfield", "Cillian Murphy", "Michael B. Jordan", "Seth Rogen", "Paul Rudd", "Karen Gillan", "Elizabeth Debicki", "Taron Egerton", "Javier Bardem", "Penélope Cruz", "Eva Green", "Gemma Chan", "Oscar Isaac", "Daniel Radcliffe", "Emma Thompson", "Benedict Cumberbatch", "Joe Alwyn", "Benicio Del Toro", "Robert Pattinson", "Elizabeth Banks", "Zoë Kravitz", "Cara Delevingne", "Hailee Steinfeld", "Lily James", "Henry Cavill", "Chris Evans"],
        "food": ["Pizza", "Burger", "Sushi", "Pasta", "Tacos", "Sandwich", "Fried Chicken", "Ice Cream", "Steak", "French Fries", "Chocolate", "Cheeseburger", "Ramen", "Hot Dog", "Donut", "Nachos", "Salad", "Burrito", "Curry", "Lasagna", "Chicken Wings", "Dumplings", "Pancakes", "Waffles", "Quesadilla", "Mac and Cheese", "Spaghetti", "Spring Rolls", "Pho", "BBQ Ribs", "Bagel", "Croissant", "Apple Pie", "Grilled Cheese", "Chicken Nuggets"],
        "carey": ["Ryan W", "Louis LG", "Jack K", "Jacob Z", "Morris RL", "Justin W", "Bobby", "Ange W", "Jack A", "Penghui", "Oliver L", "Grayson", "Sam Simon", "Willem N", "Leon Y", "Dominic", "Leonard L", "Silas C", "Hamish M", "Nicolas M", "Josh M", "Cameron T", "Callum W", "Thisal S", "Leo T", "Scott H"],
        "splus": ["Leo S", "Louis LG", "Finn G", "Alec A", "Matt A", "Josh M", "Kath P", "Macca", "Oven", "Valan", "James G", "Tim L", "Leon Y", "Lachlan C"],
        "countries": ["United States", "China", "India", "United Kingdom", "Germany", "France", "Italy", "Spain", "Canada", "Australia", "Brazil", "Russia", "Japan", "Mexico", "South Korea", "Indonesia", "Saudi Arabia", "Turkey", "Netherlands", "Switzerland", "Sweden", "Belgium", "Norway", "Austria", "Poland", "South Africa", "Argentina", "Ireland", "Singapore", "New Zealand", "Denmark", "Malaysia", "Israel", "Finland", "Portugal", "Greece", "Czech Republic", "Hungary", "Thailand", "Egypt", "Philippines", "Colombia", "Vietnam", "Romania", "Ukraine", "Chile", "Peru", "Pakistan", "Iraq", "Kazakhstan", "Morocco", "Algeria", "Lebanon", "Qatar", "Kuwait", "Oman", "Bahrain", "Slovakia", "Slovenia", "Croatia", "Serbia", "Bulgaria", "Estonia", "Latvia", "Lithuania", "Iceland", "Luxembourg", "Cyprus", "Malta", "Jordan", "Sri Lanka", "Nepal", "Bangladesh", "Myanmar", "Uzbekistan", "Belarus", "Azerbaijan", "Georgia", "Armenia", "Afghanistan", "Sudan", "Ethiopia", "Kenya", "Tanzania", "Uganda", "Ghana", "Cameroon", "Angola", "Zimbabwe", "Bolivia", "Ecuador", "Paraguay", "Uruguay", "Venezuela", "Costa Rica", "Panama", "Dominican Republic", "Fiji"],
        "custom": ["dog", "jack"],
    },
    # List of question pairs for gamemode 2.
    "question_pairs": [
        ("What is your the most underrated movie?", "What is the worst movie you've watched?"),
        ("What animal would you want by your side during the apocolypse?", "What is the most random medium-large land animal?"),
        ("Craziest place you've wanked?", "Most romantic spot to go on a date?"),
        ("How many urinals away from another person do you go, counting the gaps?", "Pick a number from 0-8"),
        ("What height would you be if you could pick any? In cm", "If you had to choose your girlfriends height, what would she be? In cm"),
        ("What would you rate your attractiveness out of 10?", "Pick a number from 4-10"),
        ("If you could transform into any animal, what would it be?", "What is the stupidest animal?"),
        ("What TV show would you show your kids?", "Best TV show you've seen in the last few years"),
        ("How long do you stay in bed after you wake up when you have nowhere to be?", "Pick a time between 3 minutes and 3 hours"),
        ("What is the most amount of time you've wanked in a day?", "Pick a number between 4-10"),
        ("What celebrity would you want to be stuck on a deserted island with?", "Who is the baddest celebrity?"),
        ("Who is the baddest celebrity?", "Name a adult actor"),
        ("What is the most romantic thing you can say to someone?", "Favourite quote?"),
        ("Favourite quote?", "Most outrageous sentence you can think of"),
        ("If you could have any superpower, what would it be?", "Best superpower to commit crimes"),
        ("What's your go-to karaoke song?", "What's the most overrated song?"),
        ("What's your go-to emoji?", "Most overused emoji that actually sucks?"),
        ("What's your ideal hangout spot?", "What's the most awkward place you've been caught?"),
        ("What are you most excited for in university?", "What is the best sex position?"),
        ("What country would you most want to visit?", "What is the most dangerous country in the world?"),
        ("What is your ideal date?", "What is the best gooning spot?"),
        ("What's the best item to have in a zombie apocolypse?", "Whats the worst gift to receive?"),
        ("How much have you spent on Onlyfans or other websites", "Pick a number from 1-10"),
        ("Safest time of day to go out", "Best time to rob someone"),
        ("Best pickup line", "Best line to gross out a person of the opposite gender"),
        ("What's your favorite way to chill after a wild night?", "What's the most scandalous thing you've done in a public spot?"),
        ("Ideally, how much younger would you want your girlfriend to be?", "Pick a number from 2-5"),
        ("Where would you go if you could teleport anywhere?", "Best place to beat up someone without getting caught?"),
        ("Age when you first gooned", "Pick a number from 7-15"),
        ("What is your comfort food?", "What is an exotic, 'rich' type food?"),
        ("What's the most scandalous thing you've done in a public spot?", "What's your favorite way to chill after a wild night?"),
        ("How long should you wait for a friend if they’re running late?", "What is the latest you’ve been to a meetup with friends?"),
        ("What’s the most useless superpower?", "What superpower would you want?"),
        ("What’s the last movie that made you cry?", "What’s the worst movie you’ve ever seen?"),
        ("How many close friends does the average person have?", "Pick a range between 5-20"),
        ("Which celebrity would you want to go on a road trip with?", "Who would be the worst celebrity to have as a roommate?"),
        ("What celebrity living or dead would you want to have dinner with?", "Which celebrity are you afraid of?"),
        ("If you could never use the internet again what would you miss the most?", "what is the worst thing about the internet?"),
        ("What is your guilty pleasure song that you are embarrassed to admit that you love?", "what is a song that you hate?"),
        ("What is one word you would use to describe Melbourne?", "What is one word you would use to describe your school?"),
        ("What is one word you would use to describe yourself?", "what is one word you would use to describe Leo Scarborough"),
        ("what sport would you be most likely to go pro in?", "what is the hardest sport to go pro in?"),
        ("What sport requires the most skill?", "What sport do you think is overrated?"),
        ("What musician do you think is the most talented?", "what musician do you think is overrated?"),
        ("What videogame requires the most skill?", "What is a game you would play with your kids?"),
        ("Number of days you could last in prison?", "Pick a number of days between 30-500"),
        ("What age should you stop going to the club or partying?", "Pick a number between 25-50"),
        ("What’s a song to pump you up?", "What song did you listen to last by yourself?"),
        ("How much money would it take for you to dropout of school?", "Pick a number between $1 Million and $50 million"),
        ("How much money would it take for you to run through the streets naked?", "Pick a number between $5000- $100000"),
        ("What show or movie would be uncomfortable to watch with your parents?", "What’s a tv show you’ve watched that you would not recommend to a kid"),
        ("What influencer could you beat in a fight?", "Which influencer would you go fishing with?"),
        ("What age did you get your first allowance?", "What age did your parents buy you your first video game?"),
        ("How many people would show up to your birthday party?", "Pick a range between 5-50"),
        ("Which two artists should collaborate on a song?", "Which two artists should date?"),
        ("Worst emoji to reply to the FBI?", "which emoji annoys you the most?"),
        ("How many days can you go without eating?", "Pick a range between 7-21?"),
        ("Best age to retire?", "Pick a number between 30-70"),
        ("What age do you want to have kids?", "Pick a number between 24-36"),
        ("how many 10-year-olds could you take in a fight?", "Pick a number between 10-100"),
        ("What athlete could you beat at their sport?", "Pick a female athlete"),
        ("What's the most awkward place you've been caught?", "What's your ideal hangout spot?"),

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
# Command: Kick all players from the game
# ---------------------------
@bot.command(name="kickall")
async def kick_all(ctx):
    game_state["players"].clear()
    await ctx.send("All players have been kicked from the game.")

# ---------------------------
# Command: Kick a specific player (Owner only)
# ---------------------------
@bot.command(name="kick")
async def kick_player(ctx, member: discord.Member):
    if ctx.author.id != ctx.guild.owner_id:
        await ctx.send("Only the server owner can use this command.")
        return
    if member in game_state["players"]:
        game_state["players"].remove(member)
        await ctx.send(f"{member.mention} has been kicked from the game.")
    else:
        await ctx.send(f"{member.mention} is not in the game.")

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
    players = game_state["players"]
    # Check if enough players are present.
    if len(players) < 3:
        await ctx.send("Need at least **3 players** to start the game.")
        return
    # Ensure game mode is selected.
    if game_state["mode"] is None:
        await ctx.send("Game mode not set. Use `!set_mode <1 or 2>` to set a mode.")
        return
    # For gamemode 1, ensure a theme is selected.
    if game_state["mode"] == 1 and game_state["theme"] is None:
        await ctx.send("Theme not set. Use `!set_theme <theme>` to set one.")
        return

    # Determine number of imposters based on player count
    num_imposters = 1
    if len(players) >= 4:
        roll = random.random()
        if roll < 0.05:
            num_imposters = 3
        elif roll < 0.30:  # 0.05 + 0.25
            num_imposters = 2
    # Select imposters
    imposters = random.sample(players, num_imposters)
    game_state["imposters"] = imposters
    # For backwards compatibility, record the first as the main "imposter"
    game_state["imposter"] = imposters[0]
    # define local imposter variable for Mode 2 logic
    imposter = game_state["imposter"]

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
        for player in players:
            try:
                if player in imposters:
                    await player.send("You are the **imposter**! Try to blend in.")
                else:
                    await player.send(f"Your word is: **{word}**")
            except Exception as e:
                await ctx.send(f"Could not send DM to {player.mention}.")
    # -------------------------------------
    # Gamemode 2: Each non-imposter gets one question,
    # and the imposter gets a corresponding (different) question.
    # (Note: No theme is required for gamemode 2)
    # -------------------------------------
    elif game_state["mode"] == 2:
        if not game_state["question_pairs"]:
            await ctx.send("No question pairs available. Please add them in the code.")
            return
        # Choose a random pair from the list and store it for later reference.
        question_pair = random.choice(game_state["question_pairs"])
        game_state["last_question_pair"] = question_pair
        for player in players:
            try:
                if player == imposter:
                    await player.send(f"Your question is: **{question_pair[1]}**")
                else:
                    await player.send(f"Your question is: **{question_pair[0]}**")
            except Exception as e:
                await ctx.send(f"Could not send DM to {player.mention}.")

# ---------------------------
# Command: Reveal the non-imposter question (Game Mode 2 only)
# ---------------------------
@bot.command(name="reveal")
async def reveal_question(ctx):
    if game_state["mode"] != 2:
        await ctx.send("Reveal command is only applicable for Game Mode 2.")
        return
    if not game_state.get("last_question_pair"):
        await ctx.send("No question has been set for this round yet.")
        return
    question_for_non_imposters = game_state["last_question_pair"][0]
    await ctx.send(f"The question given to non-imposters was: **{question_for_non_imposters}**")

# ---------------------------
# Command: Start a new round
# ---------------------------
@bot.command(name="new_round")
async def new_round(ctx):
    # Reset imposter data but keep players and theme
    game_state["imposter"] = None
    game_state["imposters"] = []
    game_state["last_question_pair"] = None
    await ctx.send("New round started! Current players are still in the game. Use `!start` to begin the round.")

# ---------------------------
# Run the bot
# ---------------------------
keep_alive()
bot.run(os.getenv("bot_token"))
