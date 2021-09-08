GitDiaryBot
===========

This file is intended for developers, if you want to use GitDiaryBot, go to `usage page <https://gitdiarybot.github.io/>`_.

Telegram bot, that writes incoming messages to a text file and synchronizes using Git repository.
In addition to plain text input it also understands locations, voice recordings and photos.

The bot is meant to be self-hosted.
`Demo bot <https://t.me/GitDiaryBot>`_ is running in multi-user mode and can be used for trial.

Decisions and Trade-offs
------------------------

Problem
~~~~~~~

I want to keep a private journal/diary. I post there what's important for me at the moment.
Sometimes I reorganize the content, edit old records. I don't want to share any part of it.

Requirements
~~~~~~~~~~~~

GitDiaryBot has to be:

1. Private - no third party should be able to the diary, or control it.
2. Simple - no special software should be needed to read/write the records.
3. Reliable - network/hard drive failures should not result in lost or unsaved records.
4. Independent - supports self-hosted server side, private repositories.

Choices
~~~~~~~

GitDiaryBot is designed from three assumptions:

1. Diary is a single plain text file, that grows by appending records.
2. Git is used for synchronization and backup.
3. New records come from messages to a chat bot.

While each part can be replaced, the primary goal is to have this combination working.


OOP Architecture
----------------

Dispatcher is reacting to Telegram.Bot updates by delegating to 2 classes:

1. Installer
2. Receiver

Receiver attempts to load tenant using effective user ID from incoming update.
If tenant does not exists, Dispatcher calls Installer to run installation flow.

For successfully loaded Tenant, Dispatcher calls Receiver which extracts GitDiaryBot Events from
Telegram Update Message and invokes appropriate handler.

Handlers processes Events using Core classes.

Core classes' responsibilities are:

* Save journaling records.
* Synchronize with upstream.
* Transcribe voice.
* Geocode coordinates.
* Annotate photos.

Core classes are not allowed to import anything outside core directory.

Transformers use core classes to extract plain text records from other media.

Skill combines telegram filter, extractor, event type and handler.
Skillset defines capabilities available to a Tenant.
