//!function(){"use strict";var a=window.location,o=window.document,t=o.currentScript,r="https://plausible.io/api/event",l="funhtml5games.com";function s(t,e){t&&console.warn("Ignoring Event: "+t),e&&e.callback&&e.callback()}function e(t,e){if(/^localhost$|^127(\.[0-9]+){0,2}\.[0-9]+$|^\[::1?\]$/.test(a.hostname)||"file:"===a.protocol)return s("localhost",e);if((window._phantom||window.__nightmare||window.navigator.webdriver||window.Cypress)&&!window.__plausible)return s(null,e);try{if("true"===window.localStorage.plausible_ignore)return s("localStorage flag",e)}catch(t){}var n={},i=(n.n=t,n.u=a.href,n.d=l,n.r=o.referrer||null,e&&e.meta&&(n.m=JSON.stringify(e.meta)),e&&e.props&&(n.p=e.props),new XMLHttpRequest);i.open("POST",r,!0),i.setRequestHeader("Content-Type","text/plain"),i.send(JSON.stringify(n)),i.onreadystatechange=function(){4===i.readyState&&e&&e.callback&&e.callback({status:i.status})}}var n=window.plausible&&window.plausible.q||[];window.plausible=e;for(var i,p=0;p<n.length;p++)e.apply(this,n[p]);function c(){i!==a.pathname&&(i=a.pathname,e("pageview"))}function u(){c()}var w,t=window.history;t.pushState&&(w=t.pushState,t.pushState=function(){w.apply(this,arguments),u()},window.addEventListener("popstate",u)),"prerender"===o.visibilityState?o.addEventListener("visibilitychange",function(){i||"visible"!==o.visibilityState||c()}):c()}();

!function(){"use strict";var i=window.location,r=window.document,t=r.currentScript,o="https://plausible.io/api/event",l="funhtml5games.com";function s(t,e){t&&console.warn("Ignoring Event: "+t),e&&e.callback&&e.callback()}function e(t,e){if (window.top !== window.self) {
  try {
    if (window.top.location.hostname === window.location.hostname) {
      return s("Same site iframe", e);
    }
  } catch (err) {
  }
}if(/^localhost$|^127(\.[0-9]+){0,2}\.[0-9]+$|^\[::1?\]$/.test(i.hostname)||"file:"===i.protocol)return s("localhost",e);if((window._phantom||window.__nightmare||window.navigator.webdriver||window.Cypress)&&!window.__plausible)return s(null,e);try{if("true"===window.localStorage.plausible_ignore)return s("localStorage flag",e)}catch(t){}var n={},t=(n.n=t,e&&e.u),a=(n.u=t||i.href,n.d=l,n.r=r.referrer||null,e&&e.meta&&(n.m=JSON.stringify(e.meta)),e&&e.props&&(n.p=e.props),new XMLHttpRequest);a.open("POST",o,!0),a.setRequestHeader("Content-Type","text/plain"),a.send(JSON.stringify(n)),a.onreadystatechange=function(){4===a.readyState&&e&&e.callback&&e.callback({status:a.status})}}var n=window.plausible&&window.plausible.q||[];window.plausible=e;for(var a=0;a<n.length;a++)e.apply(this,n[a])}();

window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) }

function prepareUrl(params) {
    const url = new URL(location.href)
    const queryParams = new URLSearchParams(location.search)
    let customUrl = url.protocol + "//" + url.hostname + url.pathname.replace(/\/$/, '')
    for (const paramName of params) {
      const paramValue = queryParams.get(paramName)
      if (paramValue) customUrl = customUrl + '/' + paramValue
    }
    return customUrl
  }
  
plausible('pageview', { u: prepareUrl(["play", "embed"]) + window.location.search })

