from typing import Any, Dict, Optional
from workers import WorkerEntrypoint, Request, Response
import json

from zulip import Client
from zulip_bots.lib import AbstractBotHandler, ExternalBotHandler

class HelloWorldHandler:
    def handle_message(self, message: Dict[str, Any], bot_handler: AbstractBotHandler) -> None:
        content = "beep boop"
        bot_handler.send_reply(message, content)
        bot_handler.react(message, "wave")

class Default(WorkerEntrypoint):
    async def fetch(self, request: Request) -> Response:
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
            payload: Optional[Dict[str, Any]] = await request.json()
            if not payload:
                return Response.json({"error": "Missing request content"}, status=400)
            message: Dict[str, Any] = payload.get("message")
            if not message:
                return Response.json({"error": "Missing 'message' in request"}, status=400)
            handler = HelloWorldHandler()
            handler.handle_message(message, bot_handler)
            return Response(json.dumps({"result": "success"}), status=200)
            
        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500)
