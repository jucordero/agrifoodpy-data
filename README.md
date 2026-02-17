# agrifoodpy-data
AgriFoodPy Data is a data repository and companion package to
[AgriFoodPy](https://github.com/FixOurFood/AgriFoodPy), providing easy access
to curated datasets related to agriculture, food systems, environmental
impacts, land use, and population. These datasets are essential for modeling,
analysis, and research in sustainable food systems.

All datasets are stored in NetCDF format and loaded as xarray DataArrays or
Datasets for efficient handling in Python.

## Datasets

**FAOSTAT food balance sheet**
- Can be found at [www.fao.org/faostat/en/#data/FBS](https://www.fao.org/faostat/en/#data/FBS)
- Food supply elements disaggregated into country, item, and year. Elements include production, imports, exports and domestic use, among others.
- It is the basis of the calculator, and defines the baseline scenario from which we project consumption and production towards 2050



**Nationally determined contributions (NDC)**
- Can be found at [unfccc.int/nationally-determined-contributions-ndcs](https://unfccc.int/process-and-meetings/the-paris-agreement/nationally-determined-contributions-ndcs)
- The NDCs are climate action plans submitted by each country as part of the Paris Agreement. They report past emissions using a standardized form (National Inventory Report) and describe the policies and actions planned and in action to reduce emissions by 2050.



**Nature England Agricultural Land Classification (ALC) data**
- Alias: _not yet included in Agrifoodpy_ (currently in NaturalEngland/Reading_ALC_data.ipynb)
- Can be found at [naturalengland-defra.opendata.arcgis.com/datasets](https://naturalengland-defra.opendata.arcgis.com/datasets/Defra::provisional-agricultural-land-classification-alc-england/about)
- Using a combination of different geographical and climate datasets, the ALC map grades land based on its agricultural capabilities, ranging from least productive (grade 5, typically mountains, high gradient pasture, rocky soils, urban areas) to most productive (low altitude, low gradient, moderate rainfall, nutrient rich soils). The dataset is distributed as a vector map of different grades, but we have rasterised it to match the CEH grid. Both geospatial datasets are matched to the British National Grid



**UK Centre for Ecology and Hydrology Land Cover maps (UK CEH)**
- Alias: _not yet included in Agrifoodpy_
- Can be found at [ceh.ac.uk/data](https://www.ceh.ac.uk/data/ukceh-land-cover-maps), while 1000m rasterised data can be downloaded from [catalogue.ceh.ac.uk/documents](https://catalogue.ceh.ac.uk/documents/a3ff9411-3a7a-47e1-9b3e-79f21648237d.)
- The CEH land cover maps are generated using machine learning on remote sensing images, and present a description of the different land use types in the UK. While the main dataset provides utilisation values for a grid with a resolution of 25m, we use the summary 1km grid maps to identify and map food production in the UK.



**UK Centre for Ecology and Hydrology Land Cover Plus crop maps**
- Can be found at [ceh.ac.uk/services/ceh-land-cover-plus-crops-2015](https://www.ceh.ac.uk/services/ceh-land-cover-plus-crops-2015). Data can be accessed through a free academic licence from Digimap [digimap.edina.ac.uk](https://digimap.edina.ac.uk/environment). 
- A catalogue of land parcels classified by crop types is generated using remote sensing data from two satellites, Copernicus Sentinel-1 C-band SAR and Sentinel-2 optical imaging. Land Cover Plus provides data for the 2016-2020 year range.



**UK Office of National Statistics population tables**
- Alsias: from agrifoodpy.population.population import UK_ONS
which can be downloaded in zip format here: [ons.gov.uk/file](https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/populationandmigration/populationprojections/datasets/z1zippedpopulationprojectionsdatafilesuk/2022based/uk.zip)



**United Nations (UN) population data**
- Alias: from agrifoodpy.population.population import UN
- The original CSV file read in this notebook can be obtained here: [population.un.org](https://population.un.org/wpp/)
- This dataset provides country-level population estimates and projections by year, using multiple scenarios for fertility, mortality, and international migration. In Agrifood these are employed to project the change in domestic consumption relative to today’s values. 


For a full list of datasets please visit

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
