import unittest

boardWidth = 10
boardHeight = 10

class Ship():
  ships = {'carrier':5, 'battleship':4, 'cruiser':3, 'submarine':3, 'destroyer':2}
  def __init__(self, location = 0, type ='carrier', direction="horizontal"):
    if not self.isValidLocation(location):
      raise ValueError('Out of bounds _loc in creation')
    self._loc = location
    self._len = self.ships[type]
    self.assignDirection(direction)
    self.assignCells(location)

  def loc(self):
    return self._loc

  def len(self):
    return self._len

  def assignDirection(self, direction):
    if direction == "horizontal":
      self._horz = 0
      self._vert = 1
    else:
      self._horz = 1
      self._vert = 0

  def assignCells(self, location):
    self._cells = []
    for i in range(0, self.len()):
      cell_storing_location = self._loc + self._horz*boardWidth*i + i*self._vert
      if not self.isValidLocation(cell_storing_location):
        raise ValueError('Out of bounds cell_storing_location during assignCells:: value:' + str(cell_storing_location))
      self._cells.append(cell_storing_location)

  def isValidLocation(self, location):
    return location < boardWidth * boardHeight and location >= 0

  def checkExists(self, location):
    return location in self._cells

  def hit(self, location):
    if self.checkExists(location):
      self._cells.remove(location)
      return True
    return False

  def dead(self):
    return len(self._cells) == 0

  def collision(self, ship):
    for cell in self._cells:
      if ship.checkExists(cell):
        return True
    return False

class Game():
  player1 = []
  player2 = []
  def __init__(self):
    pass

  def addShip(self, player_id, ship):
    if player_id == 1:
      if not self.checkIfColliding(self.player1, ship):
        self.player1.append(ship)
        return True

  def checkIfColliding(self, player, ship):
    for existingShip in player:
      if ship.collision(existingShip):
        raise ValueError('Collision with existing ship')
    return False






class TestBattleship(unittest.TestCase):
  def test_ShipClass(self):
    self.assertEqual(Ship().loc(), 0)
    self.assertEqual(Ship(8).loc(), 8)
    with self.assertRaises(ValueError):
       Ship(200)
    self.assertEqual(Ship(10, 'destroyer').len(),2)
    self.assertFalse(Ship(10).isValidLocation(100))
    self.assertTrue(Ship(10).isValidLocation(50))
    self.assertTrue(Ship(50, direction="horizontal").checkExists(54))
    self.assertTrue(Ship(50, direction="vertical").checkExists(90))
    self.assertFalse(Ship(50).checkExists(55))
    testShip = Ship(50)
    self.assertTrue(testShip.hit(51))
    self.assertFalse(testShip.checkExists(51))
    self.assertFalse(testShip.hit(51))
    testShip.hit(50)
    testShip.hit(52)
    testShip.hit(53)
    testShip.hit(54)
    self.assertTrue(testShip.dead())

  def test_Battleship(self):
    self.assertTrue(Game())
    testShip = Ship(50)
    testGame = Game()
    self.assertTrue(testGame.addShip(1, testShip))


def main():
  unittest.main()

if __name__ == '__main__':
  main()
