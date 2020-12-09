import { Component } from 'react';
import '../styling/App.css';
import MainContent from './MainContent';
import TopNavbar from './TopNavbar';
import UserDataList from './UserDataList';


class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      client_id: 'QQXiO3hlQqcbem2FxJuiiw25VSccHotvQEYMdBh3',
      secret_key: 'XjFwDET0thNoVVUenb4Q1OBsw54u2ZQ1Q9ljWNqApwfNseMxie1jBQCxmdV8hjrQ6eO4u3lQNzpF2qnwoyaU1BKo21d6GCVD8MWMKX4ow0dA96j7w9biBzwHx80oFmZE'
    }
  }

  findGetParam(paramName) {
    let res = null
    document.location.search.substr(1).
    split('&').forEach(item => {
        let tmpVal = item.split('=');
        if (tmpVal[0] === paramName)
            res = decodeURIComponent(tmpVal[1])
    });

    return res
  }

  componentDidMount() {
    let auth_token = this.findGetParam('code')
    this.setState({
      auth_token: auth_token
    })
  }
  
  render() {
    return (
      <div className="App">
        <TopNavbar />
        {this.state.auth_token ? <UserDataList auth_token={ this.state.auth_token }/> : <MainContent client_id={ this.state.client_id }/>}
      </div>
    );
  }
}

export default App;
