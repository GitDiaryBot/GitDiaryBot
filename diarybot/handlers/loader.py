import os
from typing import Dict, Type, List

from diarybot.core.git_sync import GitSync
from diarybot.core.journal import PlainTextJournal
from diarybot.core.buy_list import BuyList
from diarybot.core.recorder import TextRecorder
from diarybot.handlers.interface import EventHandler
from diarybot.tenant_config import TenantConfig
from diarybot.skill_interface import Skill


class HandlerLoader:
    def __init__(self, tenant_config: TenantConfig, skills: List[Skill]) -> None:
        self._tenant_config = tenant_config
        self._skills = skills

    def load(self) -> Dict[Type, EventHandler]:
        recorder = self._load_recorder(self._tenant_config)
        return {
            skill.event_class: skill.event_handler_class.load(
                tenant_config=self._tenant_config,
                recorder=recorder
            )
            for skill in self._skills
        }

    @staticmethod
    def _load_recorder(config: TenantConfig) -> TextRecorder:
        sync = GitSync(git_dir=config.base_dir)
        journal_path = os.path.join(config.base_dir, config.diary_file_name)
        return TextRecorder(
            before_write=[sync.on_before_write],
            on_write=[
                PlainTextJournal(file_path=journal_path),
                BuyList(os.path.join(config.base_dir, 'buy_list.md')),
            ],
            after_write=[sync.on_after_write],
        )
