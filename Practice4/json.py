import json

def main():
    with open("sample-data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for item in data.get("imdata", []):
        obj = item.get("l1PhysIf", {})
        attrs = obj.get("attributes", {})
        dn = attrs.get("dn", "")
        descr = attrs.get("descr", "")
        speed = attrs.get("speed", "")
        mtu = attrs.get("mtu", "")
        rows.append((dn, descr, speed, mtu))

    dn_w = 50
    desc_w = 20
    speed_w = 8
    mtu_w = 6

    print("Interface Status")
    print("=" * (dn_w + 1 + desc_w + 2 + speed_w + 2 + mtu_w))
    print(f'{"DN":<{dn_w}} {"Description":<{desc_w}}  {"Speed":<{speed_w}}  {"MTU":<{mtu_w}}')
    print(f'{"-"*dn_w} {"-"*desc_w}  {"-"*speed_w}  {"-"*mtu_w}')

    for dn, descr, speed, mtu in rows:
        print(f"{dn:<{dn_w}} {descr:<{desc_w}}  {speed:<{speed_w}}  {mtu:<{mtu_w}}")

if __name__ == "__main__":
    main()