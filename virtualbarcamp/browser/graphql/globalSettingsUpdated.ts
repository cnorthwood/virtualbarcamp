/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

import { EventState } from "./globalTypes";

// ====================================================
// GraphQL subscription operation: globalSettingsUpdated
// ====================================================

export interface globalSettingsUpdated_globalSettings {
  __typename: "GlobalSettings";
  eventState: EventState;
  doorsOpenTime: GraphqlDateTime | null;
  gridOpenTime: GraphqlDateTime | null;
}

export interface globalSettingsUpdated {
  globalSettings: globalSettingsUpdated_globalSettings;
}
