import React, { Component } from 'react'
import './Content.css';
import Card from '../Card';
 


const API = 'http://127.0.0.1:8000/GetAllPerson';


class Content extends Component {
    constructor(props) {
        super(props);
        this.state = {
            ErrorCode : '',
            Permission: '',
            Users: [],
            loading: false,
        }
    }

    componentDidMount() {
        console.log("fetch");
        fetch(API)
        .then(response=>response.json())
        .then(json => {
            this.setState({
                ErrorCode: json.ErrorCode,
                Permission: json.Permission,
                Users: json.Users,
                loading: true
            })
        })
    };

    render() {
        console.log("render");
        const { ErrorCode, Permission, Users, loading } = this.state;
        // let ErrorCode = ''
        // let loading = true;
        // let data = {
        //     Users :[
        //         {
        //             "id": 4023,
        //             "first_name": "Admin",
        //             "last_name": "Admin",
        //             "username": "admin",
        //             "email": "admin@mail.ru",
        //             "skype": "live:skype.ru",
        //             "phone": "+3754545454545"
        //         },
        //         {
        //             "id": 4026,
        //             "first_name": "Admin",
        //             "last_name": "Admin",
        //             "username": "admin",
        //             "email": "",
        //             "skype": "live:skype.ru",
        //             "phone": "+3754545454545"
        //         },
        //         {
        //             "id": 4025,
        //             "first_name": "Admin",
        //             "last_name": "Admin",
        //             "username": "admin",
        //             "email": "admin@mail.ru",
        //             "skype": "live:skype.ru",
        //             "phone": "+3754545454545"
        //         }
        //     ]
        // }
        
        if (loading)
            return (
                <div className="App">
                    <h1>List of Users</h1>
                    {(ErrorCode === '') ?
                        <div className='grid-container'>
                            {
                                Users.map( user =>
                                    <Card user={user} />
                                    // <tr>
                                    //     <td>{user.id}</td>
                                    //     <td>{user.first_name}</td>
                                    //     <td>{user.last_name}</td>
                                    //     <td>{user.phone}</td>
                                    //     <td>{user.email}</td>
                                    //     <td>{user.skype}</td>
                                    //     <td>{user.username}</td>
                                    // </tr>

                                )
                            }
                        </div>
                    : 
                        <div>
                            <h2 id="ErrorCode">Session Expired</h2>
                            <a href="/form">Login</a>
                        </div>
                    }
                
                </div>
            );
        else 
            return <div className=""><h1>Loading...</h1></div>
      }
}
export default Content
