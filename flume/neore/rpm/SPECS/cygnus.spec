# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
# 
# This file is part of fiware-connectors (FI-WARE project).
# 
# cosmos-injector is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
# cosmos-injector is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
# 
# You should have received a copy of the GNU Affero General Public License along with fiware-connectors. If not, see
# http://www.gnu.org/licenses/.
# 
# For those usages not covered by the GNU Affero General Public License please contact with iot_support at tid dot es

Summary:          Package for cygnus component
Name:             cygnus
Version:          %{_product_version}
Release:          %{_product_release}
License:          AGPLv3
BuildRoot:        %{_topdir}/BUILDROOT/
BuildArch:        x86_64
Requires(post):   /sbin/chkconfig, /usr/sbin/useradd
Requires(preun):  /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
Group:            Applications/cygnus
Vendor:           Telefonica I+D

%description
This connector is a (conceptual) derivative work of ngsi2cosmos, and implements
a Flume-based connector for context data coming from Orion Context Broker.

# Project information 
%define _project_name cygnus
%define _project_user cygnus
%define _service_name cygnus

# System folders
# _sourcedir =${topdir}/SOURCES
%define _srcdir %{_sourcedir}/../../../
%define _install_dir /usr
%define _project_install_dir %{_install_dir}/%{_project_name}

# _localstatedir is a system var that goes to /var
 %define _log_dir %{_localstatedir}/log/%{_project_name}

# RPM Building folder
%define _build_root_project %{buildroot}%{_project_install_dir}

# -------------------------------------------------------------------------------------------- #
# prep section, setup macro:
# -------------------------------------------------------------------------------------------- #
%prep
# read from SOURCES, write into BUILD

echo "[INFO] Preparing installation"
# Create rpm/BUILDROOT folder
rm -Rf $RPM_BUILD_ROOT && mkdir -p $RPM_BUILD_ROOT
[ -d %{_build_root_project} ] || mkdir -p %{_build_root_project}

# Copy all from src to rpm/BUILD
cp -R  %{_srcdir}/src \
       %{_srcdir}/pom.xml \
       %{_srcdir}/README.md \
       %{_builddir}

# Copy "extra files" from rpm/SOURCES to rpm/BUILDROOT
cp -R %{_sourcedir}/* %{_builddir}

# -------------------------------------------------------------------------------------------- #
# Build section:
# -------------------------------------------------------------------------------------------- #
%build
# Read from BUILD, write into BUILD

echo "[INFO] Building..."

# -------------------------------------------------------------------------------------------- #
# pre-install section:
# -------------------------------------------------------------------------------------------- #
%pre
# Read from BUILD, write into BUILDROOT

echo "[INFO] Creating %{_project_user} user"
getent group  %{_project_user} >/dev/null || groupadd -r %{_project_user}
getent passwd %{_project_user} >/dev/null || useradd -r -g %{_project_user} -m -s /bin/bash -c 'Cygnus user account' %{_project_user}

# -------------------------------------------------------------------------------------------- #
# Install section:
# -------------------------------------------------------------------------------------------- #
%install
# Read from BUILD and write into BUILDROOT
# RPM_BUILD_ROOT = BUILDROOT

echo "[INFO] Installing the %{name}"

echo "[INFO] Creating the directories"
mkdir -p %{_build_root_project}/init.d
# Create folder to store the PID (used by the Service)
mkdir -p %{buildroot}/var/run/%{_project_name}
# Create log folder
mkdir -p %{buildroot}/${_log_dir}
# Create /etc/cron.d directory
mkdir -p %{buildroot}/etc/cron.d
# Create /etc/logrotate.d directory
mkdir -p %{buildroot}/etc/logrotate.d

cp -R %{_builddir}/usr/cygnus/*                       %{_build_root_project}
cp %{_builddir}/init.d/%{_service_name}               %{_build_root_project}/init.d/%{_service_name}
cp %{_builddir}/config/*                              %{_build_root_project}/conf/
cp %{_builddir}/cron.d/cleanup_old_cygnus_logfiles    %{buildroot}/etc/cron.d
cp %{_builddir}/logrotate.d/logrotate-cygnus-daily    %{buildroot}/etc/logrotate.d

# -------------------------------------------------------------------------------------------- #
# post-install section:
# -------------------------------------------------------------------------------------------- #
%post

echo "[INFO] Configuring application"
mkdir -p /etc/%{_project_name}
echo "[INFO] Creating links"
ln -s %{_project_install_dir}/init.d/%{_service_name} /etc/init.d/%{_service_name}
ln -s %{_project_install_dir}/conf/flume.conf /etc/%{_project_name}/flume.conf
ln -s %{_project_install_dir}/bin/flume-ng /usr/bin/flume-ng

#Logs
echo "[INFO] Creating log directory"
mkdir -p %{_log_dir}
chown %{_project_user}:%{_project_user} %{_log_dir}
chmod g+s %{_log_dir}
setfacl -d -m g::rwx %{_log_dir}
setfacl -d -m o::rx %{_log_dir}

echo "[INFO] Configuring application service"
# FIXME! Not supported
# chkconfig --add %{_service_name}
echo "Done"

# -------------------------------------------------------------------------------------------- #
# pre-uninstall section:
# -------------------------------------------------------------------------------------------- #
%preun

echo "[INFO] Uninstall the %{_project_name}"
/etc/init.d/%{_service_name} stop
/sbin/chkconfig --del %{_service_name}

echo "[INFO] Deleting links"
rm /etc/init.d/%{_service_name} \
/etc/%{_project_name}/flume.conf \
/usr/bin/flume-ng

echo "[INFO] Removing application log files"
[ -d %{_log_dir} ] && rm -rfv %{_log_dir} &> /dev/null

echo "[INFO] Deleting the %{_project_name} folder"
[ -d %{_project_install_dir} ] && rm -rfv %{_project_install_dir} &> /dev/null

echo "[INFO] Deleting the %{_project_user} user"
sudo userdel %{_project_user}

echo "Done"

# -------------------------------------------------------------------------------------------- #
# post-uninstall section:
# clean section:
# -------------------------------------------------------------------------------------------- #
%postun
%clean
rm -rf $RPM_BUILD_ROOT


# -------------------------------------------------------------------------------------------- #
# Files to add to the RPM
# -------------------------------------------------------------------------------------------- #
%files
%defattr(755,%{_project_user},%{_project_user},755)
%attr(0644, root, root) /etc/cron.d/cleanup_old_cygnus_logfiles
%attr(0644, root, root) /etc/logrotate.d/logrotate-cygnus-daily

%{_project_install_dir}
/var/run/%{_project_name}

%changelog
* Tue Nov 11 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.4.2
- Enable https connections in CKAN (#230)
- Bug fixing: solve a conflict with Monit when running Cygnus as a service (#214)
- Bug fixing: delete the "cygnus" user when removing the Cygnus RPM (#213)
- Bug fixing: fix the events TTL parameter in the configuration template (#210)
- Bug fixing: errors when using '.' in CKAN organization names (#200)
- Bug fixing: process notifications with no contextAttributeList (#194)

* Sun Oct 19 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.5.1
- Bug fixing: typo in the configuration template (#238)
- Bug fixing: wrong path for the matching table (#239)

* Thu Oct 02 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.5
- Usage of SAX parser for XML-based notifications (#201)
- Cygnus version and snapshot shown in the logs (#187)
- Document how a developer may build his/her own sink (#136)
- Pattern-based grouping into tables (#107)
- Bug fixig: process notifications with no contextAttributeList (#222)
- Bug fixing: do the RPM scripts do not change the ownership of the whole /var/run folder (#203)
- Bug fixing: process the "value" tag in XML notifications instead of "contextValue" (#227)

* Wed Sep 05 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.4.1
- Only Flume events related to a persistence error are reínjected in the agent channel (#52)
- A TTL has been added to the re-injected Flume events (#126)
- Cygnus version is now showed in the logs (#104)
- Manual build and RPM build both using the same lo4j.properties.template (#111)
- Usage of Timestamp Interceptor instead of custom timestamping mechanism (#143)
- Configurable Hive endpoint independent of the HDFS endpoint (#173)
- Multiple HDFS endpoint setup (#175)
- Migration from Cygnus 0.1 to 0.2 or higher has been documented (#135)
- Migration from ngsi2cosmos to Cygnus has been documented (#105)
- Alarms related to Cygnus have been documented (#112)

* Thu Jul 31 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.4
- TDAF-like logs (#109)
- Standardize the default Cygnus logs path (#91)
- Bug fixing: quotes appearing in CKAN resource values (PR #97)
- Script for removing old data within CKAN-based short term historic (#62)
- CKAN basic management script (PR #99)
- CKAN cleanup script (PR #98)

* Thu Jul 03 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.3
- Attribute metadata persistence (#41)
- Multi-tenancy features (#36)
- Per column attribute persistence (#54 #60 #51)
- Move reception timestamping from the sink to the source (#53)
- MySQL connector added as a pom dependency (#78)
- RPM building framework (#76)
- Relaxed Orion version checking (#70)
- MySQL Connector added to pom.xml (#78)
- Translation scripts from Cygnus 0.1 to Cygnus 0.3 (#65)
- Script for removing old data within MySQL-based short term historic (#63)

* Wed Jun 04 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.2.1
- Change the OrionMySQLSink database and table names, by removing the "cygnus_" part (#57)
- Fixed bug in CKAN insertion mechanism

* Tue Jun 03 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.2
- Support for complex attribute values, specifically, vectors and objects (#43)
- Json-like persistency, independently of the notification type (XML or Json) or the backend (#29)
- Persistence in a MySQL backend (#42)
- Persistence in a CKAN backend (basic functionality) (#31)
- HDFS dataset and Hive table creation at startup time (#13)
- Change package names accordingly to the new repo structure (#30)
- Unit tests (#18)
- Add a template for cygnus.conf (#37)
- README files in UTF-8 (#33)
- Avoid special characters in HDFS file names, CKAN datastores IDs and MySQL table names (#9)
- Refactor the sinks and the HDFS backends, getting common code (#34)
- Per column attribute persistence in MySQL sink (#50)
- Hive basic client (#26)
- Plague Tracker application (#27)
- Translation scripts for moving from Cygnus 0.1 to Cygnus 0.2 (#29)
- XML and Json simple and compound notifications examples for testing (#39)

* Thu Mar 20 2014 Francisco Romero <francisco.romerobueno@telefonica.com> 0.1
- Parsing of simple (string-like values only) Json notifications (#8)
- Parsing of simple (string-like values only) XML notifications (#3)
- Persistence in a WebHDFS/HttpFS backend (#20)
- SFTP basic client
