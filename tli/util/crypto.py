# The MIT License (MIT)
#
# Copyright (c) 2016 Leon Jacobs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import base64

from Crypto.Cipher import AES

BLOCK_SIZE = 32
PADDING = '&'


def _pad(data, pad_with=PADDING):
    """
        Data to be encrypted should be on 16, 24 or 32 byte boundaries.
        So if you have 'hi', it needs to be padded with 30 more characters
        to make it 32 bytes long. Similary if something is 33 bytes long,
        31 more bytes are to be added to make it 64 bytes long which falls
        on 32 boundaries.

        - BLOCK_SIZE is the boundary to which we round our data to.
        - PADDING is the character that we use to padd the data.
    """
    return data + (BLOCK_SIZE - len(data) % BLOCK_SIZE) * PADDING


def encrypt(secret_key, data):
    """
        Encrypts the given data with given secret key.
    """
    cipher = AES.new(_pad(secret_key, '@')[:32])
    return base64.b64encode(cipher.encrypt(_pad(data)))


def decrypt(secret_key, encrypted_data):
    """
        Decryptes the given data with given key.
    """
    cipher = AES.new(_pad(secret_key, '@')[:32])
    return cipher.decrypt(base64.b64decode(encrypted_data)).rstrip(PADDING)
