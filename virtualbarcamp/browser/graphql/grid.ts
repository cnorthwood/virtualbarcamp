/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: grid
// ====================================================

export interface grid_grid_sessions_slots_room {
  __typename: "Room";
  id: string;
  name: string;
}

export interface grid_grid_sessions_slots_talk_speakers {
  __typename: "Speaker";
  id: string;
  name: string;
}

export interface grid_grid_sessions_slots_talk {
  __typename: "Talk";
  id: string;
  title: string;
  isMine: boolean;
  isOpenDiscussion: boolean;
  speakers: grid_grid_sessions_slots_talk_speakers[];
}

export interface grid_grid_sessions_slots {
  __typename: "Slot";
  id: string;
  room: grid_grid_sessions_slots_room;
  talk: grid_grid_sessions_slots_talk | null;
}

export interface grid_grid_sessions {
  __typename: "Session";
  id: string;
  name: string;
  startTime: GraphqlDateTime;
  endTime: GraphqlDateTime;
  event: string | null;
  slots: grid_grid_sessions_slots[] | null;
}

export interface grid_grid {
  __typename: "Grid";
  sessions: grid_grid_sessions[];
}

export interface grid {
  grid: grid_grid;
}
