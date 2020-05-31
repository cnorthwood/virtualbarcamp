import React, { FunctionComponent } from "react";
import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import ApolloClient from "apollo-client";
import { split } from "apollo-link";
import { WebSocketLink } from "apollo-link-ws";
import { HttpLink } from "apollo-link-http";
import { getMainDefinition } from "apollo-utilities";

function initApolloClient(): ApolloClient<NormalizedCacheObject> {
  return new ApolloClient({
    cache: new InMemoryCache(),
    link: split(
      // split based on operation type
      ({ query }) => {
        const definition = getMainDefinition(query);
        return definition.kind === "OperationDefinition" && definition.operation === "subscription";
      },
      new WebSocketLink({
        uri: `${window.location.protocol === "http" ? "ws" : "wss"}://${
          window.location.host
        }/graphql/`,
        options: {
          reconnect: true,
        },
      }),
      new HttpLink({
        uri: "/graphql/",
      }),
    ),
  });
}

const App: FunctionComponent = () => <></>;

export default App;
