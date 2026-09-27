# Trabalho 01

## Spack

Antesde iniciar o ambiente considerando que o spack já está ativado é necessário instalar o GCC:

```bash
spack install --deprecated gcc@12.4
```

Para iniciar o teste do spack é necessário primeiro ativar o ambiente:

```bash
cd env
spack env activate .
spack install
```

Exemplo de comando para execução:

```bash
qsub -v WORKDIR=/home/lovelace/proj/proj1163/j215217/trab01,RESULTS=/home/lovelace/proj/proj1163/j215217/trab01/output osu.pbs
```
