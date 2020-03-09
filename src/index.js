import "babel-polyfill";
import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { store, history } from "./store";
import { routes } from "./routes";
import { ConnectedRouter } from "connected-react-router";
import "./assets/styles/main.css";
import { ThemeProvider } from "styled-components";
import theme from "./assets/styles/theme";

// render the main component
ReactDOM.render(
  <Provider store={store}>
    <ThemeProvider theme={theme}>
      <ConnectedRouter history={history}>{routes}</ConnectedRouter>
    </ThemeProvider>
  </Provider>,
  document.getElementById("app")
);
