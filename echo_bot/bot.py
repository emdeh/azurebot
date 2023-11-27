from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount
from openai import AsyncOpenAI
import os
import json
from web_scraper import search_website
from web_scraper import async_search_website

# Load OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text

        # Use the web scraper to get charity info
        charity_info = await async_search_website(user_input)
        if charity_info:
            # Formulate a prompt for OpenAI to summarize the charity info
            prompt = f"Please provide a summary for the following charity information. In your response, provide a summary of activities, a list of the charity programs, where the charity operates, and a brief financial summary. Here is the charity info:\n\n{charity_info}"

            try:
                # Send the prompt to OpenAI and get a summary
                chat_completion = await client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}],
                    model="gpt-3.5-turbo"
                )

                # Extracting the OpenAI response content
                bot_reply = chat_completion.choices[0].message.content
            except Exception as e:
                bot_reply = "Sorry, I am having trouble summarizing the information right now."
                print(f"Error: {e}")
        else:
            bot_reply = "I couldn't find any information on that charity."

        # Send the response (either the summary or an error message) back to the user
        await turn_context.send_activity(MessageFactory.text(bot_reply))

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome! Please tell me which charity you'd like me to look up.")