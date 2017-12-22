import logging

logger = logging.getLogger(__name__)


PUNCT = """!"#$%&'*+,-./:;<=>?@[\]^_`{|}~ ━─"""
TAMPERDICT = str.maketrans('', '', PUNCT)
FLIPDICT = str.maketrans(
    'abcdefghijklmnopqrstuvwxyzɐqɔpǝɟbɥıظʞןɯuodbɹsʇnʌʍxʎz😅🙃😞😟😠😡☹🙁😱😨😰😦😧😢😓😥😭',
    'ɐqɔpǝɟbɥıظʞןɯuodbɹsʇnʌʍxʎzabcdefghijklmnopqrstuvwxyz😄🙂🙂🙂🙂🙂🙂😀😀🙂😄🙂🙂😄😄😄😁'
)


def check(text):
    """Checks a string for anger and soothes said anger

    Args:
        text (str): The message to be flipchecked

    Returns:
        putitback (str): The righted table or text
    """

    tamperproof = text.translate(TAMPERDICT)
    if "(╯°□°）╯︵" not in tamperproof:
        # Text does not contain anger
        return False

    if "┻┻" in tamperproof:
        # For tables
        length = 0
        for letter in text:
            if letter == "━":
                length += 1.36
            elif letter == "─":
                length += 1
            elif letter == "-":
                length += 0.50

        putitback = "┬"
        for i in range(int(length)):
            putitback += "─"
        putitback += "┬﻿ ノ( ゜-゜ノ)"
    else:
        # For text
        flipstart = text.index('︵')
        flipped = text[flipstart + 1:]
        flipped = str.lower(flipped).translate(FLIPDICT)

        putitback = ''.join(list(reversed(list(flipped)))) + "ノ( ゜-゜ノ)"

    return putitback
