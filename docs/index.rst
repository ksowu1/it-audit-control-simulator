IT Audit Control Simulator
==========================

A professional, configurable IT Audit & GRC simulation platform built by
**Komi Sowu**.

This project demonstrates hands-on capability in:

- IT General Controls (ITGC)
- Access Control & Segregation of Duties (SoD)
- Change Management
- Backup & Recovery Controls
- Risk scoring & audit reporting
- Interactive and web-based audit simulations

----

Live Demo Overview
------------------

The simulator can be run in **three modes**:

1. **Config-driven audit execution**
2. **Interactive scenario builder**
3. **Web-based audit dashboard (Flask)**

It produces structured audit results similar to real-world internal audit
workpapers.

----

Key Features
------------

- Modular audit control framework
- Configurable JSON datasets
- Interactive audit scenario engine
- Web interface for live demonstrations
- CSV & PDF audit report export
- Risk scoring with severity levels
- Designed to mirror real IT audit workflows

----

Project Screenshot
------------------

.. image:: _images/project1-run.png
   :alt: Web Audit Results Demo
   :align: center
   :width: 90%

----

Getting Started
---------------

Run a default audit scenario:

.. code-block:: bash

   python -m web.app --config config/default_scenario.json

Run with the web interface:

.. code-block:: bash

   python -m web.app --config config/default_scenario.json --serve

Then open:

http://127.0.0.1:5000/run

----

Documentation
-------------

.. toctree::
   :maxdepth: 2

   architecture
   controls
   usage
   troubleshooting

----

Author
------

**Komi Sowu**
IT Audit • GRC • Cybersecurity
CISA (Exam Passed)

GitHub:
https://github.com/ksowu1/it-audit-control-simulator
