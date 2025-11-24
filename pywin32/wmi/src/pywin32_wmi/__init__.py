"""pywin32 WMI Package."""

from datetime import datetime

from wmi import WMI  # type: ignore[import-untyped]


def firewall_rules() -> None:
    """ファイアウォールのルールを取得する."""
    wmi = WMI(namespace="root\\standardcimv2")
    for rule in wmi.MSFT_NetFirewallRule():
        result = {k: getattr(rule, k) for k in rule.properties}
        profiles = rule.associators(wmi_result_class="MSFT_NetFirewallProfile")
        result["Profiles"] = [p.Name for p in profiles]
        print(result)


def programs() -> None:
    """インストールしたプラグラムを取得する."""
    wmi = WMI()
    for product in wmi.WIN32_Product():
        installed_date = datetime.strptime(product.InstallDate, r"%Y%m%d")
        print(f"{product.Name} {product.Vendor} {installed_date} {product.Version}")


if __name__ == "__main__":
    firewall_rules()
    programs()
