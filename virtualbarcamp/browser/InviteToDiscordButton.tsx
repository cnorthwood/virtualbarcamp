import React, { FunctionComponent } from "react";
import { gql, useMutation } from "@apollo/client";

import { inviteToDiscord } from "./graphql/inviteToDiscord";

const INVITE_TO_DISCORD_MUTATION = gql`
  mutation inviteToDiscord {
    inviteToDiscord
  }
`;

const InviteToDiscordButton: FunctionComponent<{ className?: string }> = ({
  className,
  children,
}) => {
  const [inviteToDiscordMutation, { loading, error, called }] = useMutation<inviteToDiscord>(
    INVITE_TO_DISCORD_MUTATION,
  );

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
      onClick={() => inviteToDiscordMutation()}
    >
      {called ? "Invited" : children}
    </button>
  );
};

export default InviteToDiscordButton;
