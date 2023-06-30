const dynamicInputLabel = (event, remove=false, className="has-value") => {
  /**
   * Method to add/remove certain class from input and its label
   * @param {Object} event The event object that emit by HTML element.
   * @param {Boolean} remove The boolean value to set remove variable which means the HTML element is blured, default false.
   * @param {String} className The string value that specify class name to add/remove from HTML element, default 'has-value'.
   */

  // Check if the element that trigger current event is 'input' tag or not.
  // if (event.srcElement.localName === 'input') {}

  // Get 'currentTarget' of event (Not 'target' because could child of element trigger this event).
  let ele = event.currentTarget;
  // Get 'id' attribute value from element.
  let id = ele.id;
  // Set 'for' attribute value of certain input element using its 'id'.
  let label = `label[for=${id}]`;
  // Select specific label element from DOM.
  let labelEle = document.querySelector(label);
  // in case 'remove' parameter is true, get input field value.
  let val = ele.value;

  // check length of 'val' if zero or less, if its empty remove the given class name.
  if (val.length <= 0) {
    // Check if 'remove' parameter is false, then add the given class name to input
    // and its label element.
    if (remove === false) {
      ele.className += labelEle.className += className;
    }
    else{
      ele.classList.remove(className);
      labelEle.classList.remove(className);
    }
  }
};

export {dynamicInputLabel}