/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: addTalk
// ====================================================

export interface addTalk_addTalk_talk_speakers {
  __typename: "Speaker";
  id: string;
  name: string;
}

export interface addTalk_addTalk_talk {
  __typename: "Talk";
  id: string;
  title: string;
  isMine: boolean;
  isOpenDiscussion: boolean;
  speakers: addTalk_addTalk_talk_speakers[];
}

export interface addTalk_addTalk {
  __typename: "Slot";
  id: string;
  talk: addTalk_addTalk_talk | null;
}

export interface addTalk {
  addTalk: addTalk_addTalk;
}

export interface addTalkVariables {
  slotId: string;
  title: string;
  isOpenDiscussion: boolean;
  additionalSpeakers: string[];
}
