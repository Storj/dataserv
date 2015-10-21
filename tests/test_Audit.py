import unittest
from dataserv.Audit import Audit
from dataserv.app import db, app
from btctxstore import BtcTxStore
from dataserv.Farmer import Farmer


class AuditTest(unittest.TestCase):

    def setUp(self):
        app.config["SKIP_AUTHENTICATION"] = True  # monkey patch
        app.config["DISABLE_CACHING"] = True

        self.btctxstore = BtcTxStore()
        self.bad_addr = 'notvalidaddress'

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def gen_btc_addr(self):
        return self.btctxstore.get_address(self.btctxstore.get_key(
                                self.btctxstore.create_wallet()))

    def test_register_audit(self):
        btc_addr = self.gen_btc_addr()
        btc_addr2 = self.gen_btc_addr()

        # register farmer and test db
        farmer1 = Farmer(btc_addr)
        self.assertFalse(farmer1.exists())
        farmer1.register()
        self.assertTrue(farmer1.exists())

        # do callbacks to properly test errors
        def callback_a():
            Audit(self.bad_addr, 0)

        def callback_b():
            Audit(btc_addr2, 0)

        def callback_c():
            Audit(btc_addr, 0).save()
            Audit(btc_addr, 0)

        def callback_d():
            Audit(btc_addr, 1, 'invalid_sha')

        self.assertRaises(ValueError, callback_a)
        self.assertRaises(LookupError, callback_b)
        self.assertRaises(IndexError, callback_c)
        self.assertRaises(ValueError, callback_d)
