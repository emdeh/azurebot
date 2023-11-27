from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount
from openai import AsyncOpenAI
import os
import json
from ais_dataset_search import retrieve_charity_data

# Load OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

# ...

class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text

        # Acknowledge the user's input
        await turn_context.send_activity(MessageFactory.text(f"Searching for information about '{user_input}'. Please wait a moment..."))


        # Use the ais_dataset_search API to get charity info
        charity_info = await retrieve_charity_data(user_input)
        if charity_info:
            charity_name = charity_info[0].get('charity name', None)
            charity_website = charity_info[0].get('charity website', None)  
            charity_abn = charity_info[0].get('abn', None)
            # Extracting the website and abn from the first charity info record for future use in response

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

                # Append the charity's website to the bot's reply if it exists
                if charity_website:
                    bot_reply += f"\n\nFor more information you can visit {charity_name}'s website: {charity_website} or search for them on the ACNC Charity Register: https://www.acnc.gov.au/charity/charities?search={charity_abn}"

            except Exception as e:
                bot_reply = "Sorry, I am having trouble summarizing the information right now."
                print(f"Error: {e}")
        else:
            bot_reply = "I couldn't find any information on that charity."

        # Send the response (either the summary or an error message) back to the user
        await turn_context.send_activity(MessageFactory.text(bot_reply))

        # Ask if the user has any further questions
        await turn_context.send_activity(MessageFactory.text("Do you have any other questions about this charity or another one?"))

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome! Please tell me which charity you'd like me to look up. Keep in mind, I only have access to AIS 2021 data. So some information might not be available or up-to-date. If you'd like the most recent information, please visit the ACNC Charity Register: https://www.acnc.gov.au/charity/charities ")