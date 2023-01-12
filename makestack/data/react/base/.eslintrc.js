module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint', 'react', 'prettier'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
    'plugin:react/recommended'
  ],
  settings: {
    react: {
      pragma: 'React',
      version: 'detect'
    }
  }
}
