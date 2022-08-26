# ESMF application makefile fragment
#
# Use the following ESMF_ variables to compile and link
# your ESMF application against this ESMF build.
#
# !!! VERY IMPORTANT: If the location of this ESMF build is   !!!
# !!! changed, e.g. libesmf.a is copied to another directory, !!!
# !!! this file - esmf.mk - must be edited to adjust to the   !!!
# !!! correct new path                                        !!!
#
# Please see end of file for options used on this ESMF build
#

#----------------------------------------------
ESMF_VERSION_STRING=8.0.1
# Not a Git repository
ESMF_VERSION_STRING_GIT=NoGit
#----------------------------------------------

ESMF_VERSION_MAJOR=8
ESMF_VERSION_MINOR=0
ESMF_VERSION_REVISION=1
ESMF_VERSION_PATCHLEVEL=1
ESMF_VERSION_PUBLIC='T'
ESMF_VERSION_BETASNAPSHOT='F'


ESMF_APPSDIR=/home/cayang/anaconda3/envs/Evaluate/bin
ESMF_LIBSDIR=/home/cayang/anaconda3/envs/Evaluate/lib


ESMF_F90COMPILER=/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/_build_env/bin/x86_64-conda_cos6-linux-gnu-gfortran
ESMF_F90LINKER=/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/_build_env/bin/x86_64-conda_cos6-linux-gnu-gfortran

ESMF_F90COMPILEOPTS=-O -fPIC  -m64 -mcmodel=small -pthread -ffree-line-length-none  -fopenmp
ESMF_F90COMPILEPATHS=-I/home/cayang/anaconda3/envs/Evaluate/mod -I/home/cayang/anaconda3/envs/Evaluate/include -I/home/cayang/anaconda3/envs/Evaluate/include
ESMF_F90COMPILECPPFLAGS=-DESMF_NO_INTEGER_1_BYTE -DESMF_NO_INTEGER_2_BYTE -DESMF_LAPACK=1 -DESMF_LAPACK_INTERNAL=1 -DESMF_MOAB=1 -DESMF_NO_ACC_SOFTWARE_STACK=1 -DESMF_NETCDF=1 -DESMF_YAMLCPP=1 -DESMF_YAML=1 -DESMF_NO_OPENACC -DESMF_BOPT_O -DESMF_TESTCOMPTUNNEL -DSx86_64_small=1 -DESMF_OS_Linux=1 -DESMF_COMM=mpiuni -DESMF_DIR=/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/work -DESMF_MPIUNI
ESMF_F90COMPILEFREECPP=
ESMF_F90COMPILEFREENOCPP=-ffree-form
ESMF_F90COMPILEFIXCPP=-cpp -ffixed-form
ESMF_F90COMPILEFIXNOCPP=

ESMF_F90LINKOPTS=   -m64 -mcmodel=small -pthread -Wl,--no-as-needed  -fopenmp
ESMF_F90LINKPATHS=-L/home/cayang/anaconda3/envs/Evaluate/lib -L/home/cayang/anaconda3/envs/Evaluate/lib -L/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/_build_env/bin/../lib/gcc/x86_64-conda_cos6-linux-gnu/7.5.0/../../../../x86_64-conda_cos6-linux-gnu/lib/../lib/
ESMF_F90ESMFLINKPATHS=-L/home/cayang/anaconda3/envs/Evaluate/lib
ESMF_F90LINKRPATHS=-Wl,-rpath,/home/cayang/anaconda3/envs/Evaluate/lib  -Wl,-rpath,/home/cayang/anaconda3/envs/Evaluate/lib -Wl,-rpath,/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/_build_env/bin/../lib/gcc/x86_64-conda_cos6-linux-gnu/7.5.0/../../../../x86_64-conda_cos6-linux-gnu/lib/../lib/
ESMF_F90ESMFLINKRPATHS=-Wl,-rpath,/home/cayang/anaconda3/envs/Evaluate/lib
ESMF_F90LINKLIBS= -lrt -lstdc++ -ldl -lnetcdff -lnetcdf
ESMF_F90ESMFLINKLIBS=-lesmf  -lrt -lstdc++ -ldl -lnetcdff -lnetcdf

ESMF_CXXCOMPILER=/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/_build_env/bin/x86_64-conda_cos6-linux-gnu-c++
ESMF_CXXLINKER=/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/_build_env/bin/x86_64-conda_cos6-linux-gnu-c++

ESMF_CXXCOMPILEOPTS=-std=c++11 -O -DNDEBUG -fPIC -DESMF_LOWERCASE_SINGLEUNDERSCORE -m64 -mcmodel=small -pthread  -fopenmp
ESMF_CXXCOMPILEPATHS= -I/home/cayang/anaconda3/envs/Evaluate/include  -I/home/cayang/anaconda3/envs/Evaluate/include -I/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/work/src/Infrastructure/stubs/mpiuni -I/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/work/src/prologue/yaml-cpp/include
ESMF_CXXCOMPILECPPFLAGS=-DESMF_NO_INTEGER_1_BYTE -DESMF_NO_INTEGER_2_BYTE -DESMF_LAPACK=1 -DESMF_LAPACK_INTERNAL=1 -DESMF_MOAB=1 -DESMF_NO_ACC_SOFTWARE_STACK=1 -DESMF_NETCDF=1 -DESMF_YAMLCPP=1 -DESMF_YAML=1 -DESMF_NO_OPENACC -DESMF_BOPT_O -DESMF_TESTCOMPTUNNEL -DSx86_64_small=1 -DESMF_OS_Linux=1 -DESMF_COMM=mpiuni -DESMF_DIR=/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/work -D__SDIR__='' -DESMF_CXXSTD=11 -DESMF_MPIUNI

ESMF_CXXLINKOPTS=  -m64 -mcmodel=small -pthread -Wl,--no-as-needed  -fopenmp
ESMF_CXXLINKPATHS=-L/home/cayang/anaconda3/envs/Evaluate/lib -L/home/cayang/anaconda3/envs/Evaluate/lib -L/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/_build_env/bin/../x86_64-conda_cos6-linux-gnu/sysroot/lib/../lib/
ESMF_CXXESMFLINKPATHS=-L/home/cayang/anaconda3/envs/Evaluate/lib
ESMF_CXXLINKRPATHS=-Wl,-rpath,/home/cayang/anaconda3/envs/Evaluate/lib  -Wl,-rpath,/home/cayang/anaconda3/envs/Evaluate/lib -Wl,-rpath,/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/_build_env/bin/../x86_64-conda_cos6-linux-gnu/sysroot/lib/../lib/
ESMF_CXXESMFLINKRPATHS=-Wl,-rpath,/home/cayang/anaconda3/envs/Evaluate/lib
ESMF_CXXLINKLIBS= -lrt -lgfortran -ldl -lnetcdff -lnetcdf
ESMF_CXXESMFLINKLIBS=-lesmf  -lrt -lgfortran -ldl -lnetcdff -lnetcdf

ESMF_SO_F90COMPILEOPTS=-fPIC
ESMF_SO_F90LINKOPTS=-shared
ESMF_SO_F90LINKOPTSEXE=-Wl,-export-dynamic
ESMF_SO_CXXCOMPILEOPTS=-fPIC
ESMF_SO_CXXLINKOPTS=-shared
ESMF_SO_CXXLINKOPTSEXE=-Wl,-export-dynamic

ESMF_OPENMP_F90COMPILEOPTS= -fopenmp
ESMF_OPENMP_F90LINKOPTS= -fopenmp
ESMF_OPENMP_CXXCOMPILEOPTS= -fopenmp
ESMF_OPENMP_CXXLINKOPTS= -fopenmp

ESMF_OPENACC_F90COMPILEOPTS=
ESMF_OPENACC_F90LINKOPTS=
ESMF_OPENACC_CXXCOMPILEOPTS=
ESMF_OPENACC_CXXLINKOPTS=

# ESMF Tracing compile/link options
ESMF_TRACE_LDPRELOAD=/home/cayang/anaconda3/envs/Evaluate/lib/libesmftrace_preload.so
ESMF_TRACE_STATICLINKOPTS=-static -Wl,--wrap=c_esmftrace_notify_wrappers -Wl,--wrap=c_esmftrace_isinitialized -Wl,--wrap=write -Wl,--wrap=writev -Wl,--wrap=pwrite -Wl,--wrap=read -Wl,--wrap=open -Wl,--wrap=MPI_Allgather -Wl,--wrap=MPI_Allgatherv -Wl,--wrap=MPI_Allreduce -Wl,--wrap=MPI_Alltoall -Wl,--wrap=MPI_Alltoallv -Wl,--wrap=MPI_Alltoallw -Wl,--wrap=MPI_Barrier -Wl,--wrap=MPI_Bcast -Wl,--wrap=MPI_Gather -Wl,--wrap=MPI_Gatherv -Wl,--wrap=MPI_Recv -Wl,--wrap=MPI_Reduce -Wl,--wrap=MPI_Scatter -Wl,--wrap=MPI_Send -Wl,--wrap=MPI_Sendrecv -Wl,--wrap=MPI_Wait -Wl,--wrap=MPI_Waitall -Wl,--wrap=MPI_Waitany -Wl,--wrap=MPI_Waitsome -Wl,--wrap=mpi_allgather_ -Wl,--wrap=mpi_allgather__ -Wl,--wrap=mpi_allgatherv_ -Wl,--wrap=mpi_allgatherv__ -Wl,--wrap=mpi_allreduce_ -Wl,--wrap=mpi_allreduce__ -Wl,--wrap=mpi_alltoall_ -Wl,--wrap=mpi_alltoall__ -Wl,--wrap=mpi_alltoallv_ -Wl,--wrap=mpi_alltoallv__ -Wl,--wrap=mpi_alltoallw_ -Wl,--wrap=mpi_alltoallw__ -Wl,--wrap=mpi_barrier_ -Wl,--wrap=mpi_barrier__ -Wl,--wrap=mpi_bcast_ -Wl,--wrap=mpi_bcast__ -Wl,--wrap=mpi_exscan_ -Wl,--wrap=mpi_exscan__ -Wl,--wrap=mpi_gather_ -Wl,--wrap=mpi_gather__ -Wl,--wrap=mpi_gatherv_ -Wl,--wrap=mpi_gatherv__ -Wl,--wrap=mpi_recv_ -Wl,--wrap=mpi_recv__ -Wl,--wrap=mpi_reduce_ -Wl,--wrap=mpi_reduce__ -Wl,--wrap=mpi_reduce_scatter_ -Wl,--wrap=mpi_reduce_scatter__ -Wl,--wrap=mpi_scatter_ -Wl,--wrap=mpi_scatter__ -Wl,--wrap=mpi_scatterv_ -Wl,--wrap=mpi_scatterv__ -Wl,--wrap=mpi_scan_ -Wl,--wrap=mpi_scan__ -Wl,--wrap=mpi_send_ -Wl,--wrap=mpi_send__ -Wl,--wrap=mpi_wait_ -Wl,--wrap=mpi_wait__ -Wl,--wrap=mpi_waitall_ -Wl,--wrap=mpi_waitall__ -Wl,--wrap=mpi_waitany_ -Wl,--wrap=mpi_waitany__
ESMF_TRACE_STATICLINKLIBS=-lesmftrace_static

# Internal ESMF variables, do NOT depend on these!

ESMF_INTERNAL_DIR=/home/conda/feedstock_root/build_artifacts/esmf_1590566296382/work

#
# !!! The following options were used on this ESMF build !!!
#
# ESMF_DIR: /home/conda/feedstock_root/build_artifacts/esmf_1590566296382/work
# ESMF_OS: Linux
# ESMF_MACHINE: x86_64
# ESMF_ABI: 64
# ESMF_COMPILER: gfortran
# ESMF_BOPT: O
# ESMF_COMM: mpiuni
# ESMF_SITE: default
# ESMF_PTHREADS: ON
# ESMF_OPENMP: ON
# ESMF_OPENACC: OFF
# ESMF_ARRAY_LITE: FALSE
# ESMF_NO_INTEGER_1_BYTE: TRUE
# ESMF_NO_INTEGER_2_BYTE: TRUE
# ESMF_FORTRANSYMBOLS: default
# ESMF_MAPPER_BUILD: OFF
# ESMF_AUTO_LIB_BUILD: ON
# ESMF_DEFER_LIB_BUILD: ON
# ESMF_SHARED_LIB_BUILD: ON
# 
# ESMF environment variables pointing to 3rd party software:
# ESMF_MOAB:              internal
# ESMF_LAPACK:            internal
# ESMF_ACC_SOFTWARE_STACK:            none
# ESMF_NETCDF:            split
# ESMF_NETCDF_INCLUDE:    /home/cayang/anaconda3/envs/Evaluate/include
# ESMF_NETCDF_LIBS:       -lnetcdff -lnetcdf
# ESMF_NETCDF_LIBPATH:    /home/cayang/anaconda3/envs/Evaluate/lib
# ESMF_YAMLCPP:           internal
