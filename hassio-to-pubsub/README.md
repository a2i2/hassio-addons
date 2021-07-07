# Home Assistant to Pub/Sub

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
[![License][license-shield]](LICENSE.md)

<!-- ![Supports armhf Architecture][armhf-shield] -->
<!-- ![Supports armv7 Architecture][armv7-shield] -->

![Supports aarch64 Architecture][aarch64-shield]

<!-- ![Supports amd64 Architecture][amd64-shield] -->
<!-- ![Supports i386 Architecture][i386-shield] -->

[![Github Actions][github-actions-shield]][github-actions]
![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

This add-on subscribes to events on the Home Assistant websocket and pushes them
to a Google Cloud Pub/Sub topic. Messages are associated with a `home_id` that
is used to distinguish between different Home Assistant installations.

## Authors & contributors

The original setup of this repository is by [Franck Nijhof][frenck].

For a full list of all authors and contributors,
check [the contributor's page][contributors].

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[commits-shield]: https://img.shields.io/github/commit-activity/y/a2i2/addon-example
[commits]: https://github.com/a2i2/addon-example/commits/main
[contributors]: https://github.com/a2i2/addon-example/graphs/contributors
[discord-ha]: https://discord.gg/c5DvZ4e
[discord-shield]: https://img.shields.io/discord/478094546522079232.svg
[discord]: https://discord.me/hassioaddons
[docs]: https://github.com/a2i2/addon-example/blob/main/example/DOCS.md
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg
[forum]: https://community.home-assistant.io/t/repository-community-hass-io-add-ons/24705?u=frenck
[frenck]: https://github.com/frenck
[github-actions-shield]: https://github.com/a2i2/addon-example/workflows/CI/badge.svg
[github-actions]: https://github.com/a2i2/addon-example/actions
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[issue]: https://github.com/a2i2/addon-example/issues
[license-shield]: https://img.shields.io/github/license/a2i2/addon-example.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2021.svg
[project-stage-shield]: https://img.shields.io/badge/project%20stage-in%20development-red.svg
[reddit]: https://reddit.com/r/homeassistant
[releases-shield]: https://img.shields.io/github/release/a2i2/addon-example.svg
[releases]: https://github.com/a2i2/addon-example/releases
[repository]: https://github.com/a2i2/repository
