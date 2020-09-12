import React, { FunctionComponent, MouseEvent, useCallback, useRef } from "react";

const SpeakersControl: FunctionComponent<{
  speakers: string[];
  availableSpeakers: { id: string; name: string }[];
  onChange: (speakers: string[]) => void;
}> = ({ speakers, availableSpeakers, onChange }) => {
  const addSpeakerRef = useRef<HTMLSelectElement>(null);
  const addSpeaker = useCallback(
    (ev: MouseEvent<HTMLButtonElement>) => {
      ev.preventDefault();
      onChange([...speakers, addSpeakerRef.current!.value]);
    },
    [addSpeakerRef, speakers, onChange],
  );
  const removeSpeaker = useCallback(
    (ev: MouseEvent<HTMLButtonElement>) => {
      ev.preventDefault();
      onChange(speakers.filter((speaker) => speaker !== ev.currentTarget.value));
    },
    [speakers, onChange],
  );

  return (
    <div className="field">
      <label className="label" htmlFor="additional-speakers">
        Additional speakers
      </label>
      {speakers.map((speaker) => {
        const { name } = availableSpeakers.find(({ id }) => id === speaker) ?? { name: "Loading" };

        return (
          <div key={speaker} className="control">
            {name}{" "}
            <button
              className="delete"
              type="button"
              aria-label={`remove ${name}`}
              value={speaker}
              onClick={removeSpeaker}
            />
          </div>
        );
      })}
      <div className="field has-addons">
        <div className="control">
          <div className="select">
            <select id="additional-speakers" ref={addSpeakerRef}>
              {availableSpeakers
                .filter((speaker) => !speakers.includes(speaker.id))
                .map(({ id, name }) => (
                  <option key={id} value={id}>
                    {name}
                  </option>
                ))}
            </select>
          </div>
        </div>
        <div className="control">
          <button className="button" onClick={addSpeaker} type="button">
            Add additional speaker
          </button>
        </div>
      </div>
    </div>
  );
};

export default SpeakersControl;
