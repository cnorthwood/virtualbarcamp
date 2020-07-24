import React, { FunctionComponent, useEffect } from "react";
import { gql, useQuery } from "@apollo/client";
import { grid } from "./graphql/grid";
import { slotChanged } from "./graphql/slotChanged";

const GRID_QUERY = gql`
  query grid {
    grid {
      sessions {
        id
        name
        startTime
        endTime
        event
        slots {
          id
          room {
            id
            name
          }
          talk {
            id
            title
            isMine
            isOpenDiscussion
            speakers {
              id
              name
            }
          }
        }
      }
    }
  }
`;

const SLOTS_SUBSCRIPTION = gql`
  subscription slotChanged {
    slotChanged {
      id
      talk {
        id
        title
        isMine
        isOpenDiscussion
        speakers {
          id
          name
        }
      }
    }
  }
`;

const ADD_TALK_MUTATION = gql`
  mutation addTalk(
    $slotId: ID!
    $title: String!
    $isOpenDiscussion: Boolean!
    $additionalSpeakers: [ID!]!
  ) {
    addTalk(
      slotId: $slotId
      title: $title
      isOpenDiscussion: $isOpenDiscussion
      additionalSpeakers: $additionalSpeakers
    ) {
      id
      talk {
        id
        title
        isMine
        isOpenDiscussion
        speakers {
          id
          name
        }
      }
    }
  }
`;

const MOVE_TALK_MUTATION = gql`
  mutation moveTalk($talkId: ID!, $oldSlot: ID!, $newSlot: ID!) {
    moveTalk(talkId: $talkId, fromSlot: $oldSlot, toSlot: $newSlot) {
      id
      talk {
        id
        title
        isMine
        isOpenDiscussion
        speakers {
          id
          name
        }
      }
    }
  }
`;

const REMOVE_TALK_MUTATION = gql`
  mutation removeTalk($slotId: ID!) {
    removeTalk(slotId: $slotId) {
      id
      talk {
        id
        title
        isMine
        isOpenDiscussion
        speakers {
          id
          name
        }
      }
    }
  }
`;

const Grid: FunctionComponent = () => {
  const { data, loading, error, subscribeToMore } = useQuery<grid>(GRID_QUERY);
  useEffect(
    () =>
      subscribeToMore<slotChanged>({
        document: SLOTS_SUBSCRIPTION,
        updateQuery: (
          previousData,
          {
            subscriptionData: {
              data: { slotChanged },
            },
          },
        ) => {
          return {
            grid: {
              ...previousData.grid,
              sessions: previousData.grid.sessions.map((session) => ({
                ...session,
                slots:
                  session.slots?.map((slot) =>
                    slotChanged.id === slot.id ? { ...slot, ...slotChanged } : slot,
                  ) ?? null,
              })),
            },
          };
        },
      }),
    [subscribeToMore],
  );

  if (error) {
    return (
      <div className="container">
        <div className="message">
          <div className="message-header">An error has occurred</div>
          <div className="message-body">
            <p>An error occurred when loading the grid</p>
            <pre>{error.message}</pre>
          </div>
        </div>
      </div>
    );
  }

  if (loading || !data) {
    return (
      <div className="container">
        <progress className="progress is-large is-primary" />
      </div>
    );
  }

  return <></>;
};

export default Grid;
