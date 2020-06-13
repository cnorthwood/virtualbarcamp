import React, { FunctionComponent } from "react";
import Countdown from "./Countdown";

const PreEventLanding: FunctionComponent<{ doorsOpenTime: string | null }> = ({
  doorsOpenTime,
}) => (
  <div className="hero">
    <div className="hero-body">
      <div className="container">
        <h2 className="title">You are registered!</h2>
        <p className="subtitle">
          {doorsOpenTime === null ? (
            "Check back when the event opens to access the grid and the lobby"
          ) : (
            <>
              Doors open in <Countdown end={doorsOpenTime} />.
            </>
          )}
        </p>
      </div>
    </div>
  </div>
);

export default PreEventLanding;
