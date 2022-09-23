import os
from enum import Enum

import DB as db
from Classes import *
from Enemy import *
from Hero import Hero


def cls():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


class Game:
    class Menu(Enum):
        Nueva_Partida = 1
        Cargar_Partida = 2
        Cerrar_Juego = 3

    class PlayerMenu(Enum):
        Atacar = 1
        Defender = 2
        Inventario = 3
        Guardar = 4
        Salir = 5

    class Estados(Enum):
        MenuPrincipal = 1
        CrearPartida = 2
        CargarPartida = 3
        PrePlayerTurn = 4
        PlayerTurn = 5
        PostPlayerTurn = 6
        Atacando = 7
        Inventario = 8
        ObjetoSeleccionado = 9
        EnemyTurn = 10

    _exit = False

    def __init__(self):
        self.startingRound = 1
        self.enemiesKilled = 0
        self.round = self.startingRound + int(self.enemiesKilled / 10)
        self.player = None
        self.enemy = None
        self.estado = self.Estados.MenuPrincipal

        self.exit = False
        self.toMainMenu = False
        return

    def _print_header(self):
        cls()
        print(self.player)
        print(self.enemy)

    def print_player_menu(self):
        self._print_header()
        result = '\nQue quieres hacer'
        for x in self.PlayerMenu:
            result += '\n\t-' + str(x.value) + '. ' + x.name

        print(result)

    def print_attack_menu(self):
        self._print_header()
        self.player.print_attacks()
        print("\t-> 0. Volver")

    def _print_menu(self):
        cls()
        result = '\nMenú Principal'
        for x in self.Menu:
            result += '\n\t-' + str(x.value) + '. ' + x.name
        print(result)

    def _save_action(self):

        players = db.PlayerController.get_all_players()
        dict_players = {}
        for player in players:
            dict_players[player.name] = player
        if self.player.name in dict_players:
            db.PlayerController.update_player(self.player)
        else:
            db.PlayerController.save_player(self.player)

    def load_game(self):

        players = db.PlayerController.get_all_players()

        if len(players) == 0:
            return False

        cls()
        print("Personajes:")
        dict_players = {}
        for player in players:
            print("->", player)
            dict_players[player.name] = player

        print("-> Volver")

        personaje = input("Escoge personaje: ")
        if personaje in dict_players:
            self.player = db.PlayerEntity.from_entity(
                dict_players[personaje])
            self.estado = self.Estados.PlayerTurn
        elif personaje == "Volver":
            self.estado = self.Estados.MenuPrincipal

    def start_new_game(self):
        # Cargar nombres guardados
        players = db.PlayerController.get_all_players()
        player_names = [x.name for x in players]
        name = input("Pon un nombre a tu heroe: ")
        if name in player_names:
            sobreescribir = input(
                "Ya existe un personaje con ese nombre.\nQuieres sobreescribirlo?Y/otra cosa para cancelar xD")
            if sobreescribir.upper() == 'Y':
                db.PlayerController.delete_player(name)
            else:
                self.estado = self.Estados.MenuPrincipal
                return

        text = "Clases:"
        for x in classes:
            text += "\n\t -> " + x
        print(text)

        self.player = None
        while self.player is None:
            seleccionada = input("Selecciona una clase: ")
            if seleccionada in classes:
                self.player = classes[seleccionada](name)
                self.estado = self.Estados.PlayerTurn
            else:
                print("Elección inválida", seleccionada)

    def initialize_game(self):

        self.startingRound = 1
        self.enemiesKilled = 0
        self.round = self.startingRound + int(self.enemiesKilled / 10)
        self.enemy = Enemy(1)

    def play(self):
        while not self.exit:
            if self.estado == self.Estados.MenuPrincipal:
                if self.player is not None and self.player.dead:
                    self._save_action()
                self.menu_estado()
            elif self.estado == self.Estados.CrearPartida:
                self.start_new_game()
                if self.estado == self.Estados.PlayerTurn:
                    self.initialize_game()
            elif self.estado == self.Estados.CargarPartida:
                self.load_game()
                if self.estado == self.Estados.PlayerTurn:
                    self.initialize_game()
            elif self.estado == self.Estados.PrePlayerTurn:
                self.estado = self.Estados.PlayerTurn
                self.pre_turn_actions(self.player, self.Estados.PostPlayerTurn)
            elif self.estado == self.Estados.PlayerTurn:
                if self.enemy.dead:
                    self.enemiesKilled += 1
                    self.round = self.startingRound + \
                                 int(self.enemiesKilled / 10)
                    self.enemy = Enemy(self.round)
                    self.player.add_exp(self.enemy)
                    self.player.add_to_inventory(self.enemy.drop())
                self.player_menu_estado()
            elif self.estado == self.Estados.PostPlayerTurn:
                self.post_turn_actions(self.player)
                self.estado = self.Estados.EnemyTurn
            elif self.estado == self.Estados.Atacando:
                self.atacando_estado()
            elif self.estado == self.Estados.Inventario:
                self.inventory_estado()
            elif self.estado == self.Estados.EnemyTurn:

                self.estado = self.Estados.PrePlayerTurn
                self.pre_turn_actions(self.enemy, self.Estados.PrePlayerTurn)
                self.enemy_turn_estado()
                self.post_turn_actions(self.enemy)

    def menu_estado(self):
        self._print_menu()

        option = input("\nSelecciona una opción: ")
        if option.isdigit():
            option = int(option)

        if option == 1:
            self.estado = self.Estados.CrearPartida
        elif option == 2:
            self.estado = self.Estados.CargarPartida
        elif option == 3:
            self.exit = True
        else:
            print("Opción invalida")

    def player_menu_estado(self):

        self.print_player_menu()

        option = input('Opcion elegida: ')
        if option.isdigit():
            option = int(option)

        if option in [x.value for x in self.PlayerMenu]:
            if option == self.PlayerMenu.Atacar.value:
                self.estado = self.Estados.Atacando
            elif option == self.PlayerMenu.Defender.value:
                self.player.defend()
                self.estado = self.Estados.PostPlayerTurn
            elif option == self.PlayerMenu.Inventario.value:
                self.estado = self.Estados.Inventario
            elif option == self.PlayerMenu.Guardar.value:
                self._save_action()
            elif option == self.PlayerMenu.Salir.value:
                self.estado = self.Estados.MenuPrincipal

    def atacando_estado(self):
        self.print_attack_menu()
        ataque = input('Seleccione un ataque: ')

        if ataque.isdigit() and 0 < int(ataque) <= len(self.player.attacks):
            attack = self.player.select_attack(ataque)
            if self.player.has_mana(attack.manaCost):
                self.player.launch_attack(
                    self.enemy, attack)

                self.estado = self.Estados.PostPlayerTurn
            else:
                input("Not enough mana(press enter to continue)")

        elif ataque.isdigit() and int(ataque) == 0:
            self.estado = self.Estados.PlayerTurn

    def inventory_estado(self):

        self.player.print_inventory()

        input()

        self.estado = self.Estados.PostPlayerTurn

    def enemy_turn_estado(self):

        ataque = rand.randint(0, len(self.enemy.attacks) - 1)
        self.enemy.launch_attack(self.player, self.enemy.attacks[ataque])
        if self.player.dead:
            self.estado = self.Estados.MenuPrincipal
        else:
            self.estado = self.Estados.PrePlayerTurn

    def pre_turn_actions(self, character, stunned_state):

        character.reset()

        if character.stunned:
            self.estado = stunned_state

            input("Press something to continue")

    def post_turn_actions(self, character):

        character.check_invariants()

        if character.apply_effects():
            input("Press something to continue")

        if isinstance(character, Hero):
            character.regenerate_mana()

    def main(self):
        self.play()
