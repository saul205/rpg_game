from enum import Enum
from glob import escape
from operator import truediv
from Enemy import *
from Classes import *
import random as rand
import DB as db

import os

from Hero import Hero


def cls():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


class Game:

    class _menu(Enum):
        Nueva_Partida = 1
        Cargar_Partida = 2
        Cerrar_Juego = 3

    class _playerMenu(Enum):
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
        self.round = self.startingRound + int(self.enemiesKilled/10)
        self.player = None
        self.enemy = None
        self.estado = self.Estados.MenuPrincipal

        self.exit = False
        self.toMainMenu = False
        return

    def _printHeader(self):
        cls()
        print(self.player)
        print(self.enemy)

    def printPlayerMenu(self):
        self._printHeader()
        result = '\nQue quieres hacer'
        for x in self._playerMenu:
            result += '\n\t-' + str(x.value) + '. ' + x.name

        print(result)

    def printAttackMenu(self):
        self._printHeader()
        self.player.printAttacks()
        print("\t-> 0. Volver")

    def _printMenu(self):
        cls()
        result = '\nMenú Principal'
        for x in self._menu:
            result += '\n\t-' + str(x.value) + '. ' + x.name
        print(result)

    def _saveAction(self):

        players = db.PlayerController.getAllPlayers()
        dictPlayers = {}
        for player in players:
            dictPlayers[player.name] = player
        if self.player.name in dictPlayers:
            db.PlayerController.updatePlayer(self.player)
        else:
            db.PlayerController.savePlayer(self.player)

    def loadGame(self):

        players = db.PlayerController.getAllPlayers()

        if len(players) == 0:
            return False

        cls()
        print("Personajes:")
        dictPlayers = {}
        for player in players:
            print("->", player)
            dictPlayers[player.name] = player

        print("-> Volver")

        personaje = input("Escoge personaje: ")
        if personaje in dictPlayers:
            self.player = db.PlayerEntity.FromEntity(
                dictPlayers[personaje])
            self.estado = self.Estados.PlayerTurn
        elif personaje == "Volver":
            self.estado = self.Estados.MenuPrincipal

    def startNewGame(self):
        # Cargar nombres guardados
        players = db.PlayerController.getAllPlayers()
        playerNames = [x.name for x in players]
        name = input("Pon un nombre a tu heroe: ")
        if name in playerNames:
            sobreescribir = input(
                "Ya existe un personaje con ese nombre.\nQuieres sobreescribirlo?Y/otra cosa para cancelar xD")
            if sobreescribir.upper() == 'Y':
                db.PlayerController.deletePlayer(name)
            else:
                self.estado = self.Estados.MenuPrincipal
                return

        text = "Clases:"
        for x in classes:
            text += "\n\t -> " + x
        print(text)

        self.player = None
        while self.player == None:
            seleccionada = input("Selecciona una clase: ")
            if seleccionada in classes:
                self.player = classes[seleccionada](name)
                self.estado = self.Estados.PlayerTurn
            else:
                print("Elección inválida", seleccionada)

    def initializeGame(self):

        self.startingRound = 1
        self.enemiesKilled = 0
        self.round = self.startingRound + int(self.enemiesKilled/10)
        self.enemy = Enemy(1)

    def play(self):
        while not self.exit:
            if self.estado == self.Estados.MenuPrincipal:
                if self.player is not None and self.player.dead:
                    self._saveAction()
                self.menuEstado()
            elif self.estado == self.Estados.CrearPartida:
                self.startNewGame()
                if self.estado == self.Estados.PlayerTurn:
                    self.initializeGame()
            elif self.estado == self.Estados.CargarPartida:
                self.loadGame()
                if self.estado == self.Estados.PlayerTurn:
                    self.initializeGame()
            elif self.estado == self.Estados.PrePlayerTurn:
                self.estado = self.Estados.PlayerTurn
                self.preTurnActions(self.player, self.Estados.PostPlayerTurn)
            elif self.estado == self.Estados.PlayerTurn:
                if self.enemy.dead:
                    self.enemiesKilled += 1
                    self.round = self.startingRound + \
                        int(self.enemiesKilled / 10)
                    self.enemy = Enemy(self.round)
                    self.player.addExp(self.enemy)
                    self.player.addToInventory(self.enemy.drop())
                self.playerMenuEstado()
            elif self.estado == self.Estados.PostPlayerTurn:
                self.postTurnActions(self.player)
                self.estado = self.Estados.EnemyTurn
            elif self.estado == self.Estados.Atacando:
                self.atacandoEstado()
            elif self.estado == self.Estados.Inventario:
                self.inventoryEstado()
            elif self.estado == self.Estados.EnemyTurn:

                self.estado = self.Estados.PrePlayerTurn
                self.preTurnActions(self.enemy, self.Estados.PrePlayerTurn)
                self.enemyTurnEstado()
                self.postTurnActions(self.enemy)

    def menuEstado(self):
        self._printMenu()

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

    def playerMenuEstado(self):

        self.printPlayerMenu()

        option = input('Opcion elegida: ')
        if option.isdigit():
            option = int(option)

        if option in [x.value for x in self._playerMenu]:
            if option == self._playerMenu.Atacar.value:
                self.estado = self.Estados.Atacando
            elif option == self._playerMenu.Defender.value:
                self.player.defend()
                self.estado = self.Estados.PostPlayerTurn
            elif option == self._playerMenu.Inventario.value:
                self.estado = self.Estados.Inventario
            elif option == self._playerMenu.Guardar.value:
                self._saveAction()
            elif option == self._playerMenu.Salir.value:
                self.estado = self.Estados.MenuPrincipal

    def atacandoEstado(self):
        self.printAttackMenu()
        ataque = input('Seleccione un ataque: ')

        if ataque.isdigit() and 0 < int(ataque) <= len(self.player.attacks):
            attack = self.player.selectAttack(ataque)
            if self.player.hasMana(attack.manaCost):
                self.player.launchAttack(
                    self.enemy, attack)

                self.estado = self.Estados.PostPlayerTurn
            else:
                input("Not enough mana(press enter to continue)")

        elif ataque.isdigit() and int(ataque) == 0:
            self.estado = self.Estados.PlayerTurn

    def inventoryEstado(self):

        self.player.printInventory()

        input()

        self.estado = self.Estados.PostPlayerTurn

    def enemyTurnEstado(self):

        ataque = rand.randint(0, len(self.enemy.attacks) - 1)
        self.enemy.launchAttack(self.player, self.enemy.attacks[ataque])
        if self.player.dead:
            self.estado = self.Estados.MenuPrincipal
        else:
            self.estado = self.Estados.PrePlayerTurn

    def preTurnActions(self, character, stunnedState):

        character.reset()

        if character.Stunned:

            self.estado = stunnedState

            input("Press something to continue")

    def postTurnActions(self, character):

        character.checkInvariants()

        if character.applyEffects():
            input("Press something to continue")

        if isinstance(character, Hero):

            character.regenerateMana()

    def main(self):
        self.play()
