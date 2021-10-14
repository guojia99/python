import re


class Analysis(object):
    @staticmethod
    def config_to_list(config: str) -> list:
        out = []
        split_lines = config.splitlines()
        for line in split_lines:
            kv = re.split(r"[ ]+|\t+", line)
            if len(kv) == 2:
                key, value = kv[0], kv[1]
                try:
                    value = int(value)
                except:
                    pass
                out.append([key, value])
        return out

    @staticmethod
    def list_to_config(configs: list) -> str:
        out = ""
        for item in configs:
            out += f"{item[0]}\t{item[1]}\n"
        return out

    @staticmethod
    def update_config(config: str, **kv) -> str:
        datas = Analysis().config_to_list(config)
        for re_key in kv.keys():
            num = 0
            for d in datas:
                if d[0] == re_key:
                    datas[num] = [re_key, kv[re_key]]
                    break
                num += 1
        return Analysis().list_to_config(datas)


if __name__ == "__main__":
    data = """DeviceLinkSelector    0
DeviceLinkHeartbeatMode	On
DeviceStreamChannelSelector	0
DeviceStreamChannelPacketSize	1500
"""
    print(Analysis().update_config(config=data, DeviceLinkSelector=1, DeviceStreamChannelPacketSize=1600))
