"""Backward-compatible shim for legacy ShopifySentinel.main entrypoint."""

from shopify_sentinel.main import main


if __name__ == "__main__":
    main()
