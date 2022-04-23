import os
from typing import Dict, Type, List

import git

from diarybot.core.git_sync import GitSync
from diarybot.core.journal import PlainTextJournal
from diarybot.core.buy_list import BuyList
from diarybot.core.recorder import TextRecorder
from diarybot.handlers.interface import EventHandler
from diarybot.tenant_config import TenantConfig
from diarybot.skill_interface import Skill
from diarybot.dgit import Git


class HandlerLoader:
    def __init__(self,
                 tenant_config: TenantConfig,
                 private_key_path: str,
                 skills: List[Skill]) -> None:
        self._tenant_config = tenant_config
        self._private_key_path = private_key_path
        self._skills = skills

    def load(self) -> Dict[Type, EventHandler]:
        recorder = self._load_recorder(self._tenant_config)
        handlers = {}
        for skill in self._skills:
            handlers[skill.event_class] = skill.event_handler_class.load(
                tenant_config=self._tenant_config,
                recorder=recorder,
            )
        return handlers

    def _load_recorder(self, config: TenantConfig) -> TextRecorder:
        sync = GitSync(git=Git(git.Repo(config.base_dir), private_key_path=self._private_key_path))
        journal_path = os.path.join(config.base_dir, config.diary_file_name)
        return TextRecorder(
            before_write=[sync.on_before_write],
            on_write=[
                PlainTextJournal(file_path=journal_path),
                BuyList(os.path.join(config.base_dir, 'buy_list.md')),
            ],
            after_write=[sync.on_after_write],
        )
