### RPM external yaksa 0.4
%define branch main
%define tag v%{realversion}
Source: git+https://github.com/pmodels/yaksa.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Patch0: yaksa-0.4-cuda-sys-driver-mismatch

BuildRequires: autotools
%{!?without_cuda:Requires: cuda}

%prep
%setup -q -n %{n}-%{realversion}
%patch0 -p1
./autogen.sh

%build
./configure \
  --prefix=%{i} \
  --enable-shared \
  --disable-static \
  --disable-dependency-tracking \
  --with-pic \
  --with-gnu-ld \
%if 0%{!?without_cuda:1}
  --with-cuda=$CUDA_ROOT \
%else
  --without-cuda \
%endif
  --without-hip

make %{makeprocesses}

%install
make install

# remove the libtool library files
rm -f %{i}/lib/lib*.la

# remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
rm -rf %{i}/lib/pkgconfig

%post
