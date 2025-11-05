# CodeFetcherBot

A Telegram bot that fetches Netflix verification codes from your email and sends them to you via Telegram. This bot supports multiple chat IDs and uses IMAP to fetch emails.

## Features

- Automatically fetches Netflix verification codes from your email
- Supports multiple authorized Telegram chats
- Secure authentication using chat ID verification
- Markdown V2 formatted messages for better readability
- Backward compatible with old commands

## Prerequisites

- Python 3.12 or higher
- A Gmail account (with App Password if 2FA is enabled)
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/dionlahh/CodeFetcherBot.git
   cd CodeFetcherBot
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot**

   - Copy `config.properties.template` to `config.properties`

   ```bash
   cp config.properties.template config.properties
   ```

   - Edit `config.properties` with your settings:

     ```properties
     # Telegram Settings
     telegram.bot_token=YOUR_BOT_TOKEN
     telegram.authorized_chat_ids=CHAT_ID1,CHAT_ID2

     # Email Settings
     email.host=imap.gmail.com
     email.username=YOUR_EMAIL@gmail.com
     email.password=YOUR_APP_PASSWORD
     ```

5. **Get your Telegram Chat ID**

   - Start a chat with [@RawDataBot](https://t.me/RawDataBot)
   - It will show you your chat ID
   - For group chats, add the bot to the group and check the group ID

6. **Set up Gmail App Password** (if using 2FA)
   - Go to your Google Account settings
   - Navigate to Security > 2-Step Verification
   - Scroll down and click on "App passwords"
   - Create a new app password for "Mail"
   - Use this password in your `config.properties`

## Running the Bot

1. **Start the bot**

   ```bash
   python main.py
   ```

2. **Available Commands**
   - `/netflix_start` - Start the bot
   - `/netflix_help` - Show help message
   - `/netflix_code` - Fetch the latest Netflix verification code
   - `/getCode` - (Legacy) Fetch the latest Netflix verification code

## Docker Support

You can also run the bot using Docker:

1. **Build the Docker image**

   ```bash
   docker build -t codefetcherbot .
   ```

2. **Run with Docker**
   ```bash
   docker run -v $(pwd)/config.properties:/app/config.properties codefetcherbot
   ```

Or use Docker Compose:

```bash
docker-compose up -d
```

## Security Notes

- Never share your `config.properties` file
- Keep your bot token private
- Use App Passwords instead of your main Gmail password
- Regularly update the authorized chat IDs list
- Monitor the bot logs for unauthorized access attempts

## Troubleshooting

1. **Email Access Issues**

   - Ensure IMAP is enabled in your Gmail settings
   - Verify your app password is correct
   - Check if less secure app access is enabled (if not using 2FA)

2. **Telegram Issues**
   - Verify your bot token is correct
   - Ensure your chat ID is in the authorized list
   - Check the bot has proper permissions in group chats

## Contributing

Feel free to submit issues and enhancement requests!
