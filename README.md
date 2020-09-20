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

You will need to create a Discord server for your event, and then obtain an
OAuth2 secret for Discord to develop this. You can either
[grab your own](https://discord.com/developers/docs/topics/oauth2), and then
create a `.env` file at the root of the project with content like:

```
DISCORD_OAUTH_CLIENT_ID=123456
DISCORD_OAUTH_CLIENT_SECRET=abcdef
DISCORD_OAUTH_BOT_TOKEN=foobarbaz
DISCORD_GUILD_ID=721357132326502400
DISCORD_MODERATOR_ROLE_ID=741674771070320720
```

You should also create a Discord role that corresponds to the role your
volunteers will have.

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
2. The first admin will need to obtain a shell:
 * For the dev environment: `docker exec -it virtualbarcamp_app_1 poetry run ./manage.py shell`
 * For the live environment:<br>
   `doctl kubernetes cluster kubeconfig save virtualbarcamp` (to log in to the cluster)<br>
   `kubectl get pod` and find the name of the pod starting `virtualbarcamp-www`<br>
   `kubectl exec -it virtualbarcamp-www-<pod-full-name> ./manage.py shell`
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

For live, obtain a shell like so:

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

1. Install Terraform and create a DigitalOcean account, obtaining a token.
2. Install doctl and then `doctl auth init` using your DO token.
3. Add NS records for the subdomain you want to `ns{1,2,3}.digitalocean.com`
4. Create a GitLab token with the read_registry permission
5. Create a `infrastructure/secrets.tfvars` file that looks a bit like:
   ```
   do_token                     = "..."
   gitlab_deploy_token_username = "..."
   gitlab_deploy_token_password = "..."
   discord_oauth_client_id      = "..."
   discord_oauth_client_secret  = "..."
   discord_oauth_bot_token      = "..."
   discord_guild_id             = "..."
   discord_moderator_role_id    = "..."
   app_hostname                 = "online.barcampmanchester.co.uk"
   letsencrypt_account_email    = "you@myemail.com"
   ```
6. `terraform init` (on first run only)
7. `terraform apply -var-file secrets.tfvars` and enter the version of the app
   you wish to deploy
8. If you have any migrations you need to apply, then you can run these like so:<br>
   `doctl kubernetes cluster kubeconfig save virtualbarcamp` (to log in to the cluster)<br>
   `kubectl get pod` and find the name of the pod starting `virtualbarcamp-www`<br>
   `kubectl exec virtualbarcamp-www-<pod-full-name> /app/init.sh migrate`

If you need to scale, you can do so by overriding the default number of
workers, or default node size like so:

    terraform apply -var-file secrets.tfvars

## Event Runbook

### How the event works

<iframe src="https://player.vimeo.com/video/457708988" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>

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

Sign into the grid using an account which has staff permissions, and then
visit `/admin/`. Create the rooms you want to use - this will automatically
create the correct channels in Discord.

Now, in the Django admin, create the sessions you wish to have. If you want a
session to be one that people can drop cards into, you must select the rooms
you want to be available for those sessions. If you want the session to be a
placeholder in the schedule (e.g., to show lunch break, etc), then do not
select any rooms and instead complete the "Event" field showing the event
which happens at this time.

### Moderation

#### Removing users

Access the Django admin pages, go into users, and untick the "active"
checkbox. They will no longer be able to log in, and will not be able to
sign up again with the same account. They should also be booted from the
Discord server if they have joined it.

#### Removing cards from the grid

Sign into the grid using an account which has staf permissions, and then
visit `/admin/`. In the Django admin, go into the talks field, find the 
talk you want and then delete it.
