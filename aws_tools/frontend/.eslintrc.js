// https://eslint.org/docs/user-guide/configuring

module.exports = {
  root: true,

  parserOptions: {
    parser: 'babel-eslint'
  },

  env: {
    browser: true,
    node: true
  },

  // required to lint *.vue files
  plugins: ['vue'],

  // add your custom rules here
  rules: {
    'generator-star-spacing': 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off'
  },

  extends: [
    'plugin:vue/recommended',
    'standard',
    'plugin:vue/essential',
    '@vue/standard'
  ]
}
