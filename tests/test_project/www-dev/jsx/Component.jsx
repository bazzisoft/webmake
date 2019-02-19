
'use strict'

import React from 'react'
import Subcomponent from './Subcomponent.jsx'


export default class Component extends React.Component {
    render() {
        console.log('foobars')
        return (
          <div>
            <h3>React.js Component</h3>
            <Subcomponent name="foo"/>
          </div>
        )
    }
}
