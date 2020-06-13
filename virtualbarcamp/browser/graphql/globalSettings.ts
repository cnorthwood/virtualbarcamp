/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

import { EventState } from "./globalTypes";

// ====================================================
// GraphQL query operation: globalSettings
// ====================================================

export interface globalSettings_globalSettings {
  __typename: "GlobalSettings";
  eventState: EventState;
  doorsOpenTime: GraphqlDateTime | null;
  gridOpenTime: GraphqlDateTime | null;
}

export interface globalSettings {
  globalSettings: globalSettings_globalSettings;
}
