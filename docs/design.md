# Virtual BarCamp Design Document

## Requirements

- Users can register an account in advance of the event to obtain a "ticket"
  - they must agree to the code of conduct
  - admins can open/close registration
- Users can reset their password if forgotten
- Users can sign in on the day
  - Users can change their password in advance
  - If they log in in advance, they get given a holding page
- Once "doors open" but before any tracks start, users are dumped in the
  lobby where text chat can occur. This is also the default mode if there are
  no tracks running (lunch time, coffee break, or end of day).
- Opening/closing plenary - all users are dumped into the opening plenary
  session (single track)
- Grid open - users fill in their index card, and then place it on empty
  grid slot
  - no user can fill more than one slot in the same session
  - no user can have more than N sessions in total
  - users can move their own card out of a session
  - only admins can remove other cards from the grid
- Sessions start
  - Users can see grid, but also pick a room
  - Upon joining a room, they enter the text chat for that room and connect
    to the video stream for presenter and also their media (if used)
  - If presenter is not connected, presenter view shows holding images
  - When presenter joins a room, they are offered to share two feeds, one for
    webcam, the other for presentation (e.g., screen share)
  - Five minute change over time, presenter auto kicked off (shown a count
    down timer). Next presenter invited to join room, and start sharing in
    advance of session starting for tech check period. Can request moderator
    assistance in text chat. Only moderator can see shared content in
    changeover period to check it's working. Countdown begins to start of
    session.
- Moderation
  - "flag CoC violation" feature throughout site (in session, on user, on
    text chat)
  - moderators can remove user from event
  - moderators can remove individual message from messaging history
  - moderators can always share content into a room regardless of grid
  - moderators have "panopticon" view, where all text streams and all video
    streams are simultaneously shown

## Architecture

The bulk of the UI is handled by a Django app that handles authentication,
any server-side logic and serves the client. The client is a React
single-page app.

Text chat distribution to be handled in a to-be-defined way. (Perhaps a
simple relay, or perhaps integration with an existing chat app?)

Video distribution is handled by WebRTC. A secret WebRTC peer is offered up
for each presenter (one for screen sharing, and another for presenter view)
and this is taken and then multiplexed out to all connected WebRTC peers.
