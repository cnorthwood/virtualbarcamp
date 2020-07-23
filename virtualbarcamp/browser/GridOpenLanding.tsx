import React, { FunctionComponent } from "react";

import DiscordInviteModal from "./DiscordInviteModal";
import Grid from "./Grid";

const GridOpenLanding: FunctionComponent = () => (
  <>
    <DiscordInviteModal />
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
      <Grid />
    </section>
  </>
);

export default GridOpenLanding;
