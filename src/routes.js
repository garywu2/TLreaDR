import React from 'react';
import { Route, Switch } from 'react-router-dom';
import App from './components/App';
import Home from './components/Home';
import SignupPage from './components/SignupPage';
import SignInPage from './components/SignInPage';

const routes = (
  <App>
    <Switch>
      <Route exact path='/' component={Home} />
      <Route path='/sign-up' component={SignupPage} />
      <Route path='/sign-in' component={SignInPage} />
    </Switch>
  </App>
)

export { routes };