from .variable import Variable, logger
from .loss import TextLoss
from .model import BlackboxLLM
from .engine import EngineLM, get_engine
from .optimizer import TextualGradientDescent, TGD, TextualGradientDescentwithMomentum, TextualGradientDescent_v2, TGD_v2
from .config import set_backward_engine, SingletonBackwardEngine
from .autograd import sum, aggregate

singleton_backward_engine = SingletonBackwardEngine()