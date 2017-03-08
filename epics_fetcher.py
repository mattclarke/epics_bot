from CaChannel import ca, CaChannel, CaChannelException
import zlib


class PvNotFoundException(Exception):
    pass


class EpicsFetcher(object):
    def waveform_to_string(self, value):
        output = ""
        for i in value:
            if i == 0:
                break
            output += str(unichr(i))
        return output

    def dehex_and_decompress(self, value):
        return zlib.decompress(value.decode('hex'))

    def caget(self, name, as_str=False):
        try:
            chan = CaChannel(name)
            chan.searchw(name)
            if as_str:
                return self.caget_str(chan)
            else:
                return chan.getw()
        except:
            raise PvNotFoundException("Unable to find PV %s" % name)

    def caget_str(self, chan):
        ftype = chan.field_type()
        if ca.dbr_type_is_ENUM(ftype) or ca.dbr_type_is_STRING(ftype):
            value = chan.getw(ca.DBR_STRING)
        else:
            value = chan.getw(ca.DBR_CHAR)
        if isinstance(value, list):
            return self.waveform_to_string(value)
        else:
            return str(value)