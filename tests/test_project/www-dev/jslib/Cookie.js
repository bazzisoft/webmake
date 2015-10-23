/**
 * Provides functions to read, write and erase cookies.
 *
 * Dependencies: None.
 *
 */

"use strict";


var Cookie = {};


/**
 * Set a cookie.
 *
 * @param {string} name - Name of the cookie.
 * @param {string} value - Value of the cookie.
 * @param {int} expiryDays - In how many days the cookie should be erased.
 *      If not provided, creates a session cookie.
 */
Cookie.setCookie = function(name, value, expiryDays)
{
    var expires = '';

    if (expiryDays)
    {
        var date = new Date();
        date.setTime(date.getTime() + (expiryDays * 24 * 60 * 60 * 1000));
        expires = '; expires=' + date.toGMTString();
    }

    document.cookie = encodeURIComponent(name) + '=' + encodeURIComponent(value) + expires + '; path=/';
};


/**
 * Get a cookie.
 *
 * @param {string} name - Name of the cookie.
 */
Cookie.getCookie = function(name)
{
    var nameEQ = name + '=';
    var ca = document.cookie.split(';');

    for (var i = 0; i < ca.length; i++)
    {
        var c = ca[i];
        while (c.charAt(0) == ' ')
        {
            c = c.substring(1, c.length);
        }

        if (c.indexOf(nameEQ) == 0)
        {
            return c.substring(nameEQ.length, c.length);
        }
    }

    return null;
};


/**
 * Deletes a cookie, if it exists.
 *
 * @param {string} name - Name of the cookie.
 */
Cookie.clearCookie = function(name)
{
    Cookie.setCookie(name, '', -1);
};


//****************************
//* EXPORTS
//****************************

module.exports = Cookie;
