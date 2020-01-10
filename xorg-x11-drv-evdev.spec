%global tarball xf86-input-evdev
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input
%global policydir %{_datadir}/hal/fdi/policy/10osvendor

#global gitdate 20120718
#global gitversion f5ede9808

Summary:    Xorg X11 evdev input driver
Name:       xorg-x11-drv-evdev
Version:    2.7.3
Release:    5%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
URL:        http://www.x.org
License:    MIT
Group:      User Interface/X Hardware Support
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0:    ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
%endif
Source3:    10-x11-lid.fdi

# Bug 805902 - Scrollwheels on tablets are broken
Patch02: 0001-Allow-relative-scroll-valuators-on-absolute-devices.patch
Patch03:  evdev-2.6.0-lid.patch
Patch04:  evdev-2.6.0-revert-mb-emu-changes.patch
Patch05:  evdev-2.7.3-0001-Undefine-HAVE_SMOOTH_SCROLLING.patch

ExcludeArch: s390 s390x

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-sdk >= 1.10.99.902
BuildRequires: libxkbfile-devel libudev-devel
BuildRequires: mtdev-devel
BuildRequires: xorg-x11-util-macros >= 1.17
Requires:  Xorg %(xserver-sdk-abi-requires ansic)
Requires:  Xorg %(xserver-sdk-abi-requires xinput)
Requires:  xkeyboard-config >= 1.4-1
Requires: libudev
Requires: mtdev

%description 
X.Org X11 evdev input driver.

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{policydir}
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{policydir}

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING
%{driverdir}/evdev_drv.so
%{_mandir}/man4/evdev.4*
%{policydir}/10-x11-lid.fdi


%package devel
Summary:    Xorg X11 evdev input driver development package.
Group:      Development/Libraries
Requires:   pkgconfig
%description devel
X.Org X11 evdev input driver development files.

%files devel
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/pkgconfig/xorg-evdev.pc
%dir %{_includedir}/xorg
%{_includedir}/xorg/evdev-properties.h


%changelog
* Thu Nov 01 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.7.3-5
- Fix {?dist} tag (#871447)

* Mon Aug 27 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.7.3-4
- Rebuild for server 1.13 (#835225)

* Mon Aug 20 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7.3-2
- Merge evdev 2.7.3 from F18 (#835225)
- Restore RHEL6.x middle mouse button emulation default (auto)
- Restore RHEL6.x lid patch to re-scan xrandr outputs
- Disable smooth scrolling, no client stack support

* Fri Jul 22 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.6.0-2
- evdev-2.6.0-Always-reset-the-fd-to-1.patch: avoid early log file closure

* Thu Jun 30 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.6.0-1
- evdev 2.6.0 (#713786)
- evdev-2.6.0-lid.patch: update against 2.6.0
- evdev-2.6.0-revert-mb-emu-changes.patch: go back to previous MB emulation
  defaults

* Fri Jul 30 2010 Adam Jackson <ajax@redhat.com> 2.3.2-8
- 10-x11-lid.fdi: Add so switch devices appear to have an X driver in hal.
- evdev-2.3.2-lid.patch: Scan for lid switch devices, translate events on
  them into RANDR rescans so the desktop will pick them up. (#618845)

* Wed Jun 30 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-7
- evdev-2.3.2-max-valuators-oob.patch: avoid OOB access when a device has
  more than MAX_VALUATORS axes (#609333)

* Wed Apr 21 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-6
- evdev-2.3.3-memory-leaks.patch: free up memory after using options.
  (#584234)

* Tue Apr 20 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-5
- evdev-2.3.2-wheel-motion-events.patch: don't send motion events for wheel
  events (#583878)

* Mon Feb 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-4
- evdev-2.3.2-reopen-infinity.patch: Don't reopen into infinity if
  ReopenAttempts is 0. (#562687)

* Wed Jan 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-3
- Use global instead of define as per Packaging Guidelines
- Remove tab/spaces mixup.

* Tue Jan 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-2
- remove references to git builds and matching sources aux files.
- remove libxkbfile-devel BuildRequires
- actually disable autoreconf this time.

* Fri Dec 11 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-1
- evdev 2.3.2
- disable autoreconf, we're not building from git anymore.

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.1-2
- 0001-Fix-drag-lock-property-handler-for-multiple-draglock.patch
  drop, merged upstream.

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.1-1
- evdev 2.3.1

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.0-4
- BuildRequires macros, not Requires.

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.0-3
- Require xorg-x11-util-macros 1.3.0

* Mon Nov 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.0-2
- 0001-Fix-drag-lock-property-handler-for-multiple-draglock.patch
  Fix property handler indexing for multiple draglock buttons
  (#524428).

* Mon Oct 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.0-1
- evdev 2.3.0

* Thu Oct 08 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99.2-1
- evdev 2.2.99.2

* Wed Sep 23 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-8.20090923
- Update to today's git master (fixes wheel emulation)

* Wed Sep 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-7.20090909
- Update to today's git master

* Fri Aug 14 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-6.20090814
- Update to today's git master

* Thu Jul 30 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-5.20090730
- Update to today's git master

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.99-4.20090629.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 2.2.99-3.20090629.1
- ABI bump

* Thu Jul 09 2009 Adam Jackson <ajax@redhat.com> 2.2.99-3.20090629
- Fix EVR inversion, 1.20090629 < 2.20090619

* Mon Jun 29 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-1.20090629
- Update to today's git master
- Add commitid file with git's sha1.

* Fri Jun 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-2.20090619
- rebuild for server ABI 7

* Fri Jun 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-1.20090619
- Update to today's git master

* Thu May 21 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-1.20090521
- Update to today's git master

* Thu May 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.2-1
- evdev 2.2.2

* Mon Apr 06 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-2
- evdev-2.2.1-read-deadlock.patch: handle read errors on len <= 0 (#494245)

* Tue Mar 24 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-1
- evdev 2.2.1 

* Mon Mar 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.0-1
- evdev 2.2.0

* Mon Mar 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99.1-1
- evdev 2.2 snapshot 1

* Thu Feb 26 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99.2.20090226
- Update to today's git master.

* Thu Feb 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99-1.20090219
- Update to today's git master.

* Thu Feb 19 2009 Peter Hutterer <peter.hutterer@redhat.com>
- purge obsolete patches.

* Tue Feb 17 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.3-1
- evdev 2.1.3

* Mon Feb 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.2-1
- evdev 2.1.2

* Tue Jan 13 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.1-1
- evdev 2.1.1
- update Requires to 1.5.99.1 to make sure the ABI is right.

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 2.1.0-3
- Rebuild again - latest tag wasn't in buildroot

* Mon Dec 22 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.1.0-2
- Rebuild for server 1.6.

* Wed Nov 19 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.1.0-1
- evdev 2.1.0

* Tue Nov 4 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99.3-1
- evdev 2.0.99.3 (evdev 2.1 RC 3)

* Fri Oct 24 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99.2-1
- evdev 2.0.99.2 (evdev 2.1 RC 2)

* Fri Oct 17 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99.1-1
- evdev 2.0.99.1 (evdev 2.1 RC 1)
- Upstream change now requires libxkbfile-devel to build.

* Mon Oct 13 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99-1
- Today's git snapshot.
- Require xkeyboard-config 1.4 and higher for evdev ruleset.
- Provide devel subpackage for evdev header files.

* Fri Oct 3 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.6-1
- update to 2.0.6
- remove patches merged upstream.

* Fri Sep 12 2008 Adam Jackson <ajax@redhat.com> 2.0.4-3
- evdev-2.0.4-reopen-device.patch: When arming the reopen timer, stash it in
  the driver private, and explicitly cancel it if the server decides to
  close the device for real.
- evdev-2.0.4-cache-info.patch: Rebase to account for same.

* Thu Aug 28 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.4-2
- evdev-2.0.4-reopen-device.patch: try to reopen devices if a read error
  occurs on the fd.
- evdev-2.0.4-cache-info.patch: cache device info to ensure reopened device
  isn't different to previous one.

* Mon Aug 25 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.4-1
- evdev 2.0.4

* Fri Aug 1 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.3-1
- evdev 2.0.3

* Mon Jul 21 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.2-1
- evdev 2.0.2

* Fri Mar 14 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.5
- Today's snapshot.  Maps REL_DIAL to REL_HWHEEL.

* Wed Mar 12 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.4
- Today's snapshot.  Fixes mouse button repeat bug, and therefore Apple
  Mighty Mice are usable.  Props to jkeating for the hardware.

* Tue Mar 11 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.3
- Today's snapshot.  Fixes right/middle button swap hilarity.

* Mon Mar 10 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.2
- Updated snapshot, minor bug fixes.

* Fri Mar 07 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.1
- evdev 2.0 git snapshot

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.0-2
- Autorebuild for GCC 4.3

* Tue Nov 27 2007 Adam Jackson <ajax@redhat.com> 1.2.0-1
- xf86-input-evdev 1.2.0

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.1.2-5
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.1.2-4
- Update Requires and BuildRequires.  Disown the module directories.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.1.2-3
- ExclusiveArch -> ExcludeArch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Tue Jun 13 2006 Adam Jackson <ajackson@redhat.com> 1.1.2-2
- Build on ppc64

* Mon Jun 05 2006 Adam Jackson <ajackson@redhat.com> 1.1.2-1
- Update to 1.1.2 + CVS fixes.

* Mon Apr 10 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-3
- Work around header pollution on ia64, re-add to arch list.

* Mon Apr 10 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-2
- Disable on ia64 until build issues are sorted.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Update to 1.1.0 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.0.5-1
- Updated xorg-x11-drv-evdev to version 1.0.0.5 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.4-1
- Updated xorg-x11-drv-evdev to version 1.0.0.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.2-1
- Updated xorg-x11-drv-evdev to version 1.0.0.2 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-evdev to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for evdev input driver generated automatically
  by my xorg-driverspecgen script.
