import React, { Component } from 'react'

export default class WelcomeJumbatron extends Component {
    render() {
        return (
            <div className='jumbotron'>
                <h1 className='display-4'>Welcome to Business App</h1>
                <p className='lead'>It is created to test OAuth authentication</p>
                <p>To start working, please login or signup</p>
                <a className="btn btn-success btn-lg login-btn" href="#" role="button">Login</a>
                <a className="btn btn-primary btn-lg signup-btn" href="#" role="button">SignUp</a>
            </div>
        )
    }
}