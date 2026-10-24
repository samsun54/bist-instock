# İndikatör paketi — TA-Lib opsiyonel

from .simple_indicators import add_basic_indicators

try:
    from .calculate_indicator import get_indicators, get_indicator
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False

    def get_indicators(data, **kwargs):
        return add_basic_indicators(data)

    def get_indicator(*args, **kwargs):
        return None

__all__ = ["get_indicators", "get_indicator", "add_basic_indicators", "HAS_TALIB"]
