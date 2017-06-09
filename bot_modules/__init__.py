# Main modules
import bot_modules.music

# Reply modules
import bot_modules.replies
import bot_modules.tableflip
import bot_modules.chatbot

# Game modules
import bot_modules.rocketleague

reactors = {
    'on_message': [
        # Main modules
        bot_modules.music,

        # Reply modules
        bot_modules.replies,
        bot_modules.tableflip,
        bot_modules.chatbot,

        # Game modules
        bot_modules.rocketleague
    ],
    'on_reaction_add': [
        # Main modules
        bot_modules.music

        # Reply modules

        # Game modules
    ]
}
