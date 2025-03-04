# Stubs for mlconjug3.mlconjug3 (Python 3)

from .PyVerbiste import Verb, ConjugManager
from sklearn.pipeline import Pipeline

# I am commenting out the sklearn imports because they have yet no stub files.
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.base import BaseEstimator
from typing import Optional, Mapping, List, Sequence, DefaultDict, Any, Tuple, Type, AbstractSet, Union


_RESOURCE_PACKAGE: str = __name__
_LANGUAGE_FULL: Mapping[str, str]
_VERBS: Mapping[str, Type[Verb]]
_PRE_TRAINED_MODEL_PATH: Mapping[str, str]


def extract_verb_features(verb: str,
                              lang: str,
                              ngram_range: Tuple[int, int]
                              ) -> Sequence[str]: ...


class Conjugator:
    language: str = ...
    conjug_manager: ConjugManager = ...
    model: Model = ...
    def __init__(self,
                 language: str = ...,
                 model: Optional[Model] = ...
                 ) -> None: ...

    def __repr__(self) -> str: ...

    def conjugate(self,
                  verb: str,
                  subject: str = ...
                  ) -> Optional[Verb]: ...

    def set_model(self,
                  model: Model
                  ) -> None: ...


class DataSet:
    verbs_dict: Mapping[str, Mapping[str, str]] = ...
    verbs: AbstractSet[str] = ...
    templates: List[str] = ...
    verbs_list: List[str] = ...
    templates_list: List[int] = ...
    dict_conjug: Optional[DefaultDict[str,Sequence[str]]] = ...
    train_input: Sequence[str] = ...
    train_labels: Sequence[int] = ...
    test_input: Sequence[str] = ...
    test_labels: Sequence[int] = ...
    min_threshold: int = ...
    split_proportion: float = ...
    def __init__(self,
                 verbs_dict: Mapping[str, Mapping[str, str]] = ...
                 ) -> None: ...

    def __repr__(self) -> str: ...

    def construct_dict_conjug(self) -> None: ...

    def split_data(self,
                   threshold: int = ...,
                   proportion: Union[float, int] = ...
                   ) -> None: ...

class Model:
    pipeline: Pipeline = ...
    language: str = ...
    def __init__(self,
                 vectorizer: Optional[Any] = ...,
                 feature_selector: Optional[Any] = ...,
                 classifier: Optional[Any] = ...,
                 language: Optional[str] = ...
                 ) -> None: ...

    def __repr__(self) -> str: ...

    def train(self,
              samples: Sequence[str],
              labels: Sequence[int],
              ) -> None: ...

    def predict(self,
                verbs: Sequence[str]
                ) -> Sequence[int]: ...
