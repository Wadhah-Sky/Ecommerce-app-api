module.exports = {
  "presets": [
    "@vue/cli-plugin-babel/preset"
  ],
  "env": {
      "development" : {
        // to solve the warning of:
        // BABEL Note: The code generator has deoptimised the styling, it exceeds the max of 500KB.
        // Note: in 'production' will automatically set to be true.
        "compact": false
      }
    }
}