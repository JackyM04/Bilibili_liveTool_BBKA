// routes/UsersRoutes.js
import React from 'react';
import { Route } from 'react-router-dom';
import Users from '../components/Users';
import UserProfile from '../components/UserProfile';

function UsersRoutes() {
  return (
    <div>
      <Route path="/users" exact component={Users} />
      <Route path="/users/:userId" component={UserProfile} />
    </div>
  );
}

export default UsersRoutes;
