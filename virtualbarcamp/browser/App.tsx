import React, { FunctionComponent, useEffect } from "react";
import gql from "graphql-tag";
import { useQuery } from "@apollo/react-hooks";
import { globalSettings } from "./graphql/globalSettings";
import { globalSettingsUpdated } from "./graphql/globalSettingsUpdated";

const GLOBAL_STATE_QUERY = gql`
  query globalSettings {
    globalSettings {
      eventState
    }
  }
`;

const GLOBAL_STATE_SUBSCRIPTION = gql`
  subscription globalSettingsUpdated {
    globalSettings {
      eventState
    }
  }
`;

const App: FunctionComponent = () => {
  const { data, error, subscribeToMore } = useQuery<globalSettings>(GLOBAL_STATE_QUERY);
  useEffect(() => {
    subscribeToMore<globalSettingsUpdated>({
      document: GLOBAL_STATE_SUBSCRIPTION,
      updateQuery: (previousData, { subscriptionData }) => {
        return subscriptionData.data ?? previousData;
      },
    });
  }, [subscribeToMore]);

  if (error) {
    return (
      <div className="message is-danger">
        <div className="message-body">Sorry, an error occurred whilst loading this page.</div>
      </div>
    );
  }

  return <>{data?.globalSettings.eventState}</>;
};

export default App;
