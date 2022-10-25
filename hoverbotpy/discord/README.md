# Rasp Pi Discord Bot

This bot is used to find the ip address of the pi.

It may further be extended into an easy to use console.

# Backlog (would be nice but not needed)

- Smarter way of handling API keys such as environment variables or CLI flags
- Make it a full fledged CLI interface to the hovercraft (we need a hovercraft
  first).
- Package this like a proper Python package (could run with `python -m
  hoverbot`).

# Setup

## Dependencies

Requires Python 3.8 or later.

Install all dependencies in `requirements.txt`. It is recommended you create a
virtualenv. In fact, there is a handy script called `setup-env.sh` that will
create a virtual env for you and install dependencies.

```
./setup-env.sh
```

## Bot Token

You need to create a Discord API bot token. Do that from the [developer
portal](https://discord.com/developers/applications/).

- Create an app
- Add bot to the app
- Generate bot token

Copy the file `botkey_template.py` to `botkey.py`. `botkey.py` is in the
projects gitignore file. HOWEVER, STILL PLEASE BE CAREFUL DO NOT COMMIT YOUR
KEY. Modify `botkey.py` to put your token in.

# Run

## Manually

Invite the bot to your server. This can be done through the development portal
in `my_app->OAuth2->URL_Generator`. It needs permission to read and send
messages.

Run the bot with `python bot.py`. It is recommended you put this in a tmux or
screen session.

## Automatically via SystemD

I'm pretty sure this is NOT how you're supposed to go about writing SystemD
units, but this is a Raspberry Pi project so it's fine enough.

There is a template file called `./hoverbot@.service`. Copy that to
`/etc/systemd/system/`. Modify the template as instructed by the comments.
