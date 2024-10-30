# Setting up a Telegram Bot
Outline of steps to get up an running on Telegram for chamber notifications

## Create and Connect to a Telegram Bot
> [!NOTE]
> Setup must first be completed on a mobile device to enable setup on a Desktop
1. On your prefered mobile device, install Telegram, search `@BotFather` and start a new chat.
2. Send `/newbot` to the chat and follow prompts to create a name and user name for the bot.
3. Record the provided HTTP API token that is provided as it is what will be used to send messages to the chat.
4. Bot settings and options can be accessed by sending `/mybots`, selecting a bot, and using menu to find information or make changes.
6. Create a new channel, set to `public`, noting the link name
7. In settings, add a new administrator, searching the bot by its name
8. TODO: Set the BOT_TOKEN and CHAT_ID variable with the provided HTTP API token from Step 3 and the channel link from step 6

The new bot should now be able to send messages to the public channel!
