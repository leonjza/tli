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
import tweepy


class Twitter(object):
    """
        This Class is the State object used within the Click
        application
    """

    def __init__(self, verbose=False, language_filter=None, consumer_key=None, consumer_secret=None, access_token=None,
                 access_token_secret=None):
        self.auth = None
        self.api = None
        self.stream = None

        self.verbose = verbose
        self.language_filter = language_filter
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        self.setup()

    def setup(self):
        click.secho('[v] Twitter Auth Setup', fg='yellow', dim=True) if self.verbose else None
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

        click.secho('[v] Twitter API Setup', fg='yellow', dim=True) if self.verbose else None
        self.api = tweepy.API(
            self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        click.secho('[v] Twitter Stream Setup', fg='yellow', dim=True) if self.verbose else None
        self.stream = tweepy.Stream(
            auth=self.api.auth, listener=StreamListener(
                api=self.api, language_filter=self.language_filter, verbose=self.verbose))

        click.secho('[v] Done Stream Setup', fg='yellow', dim=True) if self.verbose else None


class StreamListener(tweepy.StreamListener):
    """
        This Class is responsible for handling updates
        that come in from Twitter and printing them
        to the screen
    """

    def __init__(self, api=None, language_filter=None, verbose=False):
        self.api = api or tweepy.API()
        self.language_filter = language_filter
        self.verbose = verbose

    def on_status(self, status):

        """
            When a Status Update comes in, handle it based on
            retweet status and print it.

            :param status:
            :return:
        """
        if self.language_filter and status.lang not in self.language_filter:
            click.secho(
                '[*] Skipping tweet as its in {lang} and not in a filtered language.'.format(lang=status.lang),
                fg='yellow') if self.verbose else None
            return

        click.echo('\n')

        if hasattr(status, 'retweeted_status'):
            self._print_status(status, is_retweet=True)
        else:
            self._print_status(status)

    def on_error(self, status_code):

        """
            Print an error if it occurs

            :param status_code:
            :return:
        """
        click.secho('[*] Error {code}'.format(code=status_code), fg='red', bold=True)

        if status_code == 402:
            click.secho('[*] Rate limited, exiting.', fg='red', bold=True)
            return False

        if status_code == 401:
            click.secho('[*] Auth failure. Are twitter keys correct/valid? Is config decryption password valid?',
                        fg='red', bold=True)
            return False

    def _print_status(self, status, is_retweet=False):

        """
            Prints a Tweet to the screen

            :param status:
            :param is_retweet:
            :return:
        """

        if is_retweet:
            click.secho('Retweet! RTs: {rt}, FAVs: {fav}'.format(
                rt=status.retweeted_status.retweet_count,
                fav=status.retweeted_status.favorite_count
            ), fg='red')

        click.secho(
            '{created} [{lang}] @{user} ({name}) via \'{source}\' | https://twitter.com/statuses/{twitter_id}'.format(
                created=status.created_at,
                lang=status.lang,
                user=status.user.screen_name.encode('utf-8'),
                name=status.user.name.encode('utf-8'),
                fav=status.favorite_count,
                rt=status.retweet_count,
                source=status.source.encode('utf-8'),
                twitter_id=status.id))

        if not is_retweet:
            click.secho(' "{text}"'.format(
                text=status.text.encode('utf-8')),
                bold=True, fg='green' if not is_retweet else 'yellow')

            if status.entities['urls']:
                self._print_urls(status.entities['urls'])

            if 'media' in status.entities:
                self._print_media(status.entities['media'])

        if is_retweet:
            self._print_status(status.retweeted_status)

    def _print_urls(self, urls):

        """
            Prints the URLs of a Tweet to the screen

            :param urls:
            :return:
        """

        urls = '\n'.join(['Url: ' + x['expanded_url'].encode('utf-8') for x in urls])
        click.secho('{urls}'.format(urls=urls), dim=True)

    def _print_media(self, media):

        """
            Prints the URLs to Media in a Tweet to the screen

            :param media:
            :return:
        """

        urls = '\n'.join(['Media: ' + x['expanded_url'].encode('utf-8') for x in media])
        click.secho('{media}'.format(media=urls), dim=True)
