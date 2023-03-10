# Django based Webapp for PID Control Tuning

A responsive website for PID controllers tuning using modern tuning techniques, fractional calculus and opensource software to run identiication routines for raw process data.
This project goal is to allow most of the mobile devices to approach controller parametes even with their default hardware limitations switching the computation load to the cloud,
this makes low stats computers able to display good aproximations and simulations anywhere they are needed.

The project includes the features below.
- Raw process data fractional order modeling by IDFOM identification rule (Guevara et al. 2015)
- Tune rule for PI/PID controller 0dol through FOMRoT method (Meneses et al. 2019)
- Close-loop simulations and ploting on Plotly library for Python

<!-- GETTING STARTED -->
## Getting Started
Follow the next instructions about how to setting up the project locally for development and testing.

### Prerequisites

Install the software below to get the project running properly.
* virtualenv
   ```bash
   # For Archlinux, EndevourOS >
   pacman -S python-virtualenv

   # For Ubuntu, Debian, Mint
   apt install python3-virtualenv
   ```
* npm
  ```bash
   # For Archlinux, EndevourOS >
   pacman -S npm

   # For Ubuntu, Debian, Mint
   apt install npm

  ```
* pip
  ```bash
   # For Archlinux, EndevourOS >
   pacman -S python-pip

   # For Ubuntu, Debian, Mint
   apt install python3-pip

  ```

### Installation

1. Clone the repository.
   ```bash
   git clone https://github.com/jeancahu/PID_synthesis_tool.git
   ```
2. Go to test directory, install the virtualenv and project dependencies.
   ```bash
   cd test/server_demo              # Relative to the cloned repository
   virtualenv venv                  # Install the virtualenv once
   source venv/bin/activate

   pip install -r requirements.txt  # Install the Django Framework and its dependencies
   ```
3. Install _pidtune_ dependency as developer.
   ```bash
   # TODO
    ```

<!-- USAGE -->
## Usage

1. Go to test directory, activate the virtualenv and run the developer server
   ```bash
   cd test/server_demo        # Relative to the cloned repository
   source venv/bin/activate

   ./manage.py runserver
   ```
Open the [Local site](http://127.0.0.1:8000/) on your preferred browser.


<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE.txt` for more information.


<!-- CONTACT -->
## Contact

[Jean Hidalgo](https://caroje.com/static/jeancahu/) - jeancahu@gmail.com

Jose Mario -

Project Repository: [https://github.com/jeancahu/PID_synthesis_tool](https://github.com/jeancahu/PID_synthesis_tool)
