import React, { FunctionComponent } from "react";

import DiscordInviteModal from "./DiscordInviteModal";
import Grid from "./Grid";

const GridOpenLanding: FunctionComponent = () => (
  <>
    <DiscordInviteModal />
    <div className="hero">
      <div className="hero-body">
        <div className="container">
          <div className="level">
            <div className="level-item level-left">
              <div>
                <h2 className="title">The Grid</h2>
                <p className="subtitle">
                  The grid shows the sessions that are running, at what time and in which room.
                  <br />
                  Want to run your own session? Fill in the blank card and drag it into a free spot!
                </p>
              </div>
            </div>
            <div className="level-item level-right">
              <a
                href="https://discord.com/channels/721357132326502400/721357132787875932"
                className="button is-primary is-large"
              >
                Access the Discord server
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <section className="section">
      <Grid />
    </section>
  </>
);

export default GridOpenLanding;
