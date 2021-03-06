import React from 'react';
import { Route, Switch } from 'react-router-dom';
import App from './components/App';
import Home from './components/Home';
import SignupPage from './components/SignupPage';
import SignInPage from './components/SignInPage';
import CategoryPage from './components/CategoryPage';
import SearchResultsPage from './components/SearchResultsPage';
import NewPostPage from "./components/NewPostPage";
import ProfilePage from "./components/ProfilePage";
import PostPage from "./components/PostPage";
import EditProfilePage from "./components/EditProfilePage";
import EditPostPage from "./components/EditPostPage";
import ManageCategoryPage from './components/ManageCategoryPage';

const routes = (
  <App>
    <Switch>
      <Route exact path="/" component={Home} />
      <Route path="/sign-up" component={SignupPage} />
      <Route path="/sign-in" component={SignInPage} />
      <Route path="/category/:category" component={CategoryPage} />
      <Route path="/post/:post/edit" component={EditPostPage} />
      <Route path="/post/:post" component={PostPage} />
      <Route path='/search/:input' component={SearchResultsPage} />
      <Route path="/new" component={NewPostPage} />
      <Route path="/user/edit/:uuid" component={EditProfilePage} />
      <Route path="/user/:uuid" component={ProfilePage} />
      <Route path="/category-edit" component={ManageCategoryPage} />
    </Switch>
  </App>
);

export { routes };
