import React, { FunctionComponent } from "react";
import Countdown from "./Countdown";
import InviteToDiscordButton from "./InviteToDiscordButton";
import { useQuery } from "@apollo/client";
import { isOnDiscord } from "./graphql/isOnDiscord";
import { IS_ON_DISCORD_QUERY } from "./DiscordInviteModal";

const DoorsOpenLanding: FunctionComponent<{ gridOpenTime: string | null }> = ({ gridOpenTime }) => {
  const { data } = useQuery<isOnDiscord>(IS_ON_DISCORD_QUERY);

  return (
    <>
      <div className="hero">
        <div className="hero-body">
          <div className="container">
            <div className="columns is-centered">
              <div className="column is-two-thirds">
                <h2 className="title">Welcome to Winter BarCamp!</h2>
                <p className="subtitle">
                  {gridOpenTime !== null ? (
                    <>
                      The grid will open in <Countdown end={gridOpenTime} />.
                    </>
                  ) : null}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <section className="section">
        <div className="container">
          <div className="columns is-centered">
            <div className="column is-two-thirds content">
              <p>
                Winter BarCamp is taking place using Discord. Join our Discord server now to meet
                your fellow attendees in the lobby, and if you're presenting, you can find a test
                room to check your technology in (using Discord's Go Live function).
              </p>
              <p className="has-text-centered">
                {data?.isOnDiscord ? (
                  <a
                    href="https://discord.com/channels/721357132326502400/721357132787875932"
                    className="button is-primary is-large"
                  >
                    Access the Discord server
                  </a>
                ) : (
                  <InviteToDiscordButton className="is-primary is-large">
                    Send me an invite on Discord
                  </InviteToDiscordButton>
                )}
              </p>
              <p>
                Shortly after the opening plenary, the grid will open here for you to submit your
                talks. The rooms are in Discord which incorporate a text chat element, and a voice
                chat element. Voice chats can be limited to only the presenter (who put the card on
                the Grid), but can optionally include co-presenters or be an open discussion, with
                everyone able to speak. If you present slides (using Discord's go live feature), the
                maximum capacity of your room will be 25 people.
              </p>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default DoorsOpenLanding;
