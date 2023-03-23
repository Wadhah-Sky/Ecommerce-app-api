const endpointSerializer = (endpoint, parameterArray, queryArray=null) => {
    /**
     * Method to return URL by using endpoint, array of parameter and query.
     *
     * @param {String} endpoint The string that end with backslash
     * @param {Array} parameterArray The array of string parameters
     * @param {Array} queryArray The array of string objects => [{<query_name> : <value>, value : <query_name_value>}, ]
     */

    /* You can use join() method to convert an array to string using seperator
       that the default value is comma (',').
     */
    let path = parameterArray.join('/');
    let fullPath = '';

    // In case the queryArray is not none or empty.
    if ((queryArray || []).length) {

        fullPath = endpoint + path + '/?';

        // loop over array of query using entries() method to get value of index:value
        for (let [index, val] of queryArray.entries()) {
            // In case the value of 'value' key is NOT undefined or empty.
            if ( !([null, undefined, ''].includes(val.value)) ) {
                if (index === queryArray.length - 1) {
                    // Means the current obj is the last in the loop.
                    fullPath += `${val.query}=${val.value}`;
                } else {
                    fullPath += `${val.query}=${val.value}&`;
                }
            }
        }
    }
    else {
       fullPath = endpoint + path
    }

    return fullPath
};

export {endpointSerializer}