def convert_hex_value(message, needs_prefix=True):
    prefixes = ["0x", "#"]
    hex_chars = "0123456789ABCDEF"

    for s in message.split(' '):
        is_hex_prefix = False
        for prefix in prefixes:
            if s.startswith(prefix):
                is_hex_prefix = True
                s = s[len(prefix):]
                break

        if is_hex_prefix or not needs_prefix:
            # Convert 3-hex to 6-hex
            if len(s) == 3:
                s = s[0]*2 + s[1] * 2 + s[2] * 2

            if len(s) == 6:
                s = s.upper()
                is_all_hex = True
                for c in s:
                    if c not in hex_chars:
                        is_all_hex = False
                        break

                if is_all_hex:
                    return True, s

    return False, ""
