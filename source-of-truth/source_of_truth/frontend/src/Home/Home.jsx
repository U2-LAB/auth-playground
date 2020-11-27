import React, { Component } from 'react'
import Header from '../Header'
import Content from '../Content'

import './Home.css'

export default class Home extends Component {
    render() {
        return (
            <div>
                <Header/>
                <Content/>
            </div>
        )
    }
}
