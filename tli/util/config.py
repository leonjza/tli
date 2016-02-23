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

from ConfigParser import SafeConfigParser

import click
import os
from crypto import encrypt, decrypt

userhome = os.path.expanduser('~')
confighome = os.path.join(userhome, '.tli.conf')

config = SafeConfigParser()


def readconfig():
    """
        Read the client configuration from a File
    """
    if not os.path.exists(confighome):
        click.secho('[*] Config file {path} does not exist!'.format(path=confighome), fg='red', bold=True)
        click.secho('[*] Entering first time setup.', fg='green', bold=True)

        return setupconfig()

    config.read(confighome)
    consumer_key = config.get('twitter', 'consumer_key')
    consumer_secret = config.get('twitter', 'consumer_secret')
    access_token = config.get('twitter', 'access_token')
    access_token_secret = config.get('twitter', 'access_token_secret')
    username = config.get('twitter', 'username')

    if config.getboolean('main', 'encrypted'):
        click.secho('[*] Configuration is encrypted.', fg='green')
        passphrase = click.prompt('[q] Config decryption passphrase', hide_input=True)
    else:
        passphrase = None

    if passphrase:
        consumer_key = decrypt(passphrase, consumer_key)
        consumer_secret = decrypt(passphrase, consumer_secret)
        access_token = decrypt(passphrase, access_token)
        access_token_secret = decrypt(passphrase, access_token_secret)
        username = decrypt(passphrase, username)

    return consumer_key, consumer_secret, access_token, access_token_secret, username


def setupconfig():
    """
        Ask the user questions to setup the configuration file
    """

    click.echo('[*] TLI supports encryption configuration objects.')
    click.echo('[*] If you *enable* encryption, you will have to type a password everytime you lauch TLI.\n')

    passphrase = None
    passphrase_one = 'None'
    passphrase_two = None
    if click.confirm('[*] Do you want to encrypt your config file?'):
        while passphrase_one != passphrase_two:
            passphrase_one = click.prompt('[q] Enter a passphrase', hide_input=True)
            passphrase_two = click.prompt('[q] Confirm the passphrase', hide_input=True)

            if passphrase_one != passphrase_two:
                click.secho('[*] Passphrases dont match, retry.', fg='yellow')

        passphrase = passphrase_one

    click.echo('[*] Ok, we need 5 things to get going.')
    click.echo('[*] Make sure you have setup an app at https://apps.twitter.com/ first!\n')

    consumer_key = click.prompt('[q] Consumer Key')
    consumer_secret = click.prompt('[q] Consumer Secret')
    access_token = click.prompt('[q] Access Token')
    access_token_secret = click.prompt('[q] Access Token Secret')
    username = click.prompt('[q] Twitter Screen Name')

    config.add_section('main')
    config.set('main', 'encrypted', 'True' if passphrase else 'False')

    config.add_section('twitter')
    config.set('twitter', 'consumer_key', consumer_key if not passphrase else encrypt(passphrase, consumer_key))
    config.set('twitter', 'consumer_secret',
               consumer_secret if not passphrase else encrypt(passphrase, consumer_secret))
    config.set('twitter', 'access_token', access_token if not passphrase else encrypt(passphrase, access_token))
    config.set('twitter', 'access_token_secret',
               access_token_secret if not passphrase else encrypt(passphrase, access_token_secret))
    config.set('twitter', 'username', username if not passphrase else encrypt(passphrase, username))

    click.echo('[*] Writing configuration to: {path}'.format(path=confighome))

    os.umask(0077)
    with open(confighome, 'w') as f:
        config.write(f)

    click.secho('[*] First time setup complete.', fg='green', bold=True)

    return readconfig()
