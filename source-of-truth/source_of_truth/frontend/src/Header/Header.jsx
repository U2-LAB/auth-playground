import React, { Component } from 'react';
import './Header.css';

export default class Header extends Component {
    state = {
        'logotype' : 'Source of Truth',
    }
    

    render() {
        const log_out = () =>{
            fetch('http://127.0.0.1:8000/logout')
            .then(() => document.location.href = '/form');
        }
        return (
            <header id="header">
                <div id="logo-box">
                <h1 id="logotype">{ this.state.logotype }</h1>
                </div>
                <div id="logout-box">
                    <input type="button" value="Logout" onClick={log_out} id="logout_btn"/>
                </div>
            </header>
        )
    }
}
