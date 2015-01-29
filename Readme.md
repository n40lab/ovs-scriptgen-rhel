<snippet>
  <content><![CDATA[
# ${1:Project Name}

This simple script written in Python will generate network configuration 
scripts integrating Open vSwitch  for RHEL-based Linux distributions like 
CentOS. Note that the Open vSwitch integration is optional but is quite useful.

The script comes with a wizard that creates the content for a network script
that should be placed in the /etc/sysconfig/network-scripts directory.

The README.RHEL included with Open vSwitch explains how to use the optional
Open vSwitch integration with RHEL network configuration scripts identifying
all the attributes and values you can add to the scripts. This simple script
try to help you to generate the content of those files answering some questions.

## Usage

You should need Python 2.x and the script has been tested with CentOS 7 and
Python 2.7.5

## Credits

A big thank you to the Open vSwitch team!

## License
GNU General Public License version 3
http://www.gnu.org/copyleft/gpl.html

]]></content>
  <tabTrigger>readme</tabTrigger>
</snippet>