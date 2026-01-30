import System.Random
import Data.Time.Calendar

randomDay :: IO Day
randomDay = do
    year <- randomRIO (2000, 2025)
    month <- randomRIO (1, 12)
    day <- randomRIO (1, 28) -- Para simplificar, consideramos até 28 dias em todos os meses
    return $ fromGregorian year month day

main :: IO ()
main = do
    date <- randomDay
    putStrLn $ "Data aleatória: " ++ show date