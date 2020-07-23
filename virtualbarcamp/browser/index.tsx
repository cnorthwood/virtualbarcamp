import React from "react";
import ReactDOM from "react-dom";
import {
  ApolloClient,
  ApolloProvider,
  HttpLink,
  InMemoryCache,
  NormalizedCacheObject,
  split,
} from "@apollo/client";
import { WebSocketLink } from "@apollo/client/link/ws";
import { getMainDefinition } from "@apollo/client/utilities";

import csrfToken from "./csrf";
import App from "./App";

import "./styles.scss";

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
        uri: `${window.location.protocol === "http:" ? "ws" : "wss"}://${
          window.location.host
        }/graphql/`,
        options: {
          reconnect: true,
        },
      }),
      new HttpLink({
        uri: "/graphql/",
        headers: {
          "x-csrftoken": csrfToken,
        },
      }),
    ),
  });
}

const apolloClient = initApolloClient();

ReactDOM.render(
  <React.StrictMode>
    <ApolloProvider client={apolloClient}>
      <App />
    </ApolloProvider>
  </React.StrictMode>,
  document.getElementById("root"),
);

if (module.hot) {
  module.hot.accept("./App", () => {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const NewApp = require("./App").default;

    ReactDOM.render(
      <ApolloProvider client={apolloClient}>
        <NewApp />
      </ApolloProvider>,
      document.getElementById("root"),
    );
  });
}
