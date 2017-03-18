
import wave
import audioop
import contextlib
from os import path, makedirs

def wav_duration(vm_file):
    """ Returns the length of the VM Wav file. """

    if path.exists(vm_file):
        with contextlib.closing(wave.open(vm_file, 'r')) as wav:
            frames = wav.getnframes()
            rate = wav.getframerate()
            duration = frames / float(rate)
            return duration
    else:
        return -1

def check_format(vm_file, rate=8000, channels=1, bits=16):
    """ Check if the specified Wav recording is in an Asterisk Compatible format. """
    if not path.exists(vm_file):
        return False

    wav_read = wave.open(vm_file, 'r')
    wav_rate = wav_read.getframerate()
    wav_channels = wav_read.getnchannels()
    wav_width = wav_read.getsampwidth()
    width = bits/8
    if (wav_rate, wav_channels, wav_width) == (rate, channels, width):
        return True
    else:
        return False

def wav_convert(src, dst, out_rate=8000, out_channels=1, out_bits=16):
    """
    Convert Wav file to specified format.
    Defaults represent Asterisk requirements for PCM.
    """
    if not path.exists(src):
        print 'Source not found!'
        return False


    if not path.exists(path.dirname(dst)):
        makedirs(path.dirname(dst))

    try:
        s_read = wave.open(src, 'r')
        s_write = wave.open(dst, 'w')
    except:
        print 'Failed to open files!'
        return False

    in_rate = s_read.getframerate()
    in_channels = s_read.getnchannels()
    in_width = s_read.getsampwidth()
    out_width = out_bits/8
    if (in_rate, in_channels, in_width) == (out_rate, out_channels, out_width):
        return True

    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)

    try:
        converted = audioop.ratecv(data, out_width, in_channels, in_rate, out_rate, None)
        if out_channels == 1:
            converted = audioop.tomono(converted[0], 2, 1, 0)
    except:
        print 'Failed to downsample wav'
        return False

    try:
        s_write.setparams((out_channels, 2, out_rate, 0, 'NONE', 'Uncompressed'))
        s_write.writeframes(converted)
    except:
        print 'Failed to write wav'
        return False

    try:
        s_read.close()
        s_write.close()
    except:
        print 'Failed to close wav files'
        return False

    return True
