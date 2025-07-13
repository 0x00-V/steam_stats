import requests, sys, csv, json



def print_docs():
    print("Steam Stats Command Documentation")
    print("[-h] --help   | Return useful commands")
    print("[-s] --stats <appid> <currency code>   | Return game statistics (e.g. gb, us, ca) | Optional args: [-e] or --export <filename.json/filename.csv>   | Export stats as CSV/JSON")

def game_details(app_id, cc):
    response_game_details = requests.get(f'https://store.steampowered.com/api/appdetails?appids={app_id}&cc={cc}')
    json_data_game_details = response_game_details.json()
    response_player_count = requests.get(f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}')
    json_player_count = response_player_count.json()
    
    game_detail = json_data_game_details.get(str(app_id), {})
    if not game_detail.get('success'):
        return None

    game_detail_data = game_detail.get('data', {})
    name = game_detail_data.get('name', 'N/A')
    price_ov = game_detail_data.get('price_overview', {})
    price = price_ov.get('final_formatted', 'Free or No price info')
    release_date = game_detail_data.get('release_date', {}).get('date', 'Unknown')
    player_count = json_player_count.get('response', {}).get('player_count', 0)

    return {
        'name': name,
        'price': price,
        'release_date': release_date,
        'player_count': player_count,
    }


def export_data(info, filename):
    if filename.endswith('.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=4)
        print(f"Exported to {filename}")
    elif filename.endswith('.csv'):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(info.keys())
            writer.writerow(info.values())
        print(f"Exported to {filename}")
    else:
        print("Unsupported file format. Use .csv or .json")


def main():
    if len(sys.argv) < 2:
        print("Incorrect Usage.\nUse -h or --help for a full list of commands.")
        return

    cmd = sys.argv[1]


    if cmd in ['-h', '--help']:
        print_docs()
    elif cmd in ['-s', '--stats']:
        if len(sys.argv) < 4:
            print("Incorrect Usage.\n[Syntax: -s <App ID> <Currency Code>]")
            return
        app_id = sys.argv[2]
        currency = sys.argv[3]
        info = game_details(app_id, currency)
        if info:
            for key, val in info.items():
                print(f"{key.capitalize()}: {val}")
            if len(sys.argv) > 5 and sys.argv[4] in ['-e', '--export']:
                filename = sys.argv[5]
                export_data(info, filename)
        else:
            print("Failed to retrieve game details. Check the App ID and try again.")
    else:
        print("Incorrect Usage.\nUse -h or --help for a full list of commands.")
    

if __name__ == "__main__":
    main()