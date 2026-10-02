# python-for-android-PySDL3-recipe
a recipe for p4a to install PySDL3

**NOTE: it is not completed yet, tested OK only on Android**

## Why this

PySDL3 is a pure python module, but it will collect the binaries and a part of API spec during the first import, this needs
internet permission and probably the binaries cannot work. This recipe can solve the problem, it builds the whole structure
during packaging and patches the API loading problem, so the module will be fully functional before the first run.
