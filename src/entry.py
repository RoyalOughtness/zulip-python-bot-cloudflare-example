from workers import WorkerEntrypoint, Response
import json

from zulip import Client
from zulip_bots.lib import ExternalBotHandler

class HelloWorldHandler:
    def handle_message(self, message, bot_handler):
        content = "I am responding from cloudflare"
        bot_handler.send_reply(message, content)
        bot_handler.react(message, "wave")

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        client = Client(
            email=self.env.ZULIP_EMAIL,
            api_key=self.env.ZULIP_API_KEY,
            site=self.env.ZULIP_SITE
        )

        bot_handler = ExternalBotHandler(
            client=client,
            root_dir=None,
            bot_details={"name": "HelloWorldBot"}
        )

        try:
            payload = await request.json()
            message = payload.get("message")
            
            if message:
                handler = HelloWorldHandler()
                handler.handle_message(message, bot_handler)
                
            return Response(json.dumps({"result": "success"}), status=200)
            
        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500)
