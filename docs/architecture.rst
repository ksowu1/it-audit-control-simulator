Architecture
============

Overview
--------

The project uses a modular architecture with isolated components:

- **config/** – YAML-based control definitions
- **controls/** – individual control logic
- **utils/** – shared helper functions
- **export/** – report generation
- **tests/** – automated unit tests

Control Engine
--------------

Each control inherits from a base control class and implements:

- input validation
- execution logic
- scoring logic

Main Entry Point
----------------

``main.py`` loads configuration files, initializes modules, and executes selected controls.
