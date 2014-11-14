#!
#
# if script is called with:
#   no argument: stable version is installed 
#   devel: devel version with ssh 
#   any other argument: devel version with https is used
NARGS=$#
ARG1=$1

# echo "$ARG1"
# if [ "$ARG1" = "" ] ; then
#     echo "asdfa"
#     # stable version
# elif [ "$ARG1" = "devel" ] ; then
#     echo "Cloning unstable branch using ssh"
#         # if there is an any argument, install as developer
#         # apt-get install -y sshpass virtualbox
# else
#     echo "Cloning unstable branch using http"
# fi
# exit
HOMEDIR="`pwd`"
USER="$(echo `pwd` | sed 's|.*home/\([^/]*\).*|\1|')"

echo "installing for user:"
echo "$USER"

apt-get update
apt-get upgrade -y

# 1. deb package requirements
apt-get install -y python git python-dev g++ python-numpy python-scipy python-matplotlib python-sklearn python-skimage python-dicom cython python-yaml sox make python-qt4 python-vtk python-setuptools curl python-pip cmake

# 2. easy_install requirements simpleITK  
easy_install -U SimpleITK mahotas

# 3. pip install our packages pyseg_base and dicom2fem
sudo -u $USER pip install pysegbase dicom2fem sed3 io3d --user

sudo -u $USER mkdir ~/projects

# 4. install gco_python

sudo -u $USER mkdir ~/projects/gco_python
sudo -u $USER git clone https://github.com/mjirik/gco_python.git ~/projects/gco_python
cd $HOMEDIR
cd projects/gco_python
echo `pwd`
sudo -u $USER make
sudo -u $USER python setup.py install --user


# 5. skelet3d - optional for Histology Analyser
sudo apt-get install -y cmake python-numpy libinsighttoolkit3-dev libpng12-dev
# sudo -u $USER cd ~/projects
sudo -u $USER mkdir ~/projects/skelet3d
sudo -u $USER git clone https://github.com/mjirik/skelet3d.git ~/projects/skelet3d
sudo -u $USER mkdir ~/projects/skelet3d/build
cd $HOMEDIR
cd projects/skelet3d/build
sudo -u $USER cmake ..
sudo -u $USER make
sudo make install
# sudo -u $USER sh -c "cd ~/projects/skelet3d/build && cmake .. && make"
# sudo -u $USER mkdir build
# sudo -u $USER cd build

# Clone Lisa, make icons
cd ~/projects
if [ "$ARG1" = "" ] ; then
    echo "Cloning stable version"
    # stable version
    sudo -u $USER git clone --recursive -b stable https://github.com/mjirik/lisa.git
elif [ $ARG1 -eq "devel" ] ; then
    echo "Cloning unstable branch using ssh"
    # if there is an any argument, install as developer
    # apt-get install -y sshpass virtualbox
    sudo -u $USER git clone --recursive git@github.com:mjirik/lisa.git
else
    echo "Cloning unstable branch using http"
    sudo -u $USER git clone --recursive https://github.com/mjirik/lisa.git

fi
cd lisa
sudo -u $USER python mysetup.py -d
sudo -u $USER python mysetup.py -icn

cd $HOMEDIR
# python src/update_stable.py
# python lisa.py $@
