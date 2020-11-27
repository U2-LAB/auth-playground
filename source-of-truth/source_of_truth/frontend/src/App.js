import './App.css';
import Form from './Form';
import Home from './Home';

import React, { Component } from 'react'
import { Route } from 'react-router-dom';

export default class App extends Component {

  render() {
    return (
      <div>
        <Route path='/form' component={Form}/>
        <Route path='/home' component={Home}/>
        {/* <Header /> */}
        {/* <Form /> */}
        {/* <Content /> */}
      </div>
    )
  }
}
