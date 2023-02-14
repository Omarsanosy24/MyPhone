import nanoid

# Does not produce obscene words
# See here: https://github.com/CyberAP/nanoid-dictionary#nolookalikessafe
SAFE_ALPHABET = "6789BCDFGHJKLMNPQRTW"


def generate_order_reference():
    # ~1 year with 1000 IDs by hours to have 1% probability of collision
    # See here: https://zelark.github.io/nano-id-cc/
    return nanoid.generate(alphabet=SAFE_ALPHABET, size=12)
