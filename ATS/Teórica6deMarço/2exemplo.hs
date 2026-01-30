import Test.QuickCheck
import System.Random

data Age = Age Int
data Person = Person String Age
    
instance Arbitrary Age where
    arbitrary = do
        n <- choose (0, 100)
        return (Age n)

instance Arbitrary Person where
    arbitrary = do
        name <- elements ["John","BOB"]
        age <- arbitrary
        return (Person name age)