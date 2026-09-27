# Base Image
Stage0 += baseimage(image="ubuntu:24.04")
Stage0 += packages(ospackages=["build-essential", "python3"])

# GCC
compiler = gnu(version="12")
Stage0 += compiler

# MLNX OFED
Stage0 += mlnx_ofed(
    version="5.8-3.0.7.0",
    oslabel="ubuntu22.04",
    packages=[
        "libibverbs1",
        "libibverbs-dev",
        "ibverbs-providers",
        "ibverbs-utils",
        "libibmad5",
        "libibmad-dev",
        "libibumad3",
        "libibumad-dev",
        "librdmacm1",
        "librdmacm-dev",
        "ofed-scripts",
    ],
)

# UCX 1.14.0
Stage0 += knem(ldconfig=True)
Stage0 += xpmem(ldconfig=True, toolchain=compiler.toolchain)
Stage0 += ucx(
    version="1.14.0",
    toolchain=compiler.toolchain,
    prefix="/usr/local/ucx",
    knem="/usr/local/knem",
    xpmem="/usr/local/xpmem",
    ofed=True,
    enable_mt=True,
    enable_cma=True,
    without_java=True,
    without_go=True,
    without_rocm=True,
    without_fuse3=True,
    without_ugni=True,
    ldconfig=True,
    cuda=False,
)

# MPICH 5.0.1 com ch4:ucx
Stage0 += mpich(
    version="5.0.1",
    toolchain=compiler.toolchain,
    prefix="/usr/local/mpich",
    with_device="ch4:ucx",
    with_ucx="/usr/local/ucx",
    ldconfig=True,
)

# OSU Benchmark
osu_version = "7.5.2"
Stage0 += generic_autotools(
    url=f"https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-{osu_version}.tar.gz",
    prefix="/usr/local/osu",
    build_environment={"CC": "mpicc", "CXX": "mpicxx"},
)
Stage0 += shell(
    commands=[
        "find /usr/local/osu/libexec -type f -executable -name 'osu_*' "
        "-exec ln -sf {} /usr/local/bin/ \\;",
    ]
)
