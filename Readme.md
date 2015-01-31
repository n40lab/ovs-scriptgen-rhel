<snippet>	
# ovs-scriptgen-rhel.py

This simple script written in Python will generate network configuration 
scripts integrating Open vSwitch  for RHEL-based Linux distributions like 
CentOS. Note that the Open vSwitch integration is optional but is quite useful.

The script comes with a wizard that creates the content for a network script
that should be placed in the /etc/sysconfig/network-scripts directory.

The README.RHEL included with Open vSwitch explains how to use the optional
Open vSwitch integration with RHEL network configuration scripts identifying
all the attributes and values you can add to the scripts. This simple script
tries to help you to generate the content of those files answering some questions.

## Usage

Install git on your system: yum install git

Download ovs-scriptgen-rhel: git clone https://github.com/n40lab/ovs-scriptgen-rhel.git

Execute: python ovs-scriptgen-rhel.py

## Requirements

Open vSwitch 2.3.x Long-Term Support. Previous and later versions could also work 
but please beware, changes to RHEL integration have been modified from time to time.

You should need Python 2.x. The script has been tested with CentOS 7 and
Python 2.7.5.

## Credits

A big thank you to the Open vSwitch team!

## License
GNU General Public License version 3
http://www.gnu.org/copyleft/gpl.html	
</snippet>