import React, { FunctionComponent, useState } from "react";
import gql from "graphql-tag";
import { useQuery } from "@apollo/react-hooks";
import { isOnDiscord } from "./graphql/isOnDiscord";
import InviteToDiscordButton from "./InviteToDiscordButton";

const IS_ON_DISCORD_QUERY = gql`
  query isOnDiscord {
    isOnDiscord
  }
`;

const GridOpenLanding: FunctionComponent = () => {
  const [modalClosed, setModalClosed] = useState<boolean>(false);
  const { data } = useQuery<isOnDiscord>(IS_ON_DISCORD_QUERY);

  return (
    <>
      <div className={`modal ${!data?.isOnDiscord && !modalClosed ? "is-active" : ""}`}>
        <div className="modal-background" />
        <div className="modal-content">
          <div className="box content">
            <p>
              BarCamp Manchester 10 is taking place using Discord. Join our Discord server now to
              meet your fellow attendees in the lobby, and if you're presenting, you can find a test
              room to check your technology in (using Discord's Go Live function). You can also form
              a breakout room for discussions by saying <code>!breakout My Topic</code> in the lobby
              (changing "My Topic" to the name of the breakout topic) to create a new breakout room
              for smaller discussions.
            </p>
            <p className="has-text-centered">
              <InviteToDiscordButton className="is-primary is-large">
                Send me an invite on Discord
              </InviteToDiscordButton>
            </p>
            <p>
              The grid is open here to submit your talks. The rooms are in Discord which incorporate
              a text chat element, and a voice chat element. Voice chats can be limited to only the
              presenter (who put the card on the Grid), but can optionally include co-presenters or
              be an open discussion, with everyone able to speak. If you present slides (using
              Discord's go live feature), the maximum capacity of your room will be 50 people.
            </p>
          </div>
        </div>
        <button
          className="modal-close is-large"
          aria-label="close"
          onClick={() => {
            setModalClosed(true);
          }}
        />
      </div>
      <div className="hero">
        <div className="hero-body">
          <div className="container">
            <h2 className="title">The Grid</h2>
            <p className="subtitle">
              The grid shows the sessions that are running, at what time and in which room.
              <br />
              Want to run your own session? Fill in the blank card and drag it into a free spot!
            </p>
          </div>
        </div>
      </div>
      <section className="section">
        <div className="container">
          <div className="columns is-centered">
            <div className="column is-two-thirds content"></div>
          </div>
        </div>
      </section>
    </>
  );
};

export default GridOpenLanding;
