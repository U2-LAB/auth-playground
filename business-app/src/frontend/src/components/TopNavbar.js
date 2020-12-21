import React, { Component } from 'react'

export default class TopNavbar extends Component {
    render() {
        return (
            <nav className="navbar navbar-light bg-light">
                <span className="navbar-brand">Business App</span>
                { this.props.accessToken ? <button onClick={this.props.logoutHandler} className='btn btn-primary nav-item'>Logout</button> : ''}
            </nav>
        )
    }
}
