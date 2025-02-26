import json
import os

def carregar_jogo(caminho_json):
    with open(caminho_json, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

def combate(jogador, inimigo):
    print(f"\nVocê está em combate com {inimigo['name']}!")
   

def jogar(jogo):
    local_atual_id = jogo['startLocationId']
    inventario = []

    '''item_inicial = {
        "name": "tesoura",
        "description": "Uma tesoura afiada que pode ser útil.",
        "id": "2",
        "can_take": True,
        "inactive": False
    }

    inventario.append(item_inicial)'''
    
    jogador = {
        'life': jogo['life'],
        'attack': jogo['attack'],
        'defense': jogo['defense']
    }
    turnos = 0

    while True:
        local_atual = next(loc for loc in jogo['locations'] if loc['id'] == local_atual_id)
        
        print(f"\n--- {local_atual['name']} ---")
        print(local_atual['description'])

        if local_atual['items']:
            print("\nItens no local:")
            for item in local_atual['items']:
                if not item['inactive']:
                    print(f"- {item['name']}: {item['description']}")

        if local_atual['npcs']:
            print("\nNPCs no local:")
            for npc in local_atual['npcs']:
                if not npc['inactive']:
                    print(f"- {npc['name']}: {npc['description']}")

        print("\nSaídas:")
        for saida in local_atual['exits']:
                print(f"- {saida['direction']}: {saida['description']}")

        comando = input("\nO que você quer fazer? ").strip().lower().split()
        
        os.system('cls' if os.name == 'nt' else 'clear')
        if not comando:
            continue

        acao = comando[0]
        alvo = comando[1] if len(comando) > 1 else None

        if acao == "mover":
            for saida in local_atual['exits']:
                if saida['direction'] == alvo and not saida['inactive']:
                    local_atual_id = saida['targetLocationId']
                    print(f"Você se moveu para {saida['direction']}.")
                    break
            else:
                print("Direção inválida ou bloqueada.")

        elif acao == "pegar":
            for item in local_atual['items']:
                if item['name'].lower() == alvo and item['can_take'] and not item['inactive']:
                    inventario.append(item)
                    local_atual['items'].remove(item)
                    print(f"Você pegou {item['name']}.")
                    break
            else:
                print("Item não encontrado ou não pode ser pego.")

        elif acao == "usar":
            for item in inventario:
                if item['name'].lower() == alvo:
                    for puzzle in local_atual['puzzles']:
                        if item['id'] in puzzle['solution']['requiredItems']:
                            print(f"Você usou {item['name']} para resolver o puzzle!")
                            for target_location_id in puzzle['result']['active']:
                                for saida in local_atual['exits']:
                                    if saida['targetLocationId'] == target_location_id:
                                        saida['inactive'] = False
                                        print(f"A saída para {saida['direction']} foi ativada!")
                            inventario.remove(item)
                            break
                    else:
                        print(f"Você usou {item['name']}, mas nada aconteceu.")
                    break
            else:
                print("Item não encontrado no inventário.")


        elif acao == "inventario":
            print("\nInventário:")
            for item in inventario:
                print(f"- {item['name']}: {item['description']}")

        elif acao == "falar":
            for npc in local_atual['npcs']:
                if npc['name'].lower() == alvo and not npc['inactive']:
                    print(f"\n{npc['name']}: {npc['dialogues'][0]['text']}")
                    for resposta in npc['dialogues'][0]['responses']:
                        print(f"- {resposta['text']}")
                    break
            else:
                print("NPC não encontrado ou indisponível.")

        elif acao == "sair":
            print("Obrigado por jogar!")
            break

        else:
            print("Comando inválido. Tente 'mover [direção]', 'pegar [item]', 'usar [item]', 'falar [npc]', 'inventario' ou 'sair'.")


        turnos += 1
        print(f"Turno {turnos}.")

caminho_json = "SaveSalles.json"  
jogo = carregar_jogo(caminho_json)
jogar(jogo)
