const whiteSpacesReplacer = (str, use='') => {
  /**
   * Replace all whitespace in the string you need by use global mode (search
   * through whole string).
   *
   * @param {String} str The string that contains white spaces
   * @param {string} use The special character to be use for replace white spaces in the string.
   */
  /*
     Info: use ? to handle error:
           Uncaught (in promise) TypeError: Cannot read properties of undefined (reading 'replace')

           That occurs own render time when the string is not rendered yet which means is null, so,
           it can't have function.
   */
  return str?.replace(/\s/g, use)
};

export {whiteSpacesReplacer}