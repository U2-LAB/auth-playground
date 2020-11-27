import React, { Component } from 'react';
import './Form.css';
import axios from 'axios';

export default class Form extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username : '',
            password: '',
            permission: 'READ',
        }
        // document.location.href = '/home';
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        if (event.target.name === 'login')
            this.setState({username: event.target.value});
        else {
            this.setState({password: event.target.value});
        }
    }

    handleSubmit(event) {
        event.preventDefault();
        
        var data = new FormData();
        
        data.append("username", this.state.username);
        data.append("password", this.state.password);
        
        let url = 'http://127.0.0.1:8000/Auth';
        
        axios.post(url, data)
        .then(response => {
            console.log(response);
            localStorage.setItem('session',JSON.stringify(response.data));
        })
        .then(() => document.location.href = '/home');

        
    }
    

    render() {
        // let session = JSON.parse(localStorage.session);
        // let ExpireDate = Date.parse(session.ExpireDate);

        // if (ExpireDate >= Date.now()) {
            // document.location.href = '/home';
        // } else {
            return (
                <div className="App">
                <form onSubmit={this.handleSubmit}>
                    <div className='field login'>
                    <input type="text" name="login" id="login" required value={this.state.username} onChange={this.handleChange}/>
                    <label for="login">Login</label>
                    </div>    
                    <div className='field password'>
                    <input type="password" name="password" id="password" required value={this.state.password} onChange={this.handleChange}/>
                    <label for="password">Password</label>
                    </div>
                    <input type="submit" value="Submit" />
                </form>
                </div>
            )
        // }
        
    }
        
}
