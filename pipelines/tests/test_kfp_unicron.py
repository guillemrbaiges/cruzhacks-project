def test_kfp_unicron_dependency() -> None:
    try:
        import kfp_unicron  # noqa: F401 pylint: disable=unused-import

        kfp_installed = True
    except ImportError:
        kfp_installed = False

    assert kfp_installed
