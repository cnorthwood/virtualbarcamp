import React, { FunctionComponent, useEffect } from "react";
import { gql, useQuery } from "@apollo/client";

import { globalSettings } from "./graphql/globalSettings";
import { globalSettingsUpdated } from "./graphql/globalSettingsUpdated";
import PreEventLanding from "./PreEventLanding";
import DoorsOpenLanding from "./DoorsOpenLanding";
import GridOpenLanding from "./GridOpenLanding";
import PostEventLanding from "./PostEventLanding";

const GLOBAL_STATE_QUERY = gql`
  query globalSettings {
    globalSettings {
      eventState
      doorsOpenTime
      gridOpenTime
    }
  }
`;

const GLOBAL_STATE_SUBSCRIPTION = gql`
  subscription globalSettingsUpdated {
    globalSettings {
      eventState
      doorsOpenTime
      gridOpenTime
    }
  }
`;

const App: FunctionComponent = () => {
  const { data, error, subscribeToMore } = useQuery<globalSettings>(GLOBAL_STATE_QUERY);
  useEffect(
    () =>
      subscribeToMore<globalSettingsUpdated>({
        document: GLOBAL_STATE_SUBSCRIPTION,
        updateQuery: (previousData, { subscriptionData }) => {
          return subscriptionData.data ?? previousData;
        },
      }),
    [subscribeToMore],
  );

  if (error) {
    return (
      <div className="message is-danger">
        <div className="message-body">Sorry, an error occurred whilst loading this page.</div>
      </div>
    );
  }

  return data?.globalSettings.eventState === "PRE_EVENT" ? (
    <PreEventLanding doorsOpenTime={data.globalSettings.doorsOpenTime} />
  ) : data?.globalSettings.eventState === "DOORS_OPEN" ? (
    <DoorsOpenLanding gridOpenTime={data.globalSettings.gridOpenTime} />
  ) : data?.globalSettings.eventState === "GRID_OPEN" ? (
    <GridOpenLanding />
  ) : data?.globalSettings.eventState === "POST_EVENT" ? (
    <PostEventLanding />
  ) : (
    <section className="section">
      <div className="container">
        <progress className="progress is-large is-primary" />
      </div>
    </section>
  );
};

export default App;
