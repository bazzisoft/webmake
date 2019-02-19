'use strict'

import React from 'react'


export default class Subcomponent extends React.Component {
    render() {
        return (
          <div>
            <p>Subcomponent &ndash; name={this.props.name}</p>
          </div>
        )
    }
}
