import React, {Component} from 'react';


export default class UserDataList extends Component {

    constructor(props) {
        super(props)
        this.state = {
            userData: null
        }
    }
    
    componentWillMount() {
        // Func that fetch user data from auth-portal using access_token
        const URL = 'http://localhost:8000/api/v1/user_data/'
        
        fetch(URL, {
            headers: {
                'Authorization': `Bearer ${this.props.access_token}`,
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
        let products = []
        for (let item in this.state.userData) {
            products.push(
                <li key={item}>{item} ----- {this.state.userData[item]}</li>
            )
        }

        return (
            <div className='user-data'>
                <h2>User data</h2>
                <ul>
                    {products}
                </ul>
            </div>
        )
    }
}