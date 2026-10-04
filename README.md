# Trabalho 01

## Spack

A instalação do ambiente Spack, pode ser feita com o seguinte comando:

```bash
spack env create trab01 spack/
spack env activate trab01
spack install
```

A versão utilizada do Spack no servidor foi a 1.2.2, caso tenha algum problema relacionado a sistemas deprecados altere a última linha pelo seguinte:

```bash
spack install --deprecated
```

### Uso em sessões posteriores

```bash
source $WORKDIR/spack/share/spack/setup-env.sh
spack env activate trab01
```

## Contêiner com HPCCM e Apptainer

Para a montagem do contêiner primeiro é necessário iniciar o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Feito a instalação do sistema a criação e montagem do contêiner é feita da seguinte maneira:

```bash
hpccm --recipe container/recipe.py --format singularity > osu_mpich.def
sudo apptainer build osu_mpich.sif osu_mpich.def
```

## Geração de Gráficos

```bash
python plot_osu.py
```