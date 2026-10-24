"""Package the theme + icon pack into an installable Rider plugin.

Produces the same layout the IDE expects from a plugin distribution:

    build/distributions/<name>-<version>.zip
        <name>/lib/<name>.jar          <- META-INF/plugin.xml, themes/, icons/

The JAR is written with a fixed timestamp so rebuilds are byte-identical.
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "src" / "main" / "resources"
DIST = ROOT / "build" / "distributions"

NAME = "sharp-studio-dark"
VERSION = "1.0.0"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)
#: PayPal donation link (paypal.me/<username>) and the vendor e-mail shown in the
#: JetBrains Marketplace listing -- Rider validates the e-mail format, so a
#: placeholder here makes "Install plugin from disk" fail.
DONATE_URL = "https://www.paypal.com/paypalme/HNDeveloper"
VENDOR_EMAIL = "hojjatnikan@gmail.com"
DONATE_TOKEN = "__DONATE_URL__"
VENDOR_EMAIL_TOKEN = "__VENDOR_EMAIL__"
#: anything that would mean a placeholder leaked into the shipped plugin
FORBIDDEN = (DONATE_TOKEN, VENDOR_EMAIL_TOKEN, "YOUR_EMAIL", "YOUR_PAYPAL_EMAIL", "YOUR_EMAIL@")


def collect(donate_url: str, vendor_email: str) -> list[tuple[bytes, str]]:
    """Every resource of the plugin, with the donation link and vendor e-mail filled in."""
    files: list[tuple[bytes, str]] = []
    for path in sorted(RESOURCES.rglob("*")):
        if not path.is_file():
            continue
        data = path.read_bytes()
        if path.name == "plugin.xml":
            data = data.replace(DONATE_TOKEN.encode(), donate_url.encode())
            data = data.replace(VENDOR_EMAIL_TOKEN.encode(), vendor_email.encode())
        files.append((data, path.relative_to(RESOURCES).as_posix()))
    required = {"META-INF/plugin.xml", "themes/visual-studio-2022-dark.theme.json"}
    present = {name for _data, name in files}
    missing = required - present
    if missing:
        raise SystemExit(f"missing resources: {sorted(missing)}")
    blob = b"".join(data for data, _n in files)
    leaked = [token for token in FORBIDDEN if token.encode() in blob]
    if leaked:
        raise SystemExit(
            "placeholder still present in the packaged plugin: "
            + ", ".join(leaked)
            + " -- pass --donate-url / --vendor-email"
        )
    return files


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--install-into", help="plugin directory of a Rider config to install into")
    ap.add_argument("--donate-url", default=DONATE_URL,
                    help=f"support link shown in the plugin description (default: {DONATE_URL})")
    ap.add_argument("--vendor-email", default=VENDOR_EMAIL,
                    help=f"vendor e-mail for the plugin descriptor (default: {VENDOR_EMAIL})")
    args = ap.parse_args()

    files = collect(args.donate_url, args.vendor_email)
    DIST.mkdir(parents=True, exist_ok=True)
    jar_path = DIST / f"{NAME}.jar"
    zip_path = DIST / f"{NAME}-{VERSION}.zip"

    with zipfile.ZipFile(jar_path, "w", zipfile.ZIP_DEFLATED) as jar:
        for data, name in files:
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            jar.writestr(info, data)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as dist:
        info = zipfile.ZipInfo(f"{NAME}/lib/{NAME}.jar", FIXED_TIME)
        info.compress_type = zipfile.ZIP_DEFLATED
        dist.writestr(info, jar_path.read_bytes())

    icons = sum(1 for _data, name in files if name.startswith("icons/"))
    print(f"jar    : {jar_path}  ({jar_path.stat().st_size / 1024:.0f} KB)")
    print(f"zip    : {zip_path}  ({zip_path.stat().st_size / 1024:.0f} KB)")
    print(f"content: {len(files)} files ({icons} icons, plugin.xml + theme descriptor)")
    print(f"donate : {args.donate_url}")

    if args.install_into:
        target = Path(args.install_into) / NAME
        target.mkdir(parents=True, exist_ok=True)
        lib = target / "lib"
        lib.mkdir(exist_ok=True)
        (lib / f"{NAME}.jar").write_bytes(jar_path.read_bytes())
        print(f"\ninstalled into {target}")


if __name__ == "__main__":
    main()
