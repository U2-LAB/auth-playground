import React, {Component} from 'react';
import AUTH_PORTAL_HOST from '../config';
import '../styling/userData.css';


export default class UserDataList extends Component {

    constructor(props) {
        super(props)
        this.state = {
            userData: []
        }
    }
    
    componentWillMount() {
        // Func that fetch user data from auth-portal using access_token
        const URL = `http://${AUTH_PORTAL_HOST}/api/v1/user_data/`
        
        fetch(URL, {
            headers: {
                'Authorization': `Bearer ${this.props.accessToken}`,
            }
        })
        .then(resp => {
            return resp.json()
        })
        .catch(errors => console.log(errors))
        .then(data => {
            this.setState({
                userData: data
            });
        })
    }
    
    render() {
        let products = Object.entries(this.state.userData).map(
            ([key, val]) => <li key={key}>{key} ----- {val}</li>
        )

        return (
            <div className='user-data'>
                <h2>User data</h2>
                <ul>
                    { products }
                </ul>
            </div>
        )
    }
}