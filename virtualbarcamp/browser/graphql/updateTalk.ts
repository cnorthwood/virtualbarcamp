/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: updateTalk
// ====================================================

export interface updateTalk_updateTalk_speakers {
  __typename: "Speaker";
  id: string;
  name: string;
}

export interface updateTalk_updateTalk {
  __typename: "Talk";
  id: string;
  title: string;
  isOpenDiscussion: boolean;
  speakers: updateTalk_updateTalk_speakers[];
}

export interface updateTalk {
  updateTalk: updateTalk_updateTalk;
}

export interface updateTalkVariables {
  talkId: string;
  title: string;
  isOpenDiscussion: boolean;
  additionalSpeakers: string[];
}
