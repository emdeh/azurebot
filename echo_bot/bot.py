from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount
from openai import AsyncOpenAI
import os
import json

# Load OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text

        try:
            chat_completion = await client.chat.completions.create(
                messages=[{"role": "user", "content": user_input}],
                model="gpt-3.5-turbo"
            )

            # Debug: Print the raw response
            #print("Raw response:", chat_completion)
            
            # Try to convert the response to JSON for easier inspection
            #try:
            #    response_json = json.dumps(chat_completion, default=lambda o: o.__dict__)
            #    print("JSON formatted response:", response_json)
            #except Exception as json_error:
            #    print("Error in JSON conversion:", json_error)

            # Extracting the response content
            # Update this part based on the structure revealed by the print statement

            bot_reply = chat_completion.choices[0].message.content

            # Send OpenAI's response back to the user
            await turn_context.send_activity(MessageFactory.text(bot_reply))
            
        except Exception as e:
            await turn_context.send_activity("Sorry, I am having trouble responding right now.")
            print(f"Error: {e}")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
