
"use strict";

var $ = require('jquery');
var Cookie = require('jslib/Cookie');

/*
 * Load jQuery plugins
 */

window.jQuery = $;
require('bootstrap');

/*
 * Load fastclick for mobile responsiveness
 */

var attachFastClick = require('fastclick');
attachFastClick(document.body);
