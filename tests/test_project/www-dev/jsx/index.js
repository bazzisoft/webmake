
'use strict'

import React from 'react'
import ReactDOM from 'react-dom'
import Component from './Component.jsx'


export default function renderReact(elementId)
{
    ReactDOM.render(
        <Component/>,
        document.getElementById(elementId))
}


module.exports = {
    renderReact: renderReact,
}
