# [Ploupy Python SDK](https://github.com/Plouc314/ploupy-python-sdk)

## Installation

```
pip install ploupy-sdk
```

> **Note**  
> This library requires python 3.10 or higher

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
