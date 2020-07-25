import React, { FunctionComponent, useCallback, useEffect } from "react";
import { gql, useMutation, useQuery } from "@apollo/client";
import { DragDropContext, Draggable, Droppable, DropResult } from "react-beautiful-dnd";

import { grid } from "./graphql/grid";
import { slotChanged } from "./graphql/slotChanged";
import { addTalk, addTalkVariables } from "./graphql/addTalk";
import { moveTalk, moveTalkVariables } from "./graphql/moveTalk";

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
  mutation moveTalk($talkId: ID!, $toSlot: ID!) {
    moveTalk(talkId: $talkId, toSlot: $toSlot) {
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
  const { data, loading, error: loadError, subscribeToMore } = useQuery<grid>(GRID_QUERY);
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

  const [addTalk, { error: addError }] = useMutation<addTalk, addTalkVariables>(ADD_TALK_MUTATION);
  const [moveTalk, { error: moveError }] = useMutation<moveTalk, moveTalkVariables>(
    MOVE_TALK_MUTATION,
  );

  const onDragEnd = useCallback(
    async (result: DropResult) => {
      if (!result.destination) {
        return;
      }

      if (result.draggableId === "new") {
        await addTalk({
          variables: {
            slotId: result.destination.droppableId,
            title: "A new talk",
            isOpenDiscussion: false,
            additionalSpeakers: [],
          },
        });
      } else {
        await moveTalk({
          variables: { talkId: result.draggableId, toSlot: result.destination.droppableId },
        });
      }
    },
    [addTalk, moveTalk],
  );

  if (loadError || addError || moveError) {
    return (
      <div className="container">
        <div className="message">
          <div className="message-header">An error has occurred</div>
          <div className="message-body">
            <p>An error occurred when loading the grid</p>
            <pre>{(loadError || addError || moveError)?.message}</pre>
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

  const roomIds: Record<string, string> = {};
  data.grid.sessions.forEach((session) => {
    session.slots?.forEach((slot) => {
      roomIds[slot.room.id] = slot.room.name;
    });
  });

  const rooms = Object.entries(roomIds)
    .map(([id, name]) => ({ id, name }))
    .sort((a, b) => a.name.localeCompare(b.name));

  return (
    <DragDropContext nonce={document.getElementById("root")!.dataset.nonce} onDragEnd={onDragEnd}>
      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th scope="col">Room</th>
              {data.grid.sessions.map(({ id, name, event }) => (
                <th key={id} scope="col">
                  {name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rooms.map((room, i) => (
              <tr key={room.id}>
                <th scope="row">{room.name}</th>
                {data!.grid.sessions.map(({ id, event, slots }) => {
                  if (event !== null || !slots) {
                    return i === 0 ? (
                      <td key={id} rowSpan={rooms.length}>
                        {event}
                      </td>
                    ) : null;
                  }

                  const slot = slots.find((slot) => slot.room.id === room.id);
                  if (!slot) {
                    return <td key={id} />;
                  }

                  return (
                    <Droppable key={id} droppableId={slot.id} isDropDisabled={slot.talk !== null}>
                      {(provided, snapshot) => (
                        <td ref={provided.innerRef} {...provided.droppableProps}>
                          {slot.talk ? (
                            <Draggable
                              draggableId={slot.talk.id}
                              isDragDisabled={!slot.talk.isMine}
                              index={0}
                            >
                              {(provided, snapshot) => (
                                <div
                                  ref={provided.innerRef}
                                  {...provided.draggableProps}
                                  {...provided.dragHandleProps}
                                >
                                  Drag me!
                                </div>
                              )}
                            </Draggable>
                          ) : null}
                          {provided.placeholder}
                        </td>
                      )}
                    </Droppable>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DragDropContext>
  );
};

export default Grid;
