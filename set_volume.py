import ctypes

def set_master_volume(volume):
    """
    Set the master volume on Windows. Volume should be between 0 and 100.
    This version maps 0-100 directly to 0-100% using SetMasterVolumeLevelScalar.
    """
    try:
        from ctypes import POINTER, cast
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    except ImportError:
        print("pycaw is required for volume control. Install with: pip install pycaw comtypes")
        return

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
    # Map 0-100 to 0.0-1.0 for SetMasterVolumeLevelScalar
    scalar = max(0.0, min(1.0, float(volume) / 100.0))
    volume_interface.SetMasterVolumeLevelScalar(scalar, None)
