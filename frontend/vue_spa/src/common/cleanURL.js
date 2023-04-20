const cleanUrlQuery = (registeredArray, queryObj) => {
  /**
   * Method to return clean frontend URL, by remove empty/unregistered keys from route query.
   *
   * @param {Array} registeredArray The array that contains the keys that your view is using as route query.
   * @param {Object} queryObj The route query object to examine and clean it from empty/unregistered keys.
   */

  // in Javascript, object parameter passed by value by its keys passed by reference, so it's better
  // to clone the obj that you will change its keys.
  const clonedObj = structuredClone(queryObj);

  // Loop over keys of clonedObj.
  for (let key of Object.keys(clonedObj)) {

    // Check if registeredObj including the current key or not, if not, delete this key from clonedObj.
    if (!((registeredArray).includes(key))) {
      delete clonedObj[key]
    }
    // In case registeredObj including the current key, check if current key's value is empty or undefined,
    // if that true, delete the current key from clonedObj.
    else if ( ['', undefined, null].includes(clonedObj[key]) ) {
        delete clonedObj[key];
    }
  }
  // Return the cleaned clonedObj.
  return clonedObj
};

export {cleanUrlQuery}