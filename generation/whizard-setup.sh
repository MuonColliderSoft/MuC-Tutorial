# $Id: whizard-setup.sh.in 1986 2010-03-04 16:34:20Z cnspeckn $
#
# source this file to set up environment variables for an
# installed WHIZARD in Bourne(-compatible) shells
#
########################################################################
#
# Copyright (C) 1999-2019 by 
#     Wolfgang Kilian <kilian@physik.uni-siegen.de>
#     Thorsten Ohl <ohl@physik.uni-wuerzburg.de>
#     Juergen Reuter <juergen.reuter@desy.de>
#     Christian Speckner <cnspeckn@googlemail.com>
#
# WHIZARD is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by 
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# WHIZARD is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
########################################################################


usage() {
cat <<EOI
usage: whizard-setup.sh [options]

Sets environment variables for running WHIZARD.
Default: installation paths as determined when configuring WHIZARD

Available options for custom paths:
   --prefix DIR    : directory containing the WHIZARD installation
   --bindir DIR    : directory containing the WHIZARD executables
   --libdir DIR    : directory containing the WHIZARD libraries
   -               : do not process further options
EOI
}

unset prefix
unset exec_prefix
unset bindir
unset libdir

while test -n "$1"; do
   case "$1" in
      "-")
         break
         ;;
      "--prefix")
	 if test -n "$2"; then
	     shift
	     prefix=$1
         else
             usage
	     return 1
         fi
         ;;
      "--exec_prefix")
	 if test -n "$2"; then
	     shift
	     exec_prefix=$1
         else
             usage
	     return 1
         fi
         ;;
      "--bindir")
	 if test -n "$2"; then
	     shift
	     bindir=$1
         else
             usage
	     return 1
         fi
         ;;
      "--libdir")
	 if test -n "$2"; then
	     shift
	     libdir=$1
         else
             usage
	     return 1
         fi
         ;;
      "--help")
         usage
	 return 0
         ;;
      *)
         usage
	 return 1
   esac
   shift
done

echo "Setting up paths for WHIZARD runtime environment"
if test -z "$prefix"; then
  prefix=/data/WHIZARD
fi
# echo "prefix=$prefix"
if test -z "$exec_prefix"; then
  exec_prefix=${prefix}
fi
# echo "exec_prefix=$exec_prefix"
if test -z "$bindir"; then
  bindir=${exec_prefix}/bin
fi
echo "bindir = $bindir"
if test -z "$libdir"; then
  libdir=${exec_prefix}/lib
fi
echo "libdir = $libdir"

if test "X${PATH}" = X; then
  PATH=${bindir}
else
  PATH=${bindir}:${PATH}
fi
export PATH

if test "X${LD_LIBRARY_PATH}" = X; then
  LD_LIBRARY_PATH=${libdir}
else
  LD_LIBRARY_PATH=${libdir}:${LD_LIBRARY_PATH}
fi
export LD_LIBRARY_PATH

