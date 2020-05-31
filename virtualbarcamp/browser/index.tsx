import React from "react";
import ReactDOM from "react-dom";

import App from "./App";

import "./styles.scss";

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root"),
);

// @ts-ignore
if (module.hot) {
  // @ts-ignore
  module.hot.accept("./App", () => {
    const NewApp = require("./App").default;

    ReactDOM.render(<NewApp />, document.getElementById("root"));
  });
}
