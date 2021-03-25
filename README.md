# snake_charmer
A github action for automating python package releases. 

### bUt gItHuB aLrEaDy hAs tHaT . . .

github has an action to publish to pypi. this still requires the developer know about good semantic versioning and keep the project in correct order to do so. This action runs before and actually works with the one provided by github so that releasing a new version is as simple as updating the labels on a pr.

### Project Goals
A github action where simply by tagging a PR with `major-release`, `minor-release`, or `revision-release` will correctly update your setup.py file, create a release via github (using commit history to build a changelog and the previous version defined to properly increment the version) and then publish it to PYPI. This way you only need to open a PR with your last feature for each version to create a release. 
