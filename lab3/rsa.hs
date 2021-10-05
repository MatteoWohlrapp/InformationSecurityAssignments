import Data.Char
import Data.List

splitToLines :: String -> [String]
splitToLines [] = []
splitToLines xs = takeWhile (/= '\n') xs : splitToLines (tail $ dropWhile (/= '\n') xs)

parseLine :: String -> [Integer]
parseLine [] = []
parseLine ss = (read (takeWhile isDigit ss) :: Integer) : parseLine (dropWhile (`elem` " \n") (dropWhile isDigit ss))

parseValues :: [String] -> [Integer]
parseValues xs = [head $ parseLine x | x <- xs]

triple :: Num c => [c] -> (c, c, c)
triple (a:b:c:_) = (a, b, c)
triple _ = (-1, -1, -1)

modularInverse :: Integer -> Integer -> Integer
modularInverse m n
    | f m n 1 0 < 0 = n + f m n 1 0 
    | otherwise = f m n 1 0
    where 
        f m n o p
            | m == 0 = p
            | otherwise = f (n-q*m) m (p-q*o) o
                where q = n `div` m
    
--head (filter (\x -> ((m `mod` n) * (x `mod` n)) `mod` n == 1) [1..n] ++ [-1])

factors :: Integer -> [Integer]
factors n 
    | even n = 2:factors (n `div` 2)
    | otherwise = f n 3
    where
        f n d 
            | n == 1 = []
            | n `mod` d == 0 = d : f (n `div` d) d
            | otherwise = f n (d+2)

totient :: Integer -> Integer
totient n = foldl (\x y -> x - x `div` y) n  (nub $ factors n)

modPower :: Integer -> Integer -> Integer -> Integer
modPower b e m
    | e == 1 = b `mod` m
    | even e = modPower ((b^2) `mod` m) (e `div` 2) m `mod` m
    | otherwise = (b * modPower b (e-1) m) `mod` m

encrypt :: Integer -> Integer -> Integer -> Integer -> Integer
encrypt p q e x = modPower x e (p*q)

decrypt :: Integer -> Integer -> Integer -> Integer -> Integer
decrypt p q e x = modPower x (modularInverse e (totient (p*q))) (p*q)

main :: IO()
main = do
    line1 <- getLine
    line2 <- getLine
    input <- getContents
    let (p, q, e) = triple $ parseLine line2
    let values = parseValues $ filter (not.null) (splitToLines input)
    if head line1 == 'e' then mapM_ (print . encrypt p q e) values
    else mapM_ (print . decrypt p q e) values