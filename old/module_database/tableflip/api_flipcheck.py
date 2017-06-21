def flipcheck(content):
    """Checks a string for anger and soothes said anger

    Args:
        content (str): The message to be flipchecked

    Returns:
        putitback (str): The righted table or text
    """

    # Prevent tampering with flip
    punct = """!"#$%&'*+,-./:;<=>?@[\]^_`{|}~ ━─"""
    tamperdict = str.maketrans('', '', punct)
    tamperproof = content.translate(tamperdict)

    # Unflip
    if "(╯°□°）╯︵" in tamperproof:
        # For tables
        if "┻┻" in tamperproof:
            # Calculate table length
            length = 0
            for letter in content:
                if letter == "━":
                    length += 1.36
                elif letter == "─":
                    length += 1
                elif letter == "-":
                    length += 0.50

            # Construct table
            putitback = "┬"

            for i in range(int(length)):
                putitback += "─"

            putitback += "┬﻿ ノ( ゜-゜ノ)"

            return putitback

        # For text
        else:
            # Create dictionary for flipping text
            flipdict = str.maketrans(
                'abcdefghijklmnopqrstuvwxyzɐqɔpǝɟbɥıظʞןɯuodbɹsʇnʌʍxʎz😅🙃😞😟😠😡☹🙁😱😨😰😦😧😢😓😥😭',
                'ɐqɔpǝɟbɥıظʞןɯuodbɹsʇnʌʍxʎzabcdefghijklmnopqrstuvwxyz😄🙂🙂🙂🙂🙂🙂😀😀🙂😄🙂🙂😄😄😄😁'
            )

            # Construct flipped text
            flipstart = content.index('︵')
            flipped = content[flipstart+1:]
            flipped = str.lower(flipped).translate(flipdict)

            putitback = ''.join(list(reversed(list(flipped))))

            putitback += "ノ( ゜-゜ノ)"

            return putitback
    else:
        return False
