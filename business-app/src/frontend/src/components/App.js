import { Component } from 'react';
import '../styling/App.css';
import MainContent from './MainContent';
import TopNavbar from './TopNavbar';
import UserDataList from './UserDataList';

import AUTH_PORTAL_HOST from '../config';


class App extends Component {
  constructor(props) {
    super(props)
    this.clientId = process.env.REACT_APP_CLIENT_ID;
    this.secretKey = process.env.REACT_APP_SECRET_KEY;
    this.redirectUri = process.env.REACT_APP_REDIRECT_URI;
  
    this.timer = null;

    this.state = {
      accessToken: '',
      refreshToken: '',
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

  fetchToken(URL, data) {
    // custom fetch that will be used for getting accessToken or refreshToken.
    const headers = {
      "Cache-Control": "no-cache",
      "Content-Type": "application/x-www-form-urlencoded",
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
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
        timeLeft: data.expires_in
      })
      this.startTimer()
    })
  }

  getAccessToken(authCode) {
    // Func that fetch data from auth-portal to get access_token
    const URL = `http://${AUTH_PORTAL_HOST}/oauth/token/`

    const data = {
      client_id: this.clientId,
      client_secret: this.secretKey,
      redirect_uri: this.redirectUri,
      code: authCode,
      grant_type: "authorization_code",
    }
    
    this.fetchToken(URL, data)
  }

  getRefreshToken(){
    const URL = `http://${AUTH_PORTAL_HOST}/api/v1/token/refresh`
    
    const data = {
      token: this.accessToken,
      client_id: this.clientId,
      client_secret: this.secretKey
    }
    
    this.fetchToken(URL, data)
  }

  resetState() {
    this.setState({
      accessToken: '',
      refreshToken: '',
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

  checkCurrentState() {
    // Checks if there is the state in localstorage.
    let prevState = localStorage.getItem('prevState') ? localStorage.getItem('prevState') : null

    if (prevState)
      this.setState({...JSON.parse(prevState)})
  }

  componentDidUpdate() {
    // This func will store current state in the localstorage.
    // It is maden to track expired_in time for refresh token
    localStorage.setItem('prevState', JSON.stringify(this.state))
  }

  componentWillMount() {
    this.checkCurrentState()
  }

  componentDidMount() {

    let authCode = this.findGetParam('code')

    if (this.state.accessToken) {
      if (this.state.needRefresh) {
        this.getRefreshToken()
      }
      this.startTimer()
    } else {
      if (authCode) {
        this.getAccessToken(authCode)
      }
    }
  }
  
  render() {
    return (
      <div className="App">
        <TopNavbar accessToken={ this.state.accessToken } logoutHandler={this.logout}/>
        {this.state.accessToken ? <UserDataList accessToken={ this.state.accessToken } /> : <MainContent clientId={ this.clientId }/>}
      </div>
    );
  }
}

export default App;
