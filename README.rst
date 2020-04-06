GitDiaryBot
===========

Telegram bot, that writes incoming messages to a text file and synchronizes using Git repository.
In addition to plain text input it also understands locations, voice recordings and photos.


OOP Architecture
----------------

Dispatcher is reacting to Telegram.Bot updates by delegating to 2 classes:

1. Installer
2. Receiver

Receiver attempts to load tenant using effective user ID from incoming update.
If tenant does not exists, Dispatcher calls Installer to run installation flow.

For successfully loaded Tenant, Dispatcher calls Receiver which extracts GitDiaryBot Events from
Telegram Update Message and invokes appropriate handler.

Handlers process Events using Core and Transformer classes.

Core classes' responsibilities are:

* Save journaling records.
* Synchronize with upstream.
* Transcribe voice.
* Geocode coordinates.
* Annotate photos.

Core classes are not allowed to import anything outside core directory.

Transformers use core classes to reduce complex message media to plain text records.

Skill combines telegram filter, extractor, event type and handler.
