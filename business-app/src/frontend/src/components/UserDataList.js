import React, {Component} from 'react';


export default class UserDataList extends Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const URL = 'http://localhost:8000/api/v1/user_data/'
        
        fetch(URL, {
            headers: {
                'Authorization': `Bearer ${this.props.auth_token}`,
            }
        })
        .then(resp => {
            console.log(resp);
            return resp.json()
        })
        .catch(errors => console.log(errors))
        .then(data => {
            console.log(data);
        })
    }

    render() {
        return (
            <div className='user-data'>
                <h2>User data</h2>      
            </div>
        )
    }
}