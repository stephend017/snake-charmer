# snake_charmer
A github action for automating python package releases. 

### bUt gItHuB aLrEaDy hAs tHaT . . .

yes they automated 2 simple cli instructions that still requires a lot of effort on the developer to make sure that the current version in the main branch is correctly configured and to top it all off you as the developer have to understand and be able to keep up with versioning your releases correctly. to put it bluntly I can do better. 

### Project Goals
A github action where simply by tagging a PR with `major-release`, `minor-release`, or `revision-release` will correctly update your setup.py file, create a release via github (using commit history to build a changelog and the previous version defined to properly increment the version) and then publish it to PYPI. This way you only need to open a PR with your last feature for each version to create a release. 
