import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../sdk")))
from python import SimeisSDK

def main():
    username = "test_player_simple"
    port = 9345  
    
    # Clean up the previous player JSON if any
    json_file = f"./{username}.json"
    if os.path.exists(json_file):
        os.remove(json_file)
        
    try:
        # On créé un nouveau joueur
        print(f"Creating player: {username}")
        sdk = SimeisSDK(username, "127.0.0.1", port)
        
        # Son argent de départ est 72000.0
        status = sdk.get_player_status()
        start_money = status["money"]
        print(f"Starting money: {start_money}")
        assert start_money == 72000.0, f"Expected starting money to be 72000.0, got {start_money}"
        
        sta = status["stations"][0]
        
        # On achète un vaisseau (transaction réussite)
        all_ships = sdk.shop_list_ship(sta)
        assert len(all_ships) > 0, "No ships available to buy"
        ship_to_buy = all_ships[0]
        print(f"Buying ship: {ship_to_buy['id']}")
        
        buy_ship_res = sdk.buy_ship(sta, ship_to_buy["id"])
        assert buy_ship_res.get("error") == "ok" or "error" not in buy_ship_res, f"Failed to buy ship: {buy_ship_res}"
        
        # L'argent doit avoir diminué
        status_after_ship = sdk.get_player_status()
        money_after_ship = status_after_ship["money"]
        print(f"Money after ship purchase: {money_after_ship}")
        assert money_after_ship < start_money, f"Expected money to decrease: {money_after_ship} vs {start_money}"
        
        bought_ship_id = status_after_ship["ships"][0]["id"]
        
        # On achète un module de Miner (transaction réussite)
        print("Buying Miner module...")
        buy_module_res = sdk.buy_module_on_ship(sta, bought_ship_id, "Miner")
        assert buy_module_res.get("error") == "ok" or "error" not in buy_module_res, f"Failed to buy Miner module: {buy_module_res}"
        
        # L'argent doit avoir encore diminué
        status_after_module = sdk.get_player_status()
        money_after_module = status_after_module["money"]
        print(f"Money after module purchase: {money_after_module}")
        assert money_after_module < money_after_ship, f"Expected money to decrease further: {money_after_module} vs {money_after_ship}"
        
        print("All tests passed successfully!")
        
    finally:
        if os.path.exists(json_file):
            os.remove(json_file)

if __name__ == "__main__":
    main()
