/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: removeTalk
// ====================================================

export interface removeTalk_removeTalk_talk_speakers {
  __typename: "Speaker";
  id: string;
  name: string;
}

export interface removeTalk_removeTalk_talk {
  __typename: "Talk";
  id: string;
  title: string;
  isMine: boolean;
  isOpenDiscussion: boolean;
  speakers: removeTalk_removeTalk_talk_speakers[];
}

export interface removeTalk_removeTalk {
  __typename: "Slot";
  id: string;
  talk: removeTalk_removeTalk_talk | null;
}

export interface removeTalk {
  removeTalk: removeTalk_removeTalk;
}

export interface removeTalkVariables {
  slotId: string;
}
