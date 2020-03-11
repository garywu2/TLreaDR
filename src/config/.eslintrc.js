module.exports = {
  "env": {
    "browser": true,
    "commonjs": true,
    "es6": true,
    "jest": true,
    "node": true,
  },
  "extends": "eslint:recommended",
  "rules": {
    "indent": ["error", 2, { "SwitchCase": 1 }],
    "no-console": [ 0 ],
    "no-empty": [ 0 ],
    "no-undef": ["error", { "typeof": false }],
    "no-unused-vars": ["error", { "varsIgnorePattern": "React" }],
    "quotes": ["error", "double"],
    "react/jsx-uses-vars": [ 2 ],
  },
  "plugins": [
    "react",
  ],
  "parser": "babel-eslint",
  "parserOptions": {
    "ecmaFeatures": {
      "jsx": true,
      "modules": true,
    }
  }
};