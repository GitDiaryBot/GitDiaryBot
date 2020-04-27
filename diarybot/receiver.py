from typing import Dict, List

from telegram import Message

from diarybot.tenant_config import TenantConfigLoader
from diarybot.handlers.loader import HandlerLoader
from diarybot.tenant import Tenant
from diarybot.extractors.interface import EventExtractorInterface
from diarybot.skill_interface import Skill
from diarybot.bot_config import BotConfig


class TenantLib:
    """Creates and holds tenants registry.

    Tenants are identified by chat user ID.
    Each tenant has a set of handlers parameterized with tenant config.
    """

    def __init__(self,
                 tenant_config_loader: TenantConfigLoader,
                 private_key_path: str,
                 skills: List[Skill]) -> None:
        self._tenant_config_loader = tenant_config_loader
        self._tenants: Dict[int, Tenant] = {}
        self._private_key_path = private_key_path
        self._skills = skills

    def load_tenant(self, tenant_id: int) -> Tenant:
        if tenant_id not in self._tenants:
            tenant_config = self._tenant_config_loader.load(tenant_id)
            loader = HandlerLoader(
                tenant_config=tenant_config,
                private_key_path=self._private_key_path,
                skills=self._skills,
            )
            self._tenants[tenant_id] = Tenant(handlers=loader.load())
        return self._tenants[tenant_id]


def load_tenant_lib(bot_config: BotConfig, skills: List[Skill]) -> TenantLib:
    return TenantLib(
        tenant_config_loader=TenantConfigLoader(
            single_user_id=bot_config.single_user_id,
        ),
        private_key_path=bot_config.private_key_path,
        skills=skills,
    )


class MessageReceiver:
    """Extracts internal events from incoming messages and sends them to a tenant."""

    def __init__(self,
                 tenant_lib: TenantLib,
                 event_extractor: EventExtractorInterface) -> None:
        self._tenant_lib = tenant_lib
        self._event_extractor = event_extractor

    def receive_message(self, user_id: int, message: Message) -> None:
        tenant = self._tenant_lib.load_tenant(user_id)
        for event in self._event_extractor.extract_events(message):
            tenant.handle_event(event)
        message.reply_text("Saved")
