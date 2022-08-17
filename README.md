# Ploupy SDK

## Installation

```
pip install ploupy-sdk
```

## Getting started

Here is a minimal example:

```python
import ploupy

class MyBehaviour(ploupy.Behaviour):
    pass

BOT_KEY = "..."

bot = ploupy.Bot(bot_key=BOT_KEY, behaviour_class=MyBehaviour)

if __name__ == "__main__":
    bot.run()
```
