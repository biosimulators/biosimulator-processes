from pydantic import BaseModel, validator
from typing import *
from abc import ABC, abstractmethod


class SpeciesChanges(BaseModel):  # <-- this is done like set_species('B', kwarg=) where the inner most keys are the kwargs
    species_name: str
    unit: str
    initial_concentration: float
    initial_particle_number: float
    initial_expression: str
    expression: str


class GlobalParameterChanges(BaseModel):  # <-- this is done with set_parameters(PARAM, kwarg=). where the inner most keys are the kwargs
    parameter_name: str
    initial_value: float
    initial_expression: str
    expression: str
    status: str
    param_type: str  # ie: fixed, assignment, reactions, etc


class ReactionParameter(BaseModel):
    parameter_name: str
    value: Union[float, int, str]


class ReactionChanges(BaseModel):
    reaction_name: str
    reaction_parameters: Dict[str, ReactionParameter]
    reaction_scheme: str


class ModelChanges:
    species_changes: List[SpeciesChanges]
    global_parameter_changes: List[GlobalParameterChanges]
    reaction_changes: List[ReactionChanges]


'''class ModelChange(BaseModel):
    config: Union[Dict[str, Dict[str, Dict[str, Union[float, str]]]], Dict[str, Dict[str, Union[Dict[str, float], str]]]]


class ModelChanges(BaseModel):
    species_changes: ModelChange = None
    global_parameter_changes: ModelChange = None
    reaction_changes: ModelChange = None


class ModelSource(ABC, BaseModel):
    value: str

    @validator('value')
    @classmethod
    @abstractmethod
    def check_value(cls, v):
        pass

class BiomodelId(ModelSource):
    @validator('value')
    @classmethod
    def check_value(cls, v):
        assert '/' not in v, "value must not contain '/'"
        return v

class ModelFilepath(BaseModel):
    value: str

    @validator('value')
    @classmethod
    def check_value(cls, v):
        assert '/' in v, "value must contain '/'"
        return v
    

class SedModel(BaseModel):
    model_id: Optional[str] = None
    model_source: str
    model_language: str = 'sbml'
    model_name: str = 'composite_process_model'
    model_changes: ModelChanges'''


# FromDict CLASSES
class FromDict(dict):
    def __init__(self, value: Dict):
        super().__init__(value)


class BasicoModelChanges(FromDict):
    BASICO_MODEL_CHANGES_TYPE = {
        'species_changes': {
            'species_name': {
                'unit': 'maybe[string]',
                'initial_concentration': 'maybe[float]',
                'initial_particle_number': 'maybe[float]',
                'initial_expression': 'maybe[string]',
                'expression': 'maybe[string]'
            }
        },
        'global_parameter_changes': {
            'global_parameter_name': {
                'initial_value': 'maybe[float]',
                'initial_expression': 'maybe[string]',
                'expression': 'maybe[string]',
                'status': 'maybe[string]',
                'type': 'maybe[string]'  # (ie: fixed, assignment, reactions)
            }
        },
        'reaction_changes': {
            'reaction_name': {
                'parameters': {
                    'reaction_parameter_name': 'maybe[int]'  # (new reaction_parameter_name value)  <-- this is done with set_reaction_parameters(name="(REACTION_NAME).REACTION_NAME_PARAM", value=VALUE)
                },
                'reaction_scheme': 'maybe[string]'   # <-- this is done like set_reaction(name = 'R1', scheme = 'S + E + F = ES')
            }
        }
    }

    def __init__(self, _type: Dict = BASICO_MODEL_CHANGES_TYPE):
        super().__init__(_type)


class SedModel(FromDict):
    # The first 3 params are NOT optional below for a Model in SEDML. model_source has been adapted to mean point of residence
    MODEL_TYPE = {
        'model_id': 'string',
        'model_source': 'string',    # could be used as the "model_file" or "biomodel_id" below (SEDML l1V4 uses URIs); what if it was 'model_source': 'sbml:model_filepath'  ?
        'model_language': {    # could be used to load a different model language supported by COPASI/basico
            '_type': 'string',
            '_default': 'sbml'    # perhaps concatenate this with 'model_source'.value? I.E: 'model_source': 'MODEL_LANGUAGE:MODEL_FILEPATH' <-- this would facilitate verifying correct model fp types.
        },
        'model_name': {
            '_type': 'string',
            '_default': 'composite_process_model'
        },
        'model_changes': {
            'species_changes': 'tree[string]',   # <-- this is done like set_species('B', kwarg=) where the inner most keys are the kwargs
            'global_parameter_changes': 'tree[string]',  # <-- this is done with set_parameters(PARAM, kwarg=). where the inner most keys are the kwargs
            'reaction_changes': 'tree[string]'
        },
        'model_units': 'tree[string]'
    }

    def __init__(self, _type: Dict = MODEL_TYPE):
        super().__init__(_type)


# EXAMPLES
changes = {
    'species_changes': {
        'A': {
            'initial_concent': 24.2,
            'b': 'sbml'
        }
    }
}

r = {
    'reaction_name': {
        'parameters': {
            'reaction_parameter_name': 23.2
        },
        'reaction_scheme': 'maybe[string]'
    }
}
