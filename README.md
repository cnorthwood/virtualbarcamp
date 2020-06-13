# Virtual BarCamp

Copyright (C) 2020 Chris Northwood

This is a system that allows you to host multi-track unconferences online.

The system provides a virtual Grid (user-generated event schedule) and then
links to a Discord server where the actual event runs. The system provides a
Discord bot which is mostly responsible for running the schedule and managing
the rooms.

> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU Affero General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
> GNU Affero General Public License for more details.
>
> You should have received a copy of the GNU Affero General Public License
> along with this program. If not, see <https://www.gnu.org/licenses/>.

## Dev Quick Start

You will need to obtain an OAuth2 secret for Discord to develop this. You can
either [grab your own](https://discord.com/developers/docs/topics/oauth2), and
then create a `.env` file at the root of the project with content like:

```
DISCORD_OAUTH_CLIENT_ID=123456
DISCORD_OAUTH_CLIENT_SECRET=abcdef
```

Or, if you know Chris and he trusts you, he can share the BarCamp Manchester
ones with you privately.

Now, you can start a local dev environment:

1. Make sure you have Docker, Poetry and Yarn installed locally
2. Run `poetry install` and `yarn` in the root to have local copies of the
   dependencies installed (for your IDE, etc).
3. Run `docker-compose up`
4. The webserver is running at http://localhost:8000, and all the background
   services should be running in Docker with logs appearing in stdout.

### Giving yourself admin rights

1. Once you have signed in via Discord, you will only have a regular level of
   access
2. The first admin will need to obtain a shell: `docker exec -it virtualbarcamp_app_1 poetry run ./manage.py shell`
3. Run this, varying your username appropriately:
   ```python
   from django.contrib.auth.models import User
   me = User.objects.get(username="laser")
   me.is_staff = True
   me.is_superuser = True
   me.save()
   ```
4. You will now have access to http://localhost:8000/admin/. You can use the
   admin screen to give other people staff/superuser access to the admin.

The process is the same for live, with different mechanisms for obtaining a
shell and the URL for the admin.

### Architectural Overview

The app is a Django app, with the core grid being served as a rich React app
with communication over GraphQL. Channels is used to support websockets and
GraphQL subscriptions for pushing state to the connected clients.

Celery is used to schedule and run timed events (such as doors open, and
rooms changing in the schedule) in the background, with Redis as the
communication mechanism (for both Celery messages, and Channels's message
layers for pushing state changes to connected clients).

The codebase is monolithic, but the architecture is such that it can be
scaled horizontally through multiple instances of the app behind a load
balancer, with Postgres and Redis holding state, rather than relying on a
single process. The intention is for this is to be deployed on some sort of
container platform, and the CI server outputs a single Docker image which can
be started with multiple invocations to take on the key roles.

### Deploying

_TBC_

## Event Runbook

### How the event works

_TBC_

### Opening doors

By default, your virtual BarCamp has 4 states:

- pre-event: people can sign in to the website, but are just shown a holding
  page with a countdown
- doors open: users can join the Discord server and mingle before the main event
- grid open: the grid is open, and people can place events on it. The event is
  now basically running
- post-event: a thank you screen is shown

You can schedule any of these event changes to happen at a particular time.

1. go to the Django administration page and select "Add" next to "Periodic
   Tasks"
2. Enter a name (e.g., "open doors") and then from "task (registered)" select
   the event to trigger (open_doors, open_grid, close_event).
3. Scroll down to "clocked schedule" and select + to add a time. This time is
   local time. Click save in the popup.
4. Tick "one-off task".
5. Save.

This will cause an event to be triggered within a few seconds of the saved
time. To stop this from happening, you can select "delete" in the top corner
of the periodic task from the list of periodic tasks in the admin.

### Defining your grid

_TBC_

### Moderation

#### Removing users

Access the Django admin pages, go into users, and untick the "active"
checkbox. They will no longer be able to log in, and will not be able to
sign up again with the same account. They should also be booted from the
Discord server if they have joined it.

#### Removing cards from the grid

_TBC_
