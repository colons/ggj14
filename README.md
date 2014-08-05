![A Conversation with Ymir][logo]

# A Conversation with Ymir

An [entry][ggj] in Global Game Jam 2014, by Very Scary Scenario (Chris Walden,
Alexander Rennerfelt, Nicholas Edwards and Iain Dawson). There's a
[trailer][trailer], too, if you need to be convinced.

You can play at [ggj14.colons.co][play].

## Setup

### Linux/OS X

If you don't have [virtualenvwrapper][venvw] installed, install it with `pip`
by firing up a terminal and running:

```bash
sudo pip install virtualenvwrapper
```

Create a virtualenv for ymir:

```bash
mkvirtualenv ymir
```

When the virtualenv is active, you should then be able to clone the project,
install the requirements and run it locally.

```bash
git clone https://github.com/colons/ggj14.git
cd ggj14
pip install -r requirements.txt
python manage.py syncdb
python manage.py runserver
```

### Windows

TODO (gotta find a windows box)

[logo]: https://github.com/colons/ggj14/raw/master/logo.gif
[trailer]: http://youtu.be/ED4oib6O02k
[ggj]: http://globalgamejam.org/2014/games/conversation-ymir
[play]: http://ggj14.colons.co
[venvw]: http://www.doughellmann.com/projects/virtualenvwrapper/
