import React, { FunctionComponent, useEffect, useState } from "react";
import formatDistanceStrict from "date-fns/formatDistanceStrict";
import parseISO from "date-fns/parseISO";

const distance = (end: Date) => formatDistanceStrict(end, new Date());

const Countdown: FunctionComponent<{ end: string }> = ({ end }) => {
  const target = parseISO(end);
  const [timeRemaining, setTimeRemaining] = useState<string>(distance(target));
  useEffect(() => {
    const intervalId = setInterval(() => {
      setTimeRemaining(distance(target));
    }, 1000);

    return () => clearInterval(intervalId);
  }, [target]);

  return <>{timeRemaining}</>;
};

export default Countdown;
