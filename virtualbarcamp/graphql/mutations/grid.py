from graphene import ObjectType, Field, NonNull, ID, String, List, Boolean

from virtualbarcamp.graphql.queries.grid import SlotType, TalkType


class GridMutation(ObjectType):
    remove_talk = Field(NonNull(SlotType), slot_id=NonNull(ID))
    add_talk = Field(
        NonNull(SlotType),
        title=NonNull(String),
        additional_speakers=NonNull(List(NonNull(ID))),
        is_open_discussion=NonNull(Boolean),
    )
    update_talk = Field(
        NonNull(TalkType),
        talk_id=NonNull(ID),
        title=NonNull(String),
        additional_speakers=NonNull(List(NonNull(ID))),
        is_open_discussion=NonNull(Boolean),
    )
