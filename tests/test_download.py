class TestDownload:

    def test_download(self):
        from uol_auto_vpn import driver
        file = driver.get_driver()
        assert file is not None
