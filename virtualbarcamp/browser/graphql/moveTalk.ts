/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: moveTalk
// ====================================================

export interface moveTalk_moveTalk_talk_speakers {
  __typename: "Speaker";
  id: string;
  name: string;
}

export interface moveTalk_moveTalk_talk {
  __typename: "Talk";
  id: string;
  title: string;
  isMine: boolean;
  isOpenDiscussion: boolean;
  speakers: moveTalk_moveTalk_talk_speakers[];
}

export interface moveTalk_moveTalk {
  __typename: "Slot";
  id: string;
  talk: moveTalk_moveTalk_talk | null;
}

export interface moveTalk {
  moveTalk: moveTalk_moveTalk[];
}

export interface moveTalkVariables {
  talkId: string;
  oldSlot: string;
  newSlot: string;
}
