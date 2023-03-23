//Set default properties for axios model/library.

/*
axios using 'XMLHttpRequest', an API in the form of an object whose methods
transfer data between a web browser and a web server.
So there is a way to pass 'csrftoken' inside 'X-CSRFToken' header for each
unsafe HTTP request.
*/

// By using model loader 'require' load 'axios' model and set it to a constant.
const axios = require("axios");

/* Set a specific token name 'xsrfCookieName' with its value, in our case will
be 'csrftoken' which is a token provided when using session authentication and
required by Django when doing unsafe HTTP methods. */
axios.defaults.xsrfCookieName = "csrftoken";

// Set 'xsrfHeaderName', will use to pass 'xsrfCookieName' value.
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

// export the constant.
export {axios}