### Twitter on the commandline, the way **I** wanted it to be.

![tli](http://i.imgur.com/R9qcMZD.png)  

## installation
`pip install tli`

You will also need to create yourself some Twitter API keys that will be used by TLI. Head over to [https://apps.twitter.com/app/new](https://apps.twitter.com/app/new) and create an application. Click the button to create access tokens and have them ready for the TLI setup.

## running 
Once the installation is complete, run TLI with `tli`. On first run, a configuratin file will be created to store the twitter authentication. I suggest you encrypt the config if at all possible.

```bash
$ tli timeline
 _______  ___      ___
|       ||   |    |   |
|_     _||   |    |   |
  |   |  |   |    |   |
  |   |  |   |___ |   |
  |   |  |       ||   |
  |___|  |_______||___|
 Twitter Line Interface

[*] Config file /home/bob/.tli.conf does not exist!
[*] Entering first time setup.
[*] TLI supports encryption configuration objects.
[*] If you *enable* encryption, you will have to type a password everytime you lauch TIL.

[*] Do you want to encrypt your config file? [y/N]: y
[q] Enter a passphrase:
[q] Confirm the passphrase:
[*] Ok, we need 5 things to get going.
[*] Make sure you have setup an app at https://apps.twitter.com/ first!
```

## contact
[https://twitter.com/leonjza](https://twitter.com/leonjza)
