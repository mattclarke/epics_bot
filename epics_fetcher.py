from epics import PV
import zlib


class PvNotFoundException(Exception):
    pass


class PvGetException(Exception):
    pass


class EpicsFetcher(object):
    def dehex_and_decompress(self, value):
        return zlib.decompress(value.decode('hex'))

    def caget(self, name, as_str=False):
        try:
            pv = PV(name)
            ans = pv.get(as_string=as_str)
            if not pv.connected:
                raise PvNotFoundException("Unable to find PV %s" % name)
            return ans
        except PvNotFoundException as err:
            # PV not found
            raise
        except Exception as err:
            # Something general went wrong
            raise PvGetException("Unable to get value for PV %s: %s" % (name, err.message))

    def get_ad_image_data(self, prefix):
        raw = self.caget("%s:ArrayData" % prefix)
        xsize = self.caget("%s:ArraySize0_RBV" % prefix)
        ysize = self.caget("%s:ArraySize1_RBV" % prefix)
        return raw, xsize, ysize

