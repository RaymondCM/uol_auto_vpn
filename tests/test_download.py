class TestDownload:

    def test_download(self):
        from uol_auto_vpn import driver
        from uol_auto_vpn import env
        file = driver.get_driver()
        assert file is not None
