const querySerializer = (obj, queryObj, unwantedDataArray) => {
  /**
   * Method to return clean frontend URL, by remove empty/unregistered keys from route query.
   *
   * @param {Object} obj The object that contains the keys that your view is using as route query.
   * @param {Object} queryObj The route query object to examine and add/clean it.
   * @param {Array} unwantedDataArray The array that obj keys should not be included in.
   */

  // in Javascript, object parameter passed by value by its keys passed by reference, so it's better
  // to clone the obj that you will change its keys.
  const clonedObj =  structuredClone(obj);
  const clonedQueryObj = structuredClone(queryObj);

  // Loop over the obj.
  for (let key of Object.keys(clonedObj)){
      // Check current key value of clonedObj is NOT included in 'unwantedDataArray'.
      if ( !(unwantedDataArray.includes(clonedObj[key])) ){
        clonedQueryObj[key] = clonedObj[key];
      }
      // In case current key value of clonedObj is included in 'unwantedDataArray'.
      else if(clonedQueryObj[key]){
          // Remove the key from clonedQueryObj.
          delete clonedQueryObj[key];
      }
    }

  // Return the cleaned clonedQueryObj.
  return clonedQueryObj
};

export {querySerializer}