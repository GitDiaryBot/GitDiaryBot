from typing import Dict

from telegram import Message

from diarybot.tenant_config import TenantConfigLoader
from diarybot.handlers.loader import HandlerLoader, load_recorder
from diarybot.tenant import Tenant
from diarybot.extractors.interface import EventExtractorInterface


class TenantLib:

    def __init__(self, tenant_config_loader: TenantConfigLoader) -> None:
        self._tenant_config_loader = tenant_config_loader
        self._tenants: Dict[int, Tenant] = {}

    def load_tenant(self, tenant_id: int) -> Tenant:
        if tenant_id not in self._tenants:
            tenant_config = self._tenant_config_loader.load(tenant_id)
            recorder = load_recorder(tenant_config)
            loader = HandlerLoader(tenant_config=tenant_config, recorder=recorder)
            self._tenants[tenant_id] = Tenant(handlers=loader.load())
        return self._tenants[tenant_id]


def load_tenant_lib(single_user_id: int) -> TenantLib:
    return TenantLib(
        tenant_config_loader=TenantConfigLoader(single_user_id=single_user_id),
    )


class MessageReceiver:

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
