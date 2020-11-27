import React, { Component } from 'react'
import './Card.css';

export default class Card extends Component {
    constructor(props) {
        super(props);
        this.state = {
            id: props.user.id,
            firstName: props.user.first_name,
            lastName: props.user.last_name,
            phone: props.user.phone,
            email: props.user.email,
            skype: props.user.skype,
            login: props.user.username,
        }
    }
    
    render() {
        return (
            <div className="card-block">
                <div className="card-info">
                    <img className="avatar" src="https://blog.mystart.com/wp-content/uploads/shutterstock_224423782-e1524166038524.jpg" alt="avatar" width="70px" height="70px"/>
                    <div className="card-name">
                        <h3>#{this.state.id}</h3>
                        <h3>{this.state.firstName} {this.state.lastName}</h3>
                    </div>
                </div>
                <div className="card-data">
                    {(this.state.email.length > 0) ? <h4>Email: <a href={'mailto:' + (this.state.email)}>{this.state.email}</a></h4> : ''}
                    {(this.state.skype.length > 0) ? <h4>Skype: {this.state.skype}</h4> : ''}
                    {(this.state.phone.length > 0) ? <h4>Phone: <a href={'tel:'+ (this.state.phone)}>{this.state.phone}</a> </h4> : ''}
                    {(this.state.login.length > 0) ? <h4>Login: {this.state.login}</h4> : ''}
                </div>
            </div>
        )
    }
}
