import string

import nanoid


def generate_imei():
    return nanoid.generate(string.digits, 15)


def generate_serial_number():
    return nanoid.generate(string.digits + string.ascii_uppercase, 7)
