# DiscordBot-GeminiAI
## Use Gemini on Discord, with highly customizable features. Using Thread to Create Personal Conversations with AI.
Currently, the bot only supports the Gemini Pro model, with plans to gradually add other Google models in the future!.

![demo](https://i.imgur.com/OO52TfC.gif)

## Update
> ### 2023/2/16：Add Gemini 1.0 Pro model.
   
## Features
- **Gemini Pro Model:** The bot currently supports the Gemini Pro model for powerful AI interactions.
- **Customizable:** Highly customizable features to tailor the bot to your Discord server's needs.

<details>
   <summary>
   
   ### Slash command

   </summary>
   
* `/api_key setting [choice] [api_key]`
  * Can upload own google api key or delete it. (api key get from https://makersuite.google.com/app/apikey)
    * [choice]：`delete` or `set` your api key

  ![setting](https://i.imgur.com/QWcaGG6.png)
  
* `/create conversation [model] [type] [use_prompt] [use_character]`
  * Create a thread exclusively for the user to chat with the bot.
    * [model]：Choose AI model.
    * [type]：Choose thread type, private or public.
    * [temperature]：Controls the level of randomness in the output, ranging from highly varied (closer to 1.0) to less surprising (closer to 0.0).
    * [harrassment]、[hate_speech]、[sexually_explicit]、[dangerous_content]：It's [Safety Settings](https://ai.google.dev/docs/safety_setting_gemini#safety-settings), the default is Block some.


* `/reset conversation`
  * It will only clear the chat history, personalization settings will remain unchanged.
</details>

## Usage

### Install

```
pip install -r requirements.txt
```

### Discord bot permission

![permission](https://i.imgur.com/ZHYlRJH.png)

### .env setting

```markdown
# Input your Discord bot token.
DISCORD_BOT_TOKEN=

# Can get from https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=

# Allow each commands only in specific channel, if you don't set it, just default to all channels.
# specific channel for /api_key setting
SETTING_CHANNEL_ID=

# specific channel for /create conversation
CHAT_CHANNEL_ID=

# specific channel for /reset conversation
RESET_CHAT_CHANNEL_ID=

# specific channel for /help
HELP_CMD_CHANNEL_ID=
```

## Credits
* google-generativeai - [https://github.com/google/generative-ai-python](https://github.com/google/generative-ai-python)# Z2ZGemini
