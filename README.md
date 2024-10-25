# phl-portal

This repository hosts the Passive Haptic Learning (PHL) web portal, which allows users to upload and access musical scores in a MusicXML format. Then, the users can upload MIDI recordings of their performance or upload lessons to a wearable PHL glove for musical education. If using this in your own research, please cite the original paper: 

Tan Gemicioglu, Elijah Hopper, Brahmi Dwivedi, Richa Kulkarni, Asha Bhandarkar, Priyanka Rajan, Nathan Eng, Adithya Ramanujam, Charles Ramey, Scott M. Gilliland, Celeste Mason, Caitlyn Seim, and Thad Starner. 2024. Passive Haptic Rehearsal for Augmented Piano Learning in the Wild. Proc. ACM Interact. Mob. Wearable Ubiquitous Technol. 8, 4, Article 187 (December 2024), 26 pages. https://doi.org/10.1145/3699748

# Installation Guide
If you are a developer working on the research project, you can set up a development enviroment as follows:

First, clone the git repository onto your local device:

    git clone https://github.com/tangemicioglu/phl-portal.git

### Backend
The backend of this project is written in Python and utilizes Flask. 

First, naviagte into the backend folder of the project:

    cd web-app/backend

Next, ensure that you have python 3 or later installed. Your current python version can be checked with the --version tag.

    python3 --version

Note: for some devices python3 may be accessed through just the "python" command. Just make sure you're using python3. 
Next, you will want to create and run a virtual environment:

    python3 -m venv venv
    source venv/bin/activate

Once you have entered your virtual environment (you should see a "venv" tag in your commad line prompt), you should to install the project dependencies listed in requirements.txt using pip:

    pip install -r requirements.txt

This might take a while, but once it's done you have everything you need to run the backend! You can do so with the flask run command:

    flask run
    
Your server should now be up and running. For the time being, the easiest way to check if it's working (without running the frontend)is to navigate to localhost:5000/scores in your web browser. You should get an Error: Unauthorized message. 


### Frontend 
The frontend for this project is written in Javascript and utilizes Vue 2.6 (along with Vuex & Vue Router). Getting it up and running is fairly straightforward.

Upon cloning the repository, navigate to the frontend directory: 

    cd web-app/frontend

Project dependencies will be install using the yarn package manager. You probably already have yarn installed, but if not you can install it globally with npm:

    npm install --global yarn

Next, install the project dependencies: 

    yarn install

The development can now be started up with the yarn serve command:

    yarn serve

The frontend will now be running on localhost:8080. if your server is also running, the app should work properly now!

# Important Dependencies
 - music21 (and music21j)
 - vue-bootstrap


