class TestSetup:

    def test_greeting(self):
        from uol_auto_vpn import driver
        from uol_auto_vpn import env
        file = driver.get_driver()
        assert file is not None
        file = env.load_env()
