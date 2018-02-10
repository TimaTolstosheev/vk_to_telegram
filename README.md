# vk_to_telegram
#### About:
This simple code uses [VK API](https://vk.com/dev/methods) to get records from walls
and send them to Telegram using its [bots API](https://core.telegram.org/bots/api)

#### Configuration:
There is [configuration file (config.py)](https://github.com/dkder3k/vk_to_telegram/blob/master/config.py) where:
* `telegram_token` - Telegram access token; can be got from [BotFather](https://telegram.me/botfather), when creating bot
* `chat_id` - chat where messages will be sent (in format "@channelorusername")
* `vk_token` - VK access token; described [here](https://vk.com/dev/access_token?f=3.%20Service%20Token),
service token is enough in most cases
* `vk_groups_ids` - VK pages to scan; must be set as tuple even if there is only one page to listen

  (e.g.: `(group_id1, group_id2, group_id3)` or `(group_id)`)
  
  Note that VK groups ids starts with `-`, e.g.: `-0000001`.
