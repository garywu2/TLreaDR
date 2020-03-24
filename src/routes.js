import React from "react";
import { Route, Switch } from "react-router-dom";
import App from "./components/App";
import Home from "./components/Home";
import SignupPage from "./components/SignupPage";
import SignInPage from "./components/SignInPage";
import CategoryPage from "./components/CategoryPage";
import NewPostPage from "./components/NewPostPage";
import PostPage from "./components/PostPage";

const routes = (
  <App>
    <Switch>
      <Route exact path="/" component={Home} />
      <Route path="/sign-up" component={SignupPage} />
      <Route path="/sign-in" component={SignInPage} />
      <Route path="/category/:category" component={CategoryPage} />
      <Route path="/post/:post" component={PostPage} />
      <Route path="/new" component={NewPostPage} />
    </Switch>
  </App>
);

export { routes };
