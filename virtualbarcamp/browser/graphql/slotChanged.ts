/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL subscription operation: slotChanged
// ====================================================

export interface slotChanged_slotChanged_talk_speakers {
  __typename: "Speaker";
  id: string;
  name: string;
}

export interface slotChanged_slotChanged_talk {
  __typename: "Talk";
  id: string;
  title: string;
  isMine: boolean;
  isOpenDiscussion: boolean;
  speakers: slotChanged_slotChanged_talk_speakers[];
}

export interface slotChanged_slotChanged {
  __typename: "Slot";
  id: string;
  talk: slotChanged_slotChanged_talk | null;
}

export interface slotChanged {
  slotChanged: slotChanged_slotChanged;
}
