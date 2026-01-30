import System.Random

import Test.QuickCheck

data Cardinal = North | South | East | West
    deriving (Show, Eq)

genCardinal :: Gen Cardinal
genCardinal = elements [North, South, East, West]