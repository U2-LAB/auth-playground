import React, { Component } from 'react'
import WelcomeJumbatron from './WelcomeJumbatron'

export default class MainContent extends Component {
    render() {
        return (
            <div className='main-content'>
                <WelcomeJumbatron clientId={ this.props.clientId }/>
            </div>
        )
    }
}
