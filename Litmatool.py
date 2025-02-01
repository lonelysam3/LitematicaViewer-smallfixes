import json, subprocess

json_data = json.load(open('lang/zh_cn.json', 'r', encoding='utf-8'))
json_cati = json.load(open('lang/catigory.json', 'r', encoding='utf-8'))

def convert_units(number):
    units = {'箱': 54 * 27 * 64, '盒': 27 * 64, '组': 64, '个': 1}
    result = ""
    for unit, value in units.items():
        if number >= value:
            count = number // value
            result += f"{count}{unit}"
            number %= value
    return result if result else "0个"

def cn_translate(id):
    return json_data.get(id, id)

def manual_install_pk():
    try:
        result = subprocess.run(['install.bat'], check=True, capture_output=True, text=True)
        print("Packages install successfully")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)

def find_keys_by_value_in_list(dictionary, target_value):
    return [key for key, value_list in dictionary.items() if target_value in value_list]

def Category_Tran(data):
    for key, value_list in json_cati.items():
        for prop in data.split("_"):
            if prop in value_list:
                return key
    return ""

if __name__ == "__main__":
    pass