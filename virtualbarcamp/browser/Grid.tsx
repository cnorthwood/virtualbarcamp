import React, { ChangeEvent, FunctionComponent, useCallback, useEffect, useState } from "react";
import { gql, useMutation, useQuery } from "@apollo/client";
import { DragDropContext, Draggable, Droppable, DropResult } from "react-beautiful-dnd";
import parseISO from "date-fns/parseISO";
import format from "date-fns/format";
import isPast from "date-fns/isPast";
import isWithinInterval from "date-fns/isWithinInterval";

import { grid } from "./graphql/grid";
import { slotChanged } from "./graphql/slotChanged";
import { addTalk as addTalkResults, addTalkVariables } from "./graphql/addTalk";
import { moveTalk as moveTalkResults, moveTalkVariables } from "./graphql/moveTalk";
import { availableSpeakers } from "./graphql/availableSpeakers";
import Talk from "./Talk";
import SpeakersControl from "./SpeakersControl";

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

const SPEAKERS_QUERY = gql`
  query availableSpeakers {
    speakers {
      id
      name
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

const isNow = (start: string, end: string) =>
  isWithinInterval(new Date(), { start: parseISO(start), end: parseISO(end) });

const fallbackAvailableSpeakers: { id: string; name: string }[] = [];

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
        ) => ({
          grid: {
            ...previousData.grid,
            sessions: previousData.grid.sessions.map((session) => ({
              ...session,
              slots:
                session.slots?.map((slot) =>
                  slotChanged.id === slot.id
                    ? { ...slot, ...slotChanged }
                    : slot.talk?.id === slotChanged.talk?.id
                    ? { ...slot, talk: null }
                    : { ...slot },
                ) ?? null,
            })),
          },
        }),
      }),
    [subscribeToMore],
  );

  const { data: speakersData, error: speakersError } = useQuery<availableSpeakers>(SPEAKERS_QUERY);

  const [addTalk, { error: addError }] = useMutation<addTalkResults, addTalkVariables>(
    ADD_TALK_MUTATION,
  );
  const [moveTalk, { error: moveError }] = useMutation<moveTalkResults, moveTalkVariables>(
    MOVE_TALK_MUTATION,
  );

  const [newTalkTitle, setNewTalkTitle] = useState<string>("");
  const [newTalkIsOpenDiscussion, setNewTalkIsOpenDiscussion] = useState<boolean>(false);
  const [newTalkAdditionalSpeakers, setNewTalkAdditionalSpeakers] = useState<string[]>([]);

  const changeNewTalkTitle = useCallback(
    (ev: ChangeEvent<HTMLInputElement>) => {
      setNewTalkTitle(ev.currentTarget.value);
    },
    [setNewTalkTitle],
  );

  const changeNewTalkIsOpenDiscussion = useCallback(
    (ev: ChangeEvent<HTMLInputElement>) => {
      setNewTalkIsOpenDiscussion(ev.currentTarget.checked);
    },
    [setNewTalkIsOpenDiscussion],
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
            title: newTalkTitle,
            isOpenDiscussion: newTalkIsOpenDiscussion,
            additionalSpeakers: newTalkAdditionalSpeakers,
          },
        });
        setNewTalkTitle("");
        setNewTalkIsOpenDiscussion(false);
        setNewTalkAdditionalSpeakers([]);
      } else {
        await moveTalk({
          variables: { talkId: result.draggableId, toSlot: result.destination.droppableId },
        });
      }
    },
    [
      addTalk,
      moveTalk,
      newTalkTitle,
      setNewTalkTitle,
      newTalkIsOpenDiscussion,
      setNewTalkIsOpenDiscussion,
      newTalkAdditionalSpeakers,
      setNewTalkAdditionalSpeakers,
    ],
  );

  if (loadError || addError || moveError || speakersError) {
    return (
      <div className="container">
        <div className="message">
          <div className="message-header">An error has occurred</div>
          <div className="message-body">
            <p>An error occurred when loading the grid</p>
            <pre>{(loadError || addError || moveError || speakersError)?.message}</pre>
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
        <table className="grid">
          <thead>
            <tr>
              <th />
              {data.grid.sessions.map(({ id, name, event, startTime, endTime }) => (
                <th
                  key={id}
                  scope="col"
                  className={`grid__session ${isNow(startTime, endTime) ? "in-progress" : ""}`}
                >
                  <p>{event ? "" : name}</p>
                  <p className="has-text-weight-light">
                    {format(parseISO(startTime), "p")}
                    {event ? null : <> – {format(parseISO(endTime), "p")}</>}
                  </p>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rooms.map((room, i) => (
              <tr key={room.id}>
                <th scope="row" className="grid__room">
                  {room.name}
                </th>
                {data!.grid.sessions.map(({ id, startTime, endTime, event, slots }) => {
                  if (event !== null || !slots) {
                    return i === 0 ? (
                      <td
                        key={id}
                        rowSpan={rooms.length}
                        className={`grid__event ${isNow(startTime, endTime) ? "in-progress" : ""}`}
                      >
                        <span className="grid__event-name">{event}</span>
                      </td>
                    ) : null;
                  }

                  const slotHasStarted = isPast(parseISO(startTime));
                  const slotHasEnded = isPast(parseISO(endTime));

                  const slot = slots.find((slot) => slot.room.id === room.id);
                  if (!slot) {
                    return <td key={id} />;
                  }

                  return (
                    <Droppable
                      key={id}
                      droppableId={slot.id}
                      isDropDisabled={slot.talk !== null || slotHasEnded}
                    >
                      {(provided, snapshot) => (
                        <td
                          ref={provided.innerRef}
                          {...provided.droppableProps}
                          className={`grid__slot ${isNow(startTime, endTime) ? "in-progress" : ""}`}
                        >
                          {slot.talk ? (
                            <Draggable
                              draggableId={slot.talk.id}
                              isDragDisabled={!slot.talk.isMine || slotHasStarted}
                              index={0}
                            >
                              {(provided, snapshot) => (
                                <div
                                  key={slot.id}
                                  ref={provided.innerRef}
                                  {...provided.draggableProps}
                                  {...provided.dragHandleProps}
                                >
                                  <Talk
                                    key={slot.talk!.id}
                                    id={slot.talk!.id}
                                    slotId={slot.id}
                                    title={slot.talk!.title}
                                    isEditable={slot.talk!.isMine && !slotHasEnded}
                                    isOpenDiscussion={slot.talk!.isOpenDiscussion}
                                    speakers={slot.talk!.speakers}
                                    availableSpeakers={
                                      speakersData?.speakers ?? fallbackAvailableSpeakers
                                    }
                                  />
                                </div>
                              )}
                            </Draggable>
                          ) : (
                            <div
                              key={slot.id}
                              className={`grid__empty-slot ${
                                snapshot.isDraggingOver ? "grid__empty-slot--target" : ""
                              }`}
                            />
                          )}
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
      <Droppable droppableId="new" isDropDisabled={true}>
        {(provided, snapshot) => (
          <div className="container" ref={provided.innerRef} {...provided.droppableProps}>
            <Draggable draggableId="new" isDragDisabled={newTalkTitle === ""} index={0}>
              {(provided, snapshot) => (
                <div
                  ref={provided.innerRef}
                  {...provided.draggableProps}
                  {...provided.dragHandleProps}
                  className="grid__slot--blank"
                >
                  <div className="talk talk--new">
                    <div className="field">
                      <label className="label" htmlFor="title">
                        Talk Title
                      </label>
                      <div className="control">
                        <input
                          className="input"
                          id="title"
                          type="text"
                          required
                          value={newTalkTitle}
                          onChange={changeNewTalkTitle}
                        />
                      </div>
                    </div>
                    <SpeakersControl
                      speakers={newTalkAdditionalSpeakers}
                      availableSpeakers={speakersData?.speakers ?? fallbackAvailableSpeakers}
                      onChange={setNewTalkAdditionalSpeakers}
                    />
                    <div className="field">
                      <div className="control">
                        <label className="checkbox">
                          <input
                            type="checkbox"
                            checked={newTalkIsOpenDiscussion}
                            onChange={changeNewTalkIsOpenDiscussion}
                          />{" "}
                          Open discussion
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </Draggable>
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
};

export default Grid;
