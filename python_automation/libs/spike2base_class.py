import numpy as np
from sonpy import lib as sp

from typing import Union

MAXINT32: int = int(2147483647/4)    

class Spike2SonpyReader:
    def __init__(self, spike2_filepath: str) -> None:
        self.chan: int = -1
        self.spike2_filepath: str = spike2_filepath
        self.handle: sp.SonFile = self._read(spike2_filepath)

    #-----------------------------------------------------------------------------------
    """ Init """
    def _read(self, spike2_filepath: str) -> sp.SonFile:
        with open(spike2_filepath, 'r') as f:
            return sp.SonFile(f.name, True)

    #-----------------------------------------------------------------------------------
    # Main Data-Get
    def _get_channel_data(self, start_time_secs: Union[float, np.float32], end_time_secs: Union[float, np.float32]) -> np.ndarray:
        # Conversion to sonpy function argument units
        start_time_base_ticks: np.int64 = np.int64(self._secs_to_base_tick(start_time_secs))
        end_time_base_ticks: np.int64 = np.int64(self._secs_to_base_tick(end_time_secs))
        max_time_chan_ticks: np.int64 = self._get_max_length_chan_ticks()
        # Main sonpy function call
        if self._is_wave():
            return np.array(self.handle.ReadFloats(self.chan, max_time_chan_ticks, start_time_base_ticks, end_time_base_ticks), dtype=np.float32)
        return self._chan_tick_to_secs(np.array(self.handle.ReadEvents(self.chan, MAXINT32, start_time_base_ticks, end_time_base_ticks), dtype=np.float32)) #type: ignore
    
    # Get/Set/Check Channel Index
    def _set_channel_index(self, chan: int):
        """ Takes channel index AS LISTED IN SPIKE2 FILE"""
        self.chan = chan - 1
    
    def _channel_exists(self, chan: int) -> bool:
        """
        Checks is channel exists in target Spike2 file. 'chan' argument taken as the channel index present 
        in Spike2 GUI (indexed from 1, not 0)
        """
        pre_call_target_channel: int = self.chan
        self.chan = chan - 1
        exists: bool = False
        try:
            title: str = self._get_channel_title().upper()
            if not title in ('UNTITLED', 'MEMORY'):
                exists = True
        except ValueError:
            pass
        except Exception:
            pass
        
        self.chan = pre_call_target_channel
        return exists

    def _get_channel_index(self) -> Union[int, None]:
        if self.chan < 0:
            return None
        return self.chan + 1
    
    #-----------------------------------------------------------------------------------
    # Timebase Methods
    def _get_fs(self) -> np.float32:
        return 1/np.float32(self.handle.GetTimeBase()*self.handle.ChannelDivide(self.chan))
    
    def _base_tick_to_secs(self, base_ticks: Union[int, np.int64, np.ndarray]) -> Union[np.float32, np.ndarray]:
        return np.float32(base_ticks*self.handle.GetTimeBase())
    
    def _base_tick_to_chan_tick(self, base_ticks: Union[int, np.int64, np.ndarray]) -> Union[np.int64, np.ndarray]:
        return np.int64(np.float32(base_ticks)/np.float32(self.handle.ChannelDivide(self.chan)))
    
    def _chan_tick_to_secs(self, chan_ticks: Union[int, np.int64, np.ndarray]) -> Union[np.float32, np.ndarray]:
        return np.float32(chan_ticks/self._get_fs())

    def _chan_tick_to_base_tick(self, chan_ticks: Union[int, np.int64, np.ndarray]) -> Union[np.int64, np.ndarray]:
        return np.int64(chan_ticks*self.handle.ChannelDivide(self.chan))
    
    def _secs_to_base_tick(self, secs: Union[float, np.float32, np.ndarray]) -> Union[np.int64, np.ndarray]:
        return np.int64(secs/np.float32(self.handle.GetTimeBase()))
    
    def _secs_to_chan_tick(self, secs: Union[float, np.float32, np.ndarray]) -> Union[np.int64, np.ndarray]:
        return np.int64(secs*np.float32(self._get_fs()))
    
    # Channel Max Length
    def _get_max_length_chan_ticks(self) -> np.int64:
        return np.int64(self._base_tick_to_chan_tick(self._get_max_length_base_ticks()))
    
    def _get_max_length_secs(self) -> float:
        return float(self._base_tick_to_secs(self._get_max_length_base_ticks()))
    
    def _get_max_length_base_ticks(self) -> np.int64:
        result: np.int64 = np.int64(self.handle.ChannelMaxTime(self.chan))
        return result if result > 0 else self._get_max_file_time_base_ticks()

    # File Max Length
    def _get_max_file_time_secs(self) -> float:
        return float(self._base_tick_to_secs(self.handle.MaxTime()))
    
    def _get_max_file_time_base_ticks(self) -> np.int64:
        return np.int64(self.handle.MaxTime())
    
    def _get_max_file_time_chan_ticks(self) -> np.int64:
        return np.int64(self._base_tick_to_chan_tick(self.handle.MaxTime()))

    # -----------------------------------------------------------------------------
    # Channel Type/Title
    def _is_(self, channel_type: str) -> bool:
        if channel_type in str(self.handle.ChannelType(self.chan)):
            return True
        return False

    def _is_event(self) -> bool:
        return self._is_("DataType.Event")
        
    def _is_wave(self) -> bool:
        return self._is_("DataType.Adc")
   
    def _get_channel_title(self) -> str:
        return self.handle.GetChannelTitle(self.chan)
    
    # Whole-File Info
    def _get_filepath(self) -> str:
        return self.handle.GetName()
    
    def _get_filename(self) -> str:
        return self._get_filepath().split('/')[-1]

    def _get_file_max_channels(self) -> int:
        return self.handle.MaxChannels()
    