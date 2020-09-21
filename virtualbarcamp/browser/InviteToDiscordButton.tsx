import React, { FunctionComponent, useCallback } from "react";
import { ApolloClient, gql, useApolloClient, useMutation } from "@apollo/client";

import { inviteToDiscord } from "./graphql/inviteToDiscord";
import { isOnDiscord } from "./graphql/isOnDiscord";
import { IS_ON_DISCORD_QUERY } from "./DiscordInviteModal";

const INVITE_TO_DISCORD_MUTATION = gql`
  mutation inviteToDiscord {
    inviteToDiscord
  }
`;

const InviteToDiscordButton: FunctionComponent<{ className?: string }> = ({
  className,
  children,
}) => {
  const client: ApolloClient<any> = useApolloClient();
  const [inviteToDiscordMutation, { loading, error, called }] = useMutation<inviteToDiscord>(
    INVITE_TO_DISCORD_MUTATION,
    {
      onCompleted({ inviteToDiscord }) {
        client.writeQuery<isOnDiscord>({
          query: IS_ON_DISCORD_QUERY,
          data: { isOnDiscord: inviteToDiscord },
        });
      },
    },
  );

  const clickButton = useCallback(() => {
    inviteToDiscordMutation();
  }, [inviteToDiscordMutation]);

  if (error) {
    return (
      <button className="button is-danger" disabled>
        An error occurred
      </button>
    );
  }
  return (
    <button
      className={`button ${className ?? ""} ${loading ? "is-loading" : ""}`}
      disabled={called}
      onClick={clickButton}
    >
      {called ? "Invited" : children}
    </button>
  );
};

export default InviteToDiscordButton;
