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

import click
from util.config import readconfig
from util.twitter import Twitter


def banner():
    click.echo(" _______  ___      ___  \n" +
               "|       ||   |    |   | \n" +
               "|_     _||   |    |   | \n" +
               "  |   |  |   |    |   | \n" +
               "  |   |  |   |___ |   | \n" +
               "  |   |  |       ||   | \n" +
               "  |___|  |_______||___| \n" +
               " Twitter Line Interface\n")


@click.group()
@click.version_option('2.2')
@click.option('--language-filter', '-l', default=None, metavar="COMMA SEPERATED",
              help='Filter tweets to specific languages. Accepts a comma seperated list.')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Enable verbosity.')
@click.pass_context
def cli(ctx, language_filter, verbose):
    """
        \b
         _______  ___      ___
        |       ||   |    |   |
        |_     _||   |    |   |
          |   |  |   |    |   |
          |   |  |   |___ |   |
          |   |  |       ||   |
          |___|  |_______||___|
         Twitter Line Interface

    """

    banner()

    consumer_key, consumer_secret, access_token, access_token_secret, username = readconfig()

    if language_filter:
        click.secho('[v] Configurating Language Filter', fg='yellow', dim=True) if verbose else None
        language_filter = language_filter.split(',')

    ctx.obj = Twitter(verbose=verbose,
                      language_filter=language_filter,
                      consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token=access_token,
                      access_token_secret=access_token_secret)
    ctx.verbose = verbose


@cli.command()
@click.pass_obj
def timeline(twitter):
    """
        \b
        Stream the Users Timeline

    """

    click.secho('[v] Streaming User Stream', fg='yellow', dim=True) if twitter.verbose else None
    twitter.stream.userstream()


@cli.command()
@click.option('--topics', '-t', required=True, metavar="COMMA SEPERATED",
              help='Set the topics to watch. Accepts a comma seperated list.')
@click.pass_obj
def watch(twitter, topics):
    """
        \b
        Watch Specific Topics

    """
    topics = topics.split(',')

    click.secho('[v] Streaming Topics: {topics}'.format(topics=', '.join(topics)), fg='yellow',
                dim=True) if twitter.verbose else None

    twitter.stream.filter(track=topics)


if __name__ == '__main__':
    cli()
