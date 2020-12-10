import { Component } from 'react';
import '../styling/App.css';
import MainContent from './MainContent';
import TopNavbar from './TopNavbar';
import UserDataList from './UserDataList';


class App extends Component {
  constructor(props) {
    super(props)
    this.client_id = 'TWb3uMSJrHY9CwXqRDbFGzU1QufpBLGQ6BuCaPQM';
    this.secret_key = 'AfD4CRm0SGcQJI4hxL1nfDcgPZhlONtXbgGoBu2ZHcnBOIsaYvKQ2Sbbi8UwuiamJmJ3GCpnm3tOgsGsDcYk2fnKmSljRlG1VWEogL7bY6EHLPHHgSccjQNvRd3upG4y';
    this.redirect_uri = 'http://localhost:3000/';
    
    this.timer = null;

    this.state = {
      access_token: '',
      refresh_token: '',
      needRefresh: false,
      timeLeft: 0
    }
  }

  findGetParam(paramName) {
    // General function that find the value of the GET query param
    let res = null
    document.location.search.substr(1).split('&').forEach(item => {
        let tmpVal = item.split('=');
        if (tmpVal[0] === paramName)
            res = decodeURIComponent(tmpVal[1])
    });

    return res
  }

  formEncodedBody(data) {
    // Func that encode data for body, that will be used in fetching of access_token
    let body = [];
    for (let property in data) {
      let encodedKey = encodeURIComponent(property);
      let encodedValue = encodeURIComponent(data[property]);
      body.push(encodedKey + "=" + encodedValue);
    }
    body = body.join("&");
    return body
  }

  getAccessToken(auth_code) {
    // Func that fetch data from auth-portal to get access_token
    const URL = 'http://localhost:8000/oauth/token/'
    const headers = {
      "Cache-Control": "no-cache",
      "Content-Type": "application/x-www-form-urlencoded"
    }

    const data = {
      client_id: this.client_id,
      client_secret: this.secret_key,
      redirect_uri: this.redirect_uri,
      code: auth_code,
      grant_type: "authorization_code",
    }
    
    let body = this.formEncodedBody(data)

    fetch(URL, {
      method: 'POST',
      headers: headers, 
      body: body
    })
    .then(resp => {
      return resp.json()
    })
    .catch(errors => console.log(errors))
    .then(data => {
      this.setState({
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        timeLeft: data.expires_in
      })
      this.startTimer()
    })
  }

  getRefreshToken(){}

  resetState() {
    this.setState({
      access_token: '',
      refresh_token: '',
      needRefresh: false,
      timeLeft: 0
    })
  }

  logout = () => {
    // Func that will be passed to our User detail compontent to give the ability to logout from the site
    clearInterval(this.timer)
    this.resetState()
  }

  startTimer(){
    // This func will set the timer that will track expired_in time for refresh token.
    // Timer is invoked when we get our access_token
    this.timer = setInterval(() => {
      this.setState({
        timeLeft: this.state.timeLeft - 1
      })

      if (this.state.timeLeft <= 0) {
        this.setState({
          needRefresh: true
        })
        clearInterval(this.timer)
      }
    }, 1000)
  }

  componentDidUpdate() {
    // This func will store current state in the localstorage.
    // It is maden to track expired_in time for refresh token
    localStorage.setItem('prevState', JSON.stringify(this.state))
  }

  componentWillMount() {
    // This func will try to fetch the previous state from localstorage.
    let prevState = localStorage.getItem('prevState') ? localStorage.getItem('prevState') : null 

    if (prevState)
      this.state = JSON.parse(prevState)
  }

  componentDidMount() {
    let auth_code = this.findGetParam('code')

    if (this.state.access_token) {
      if (this.state.needRefresh) {
        //refresh
      }
      this.startTimer()
    } else {
      if (auth_code) {
        this.getAccessToken(auth_code)
      }
    }
  }
  
  render() {
    return (
      <div className="App">
        <TopNavbar access_token={ this.state.access_token } logoutHandler={this.logout}/>
        {this.state.access_token ? <UserDataList access_token={ this.state.access_token } /> : <MainContent client_id={ this.client_id }/>}
      </div>
    );
  }
}

export default App;
