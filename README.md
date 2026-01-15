# agrifoodpy-data
AgriFoodPy Data is a data repository and companion package to
[AgriFoodPy](https://github.com/FixOurFood/AgriFoodPy), providing easy access
to curated datasets related to agriculture, food systems, environmental
impacts, land use, and population. These datasets are essential for modeling,
analysis, and research in sustainable food systems.

All datasets are stored in NetCDF format and loaded as xarray DataArrays or
Datasets for efficient handling in Python.

## Datasets

For a full list of available datasets, see [datasets.md](datasets.md).

## Installation

To intall AgriFoodPy Data during development:
```bash
pip install git+https://github.com/FixOurFood/agrifoodpy-data.git
```

For stable releases (once available), use:

```bash
pip install agrifoodpy-data
```

## Usage

AgriFoodPy Data integrates seamlessly with AgriFoodPy to load and utilize
datasets in both pipeline and interactive modes.

### Interactive mode

In interactive mode, datasets are loaded as module atributes by importing them
```python
from agrifoodpy_data.food import FAOSTAT
```

Alternatively, datasets can be imported using the `load_dataset` function of 
AgriFoodPy in standalone mode.

```python
from agrifoodpy.utils.nodes import load_dataset

FAOSTAT = load_dataset(module="agrifoodpy_data.food", data_attr="FAOSTAT")
```

### Pipeline mode

In pipeline mode, datasets can be stored in an AgriFoodPy Pipeline datablock
using the `load_dataset` module and used in other modules further along the
pipleine

```python
import agrifoodpy as afp

pipe = afp.pipeline.Pipeline()
pipe.add_node(
    afp.utils.nodes.load_dataset,
    name="Load fbs",
    params={
        "datablock_path": "fbs",
        "module": "agrifoodpy_data.food",
        "data_attr": "FAOSTAT",
        "coords": {
            "Item": [2731, 2511],
            "Year": [2019, 2020],
            "Region": 229},
    }
)

# add more nodes to work with the loaded dataset
```

## Contributing

Contributions are welcome! Please see the main AgriFoodPy repository for 
guidelines.
