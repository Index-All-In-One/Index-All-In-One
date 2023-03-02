# Opensearch-Conn

This is a development package for the Index-All-In-One project.<br>

opensearch_conn is the name of a package for connecting to OpenSearch, an open source distributed search and analytics engine. The package provides a Python client for interacting with OpenSearch.<br>

## Install
Go to the python project you wish to use the package and:
```
pip3 install packages/opensearch_conn
```

## Build package for remote use
```
python3 setup.py sdist
```
Source distributions(sdist) are more flexible because they can be built and installed on any platform, and can be customized or modified before installation.<br>

.dist is where the package resides, you can upload the package.<br>

To install the package this way: <br>

```
pip3 install opensearch_conn-0.0.1.tar.gz
```

## See if the package is correctly installed
```
pip3 show opensearch_conn
```

## Uninstall the package
```
pip3 uninstall opensearch-conn
```