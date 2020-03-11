import React from 'react';
import { Route, Switch } from 'react-router-dom';
import App from './components/App';
import Home from './components/Home';
import SignupPage from './components/SignupPage';

const routes = (
  <App>
    <Switch>
      <Route exact path='/' component={Home} />
      <Route path='/sign-up' component={SignupPage} />
    </Switch>
  </App>
)

export { routes };